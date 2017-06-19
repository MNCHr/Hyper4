#!/usr/bin/python

import argparse
import sys
import json
import runtime_CLI
import socket
from subprocess import call
import os
import copy
import re
from cStringIO import StringIO
from hp4command import HP4_Match_Command
from hp4command import HP4_Primitive_Command

import code

match_types = {'[DONE]':'0',
               '[EXTRACTED_EXACT]':'1',
               '[METADATA_EXACT]':'2',
               '[STDMETA_EXACT]':'3',
               '[EXTRACTED_VALID]':'4',
               '[STDMETA_INGRESS_PORT_EXACT]':'5',
               '[STDMETA_PACKET_LENGTH_EXACT]':'6',
               '[STDMETA_INSTANCE_TYPE_EXACT]':'7',
               '[STDMETA_EGRESS_SPEC_EXACT]':'8',
               '[MATCHLESS]':'99'}

primitive_types = {'[MODIFY_FIELD]':'0',
									 '[ADD_HEADER]':'1',
									 '[COPY_HEADER]':'2',
									 '[REMOVE_HEADER]':'3',
									 '[MODIFY_FIELD_WITH_HBO]':'4',
									 '[TRUNCATE]':'5',
									 '[DROP]':'6',
									 '[NO_OP]':'7',
									 '[PUSH]':'8',
									 '[POP]':'9',
									 '[COUNT]':'10',
									 '[METER]':'11',
									 '[GENERATE_DIGEST]':'12',
									 '[RECIRCULATE]':'13',
									 '[RESUBMIT]':'14',
									 '[CLONE_INGRESS_INGRESS]':'15',
									 '[CLONE_EGRESS_INGRESS]':'16',
									 '[CLONE_INGRESS_EGRESS]':'17',
									 '[CLONE_EGRESS_EGRESS]':'18',
									 '[MULTICAST]':'19',
									 '[MATH_ON_FIELD]':'20'}

MAX_PRIORITY = 2147483646

# http://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
class Capturing(list):
  def __enter__(self):
    self._stdout = sys.stdout
    sys.stdout = self._stringio = StringIO()
    return self
  def __exit__(self, *args):
    self.extend(self._stringio.getvalue().splitlines())
    del self._stringio
    sys.stdout = self._stdout

class Rule():
  def __init__(self, rule_type, table, action, mparams, aparams):
    self.rule_type = rule_type
    self.table = table
    self.action = action
    self.mparams = mparams
    self.aparams = aparams

  def __str__(self):
    ret = self.rule_type + ' ' + self.table + ' ' + self.action
    for param in self.mparams:
      ret += ' ' + param
    if self.rule_type == 'table_add':
      ret += ' =>'
    elif self.rule_type != 'table_set_default':
      print("ERROR: incorrect table command %s, table %s" % (self.command, self.table))
      exit()
    for param in self.aparams:
      ret += ' ' + param
    return ret

class Instance():
  def __init__(self, name, user, vports, program_ID, p4f, hp4tf, hp4mtf):
    self.name = name
    self.user = user
    self.vports = vports # {vportnum (int) : Virtual_Port}
    self.vmcast_grps = {} # vmcast_grp_ID (int) : Virtual_Mcast_Group
    self.vmcast_nodes = {} # vmcast_node_handle (int) : Virtual_Mcast_Node
    self.instance_ID = instance_ID
    # need this in order to properly fill in match ID parameters
    self.match_counters = {} # source table name (str) : match counter (int)
    self.t_virtnet_rule_handles = [] # [handles (ints)]
    self.func_rule_handles = {} # hp4 table name (str) : rule handle (int)
    self.match_rule_handles = {} # hp4 table name (str) : rule handle (int)
    self.p4f = p4f
    self.hp4tf = hp4tf
    self.hp4mtf = hp4mtf

  # TODO: parse the .hp4mt
  def parse_json(self):
    pass

  # TODO: from the templates created by parse_json, filter per rule request
  def get_templates(self):
    pass

