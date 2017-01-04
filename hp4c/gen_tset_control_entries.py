import math

# this code is intended to be merged into hp4c.py

pc_bits_extracted = {}
pc_bits_extracted_curr = {}
pc_action = {}
field_offsets = {}
offset = 0 # in bits

# TODO: Ensure offset is being moved back upon return from recursive calls from select statements

def gen_tset_control_entries(self, parse_state, pc_state):
  numbits = 0
  for call in parse_state.call_sequence:
    if call[0].value != 'extract':
      print("ERROR: unsupported call %s" % call[0].value)
      exit()
    # update field_offsets, numbits
    for field in call[1].fields:
      self.field_offsets[call[1].name + '.' + field.name] = self.offset
      self.offset += field.width # advance current offset
      numbits += field.width
  if pc_state in pc_bits_extracted:
    pc_bits_extracted[pc_state] += numbits
  else:
    pc_bits_extracted[pc_state] = numbits 
  
  # traverse parse tree
  next_states = []
  if parse_state.return_statement[0] == 'immediate':
    if parse_state.return_statement[1] != 'ingress':
      next_state = self.h.p4_parse_states[parse_state.return_statement[1]]
      gen_tset_control_entries(next_state, pc_state)
    else:
      pc_action[pc_state] = 'proceed'
      return
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
        if (startbytes * 8) > offset + criteria[0]:
          startbytes = (offset + criteria[0]) / 8
        if (endbytes * 8) < offset + maxcurr:
          endbytes = int(math.ceil((offset + maxcurr) / 8.0))
      else: # single field
        fieldstart = field_offsets[criteria] / 8
        fieldend = int(math.ceil((fieldstart
                                  + self.h.p4_fields[criteria].width) / 8.0))
        if startbytes > fieldstart:
          startbytes = fieldstart
        if endbytes < fieldend:
          endbytes = fieldend
        
    pc_bits_extracted[pc_state] += maxcurr
    pc_bits_extracted_curr[pc_state] = maxcurr

    # pc_action[pc_state] = 'inspect_XX_YY'
    if startbytes >= endbytes:
      print("ERROR: startbytes(%i) > endbytes(%i)" % (startbytes, endbytes))
      exit()
    def unsupported(sbytes, ebytes):
      print("Not yet supported: startbytes(%i) and endbytes(%i) cross boundaries" % (sbytes, ebytes))
      exit()
    if startbytes < self.args.seb:
      if endbytes >= self.args.seb:
        unsupported(startbytes, endbytes)
      else:
        pc_action[pc_state] = 'inspect_SEB'
    else:
      bound = self.args.seb + 10
      while bound <= 100:
        if startbytes < bound:
          if endbytes >= bound:
            unsupported(startbytes, endbytes)
          else:
            pc_action[pc_state] = 'inspect_' + str(bound - 10) + '_'
                                  + str(bound - 1)
            break
        bound += 10
    if pc_state not in pc_action:
      print("ERROR: did not find inspect_XX_YY function for startbytes(%i) and endbytes(%i)" % (startbytes, endbytes))
    
    for selectopt in parse_state.return_statement[2]:
      # selectopt: (list of values, next parse_state)
      if selectopt[1] != 'ingress':
        next_states.append(self.h.p4_parse_states[selectopt[1]])
  else:
    print("ERROR: Unknown directive in return statement: %s" \
          % parse_state.return_statement[0])
    exit()

  prev_state = pc_state
  for next_state in next_states:
    pc_state += 1
    pc_bits_extracted[pc_state] = (pc_bits_extracted[prev_state]
                                  - pc_bits_extracted_curr[prev_state])
    gen_tset_control_entries(next_state, pc_state)

gen_tset_control_entries(self.h.p4_parse_states['start'], 0)
