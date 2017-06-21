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
  def __init__(self, name, user, vports, instance_ID, p4f, hp4tf, hp4mtf):
    self.name = name
    self.user = user
    self.vports = vports # {vportnum (int) : Virtual_Port}
    self.vmcast_grps = {} # vmcast_grp_ID (int) : Virtual_Mcast_Group
    self.vmcast_nodes = {} # vmcast_node_handle (int) : Virtual_Mcast_Node
    self.instance_ID = instance_ID
    # need this in order to properly fill in match ID parameters
    self.match_counters = {} # source table name (str) : match counter (int)
    self.t_virtnet_rule_handles = [] # [handles (ints)]
    self.func_rule_handles = [] # hp4 table name (str) : [list of rule handles (ints)]
    self.match_rule_handles = {} # hp4 table name (str) : [list of rule handles (ints)]
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
        for pport in self.pports:
          handle = self.device.assignment_handles[pport]
          command = ("table_modify tset_context a_set_context "
                     + str(handle)
                     + " "
                     + str(rightinst_ID))
          commands.append(command)

      else:
        self.delete_tset_context_rules()

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
        commands.append("table_delete t_virtnet " + str(handle))
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

  def delete_tset_context_rules(self):
    "Delete tset_context rules"
    commands = []
    for pport in self.pports:
      handle = self.devices.assignment_handles[pport]
      commands.append("table_delete tset_context " + str(handle))
      del self.device.assignment_handles[pport]
    for command in commands:
      self.pushcommand(command)

  def revoke(self):
    self.device.release_ports(self.pports)
    commands = []

    self.delete_tset_context_rules()

    for instance in self.instance_chain:
      # delete t_virtnet rules
      for rh in self.user.instances[instance].t_virtnet_rule_handles:
        commands.append("table_delete t_virtnet " + str(rh))
      # delete all of the instances rules: func & match
      for table in self.user.instances[instance].func_rule_handles:
        for handle in self.user.instances[instance].func_rule_handles[table]:
          commands.append("table_delete " + table + " " + str(handle))
      self.user.instances[instance].func_rule_handles = {}
      for table in self.user.instances[instance].match_rule_handles:
        for handle in self.user.instances[instance].match_rule_handles[table]:
          commands.append("table_delete " + table + " " + str(handle))
      self.user.instances[instance].match_rule_handles = {}

    for command in commands:
      self.pushcommand(command)

