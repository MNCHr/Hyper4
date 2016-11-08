from hp4c import hp4c
from p4_hlir.main import HLIR

def firewall():
  args = hp4c.parse_args(['-o', 'arp_proxy.hp4t', 'test/arp_proxy.p4'])
  hp4compiler = hp4c.HP4C(HLIR("test/arp_proxy.p4"), args)
  return True

def test_firewall():
  assert firewall()

def test_collection():
  args = hp4c.parse_args(['-o', 'arp_proxy.hp4t', 'test/arp_proxy.p4'])
  hp4compiler = hp4c.HP4C(HLIR("test/arp_proxy.p4"), args)
  hp4compiler.collectParseStates()
  hp4compiler.collectActions()
  hp4compiler.collectTables()
  passed = 0
  for state in hp4compiler.parseStateUIDs.keys():
    if state.name == 'start' and hp4compiler.parseStateUIDs[state] == 0:
      passed += 1
    elif state.name == 'parse_arp' and hp4compiler.parseStateUIDs[state] == 1:
      passed += 1
    else:
      assert 0
  actionkeys = [1, 2, 3, 4, 5, 6]
  for action in hp4compiler.actionUIDs.keys():
    if len(actionkeys) <= 0:
      assert 0
    elif action.name == 'a_init_meta_egress' or \
         action.name == 'arp_present' or \
         action.name == 'arp_request' or \
         action.name == 'arp_reply' or \
         action.name == 'send_packet' or \
         action.name == '_no_op':
      actionkeys.remove(hp4compiler.actionUIDs[action])
      passed += 1
  if len(actionkeys) > 0:
    assert 0
  for table in hp4compiler.tableUIDs.keys():
    if table.name == 'init_meta_egress' and hp4compiler.tableUIDs[table] == 1:
      passed += 1
    elif table.name == 'check_arp' and hp4compiler.tableUIDs[table] == 2:
      passed += 1
    elif table.name == 'check_opcode' and hp4compiler.tableUIDs[table] == 3:
      passed += 1
    elif table.name == 'handle_arp_request' and hp4compiler.tableUIDs[table] == 4:
      passed += 1
    elif table.name == 'bogus' and hp4compiler.tableUIDs[table] == 5:
      passed += 1
  assert passed == 13
