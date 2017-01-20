#!/usr/bin/python

from p4_hlir.main import HLIR
import p4_hlir
from p4_hlir.hlir.p4_core import p4_enum
from collections import OrderedDict
import argparse
import code
import sys
import math

RETURN_TYPE = 0
CRITERIA = 1
NEXT_PARSE_STATE = 1
CASE_ENTRIES = 2

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
    if self.command == 'table_add':
      ret += ' =>'
    elif self.command != 'table_set_default':
      print("ERROR: incorrect table command %s, table %s" % (self.command, self.table))
      exit()
    for param in self.action_params:
      ret += ' ' + param
    return ret

class TICS(HP4_Command):
  def __init__(self):
    HP4_Command.__init__(self, '', '', '', [], [])
    self.curr_pc_state = 0
    self.next_pc_state = 0
    self.next_parse_state = '' 

class MatchParam():
  def __init__(self):
    self.value = 0
    self.mask = 0
  def __str__(self):
    return format(self.value, '#04x') + '&&&' + format(self.mask, '#04x')

class HP4C:
  def __init__(self, h, args):
    self.pc_bits_extracted = {}
    # TODO: put this to use:
    self.pc_bits_extracted_curr = {}
    self.pc_action = {}
    self.field_offsets = {}
    self.offset = 0
    # TODO: put this to use or eliminate:
    self.next_pc_states = {}
    self.ps_to_pc = {}
    self.pc_to_ps = {}
    self.pc_to_preceding_pcs = {}
    self.vbits = {}
    self.tics_match_offsets = {}
    self.tics_table_names = {}
    self.tics_list = []
    self.table_to_stage = {}
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
    # track pc - ps membership
    if self.ps_to_pc.has_key(parse_state) is False:
      self.ps_to_pc[parse_state] = set()
    if pc_state == 0:
      self.ps_to_pc[parse_state].add(1)
      self.pc_to_ps[1] = parse_state
    else:
      self.ps_to_pc[parse_state].add(pc_state)
      self.pc_to_ps[pc_state] = parse_state

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
    if parse_state.return_statement[RETURN_TYPE] == 'immediate':
      if parse_state.return_statement[NEXT_PARSE_STATE] == 'ingress':
        self.pc_action[pc_state] = '[PROCEED]'
    elif parse_state.return_statement[RETURN_TYPE] == 'select':
      tics_pc_state = pc_state
      if tics_pc_state == 0:
        tics_pc_state += 1
      # account for 'current' instances
      maxcurr = 0
      # identify range of bytes to examine
      startbytes = 100
      endbytes = 0
      self.tics_match_offsets[tics_pc_state] = []
      for criteria in parse_state.return_statement[CRITERIA]:
        if isinstance(criteria, tuple): # tuple indicates use of 'current'
          # criteria[0]: start offset from current position
          # criteria[1]: width of 'current' call
          maxcurr = criteria[0] + criteria[1]
          if (startbytes * 8) > self.offset + criteria[0]:
            startbytes = (self.offset + criteria[0]) / 8
          if (endbytes * 8) < self.offset + maxcurr:
            endbytes = int(math.ceil((self.offset + maxcurr) / 8.0))
        else: # single field
          self.tics_match_offsets[tics_pc_state].append((self.field_offsets[criteria],self.h.p4_fields[criteria].width))
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
          self.tics_table_names[tics_pc_state] = 'tset_inspect_SEB'
      else:
        bound = self.args.seb + 10
        while bound <= 100:
          if startbytes < bound:
            if endbytes >= bound:
              unsupported(startbytes, endbytes)
            else:
              namecore = 'inspect_' + str(bound - 10) + '_' + str(bound - 1)
              self.pc_action[pc_state] = '[' + namecore.upper() + ']'
              self.tics_table_names[tics_pc_state] = 'tset_' + namecore
              break
          bound += 10
      if pc_state not in self.pc_action:
        print("ERROR: did not find inspect_XX_YY function for startbytes(%i) and endbytes(%i)" % (startbytes, endbytes))
        exit()

  def fill_tics_match_params(self, criteria_fields, values, pc_state):
    if len(criteria_fields) != len(values):
      print("ERROR: criteria_fields(%i) not same length as values(%i)" % (len(criteria_fields),len(values)))
      exit()
    # looking at a single criteria field is sufficient to determine the byte
    #  range for the inspection, which affects the size of the match
    #  parameters string (20 bytes for SEB, 10 bytes for everything else)
    mparams = []
    mparams_count = 10
    if self.field_offsets[criteria_fields[0]] / 8 < self.args.seb:
      mparams_count = 20
    for i in range(mparams_count):
      mparams.append(MatchParam())

    for i in range(len(criteria_fields)):
      if values[i][0] != 'value' and values[i][0] != 'default':
        print("Not yet supported: type %s in case entry" % values[i][0])
        exit()
      fo = self.field_offsets[criteria_fields[i]]
      j = (fo / 8) % len(mparams)
      width = self.h.p4_fields[criteria_fields[i]].width
      fieldend = fo + width
      end_j = (int(math.ceil(fieldend / 8.0)) - 1) % len(mparams)
      value = 0
      if values[i][0] == 'value':
        value = values[i][1]
      while j <= end_j:
        mask = 0b00000000
        pos = fo % 8
        end = min(pos + width, 8)
        if values[i][0] == 'value':
          bit = 128 >> pos
          while pos < end:
            mask = mask | bit
            bit = bit >> 1
            pos += 1
        # truncate bits outside current byte boundary
        val = value >> (((fo % 8) + width) - end)
        # lshift to place value in correct position within current byte
        val = val << (8 - end)
        
        mparams[j].mask = mparams[j].mask | mask
        mparams[j].value = mparams[j].value | val
        j += 1
        advance = 8 - (fo % 8)
        # advance fo
        fo = fo + advance
        # reduce width
        width = width - advance
        # change values[i]
        if width > 0:
          value = value % (1 << width)
    ret = ['[program ID]', str(pc_state)]
    for mparam in mparams:
      ret.append(str(mparam))
    return ret

  def walk_ingress_pipeline(self, curr_table):
    # traverse the pipeline
    # TODO: implement this depth-first traversal

  # TODO: resolve concern that direct jumps not merged properly  
  def walk_parse_tree(self, parse_state, pc_state):
    self.process_parse_state(parse_state, pc_state)

    curr_pc_state = pc_state
    if curr_pc_state == 0:
      curr_pc_state += 1
      self.pc_to_preceding_pcs[curr_pc_state] = []

    # traverse parse tree
    next_states = []
    next_states_pcs = {}
    if parse_state.return_statement[RETURN_TYPE] == 'immediate':
      if parse_state.return_statement[NEXT_PARSE_STATE] != 'ingress':
        next_state = self.h.p4_parse_states[parse_state.return_statement[1]]
        self.walk_parse_tree(next_state, pc_state)
      else:
        return
    elif parse_state.return_statement[RETURN_TYPE] == 'select':
      self.next_pc_states[curr_pc_state] = []
      # return_statement[CASE_ENTRIES]: list of tuples (see case_entry below)
      for case_entry in parse_state.return_statement[CASE_ENTRIES]:
        t = TICS()
        t.command = "table_add"
        t.curr_pc_state = curr_pc_state
        t.table = self.tics_table_names[curr_pc_state]
        t.match_params = self.fill_tics_match_params(parse_state.return_statement[CRITERIA], case_entry[0], t.curr_pc_state)
        # case_entry: (list of values, next parse_state)
        if case_entry[1] != 'ingress':
          next_state = self.h.p4_parse_states[case_entry[1]]
          t.next_parse_state = next_state
          if next_state not in next_states:
            if pc_state == 0:
              pc_state += 1
            pc_state += 1
            next_states_pcs[next_state] = pc_state

            # track preceding pc_states
            if self.pc_to_preceding_pcs.has_key(curr_pc_state) is False:
              self.pc_to_preceding_pcs[curr_pc_state] = []
            self.pc_to_preceding_pcs[pc_state] = self.pc_to_preceding_pcs[curr_pc_state] + [curr_pc_state]

            self.next_pc_states[curr_pc_state].append(pc_state)
            # TODO: verify this line is correct; does it account for 'current'?
            self.pc_bits_extracted[pc_state] = self.offset
            next_states.append(next_state)
            t.next_pc_state = pc_state
          else:
            t.next_pc_state = next_states_pcs[next_state]
        else:
          t.next_parse_state = 'ingress'
          t.next_pc_state = t.curr_pc_state
          t.action = 'set_next_action'
          t.action_params = ['[PROCEED]', str(t.next_pc_state)]
        self.tics_list.append(t)
    else:
      print("ERROR: Unknown directive in return statement: %s" \
            % parse_state.return_statement[0])
      exit()

    save_offset = self.offset
    for next_state in next_states:
      self.walk_parse_tree(next_state, next_states_pcs[next_state])
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
          self.pc_bits_extracted[0] = self.args.seb * 8

        self.pc_bits_extracted[1] = self.pc_bits_extracted[0]
        self.pc_bits_extracted[0] = self.args.seb * 8
        self.pc_action[1] = self.pc_action[0]

      else:
        self.commands.append(HP4_Command("table_add",
                                         "tset_control",
                                         "set_next_action",
                                         ["[program ID]", str(key)],
                                         [self.pc_action[key], str(key)]))

  def gen_tset_inspect_entries(self):
    for t in self.tics_list:
      if t.next_parse_state != 'ingress':
        if self.pc_bits_extracted[t.next_pc_state] > self.pc_bits_extracted[t.curr_pc_state]:
          t.action = "extract_more"
          t.action_params = [str(self.pc_bits_extracted[t.next_pc_state]), str(t.next_pc_state)]
        else:
          print("TODO: support direct jump to new parse node without extracting more")
          exit()
      self.commands.append(t)

  def gen_tset_pr_entries(self):
    # table_set_default <table name> <action name> <action parameters>
    self.commands.append(HP4_Command("table_set_default",
                                     "tset_pr_SEB",
                                     "a_pr_import_SEB",
                                     [],
                                     []))

    # 1) identify highest byte range extracted anywhere in the parse tree
    # 2) for SEB and all later byte ranges up to and including the one identified
    #    in step 1, generate default table entry
    max_extracted = int(math.ceil(max(self.pc_bits_extracted.values()) / 8.0))
    bound = self.args.seb
    while bound < max_extracted:
      if bound >= 100:
        print("ERROR: unsupported max extraction of %i bytes" % max_extracted)
        exit()
      tablename = 'tset_pr_' + str(bound) + '_' + str(bound + 9)
      action = 'a_pr_import_' + str(bound) + '_' + str(bound + 9)
      self.commands.append(HP4_Command("table_set_default",
                                       tablename,
                                       action,
                                       [],
                                       []))
      bound += 10

  def gen_tset_pipeline_entries(self):
    # USEFUL DATA STRUCTURES:
    # self.ps_to_pc = {p4_parse_state : pc_state}
    # self.pc_to_ps = {pc_state : p4_parse_state}
    # self.pc_to_preceding_pcs = {pc_state : [pc_state, ..., pc_state]}
    # self.h.p4_ingress_ptr = {p4_table: set([p4_parse_state, ..., p4_parse_state])}
    # self.h.p4_ingress_ptr.keys()[0].match_fields: (p4_field, MATCH_TYPE, None)
    #    MATCH_TYPE: P4_MATCH_EXACT | ? (no doubt P4_MATCH_VALID, others)
    #    third is probably mask
    if len(self.h.p4_ingress_ptr.keys()) > 1:
      print("Not yet supported: multiple entry points into ingress pipeline")
      exit()
    first_table = self.h.p4_ingress_ptr.keys()[0]
    if len(first_table.match_fields) > 1:
      print("Not yet supported: multiple field matches (table: %s)" % first_table.name)
      exit()

    # create all the valid values for extracted.validbits
    pc_headers = {}
    longest = 0
    for ingress_ps in self.h.p4_ingress_ptr[first_table]:
      for pc_state in self.ps_to_pc[ingress_ps]:
        pc_headers[pc_state] = []
        #code.interact(local=locals())
        for prec_pc in self.pc_to_preceding_pcs[pc_state]:
          ps = self.pc_to_ps[prec_pc]
          for call in ps.call_sequence:
            if call[0].value != 'extract':
              print("ERROR (gen_tset_pipeline_entries): unsupported call %s" % call[0].value)
              exit()
            pc_headers[pc_state].append(call[1])
        for call in ingress_ps.call_sequence:
          if call[0].value != 'extract':
            print("ERROR (gen_tset_pipeline_entries): unsupported call %s" % call[0].value)
            exit()
          pc_headers[pc_state].append(call[1])

        if len(pc_headers[pc_state]) > longest:
          longest = len(pc_headers[pc_state])

    headerset = []
    for j in range(longest):
      headerset.append(set())
      
      for pc_state in pc_headers.keys():
        if len(pc_headers[pc_state]) > j:
          headerset[j].add(pc_headers[pc_state][j])

    # extracted.validbits is 80b wide
    # vbits: {(level (int), header name (str)): number (binary)}
    #vbits = {}
    lshift = 80
    for j in range(longest):
      numbits = len(headerset[j])
      lshift = lshift - numbits
      i = 1
      for header in headerset[j]:
        self.vbits[(j, header)] = i << lshift
        i = i << 1

    field_match = first_table.match_fields[0]
    match_type = field_match[1]
    if match_type.value != 'P4_MATCH_EXACT':
      print("Not yet supported: match type %s" % match_type.value)
      exit()
    else:
      aparam_table_ID = '[EXTRACTED_EXACT]'

    for ps in self.h.p4_ingress_ptr[first_table]:
      for pc_state in self.ps_to_pc[ps]:
        val = 0
        for i in range(len(pc_headers[pc_state])):
          val = val | self.vbits[(i, pc_headers[pc_state][i])]
        valstr = '0x' + '%x' % val

        self.commands.append(HP4_Command("table_add",
                                         "tset_pipeline",
                                         "a_set_pipeline",
                                         ['[program ID]', str(pc_state)],
                                         [aparam_table_ID, valstr]))

  def gen_stage_mappings(self):
    self.walk_ingress_pipeline(self.h.p4_ingress_ptr.keys()[0])

  def write_output(self):
    out = open(self.args.output, 'w')
    for command in self.commands:
      out.write(str(command) + '\n')
    out.close()

def main():
  args = parse_args(sys.argv[1:])
  hp4c = HP4C(HLIR(args.input), args)
  hp4c.gen_tset_context_entry()
  hp4c.gen_tset_control_entries()
  hp4c.gen_tset_inspect_entries()
  hp4c.gen_tset_pr_entries()
  hp4c.gen_tset_pipeline_entries()
  hp4c.gen_stage_mappings()
  hp4c.write_output()
  #code.interact(local=locals())

if __name__ == '__main__':
  main()
