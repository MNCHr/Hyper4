from hp4c import hp4c
from p4_hlir.main import HLIR

def firewall():
  args = hp4c.parse_args(['-o', 'firewall.hp4t', 'firewall.p4'])
  hp4compiler = hp4c.HP4C(HLIR("firewall.p4"), args)
  return True

def test_firewall():
  assert firewall()