class UDev():
  def __init__(self, user, device, pports):
    self.user = user # User()
    self.device = device # Device()
    self.instance_chain = [] # strs
    self.pports = pports # [ints]
    self.vegress_pports = {}
    counter = 1
    for pport in self.pports:
      self.vegress_pports[counter] = pport
      counter += 1

  def pushcommand(self, command):
    if command.split()[0] == 'table_add':
      try:
        handle = int(self.device.do_table_add(command.split('table_add ')[1]))
        if command.split()[1] == 'tset_context':
          pport = command.split()[3]
          self.device.assignment_handles[pport] = handle
        elif command.split()[1] == 't_virtnet':
          self.user.instances[instance].t_virtnet_rule_handles.append(handle)
      except AddRuleError as e:
        print('AddRuleError exception: ' + e.value)

    elif command.split()[0] == 'table_modify':
      try:
        self.device.do_table_modify(command.split('table_modify ')[1])
      except ModRuleError as e:
        print('ModRuleError exception: ' + e.value)

    elif command.split()[0] == 'table_delete':
      try:
        # should be faster to let caller handle assignment_handles etc.
        #handle = int(command.split()[3])
        #if command.split()[1] == 'tset_context':
        #  self.device.assignment_handles = {k: v for k, v \
        #              in self.device.assignment_handles.items() if v != handle}
        self.device.do_table_delete(command.split('table_delete ' )[1])
      except DeleteRuleError as e:
        print('DeleteRuleError exception: ' + e.value)

    else:
      print("ERROR: pushcommand: " + command + ")")
      exit()

  def insert(self, position, instance):
    commands = [] # strs
    instance_ID = self.user.instances[instance].instance_ID

    if position == 0:
      if len(self.instance_chain) > 0:
        # entry point: table_modify
        for port in pports:
          handle = self.device.assignment_handles[pport]
          command = ("table_modify tset_context a_set_context "
                     + str(handle)
                     + " "
                     + str(instance_ID))
          commands.append(command)
      else:
        # entry point: table_add
        for port in pports:
          command = ("table_add tset_context a_set_context "
                     + str(port)
                     + " => "
                     + str(instance_ID))
          commands.append(command)

    elif len(self.instance_chain) > 0:
      # link left instance to new instance
      leftinst = self.user.instances[instance_chain[position - 1]]
      for handle in leftinst.t_virtnet_rule_handles:
        command = ("table_modify t_virtnet v_fwd "
                   + str(handle)
                   + " "
                   + str(instance_ID))
        commands.append(command)

      if position < len(self.instance_chain):
        # link new instance to next instance
        rightinst_ID = self.user.instances[instance_chain[position]].instance_ID
        for vegress_val in self.vegress_pports:
          command = ("table_add t_virtnet virt_fwd "
                     + str(instance_ID)
                     + " "
                     + str(vegress_val)
                     + " => "
                     + str(rightinst_ID))
          commands.append(command)

    if position == len(self.instance_chain):
      # link new instance to physical ports
      for vegress_val in self.vegress_pports:
        command = ("table_add t_virtnet phys_fwd "
                   + str(instance_ID)
                   + " "
                   + str(vegress_val)
                   + " => "
                   + str(self.vegress_pports[vegress_val]))
        commands.append(command)

    self.instance_chain.insert(position, instance)

    # push to HyPer4 one at a time
    for command in commands:
      self.pushcommand(command)

  def remove(self, instance):
    commands = [] # strs
    instance_ID = self.user.instances[instance].instance_ID

    # delete t_virtnet rules for the instance
    for handle in self.user.instances[instance].t_virtnet_rule_handles:
      commands.append("table_delete t_virtnet " + str(handle))
    self.user.instances[instance].t_virtnet_rule_handles = []

    position = self.instance_chain.index(instance)
    if position == 0:
      if len(self.instance_chain) > 1:
        # rewire tset_context to rightinst
        rightinst_ID = self.user.instances[instance_chain[position + 1]].instance_ID
        for pport in self.device.assignment_handles:
          handle = self.device.assignment_handles[pport]
          command = ("table_modify tset_context a_set_context "
                     + str(handle)
                     + " "
                     + str(rightinst_ID))
          commands.append(command)

      else:
        # delete tset_context rules
        for pport in self.device.assignment_handles:
          handle = self.device.assignment_handles[pport]
          commands.append("table_delete tset_context " + str(handle))
        self.device.assignment_handles = []

    elif position > 0 and position < (len(self.instance_chain) - 1): # middle
      # rewire leftinst t_virtnet to rightinst
      leftinst = self.user.instances[instance_chain[position - 1]]
      rightinst = self.user.instances[instance_chain[postion + 1]]
      for handle in leftinst.t_virtnet_rule_handles:
        command = ("table_modify t_virtnet v_fwd "
                   + str(handle)
                   + " "
                   + str(rightinst.instance_ID))
        commands.append(command)

    elif position > 0 and position == (len(self.instance_chain) - 1): # tail
      # rewire leftinst t_virtnet to phys
      leftinst = self.user.instances[instance_chain[position - 1]]
      for handle in leftinst.t_virtnet_rule_handles:
        commands.append("table_delete t_virtnet v_fwd " + str(handle))
      self.user.instances[leftinst].t_virtnet_rule_handles = []
      for vegress_val in self.vegress_pports:
        command = ("table_add t_virtnet phys_fwd "
                   + str(self.user.instances[leftinst].instance_ID)
                   + " "
                   + str(vegress_val)
                   + " => "
                   + str(self.vegress_pports[vegress_val]))
        commands.append(command)

    self.instance_chain.remove(instance)

    # push to HyPer4 one at a time
    for command in commands:
      self.pushcommand(command)

