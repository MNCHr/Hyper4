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
    self.t_virtnet_rule_handles = []
    self.func_rule_handles = {} # hp4 table name (str) : rule handle (int)
    self.match_rule_handles = {} # hp4 table name (str) : rule handle (int)
    self.p4f = p4f
    self.hp4tf = hp4tf
    self.hp4mtf = hp4mtf

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
  def insert(self, position, instance):
    commands = [] # strs
    instance_ID = self.user.instances[instance].instance_ID
    if len(self.instance_chain) > 0:
      if position == 0:
        # table_modify
        for port in pports:
          handle = self.device.assignment_handles[pport]
          command = ("table_modify tset_context a_set_context "
                     + str(handle)
                     + " "
                     + str(instance_ID))
          commands.append(command)

      else: # link left instance to new instance
        leftinst = self.user.instances[instance_chain[position - 1]
        for handle in leftinst.t_virtnet_rule_handles:
          command = ("table_modify t_virtnet v_fwd "
                     + str(handle)
                     + " "
                     + str(leftinst.instance_ID))
          commands.append(command)

      if position < len(self.instance_chain):
        # link new instance to next instance
        rightinst_ID = self.user.instances[instance_chain[position]].instance_ID
        for vegress_val in self.vegress_pports:
          command = ("table_add t_virtnet virt_fwd "
                     + str(instance_ID)
                     + str(vegress_val)
                     + " => "
                     + str(rightinst_ID))

    self.instance_chain.insert(position, instance)

  def remove(self, instance):

    self.instance_chain.remove(instance)

class User():
  def __init__(self, name):
    self.name = name

    # { device name : UDev }
    self.devices = {}

    # { instance name : Instance }
    self.instances = {}

class Device():
  def __init__(self):

    # {pport : instance_ID}
    self.assignments = {}
    # {pport : tset_context rule handle}
    self.assignment_handles = {}

class Controller():
  def __init__(self):
    self.users = {}

class Client():
  def __init__(self):

