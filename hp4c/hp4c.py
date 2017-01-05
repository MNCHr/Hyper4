#!/usr/bin/python

from p4_hlir.main import HLIR
import p4_hlir
from p4_hlir.hlir.p4_core import p4_enum
from collections import OrderedDict
import argparse
import code
import sys
import math

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
    self.pc_bits_extracted = {}
    self.pc_bits_extracted_curr = {}
    self.pc_action = {}
    self.field_offsets = {}
    self.offset = 0
    self.commands = []
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

  def process_parse_state(self, parse_state, pc_state):
    numbits = self.offset
    for call in parse_state.call_sequence:
      if call[0].value != 'extract':
        print("ERROR: unsupported call %s" % call[0].value)
        exit()
      # update field_offsets, numbits
      for field in call[1].fields:
        self.field_offsets[call[1].name + '.' + field.name] = self.offset
        self.offset += field.width # advance current offset
        numbits += field.width
    self.pc_bits_extracted[pc_state] = numbits
    if parse_state.return_statement[0] == 'immediate':
      if parse_state.return_statement[1] == 'ingress':
        self.pc_action[pc_state] = '[PROCEED]'
    elif parse_state.return_statement[0] == 'select':
      # account for 'current' instances
      maxcurr = 0
      # identify range of bytes to examine
      startbytes = 100
      endbytes = 0
      for criteria in parse_state.return_statement[1]:
        if isinstance(criteria, tuple): # tuple indicates use of 'current'
          # criteria[0]: start offset from current position
          # criteria[1]: width of 'current' call
          maxcurr = criteria[0] + criteria[1]
          if (startbytes * 8) > self.offset + criteria[0]:
            startbytes = (self.offset + criteria[0]) / 8
          if (endbytes * 8) < self.offset + maxcurr:
            endbytes = int(math.ceil((self.offset + maxcurr) / 8.0))
        else: # single field
          fieldstart = self.field_offsets[criteria] / 8
          fieldend = int(math.ceil((fieldstart * 8
                                    + self.h.p4_fields[criteria].width) / 8.0))
          if startbytes > fieldstart:
            startbytes = fieldstart
          if endbytes < fieldend:
            endbytes = fieldend
          
      self.pc_bits_extracted[pc_state] += maxcurr
      self.pc_bits_extracted_curr[pc_state] = maxcurr
  
      # pc_action[pc_state] = 'inspect_XX_YY'
      if startbytes >= endbytes:
        print("ERROR: startbytes(%i) > endbytes(%i)" % (startbytes, endbytes))
        print("parse_state: %s" % parse_state)
        exit()
      def unsupported(sbytes, ebytes):
        print("Not yet supported: startbytes(%i) and endbytes(%i) cross boundaries"  % (sbytes, ebytes))
        exit()
      if startbytes < self.args.seb:
        if endbytes >= self.args.seb:
          unsupported(startbytes, endbytes)
        else:
          self.pc_action[pc_state] = '[INSPECT_SEB]'
      else:
        bound = self.args.seb + 10
        while bound <= 100:
          if startbytes < bound:
            if endbytes >= bound:
              unsupported(startbytes, endbytes)
            else:
              self.pc_action[pc_state] = '[INSPECT_' + str(bound - 10) + '_' \
                                    + str(bound - 1) + ']'
              break
          bound += 10
      if pc_state not in self.pc_action:
        print("ERROR: did not find inspect_XX_YY function for startbytes(%i) and endbytes(%i)" % (startbytes, endbytes))
        exit()
  
  # TODO: resolve concern that direct jumps not merged properly  
  def walk_parse_tree(self, parse_state, pc_state):
    self.process_parse_state(parse_state, pc_state)
  
    # traverse parse tree
    next_states = []
    if parse_state.return_statement[0] == 'immediate':
      if parse_state.return_statement[1] != 'ingress':
        next_state = self.h.p4_parse_states[parse_state.return_statement[1]]
        self.walk_parse_tree(next_state, pc_state)
      else:
        return
    elif parse_state.return_statement[0] == 'select':
      for selectopt in parse_state.return_statement[2]:
        # selectopt: (list of values, next parse_state)
        if selectopt[1] != 'ingress':
          next_state = self.h.p4_parse_states[selectopt[1]]
          if next_state not in next_states:
            next_states.append(next_state)
    else:
      print("ERROR: Unknown directive in return statement: %s" \
            % parse_state.return_statement[0])
      exit()

    save_offset = self.offset
    if pc_state == 0:
      pc_state += 1
    for next_state in next_states:
      pc_state += 1
      self.pc_bits_extracted[pc_state] = save_offset
      self.walk_parse_tree(next_state, pc_state)
      self.offset = save_offset

  def gen_tset_control_entries(self):
    self.walk_parse_tree(self.h.p4_parse_states['start'], 0)

    for key in self.pc_action.keys():
      # special handling for pc_state 0
      if key == 0:
        if self.pc_bits_extracted[0] > (self.args.seb * 8):
          self.commands.append(HP4_Command("table_add",
                                           "tset_control",
                                           "extract_more",
                                           ["[program ID]", "0"],
                                           [str(self.pc_bits_extracted[0]), "1"]))
          self.commands.append(HP4_Command("table_add",
                                           "tset_control",
                                           "set_next_action",
                                           ["[program ID]", "1"],
                                           [self.pc_action[0], "1"]))
        else:
          self.commands.append(HP4_Command("table_add",
                                           "tset_control",
                                           "set_next_action",
                                           ["[program ID]", "0"],
                                           [self.pc_action[0], "1"]))
        self.pc_bits_extracted[1] = self.pc_bits_extracted[0]
        self.pc_bits_extracted[0] = self.args.seb
        self.pc_action[1] = self.pc_action[0]
        self.pc_action[0] = "extract_more"

      else:
        self.commands.append(HP4_Command("table_add",
                                         "tset_control",
                                         "set_next_action",
                                         ["[program ID]", str(key)],
                                         [self.pc_action[key], str(key)]))

def main():
  args = parse_args(sys.argv[1:])
  hp4c = HP4C(HLIR(args.input), args)
  hp4c.gen_tset_context_entry()
  hp4c.gen_tset_control_entries()
  code.interact(local=locals())

if __name__ == '__main__':
  main()
