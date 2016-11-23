#!/usr/bin/python

from p4_hlir.main import HLIR
import p4_hlir
from p4_hlir.hlir.p4_core import p4_enum
from collections import OrderedDict
import argparse
import code
import sys

def parse_args(args):
  parser = argparse.ArgumentParser(description='HP4 Compiler')
  parser.add_argument('input', help='path for input .p4',
                    type=str)
  parser.add_argument('-o', '--output', help='path for output .hp4t file',
                    type=str, action="store", required=True)
  parser.add_argument('-s', '--seb', help='set standard extracted bytes',
                    type=int, action="store", default=20)
  return parser.parse_args(args)

class HP4_Command:
  def __init__(self, command, table, action, mparams, aparams):
    self.command = command
    self.table = table
    self.action = action
    self.match_params = mparams
    self.action_params = aparams
  def __str__(self):
    ret = self.command + ' ' + self.table + ' ' + self.action
    for param in self.match_params:
      ret += ' ' + param
    ret += ' =>'
    for param in self.action_params:
      ret += ' ' + param
    return ret

class HP4C:
  def __init__(self, h, args):
    self.parseControlStates = {}
    self.bits_needed_local = {}
    self.bits_needed_total = {}
    self.field_offsets = {}
    self.commands = []
    self.pc_state_id = 1
    self.h = h
    self.h.build()
    if len(self.h.p4_ingress_ptr) > 1:
      print("ERROR: multiple ingress entry points:")
      for node in h.p4_ingress_ptr.keys():
        print('  ' + node)
      exit()
    self.args = args

  def gen_tset_context_entry(self):
    self.commands.append(HP4_Command("table_add",
                                       "tset_context",
                                       "set_program",
                                       ["[PPORT]"],
                                       ["[program ID]", "[VPORT_0]"]))

  def collect_local_bits_needed(self, parse_state):
    numbits = 0
    # collect total number of bits to extract in the state
    for call in parse_state.call_sequence:
      if call[0].value != 'extract':
        print("ERROR: unsupported call %s" % call[0].value)
        exit()
      for key in call[1].header_type.layout.keys():
        numbits += call[1].header_type.layout[key]

    maxcurr = 0
    # look for 'current' instances in the return statement
    if parse_state.return_statement[0] == 'select':
      for criteria in parse_state.return_statement[1]:
        if isinstance(criteria, tuple): # tuple indicates use of 'current'
          # criteria[0]: start offset from current position
          # criteria[1]: width of 'current' call
          if criteria[0] + criteria[1] > maxcurr:
            maxcurr = criteria[0] + criteria[1]
      numbits += maxcurr
    elif parse_state.return_statement[0] != 'immediate':
      print("ERROR: Unknown directive in return statement: %s" % parse_state.return_statement[0])
      exit()
    self.bits_needed_local[parse_state] = (numbits, maxcurr)

  def collect_total_bits_needed(self, parse_state, preceding_parse_states):
    numbits = self.bits_needed_local[parse_state][0]
    for precstate in preceding_parse_states:
      numbits += self.bits_needed_local[precstate][0]
      # deduct for instances of 'current':
      numbits -= self.bits_needed_local[precstate][1]
    self.bits_needed_total[(parse_state, tuple(preceding_parse_states))] = numbits

    # build queue of parse_states
    next_states = []
    if parse_state.return_statement[0] == 'immediate':
      if parse_state.return_statement[1] != 'ingress':
        next_states.append(self.h.p4_parse_states[parse_state.return_statement[1]])
      else:
        return
    elif parse_state.return_statement[0] == 'select':
      for selectopt in parse_state.return_statement[2]:
        if selectopt[1] != 'ingress':
          next_states.append(self.h.p4_parse_states[selectopt[1]])
    else:
      print("ERROR: Unknown directive in return statement: %s" % parse_state.return_statement[0])
      exit()

    # recurse for every next state reachable from this state
    for next_state in next_states:
      next_preceding_states = list(preceding_parse_states)
      next_preceding_states.append(parse_state)
      self.collect_total_bits_needed(next_state, next_preceding_states)

  def collectParseControlStates(self):
    for parse_state in self.h.p4_parse_states.values():
      self.collect_local_bits_needed(parse_state)
    self.collect_total_bits_needed(self.h.p4_parse_states['start'], [])
    for key in self.bits_needed_total.keys():
      if key[0] == self.h.p4_parse_states['start']:
        self.parseControlStates[key] = 0
      else:
        self.parseControlStates[key] = self.pc_state_id
        self.pc_state_id += 1
  
  #def gen_tset_control_entries(self):
    #for pc_state in self.parseControlStates.keys():
      

def main():
  args = parse_args(sys.argv[1:])
  hp4c = HP4C(HLIR(args.input), args)
  hp4c.gen_tset_context_entry()
  hp4c.collectParseControlStates()
  #hp4c.gen_tset_control_entries()
  code.interact(local=locals())

if __name__ == '__main__':
  main()