class User():
  def __init__(self, name):
    self.name = name

    # { device name : UDev }
    self.devices = {}

    # { instance name : Instance }
    self.instances = {}

class AddRuleError(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

class ModRuleError(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

class DeleteRuleError(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

class Device():
  def __init__(self, rta):
    self.rta = rta
    self.assignments = {} # {pport : instance_ID}
    self.assignment_handles = {} # {pport : tset_context rule handle}

  def do_table_add(rule):
    with Capturing() as output:
      self.rta.do_table_add(rule)
    for out in output:
      dbugprint(out)
      if 'Entry has been added' in out:
        handle = int(out.split('handle ')[1])
        return handle
      else:
        raise AddRuleError(out)

  def do_table_modify(rule):
    "In: rule (no \'table_modify\'); Out: None (but failure raises Exception)"
    try:
      with Capturing() as output:
        self.rta.do_table_modify(rule)
    except:
      print("table_modify raised an exception (rule: " + rule + ")")
      raise
    else:
      for out in output:
        dbugprint(out)
        if ('Invalid' in out) or ('Error' in out):
          raise ModRuleError(out)

  def do_table_delete(rule):
    "In: <table name> <entry handle>"
    with Capturing() as output:
      try:
        self.rta.do_table_delete(rule)
      except:
        raise DeleteRuleError("table_delete raised an exception (rule: " + rule + ")")
    for out in output:
      dbugprint(out)
      if ('Invalid' in out) or ('Error' in out):
        raise DeleteRuleError(out)

def server(args):
  ctrl = Controller(args.debug)
  ctrl.dbugprint(args)

class Controller():
  def __init__(self, debug):
    self.users = {} # user name (str) : User
    self.devices = {} # device name (str) : Device
    self.debug = debug

  def parse_request(self, request):
    "Parse a request"
    pass

  def insert(self, user, device, position, instance):
    self.users[user].devices[device].insert(position, instance)

  def remove(self, user, device, instance):
    self.users[user].devices[device].remove(instance)

  def add_device(self, ip, port, name):
    "Add a device"
    pass

  def add_user(self, user, devices):
    "Add a user"
    pass

  def grant_device(self, user, device, pports):
    "Grant a user access to a device's physical ports"
    pass

  def compile_p4(self, user, p4f):
    "Compile a P4 program"
    pass

  def load(self, user, hp4, instance, device):
    "Link an hp4->instance and load the instance onto a device"
    pass

  def interpret(self, user, instance, rule):
    "Interpret a rule"
    pass

  def migrate(self, user, instance, newdevice):
    "Migrate an instance to a new device"
    pass

  def wipe(self, device):
    "Wipe a device clean of all rules"
    pass

  def set_defaults(self, device):
    "Push default rules to a device"
    pass

  def dbugprint(self, msg):
    if self.debug:
      print(msg)

def parse_args(args):
  class ActionToPreType(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
      if nargs is not None:
        raise ValueError("nargs not allowed")
      super(ActionToPreType, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
      assert(type(values) is str)
      setattr(namespace, self.dest, PreType.from_str(values))

  parser = argparse.ArgumentParser(description='HyPer4 Control')
  parser.add_argument('--debug', help='turn on debug mode',
                      action='store_true')

  parser.add_argument('--port', help='port for Controller',
                      type=int, action="store", default=33333)
  parser.add_argument('--pre', help='Packet Replication Engine used by target',
                      type=str, choices=['None', 'SimplePre', 'SimplePreLAG'],
                      default=runtime_CLI.PreType.SimplePre,
                      action=ActionToPreType)
  parser.set_defaults(func=server)

  return parser.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  args.func(args)

if __name__ == '__main__':
  main()
