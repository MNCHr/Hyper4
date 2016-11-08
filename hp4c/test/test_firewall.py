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
      print('parse_ipv4')
      passed += 1
    elif state.name == 'parse_tcp' and hp4compiler.parseStateUIDs[state] == 2:
      passed += 1
    elif state.name == 'parse_udp' and hp4compiler.parseStateUIDs[state] == 3:
      passed += 1
    else:
      assert 0
  assert passed == 4