class User():
  def __init__(self, name, privilege='user'):
    self.name = name
    self.privilege = privilege # 'user' | 'admin'

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
  def __init__(self, rta, entries, phys_ports):
    self.rta = rta
    self.assignments = {} # {pport : instance_ID}
    self.assignment_handles = {} # {pport : tset_context rule handle}
    self.next_PID = 1
    self.total_entries = entries
    self.phys_ports = phys_ports
    self.phys_ports_remaining = list(phys_ports)

  def request_ports(self, ports_requested):
    ports_granted = []
    for port in ports_requested:
      if port in self.phys_ports_remaining:
        self.phys_ports_remaining.remove(port)
        ports_granted.append(port)
    return ports_granted

  def release_ports(self, ports_releasable):
    ports_released = []
    for port in ports_releasable:
      if port in self.phys_ports:
        self.phys_ports_remaining.append(port)
        ports_released.append(port)
    return ports_released

  def do_table_add(self, rule):
    with Capturing() as output:
      try:
        self.rta.do_table_add(rule)
      except:
        raise AddRuleError("table_add raised an exception (rule: " + rule + ")")
      else:
        self.total_entries -= 1
    for out in output:
      dbugprint(out)
      if 'Entry has been added' in out:
        handle = int(out.split('handle ')[1])
        return handle
    raise AddRuleError(out)

  def do_table_modify(self, rule):
    "In: rule (no \'table_modify\'); Out: None (but failure raises Exception)"
    with Capturing() as output:
      try:
        self.rta.do_table_modify(rule)
      except:
        raise ModRuleError("table_modify: unhandled server exception (rule: " + rule + ")")
    for out in output:
      dbugprint(out)
      if ('Invalid' in out) or ('Error' in out):
        raise ModRuleError("table_modify: handled server exception (rule: "
                           + rule + "\nout: " + out)

  def do_table_delete(self, rule):
    "In: <table name> <entry handle>"
    with Capturing() as output:
      try:
        self.rta.do_table_delete(rule)
      except:
        raise DeleteRuleError("table_delete raised an exception (rule: " + rule + ")")
      else:
        self.total_entries += 1
    for out in output:
      dbugprint(out)
      if ('Invalid' in out) or ('Error' in out):
        raise DeleteRuleError(out)

  def do_reset_device(self):
    "Reset all device state (table entries, registers, etc.)"
    self.rta.do_reset_state('')

  def do_set_defaults(self):
    "Set HP4 instance-independent defaults"
    self.rta.do_table_set_default('tset_pr_SEB a_pr_import_SEB')
    self.rta.do_table_set_default('tset_pr_20_39 a_pr_import_20_39')
    self.rta.do_table_set_default('tset_pr_40_59 a_pr_import_40_59')
    self.rta.do_table_set_default('tset_pr_60_79 a_pr_import_60_79')
    self.rta.do_table_set_default('tset_pr_80_99 a_pr_import_80_99')
    self.rta.do_table_set_default('thp4_egress_filter_case1 _no_op')
    self.rta.do_table_set_default('thp4_egress_filter_case2 _no_op')
    self.rta.do_table_set_default('t_checksum _no_op')
    self.rta.do_table_set_default('t_resize_pr _no_op')
    self.rta.do_table_set_default('t_prep_deparse_SEB a_prep_deparse_SEB')
    self.rta.do_table_set_default('t_prep_deparse_20_39 a_prep_deparse_20_39')
    self.rta.do_table_set_default('t_prep_deparse_40_59 a_prep_deparse_40_59')
    self.rta.do_table_set_default('t_prep_deparse_60_79 a_prep_deparse_60_79')
    self.rta.do_table_set_default('t_prep_deparse_80_99 a_prep_deparse_80_99')

def server(args):
  ctrl = Controller(args)
  ctrl.add_user(['system', 'admin', 'admin'])
  ctrl.dbugprint(args)
  ctrl.serverloop(args.host, args.port)

