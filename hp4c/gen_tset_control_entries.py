# this code is intended to be merged into hp4c.py

pc_bits_extracted = {}
pc_bits_extracted_curr = {}
pc_action = {}
field_offsets = {}

def gen_tset_control_entries(self, parse_state, pc_state):
  numbits = 0
  for call in parse_state.call_sequence:
    if call[0].value != 'extract':
      print("ERROR: unsupported call %s" % call[0].value)
      exit()
    for key in call[1].header_type.layout.keys():
      numbits += call[1].header_type.layout[key]
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
    # TODO: replace XX_YY via field_offsets
    pc_action[pc_state] = 'inspect_XX_YY'
    for selectopt in parse_state.return_statement[2]:
      # selectopt: (list of values, next parse_state)
      if selectopt[1] != 'ingress':
        next_states.append(self.h.p4_parse_states[selectopt[1]])
  else:
    print("ERROR: Unknown directive in return statement: %s" % parse_state.return_statement[0])
    exit()

  for next_state in next_states:
    pc_state += 1
    gen_tset_control_entries(next_state, pc_state)

gen_tset_control_entries(self.h.p4_parse_states['start'])
