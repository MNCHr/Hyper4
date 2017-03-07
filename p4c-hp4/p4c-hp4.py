#!/usr/bin/python

from p4_hlir.main import HLIR
import p4_hlir
from p4_hlir.hlir.p4_core import p4_enum
from collections import OrderedDict
import argparse
import code
import sys
import math
import json

RETURN_TYPE = 0
CRITERIA = 1
NEXT_PARSE_STATE = 1
CASE_ENTRIES = 2

primitive_ID = {'modify_field': '[MODIFY_FIELD]',
                'add_header': '[ADD_HEADER]',
                'copy_header': '[COPY_HEADER]',
                'remove_header': '[REMOVE_HEADER]',
                'modify_field_with_hash_based_offset': '[MODIFY_FIELD_WITH_HBO]',
                'truncate': '[TRUNCATE]',
                'drop': '[DROP]',
                'no_op': '[NO_OP]',
                'push': '[PUSH]',
                'pop': '[POP]',
                'count': '[COUNT]',
                'execute_meter': '[METER]',
                'generate_digest': '[GENERATE_DIGEST]',
                'recirculate': '[RECIRCULATE]',
                'resubmit': '[RESUBMIT]',
                'clone_ingress_pkt_to_egress': '[CLONE_INGRESS_EGRESS]',
                'clone_egress_pkt_to_egress': '[CLONE_EGRESS_EGRESS]',
                'multicast': '[MULTICAST]',
                'add_to_field': '[MATH_ON_FIELD]'}

primitive_tnames = {'modify_field': 'mod',
                    'add_header': 'addh',
                    'copy_header': '',
                    'remove_header': '',
                    'modify_field_with_hash_based_offset': '',
                    'truncate' : 'truncate',
                    'drop' : 'drop',
                    'no_op' : '',
                    'push' : '',
                    'pop' : '',
                    'count' : '',
                    'execute_meter': '',
                    'generate_digest': '',
                    'recirculate': '',
                    'resubmit': '',
                    'clone_ingress_pkt_to_egress': '',
                    'clone_egress_pkt_to_egress': '',
                    'multicast': 'multicast',
                    'add_to_field': 'math_on_field'}

mf_prim_subtype_ID = {('meta', 'ingress_port'): '1',
                      ('meta', 'packet_length'): '2',
                      ('meta', 'egress_spec'): '3',
                      ('meta', 'egress_port'): '4',
                      ('meta', 'egress_instance'): '5',
                      ('meta', 'instance_type'): '6',
                      ('egress_spec', 'meta'): '7',
                      ('meta', 'const'): '8',
                      ('egress_spec', 'const'): '9',
                      ('ext', 'const'): '10',
                      ('egress_spec', 'ingress_port'): '11',
                      ('ext', 'ext'): '12',
                      ('meta', 'ext'): '13',
                      ('ext', 'meta'): '14'}

mf_prim_subtype_action = {'1': 'mod_meta_stdmeta_ingressport',
                          '2': 'mod_meta_stdmeta_packetlength',
                          '3': 'mod_meta_stdmeta_egressspec',
                          '4': 'mod_meta_stdmeta_egressport',
                          '5': 'mod_meta_stdmeta_egressinst',
                          '6': 'mod_meta_stdmeta_insttype',
                          '7': 'mod_stdmeta_egressspec_meta',
                          '8': 'mod_meta_const',
                          '9': 'mod_stdmeta_egressspec_const',
                          '10': 'mod_extracted_const',
                          '11': 'mod_stdmeta_egressspec_stdmeta_ingressport',
                          '12': 'mod_extracted_extracted',
                          '13': 'mod_meta_extracted',
                          '14': 'mod_extracted_meta'}

a2f_prim_subtype_ID = {'add': '1', 'sub': '2'}

a2f_prim_subtype_action = {'1': 'a_add2f_extracted_const_u',
                           '2': 'a_subff_extracted_const_u'}

