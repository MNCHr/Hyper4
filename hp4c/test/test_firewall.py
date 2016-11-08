from hp4c import hp4c
from p4_hlir.main import HLIR

def firewall():
  args = hp4c.parse_args(['-o', 'firewall.hp4t', 'test/firewall.p4'])
  hp4compiler = hp4c.HP4C(HLIR("test/firewall.p4"), args)
  return True

def test_firewall():
  assert firewall()

def test_collection():
  args = hp4c.parse_args(['-o', 'firewall.hp4t', 'test/firewall.p4'])
  hp4compiler = hp4c.HP4C(HLIR("test/firewall.p4"), args)
  hp4compiler.collectParseStates()
  hp4compiler.collectActions()
  hp4compiler.collectTables()
  passed = 0
  for state in hp4compiler.parseStateUIDs.keys():
    if state.name == 'start' and hp4compiler.parseStateUIDs[state] == 0:
      passed += 1
    elif state.name == 'parse_ipv4' and hp4compiler.parseStateUIDs[state] == 1:
      passed += 1
    elif state.name == 'parse_tcp' and hp4compiler.parseStateUIDs[state] == 2:
      passed += 1
    elif state.name == 'parse_udp' and hp4compiler.parseStateUIDs[state] == 3:
      passed += 1
    else:
      assert 0
  actionkeys = [1, 2, 3, 4, 5, 6, 7]
  for action in hp4compiler.actionUIDs.keys():
    if len(actionkeys) <= 0:
      assert 0
    elif action.name == '_no_op' or \
         action.name == 'tcp_present' or \
         action.name == 'tcp_not_present' or \
         action.name == 'udp_present' or \
         action.name == 'udp_not_present' or \
         action.name == '_drop' or \
         action.name == 'a_fwd':
      actionkeys.remove(hp4compiler.actionUIDs[action])
      passed += 1
  for table in hp4compiler.tableUIDs.keys():
    if table.name == 'fwd' and hp4compiler.tableUIDs[table] == 1:
      passed += 1
    elif table.name == 'is_tcp_valid' and hp4compiler.tableUIDs[table] == 2:
      passed += 1
    elif table.name == 'is_udp_valid' and hp4compiler.tableUIDs[table] == 3:
      passed += 1
    elif table.name == 'udp_src_block' and hp4compiler.tableUIDs[table] == 4:
      passed += 1
    elif table.name == 'udp_dst_block' and hp4compiler.tableUIDs[table] == 5:
      passed += 1
    elif table.name == 'tcp_src_block' and hp4compiler.tableUIDs[table] == 6:
      passed += 1
    elif table.name == 'tcp_dst_block' and hp4compiler.tableUIDs[table] == 7:
      passed += 1
  assert passed == 18