class Controller():
  def __init__(self, args):
    self.users = {} # user name (str) : User
    self.devices = {} # device name (str) : Device
    self.args = args
    self.debug = args.debug
    self.usercommands = ['insert',
                          'remove',
                          'list_devices',
                          'compile_p4',
                          'load',
                          'interpret',
                          'migrate']
    self.compiledp4s = {} # p4 filename (str) : (hp4t filename (str), hp4mt filename(str))

  def handle_request(self, request):
    "Handle a request"
    if len(request) < 2:
      return "Request format: <requester uname> <command> [parameter list]"
    requester = request.split()[0]
    command = request.split()[1]
    parameters = [requester] + request.split()[2:]
    if requester not in self.users:
      return "Denied; no user " + requester
    elif (self.users[requester].privilege == 'user'
          and command not in self.usercommands):
      return "Denied; command not available to " + requester

    resp = ""
    try:
      resp = getattr(self, command)(parameters)
    except AttributeError:
      return "Command not found: " + command
    except:
      return "Unexpected error: " + str(sys.exc_info()[0])

    return resp

  def insert(self, user, device, position, instance):
    self.users[user].devices[device].insert(position, instance)

  def remove(self, user, device, instance):
    self.users[user].devices[device].remove(instance)

  #def add_device(self, ip, port, pre, name, entries, ports):
  def add_device(self, parameters):
    "Add a device"
    ip = parameters[1]
    port = parameters[2]
    pre = parameters[3]
    name = parameters[4]
    entries = parameters[5]
    ports = parameters[6:]
    prelookup = {'None': 0, 'SimplePre': 1, 'SimplePreLAG': 2}

    try:
      hp4_client, mc_client = runtime_CLI.thrift_connect(ip, port,
                  runtime_CLI.RuntimeAPI.get_thrift_services(prelookup[pre]))
    except:
        return "Error - add_device(" + name + "): " + str(sys.exc_info()[0])
      
    json = '/home/ubuntu/hp4-src/hp4/hp4.json'
    runtime_CLI.load_json_config(hp4_client, json)
    rta = runtime_CLI.RuntimeAPI(pre, hp4_client)
    self.devices[name] = Device(rta, entries, ports)
    return "Added device: " + name

  def list_devices(self, parameters):
    "List devices"
    requester = parameters[0]
    resp = ""
    if requester == 'admin':
      for device in self.devices:
        resp += device + '\n'
    else:
      for device in self.users[requester].devices:
         resp += device + '\n'
    return resp.strip()

  def add_user(self, parameters):
    "Add a user"
    user = parameters[1]
    privilege = 'user'
    if len(parameters) > 2:
      privilege = parameters[2]
    self.users[user] = User(user, privilege)
    return "Added user: " + user

  def list_users(self, parameters):
    "List users"
    resp = ""
    for user in self.users:
      resp += user + '\n'
    return resp.strip()

  def grant_device(self, parameters):
    "Grant a user access to a device's physical ports"
    requester = parameters[0]
    user = parameters[1]
    device = parameters[2]
    pports = parameters[3:]
    pports_granted = self.devices[device].request_ports(pports)
    if len(pports_granted) == 0:
      return "Error - grant_device: none of the requested ports available for " + device
    self.users[user].devices[device] = UDev(user, self.devices[device], pports_granted)
    return "User " + user + " granted access to " + device + ": " \
           + str(pports_granted)

  def revoke_device(self, parameters):
    "Revoke a user's access to a device"
    user = parameters[1]
    device = parameters[2]
    self.users[user].devices[device].revoke
    del self.users[user].devices[device]
    return "User " + user + " access to " + device + " revoked"

  # user p4f hp4tf hp4mtf ['egress_filter']
  def compile_p4(self, parameters):
    "Compile a P4 program"
    egress_filter = False
    p4f = parameters[1]
    hp4tf = parameters[2]
    hp4mtf = parameters[3]
    if len(parameters) > 4:
      if parameters[4] == 'egress_filter':
        egress_filter = True

    if egress_filter:
      if call(["./p4c-hp4", "-o", hp4tf, "-m", hp4mtf, "-s 20", p4f, '--egress_filter']) != 0:
        return 'ERROR: could not compile ' + p4f
    else:
      if call(["./p4c-hp4", "-o", hp4tf, "-m", hp4mtf, "-s 20", p4f]) != 0:
        return 'ERROR: could not compile ' + p4f

    self.compiledp4s[p4f] = (hp4tf, hp4mtf)
    return "Program " + p4f + " compiled as " + hp4f

  def load(self, user, hp4, instance, device):
    "Link an hp4->instance and load the instance onto a device"
    pass

  def interpret(self, user, instance, rule):
    "Interpret a rule"
    pass

  def migrate(self, user, instance, newdevice):
    "Migrate an instance to a new device"
    pass

  def reset_device(self, parameters):
    device = parameters[1]
    "Reset a device: reset all state, inc. table entries, registers, etc."
    self.devices[device].do_reset_device()
    return "Device " + device + " has been reset"

  def set_defaults(self, parameters):
    "Push default rules to a device"
    device = parameters[1]
    self.devices[device].do_set_defaults()
    return "Defaults added to " + device

  def serverloop(self, host, port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    serversocket.listen(5)

    while True:
      clientsocket = None
      try:
        clientsocket, addr = serversocket.accept()
        self.dbugprint("Got a connection from %s" % str(addr))
        data = clientsocket.recv(1024)
        self.dbugprint(data)
        response = self.handle_request(data)
        clientsocket.sendall(response)
        clientsocket.close()
      except KeyboardInterrupt:
        if clientsocket:
          clientsocket.close()
        serversocket.close()
        self.dbugprint("Keyboard Interrupt, sockets closed")
        break
    

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

  parser.add_argument('--host', help='host/ip for Controller',
                      type=str, action="store", default='localhost')
  parser.add_argument('--port', help='port for Controller',
                      type=int, action="store", default=33333)
  parser.set_defaults(func=server)

  return parser.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  args.func(args)

if __name__ == '__main__':
  main()