gen_prim_subtype_action = {'add_header': 'a_addh',
                           'copy_header': '',
                           'remove_header': '',
                           'modify_field_with_hash_based_offset': '',
                           'truncate': 'a_truncate',
                           'drop': 'a_drop',
                           'no_op': '',
                           'push': '',
                           'pop': '',
                           'count': '',
                           'execute_meter': '',
                           'recirculate': '',
                           'resubmit': '',
                           'clone_ingress_pkt_to_egress': '',
                           'clone_egress_pkt_to_egress': '',
                           'multicast': 'a_multicast'}

stdmeta_ID = {'ingress_port': '[STDMETA_INGRESS_PORT]',
              'packet_length': '[STDMETA_PACKET_LENGTH]',
              'egress_spec': '[STDMETA_EGRESS_SPEC]',
              'egress_port': '[STDMETA_EGRESS_PORT]',
              'egress_instance': '[STDMETA_EGRESS_INSTANCE]',
              'instance_type': '[STDMETA_INSTANCE_TYPE]',
              'clone_spec': '[STDMETA_CLONE_SPEC]'}

def parse_args(args):
  parser = argparse.ArgumentParser(description='P4->HP4 Compiler')
  parser.add_argument('input', help='path for input .p4',
                    type=str)
  parser.add_argument('-o', '--output', help='path for output .hp4t file',
                    type=str, action="store", required=True)
  parser.add_argument('-m', '--mt_output', help='path for match template output',
                    type=str, action="store", default='output.hp4mt')
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

class HP4_Match_Command(HP4_Command):
  def __init__(self, source_table, source_action, command, table, action, mparams, aparams):
    HP4_Command.__init__(self, command, table, action, mparams, aparams)
    self.source_table = source_table
    self.source_action = source_action

def convert_to_builtin_type(obj):
  d = { '__class__':obj.__class__.__name__, '__module__':obj.__module__, }
  d.update(obj.__dict__)
  return d

class MatchParam():
  def __init__(self):
    self.value = 0
    self.mask = 0
  def __str__(self):
    return format(self.value, '#04x') + '&&&' + format(self.mask, '#04x')

class Table_Rep():
  def __init__(self, stage, match_type, source_type):
    self.stage = stage
    self.match_type = match_type
    self.source_type = source_type
    self.name = 't' + str(self.stage) + '_'
    if source_type == 'standard_metadata':
      self.name += 'stdmeta_'
    elif source_type == 'metadata':
      self.name += 'metadata_'
    elif source_type == 'extracted':
      self.name += 'extracted_'
    if match_type == 'P4_MATCH_EXACT':
      self.name += 'exact'
    elif match_type == 'P4_MATCH_VALID':
      self.name += 'valid'
    elif match_type == 'P4_MATCH_TERNARY':
      self.name += 'ternary'
    elif match_type == 'MATCHLESS':
      self.name += 'matchless'
  def table_type(self):
    if self.source_type == 'standard_metadata':
      if self.match_type == 'P4_MATCH_EXACT':
        return '[STDMETA_EXACT]'
      else:
        print("Not supported: standard_metadata with %s match type" % self.match_type)
        exit()
    elif self.source_type == 'metadata':
      if self.match_type == 'P4_MATCH_EXACT':
        return '[METADATA_EXACT]'
      else:
        print("Not supported: metadata with %s match type" % self.match_type)
        exit()
    elif self.source_type == 'extracted':
      if self.match_type == 'P4_MATCH_EXACT':
        return '[EXTRACTED_EXACT]'
      elif self.match_type == 'P4_MATCH_VALID':
        return '[EXTRACTED_VALID]'
      else:
        print("Not supported: extracted with %s match type" % self.match_type)
        exit()
    elif self.source_type == '':
      if self.match_type == 'MATCHLESS':
        return '[MATCHLESS]'
      else:
        print("Not supported: [no source] with %s match type" % self.match_type)
        exit()
    else:
      print("Not supported: source type %s, match type %s" % (self.source_type, self.match_type))
      exit()
  def __str__(self):
    return self.name

class Action_Rep():
  def __init__(self):
    self.stages = set()
    self.tables = {}
    self.call_sequence = []

class HP4C:
  def __init__(self, h, args):
    self.headers_hp4_type = {}
    self.action_ID = {}
    self.actionID = 1
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
    self.stage = 1
    self.table_to_trep = {}
    self.action_to_arep = {}
    self.commands = []
    self.command_templates = []
    self.h = h
    self.h.build()
    if len(self.h.p4_ingress_ptr) > 1:
      print("ERROR: multiple ingress entry points:")
      for node in h.p4_ingress_ptr.keys():
        print('  ' + node)
      exit()
    self.args = args

  def collect_headers(self):
    self.offset = 0
    for header_key in self.h.p4_header_instances.keys():
      header = self.h.p4_header_instances[header_key]
      if header.name == 'standard_metadata':
        self.headers_hp4_type[header_key] = 'standard_metadata'
        continue
      if header.metadata == True:
        self.headers_hp4_type[header_key] = 'metadata'
        for field in header.fields:
          fullname = header.name + '.' + field.name
          self.field_offsets[fullname] = self.offset
          self.offset += field.width
          if self.offset > 256:
            print("Error: out of metadata memory with %s" % fullname)
            exit()
      else:
        self.headers_hp4_type[header_key] = 'extracted'
    self.offset = 0

  def collect_actions(self):
    for action in self.h.p4_actions.values():
      if action.lineno > 0: # is action from source (else built-in)?
        self.action_ID[action] = self.actionID
        self.actionID += 1

  def gen_tset_context_entry(self):
    self.commands.append(HP4_Command("table_add",
                                       "tset_context",
                                       "a_set_context",
                                       ["[PPORT]"],
                                       ["[program ID]"]))

  def gen_tset_virtnet_entry(self):
    self.commands.append(HP4_Command("table_set_default",
                                      "tset_in_virtnet",
                                      "a_virt_ports_cleanup",
                                      [],
                                      []))

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
  
      # pc_action[pc_state] = 'parse_select_XX_YY'
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
          self.tics_table_names[tics_pc_state] = 'tset_parse_select_SEB'
      else:
        bound = self.args.seb + 10
        while bound <= 100:
          if startbytes < bound:
            if endbytes >= bound:
              unsupported(startbytes, endbytes)
            else:
              namecore = 'parse_select_' + str(bound - 10) + '_' + str(bound - 1)
              self.pc_action[pc_state] = '[' + namecore.upper() + ']'
              self.tics_table_names[tics_pc_state] = 'tset_' + namecore
              break
          bound += 10
      if pc_state not in self.pc_action:
        print("ERROR: did not find parse_select_XX_YY function for startbytes(%i) and endbytes(%i)" % (startbytes, endbytes))
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
    # headers_hp4_type[<str>]: 'standard_metadata' | 'metadata' | 'extracted'
    #code.interact(local=locals())
    source_type = ''
    match_type = 'MATCHLESS'
    if len(curr_table.match_fields) > 0:
      match_type = curr_table.match_fields[0][1].value
      if (match_type == 'P4_MATCH_EXACT' or
          match_type == 'P4_MATCH_TERNARY'):
        source_type = self.headers_hp4_type[curr_table.match_fields[0][0].instance.name]
      elif match_type == 'P4_MATCH_VALID':
        source_type = self.headers_hp4_type[curr_table.match_fields[0][0].name]
    self.table_to_trep[curr_table] = Table_Rep(self.stage,
                                               match_type,
                                               source_type)
    for action in curr_table.actions:
      if self.action_to_arep.has_key(action) is False:
        self.action_to_arep[action] = Action_Rep()
        for call in action.call_sequence:
          prim_type = call[0].name
          prim_subtype = self.get_prim_subtype(call)
          self.action_to_arep[action].call_sequence.append((prim_type, prim_subtype))
      stage = self.table_to_trep[curr_table].stage
      self.action_to_arep[action].stages.add(stage)
      self.action_to_arep[action].tables[stage] = curr_table.name

    for action in curr_table.next_:
      if curr_table.next_[action] == None:
        continue
      else:
        self.stage += 1
        self.walk_ingress_pipeline(curr_table.next_[action])

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

  def gen_tset_parse_control_entries(self):
    self.walk_parse_tree(self.h.p4_parse_states['start'], 0)

    for key in self.pc_action.keys():
      # special handling for pc_state 0
      if key == 0:
        if self.pc_bits_extracted[0] > (self.args.seb * 8):
          self.commands.append(HP4_Command("table_add",
                                           "tset_parse_control",
                                           "extract_more",
                                           ["[program ID]", "0"],
                                           [str(self.pc_bits_extracted[0]), "1"]))
          self.commands.append(HP4_Command("table_add",
                                           "tset_parse_control",
                                           "set_next_action",
                                           ["[program ID]", "1"],
                                           [self.pc_action[0], "1"]))
        else:
          self.commands.append(HP4_Command("table_add",
                                           "tset_parse_control",
                                           "set_next_action",
                                           ["[program ID]", "0"],
                                           [self.pc_action[0], "1"]))
          self.pc_bits_extracted[0] = self.args.seb * 8

        self.pc_bits_extracted[1] = self.pc_bits_extracted[0]
        self.pc_bits_extracted[0] = self.args.seb * 8
        self.pc_action[1] = self.pc_action[0]

      else:
        self.commands.append(HP4_Command("table_add",
                                         "tset_parse_control",
                                         "set_next_action",
                                         ["[program ID]", str(key)],
                                         [self.pc_action[key], str(key)]))

  def gen_tset_parse_select_entries(self):
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

  def gen_tset_pipeline_config_entries(self):
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
        for prec_pc in self.pc_to_preceding_pcs[pc_state]:
          ps = self.pc_to_ps[prec_pc]
          for call in ps.call_sequence:
            if call[0].value != 'extract':
              print("ERROR (gen_tset_pipeline_config_entries): unsupported call %s" % call[0].value)
              exit()
            pc_headers[pc_state].append(call[1])
        for call in ingress_ps.call_sequence:
          if call[0].value != 'extract':
            print("ERROR (gen_tset_pipeline_config_entries): unsupported call %s" % call[0].value)
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
    lshift = 80
    for j in range(longest):
      numbits = len(headerset[j])
      lshift = lshift - numbits
      i = 1
      for header in headerset[j]:
        self.vbits[(j, header)] = i << lshift
        i = i << 1

    # handle table_ID
    if len(first_table.match_fields) > 1:
      print("Not yet supported: multiple match fields (%s)" % first_table.name)
      exit()
    field_match = first_table.match_fields[0]
    field = field_match[0]
    match_type = field_match[1]
    if match_type.value != 'P4_MATCH_EXACT':
      print("Not yet supported: match type %s" % match_type.value)
      exit()
    if self.headers_hp4_type[field.instance.name] == 'standard_metadata':
      aparam_table_ID = '[STDMETA_EXACT]'
    elif self.headers_hp4_type[field.instance.name] == 'metadata':
      aparam_table_ID = '[METADATA_EXACT]'
    elif self.headers_hp4_type[field.instance.name] == 'extracted':
      aparam_table_ID = '[EXTRACTED_EXACT]'

    for ps in self.h.p4_ingress_ptr[first_table]:
      for pc_state in self.ps_to_pc[ps]:
        val = 0
        for i in range(len(pc_headers[pc_state])):
          val = val | self.vbits[(i, pc_headers[pc_state][i])]
        valstr = '0x' + '%x' % val

        self.commands.append(HP4_Command("table_add",
                                         "tset_pipeline_config",
                                         "a_set_pipeline",
                                         ['[program ID]', str(pc_state)],
                                         [aparam_table_ID, valstr]))

  def gen_bitmask(self, field):
    mask = '0x'
    offset = self.field_offsets[str(field)]
    bytes_written = offset / 8
    bits_left = field.width
    while bits_left > 0:
      byte = 0
      bit = 0b10000000 >> (offset % 8)
      if bits_left >= 8 - (offset % 8):
        for i in range(8 - (offset % 8)):
          byte = byte | bit
          bit = bit >> 1
        bits_left = bits_left - (8 - (offset % 8))
        offset = offset + 8 - (offset % 8)
      else:
        for i in range(bits_left):
          byte = byte | bit
          bit = bit >> 1
        bits_left = 0
      mask += hex(byte)[2:]
      bytes_written += 1
    maskwidth = 100
    if field.instance.metadata:
      maskwidth = 32
    mask += '[' + str(maskwidth - bytes_written) + 'x00s]'
    #while bytes_written < 100:
    #  mask += '00'
    #  bytes_written += 1
    return mask

  def gen_tX_templates(self):
    self.walk_ingress_pipeline(self.h.p4_ingress_ptr.keys()[0])
    for table in self.table_to_trep:
      tname = str(self.table_to_trep[table])
      aname = 'init_program_state'
      if self.table_to_trep[table].source_type == 'standard_metadata':
        aname = 'set_meta_stdmeta'
      match_params = ['[program ID]']
      if len(table.match_fields) > 1:
        print("Not yet supported: more than 1 match field (table: %s)" % table.name)
        exit()
      match_params_list = []
      if len(table.match_fields) == 1:      
        if table.match_fields[0][1].value == 'P4_MATCH_VALID':
          mp = '0x01&&&'
          # self.vbits[(level, header_instance)]
          hinst = table.match_fields[0][0]
          for key in self.vbits.keys():
            if hinst == key[1]:
              mp += format(self.vbits[key], '#x')
              temp_match_params = list(match_params)
              temp_match_params.append(mp)
              match_params_list.append(temp_match_params)
        elif table.match_fields[0][1].value == 'P4_MATCH_EXACT':
          field = table.match_fields[0][0]
          if field.instance.name == 'standard_metadata':
            aparams = [stdmeta_ID[field.name]]
          else:
            mp = '[val]&&&' + self.gen_bitmask(field)
            match_params.append(mp)
        match_params_list.append(match_params)

      # need a distinct template entry for every possible action
      for mparams in match_params_list:
        for action in table.next_.keys():
          if aname == 'init_program_state':
            # action_ID
            aparams = [str(self.action_ID[action])]
            # match_ID
            aparams.append('[match ID]')
            # next_table
            if table.next_[action] == None:
              aparams.append('[DONE]')
            else:
              aparams.append(self.table_to_trep[table.next_[action]].table_type())
            # primitive
            if len(action.call_sequence) == 0:
              aparams.append(primitive_ID['no_op'])
            else:
              aparams.append(primitive_ID[action.call_sequence[0][0].name])
            # primitive_subtype
            if len(action.call_sequence) > 0:
              aparams.append(self.get_prim_subtype(action.call_sequence[0]))
            else:
              aparams.append('0')

          self.command_templates.append(HP4_Match_Command(table.name,
                                            action.name,
                                            "table_add",
                                            tname,
                                            aname,
                                            mparams,
                                            aparams))
          if aname == 'set_meta_stdmeta':
            # Need an entirely new command template since stdmeta matching is
            #  handled in two steps, vs other types of matching in one step.
            stdm_tname = ('t' + str(self.table_to_trep[table].stage) +
                         '_stdmeta_' + table.match_fields[0][0].name)
            stdm_aname = 'init_program_state'
            # MATCH PARAMS:
            stdm_mparams = ['[program ID]', '[val]']
            # ACTION PARAMS:
            #   action_ID
            stdm_aparams = [str(self.action_ID[action])]
            #   match_ID
            stdm_aparams.append('[match ID]')
            #   next_table
            if table.next_[action] == None:
              stdm_aparams.append('[DONE]')
            else:
              stdm_aparams.append(self.table_to_trep[table.next_[action]].table_type())
            #   primitive
            if len(action.call_sequence) == 0:
              stdm_aparams.append(primitive_ID['no_op'])
            else:
              stdm_aparams.append(primitive_ID[action.call_sequence[0][0].name])
            #   primitive_subtype
            if len(action.call_sequence) > 0:
              stdm_aparams.append(self.get_prim_subtype(action.call_sequence[0]))
            else:
              stdm_aparams.append('0')

            self.command_templates.append(HP4_Match_Command(table.name,
                                              action.name,
                                              "table_add",
                                              stdm_tname,
                                              stdm_aname,
                                              stdm_mparams,
                                              stdm_aparams))

  # primitive_call: (p4_action, [list of parameters])
  def get_prim_subtype(self, call):
    if call[0].name == 'drop':
      return '0'
    elif call[0].name == 'add_to_field':
      if type(call[1][0]) is p4_hlir.hlir.p4_headers.p4_field:
        if call[1][0].instance.metadata == True:
          print("Not supported: metadata (%s) as dst field in add_to_field" %  call[1][0].instance.name)
          exit()
        else:
          if type(call[1][1]) is int:
            if call[1][1] < 0:
              return(a2f_prim_subtype_ID['sub'])
            else:
              return(a2f_prim_subtype_ID['add'])
          else:
            print("ERROR: Not supported: %s type for src field in add_to_field" % type(call[1][1]))
            exit()
      else:
        print("ERROR: dst field type %s in add_to_field" % type(call[1][0]))
        exit()
    elif call[0].name == 'modify_field':
      first = 0
      second = 0
      if call[1][0].instance.metadata == True:
        if call[1][0].instance.name == 'standard_metadata':
          if call[1][0].name == 'egress_spec':
            first = call[1][0].name
          else:
            print("ERROR: Unexpected stdmeta field %s as dst in modify_field primitive" % call[1][0].name)
            exit()
        else: # user-defined metadata
          first = 'meta'
      else: # parsed representation
        first = 'ext'
      if type(call[1][1]) is int:
        second = 'const'
      elif type(call[1][1]) is p4_hlir.hlir.p4_headers.p4_field:
        if call[1][1].instance.metadata == True:
          if call[1][1].instance.name == 'standard_metadata':
            second = call[1][1].name
          else:
            second = 'meta'
        else:
          second = 'ext'
      elif type(call[1][1]) is p4_hlir.hlir.p4_imperatives.p4_signature_ref:
        second = 'const'
      else:
        print("ERROR: Unexpected type %s as src in modify_field call" % type(call[1][1]))
        exit()
      return mf_prim_subtype_ID[first, second]

  def print_action_to_arep(self):
    for action in self.action_to_arep:
      print("Action: " + str(action))
      print("  stages: " + str(self.action_to_arep[action].stages))
      print("  call_sequence: " + str(self.action_to_arep[action].call_sequence))

  def gen_action_entries(self):
    for action in self.action_to_arep:
      for stage in self.action_to_arep[action].stages:
        table_name = self.action_to_arep[action].tables[stage]
        for p4_call in action.call_sequence:
          istemplate = False
          idx = action.call_sequence.index(p4_call)
          call = self.action_to_arep[action].call_sequence[idx]
          rank = idx + 1
          tname = 't_' + primitive_tnames[call[0]] + '_' + str(stage) + str(rank)
          us_tname = 'tstg' + str(stage) + str(rank) + '_update_state'
          us_aname = 'update_state'
          us_aparams = []
          if rank == len(action.call_sequence):
            us_aname = 'finish_action'
            # aparams for finish_action: next_stage
            next_table = self.h.p4_tables[table_name].next_[action]
            if next_table == None:
              us_aparams.append('0')
            else:
              us_aparams.append(str(self.table_to_trep[next_table].stage))
          else:
            # aparams for update_state: primitive_type, primitive_subtype
            next_call = action.call_sequence[idx + 1]
            next_prim_type = primitive_ID[next_call[0].name]
            next_prim_subtype = self.get_prim_subtype(next_call)
            us_aparams.append(next_prim_type)
            us_aparams.append(next_prim_subtype)

          us_mparams = ['[program ID]']
          us_mparams.append(str(self.action_ID[action]))
          if call[0] == 'modify_field':
            aname = mf_prim_subtype_action[call[1]]
          elif call[0] == 'add_to_field':
            aname = a2f_prim_subtype_action[call[1]]
          else:
            aname = gen_prim_subtype_action[call[0]]
          mparams = []
          if call[0] != 'drop':
            mparams.append('[program ID]')
            if call[0] == 'modify_field' or call[0] == 'add_to_field':
              mparams.append( call[1] )
            mparams.append(str(self.action_ID[action]))
            # If the parameter passed to the primitive in the source code is an
            # action parameter reference, the match_ID parameter should be
            # [val]&&&0x7FFFFF because each distinct match could have a different
            # value for the action parameter.  Otherwise, we don't care what the
            # match_ID is so use 0&&&0.
            match_ID_param = '0&&&0'
            for param in p4_call[1]:
              if type(param) == p4_hlir.hlir.p4_imperatives.p4_signature_ref:
                match_ID_param = '[val]&&&0x7FFFFF'
                istemplate = True
                break
            mparams.append(match_ID_param)
          aparams = self.gen_action_aparams(p4_call, call)
          if istemplate == True:
            self.command_templates.append(HP4_Match_Command(table_name,
                                            action.name,
                                            "table_add",
                                            tname,
                                            aname,
                                            mparams,
                                            aparams))
          else:
            self.commands.append(HP4_Command("table_add",
                                         tname,
                                         aname,
                                         mparams,
                                         aparams))
          self.commands.append(HP4_Command("table_add",
                                us_tname,
                                us_aname,
                                us_mparams,
                                us_aparams))

  # focus: mod, drop, math
  def gen_action_aparams(self, p4_call, call):
    aparams = []
    if call[0] == 'drop':
      return aparams
    if call[0] == 'math_on_field':
      if (a2f_prim_subtype_action[call[1]] == 'a_add2f_extracted_const_u' or
          a2f_prim_subtype_action[call[1]] == 'a_subff_extracted_const_u'):
        # aparams: leftshift, val
        dst_offset = self.field_offsets[str(p4_call[1][0])]
        leftshift = 800 - (dst_offset + p4_call[1][0].width)
        if type(p4_call[1][1]) == int:
          val = str(p4_call[1][1])
        else:
          val = '[val]'
        aparams.append(str(leftshift))
        aparams.append(val)
    if call[0] == 'modify_field':
      if mf_prim_subtype_action[call[1]] == 'mod_meta_stdmeta_ingressport':
        print("Not yet supported: %s" % mf_prim_subtype_action[call[1]])
        exit()
      elif mf_prim_subtype_action[call[1]] == 'mod_meta_stdmeta_packetlength':
        print("Not yet supported: %s" % mf_prim_subtype_action[call[1]])
        exit()
      elif mf_prim_subtype_action[call[1]] == 'mod_meta_stdmeta_egressspec':
        print("Not yet supported: %s" % mf_prim_subtype_action[call[1]])
        exit()
      elif mf_prim_subtype_action[call[1]] == 'mod_meta_stdmeta_egressport':
        print("Not yet supported: %s" % mf_prim_subtype_action[call[1]])
        exit()
      elif mf_prim_subtype_action[call[1]] == 'mod_meta_stdmeta_egressinst':
        print("Not yet supported: %s" % mf_prim_subtype_action[call[1]])
        exit()
      elif mf_prim_subtype_action[call[1]] == 'mod_meta_stdmeta_insttype':
        print("Not yet supported: %s" % mf_prim_subtype_action[call[1]])
        exit()
      elif mf_prim_subtype_action[call[1]] == 'mod_stdmeta_egressspec_meta':
        # aparams: rightshift, tmask
        rshift = 256 - (self.field_offsets[str(p4_call[1][1])] + p4_call[1][1].width)
        mask = hex(int(math.pow(2, p4_call[1][1].width)) - 1)
        aparams.append(str(rshift))
        aparams.append(mask)
      elif (mf_prim_subtype_action[call[1]] == 'mod_meta_const' or
            mf_prim_subtype_action[call[1]] == 'mod_extracted_const'):
        # aparams: val, leftshift, mask
        if type(p4_call[1][1]) == int:
          val = str(p4_call[1][1])
        else:
          val = '[val]'
        fo = self.field_offsets[str(p4_call[1][0])]
        fw = p4_call[1][0].width
        maskwidth = 800
        if mf_prim_subtype_action[call[1]] == 'mod_meta_const':
          maskwidth = 256
        leftshift = str(maskwidth - (fo + fw))
        mask = self.gen_bitmask(p4_call[1][0])
        aparams.append(val)
        aparams.append(leftshift)
        aparams.append(mask)
      elif mf_prim_subtype_action[call[1]] == 'mod_stdmeta_egressspec_const':
        if type(p4_call[1][1]) == int:
          aparams.append(str(p4_call[1][1]))
        else:
          aparams.append('[val]')
      elif mf_prim_subtype_action[call[1]] == 'mod_stdmeta_egressspec_stdmeta_ingressport':
        return aparams
      elif mf_prim_subtype_action[call[1]] == 'mod_extracted_extracted':
        # aparams:
        # - leftshift (how far should src field be shifted to align w/ dst)
        # - rightshift (how far should src field be shifted to align w/ dst)
        # - msk (bitmask for dest field)
        dst_offset = self.field_offsets[str(p4_call[1][0])]
        src_offset = self.field_offsets[str(p4_call[1][1])]
        lshift = 0
        rshift = 0
        if dst_offset > src_offset:
          rshift = dst_offset - src_offset
        else:
          lshift = src_offset - dst_offset
        aparams.append(str(lshift))
        aparams.append(str(rshift))
        aparams.append(self.gen_bitmask(p4_call[1][0]))
      elif (mf_prim_subtype_action[call[1]] == 'mod_meta_extracted' or
            mf_prim_subtype_action[call[1]] == 'mod_extracted_meta'):
        dst_offset = self.field_offsets[str(p4_call[1][0])]
        src_offset = self.field_offsets[str(p4_call[1][1])]
        lshift = 0
        rshift = 0
        dstmaskwidth = 800
        srcmaskwidth = 256
        if mf_prim_subtype_action[call[1]] == 'mod_meta_extracted':
          dstmaskwidth = 256
          srcmaskwidth = 800
        dst_revo = dstmaskwidth - (dst_offset + p4_call[1][0].width)
        src_revo = srcmaskwidth - (src_offset + p4_call[1][1].width)
        if src_revo > dst_revo:
          rshift = src_revo - dst_revo
        else:
          lshift = dst_revo - src_revo
        dstmask = self.gen_bitmask(p4_call[1][0])
        srcmask = self.gen_bitmask(p4_call[1][1])
        aparams.append(str(lshift))
        aparams.append(str(rshift))
        aparams.append(dstmask)
        aparams.append(srcmask)
    return aparams

  def gen_thp4_egress_filter_entries(self):
    self.commands.append(HP4_Command("table_set_default",
                                      "thp4_egress_filter_case1",
                                      "a_drop",
                                      [],
                                      []))
    self.commands.append(HP4_Command("table_set_default",
                                      "thp4_egress_filter_case2",
                                      "a_drop",
                                      [],
                                      []))

  def gen_t_checksum_entries(self):
    # verify presence of ipv4 checksum

    for cf in self.h.calculated_fields:
      for statement in cf[1]:
        if statement[0] == 'update':
          flc = self.h.p4_field_list_calculation[statement[1]]
          for fl in flc.input:
            count = 0
            for field in fl.fields:
              count += field.width
            if count == 144:
              if flc.algorithm == 'csum16' and flc.output_width == 16:
                # TODO
                pass

  def gen_t_prep_deparse_entries(self):
    suffixes = ['SEB', '20_39', '40_59', '60_79', '80_99']
    for suffix in suffixes:
      tname = 't_prep_deparse_' + suffix
      aname = 'a_prep_deparse_' + suffix
      self.commands.append(HP4_Command("table_set_default",
                                        tname,
                                        aname,
                                        [],
                                        []))

  def build(self):
    self.collect_headers()
    self.collect_actions()
    self.gen_tset_context_entry()
    self.gen_tset_virtnet_entry()
    self.gen_tset_parse_control_entries()
    self.gen_tset_parse_select_entries()
    self.gen_tset_pr_entries()
    self.gen_tset_pipeline_config_entries()
    self.gen_tX_templates()
    self.gen_action_entries()
    # TODO: self.gen_thp4_multicast_entries()
    self.gen_thp4_egress_filter_entries()
    # TODO: self.gen_t_checksum_entries()
    # TODO: self.gen_t_resize_pr_entries()
    self.gen_t_prep_deparse_entries()

  def write_output(self):
    out = open(self.args.output, 'w')
    for command in self.commands:
      out.write(str(command) + '\n')
    out.close()
    out = open(self.args.mt_output, 'w')
    json.dump(self.command_templates, out, default=convert_to_builtin_type, indent=2)
    out.close()

def main():
  args = parse_args(sys.argv[1:])
  hp4c = HP4C(HLIR(args.input), args)
  hp4c.build()
  #hp4c.write_output()
  code.interact(local=locals())

if __name__ == '__main__':
  main()
