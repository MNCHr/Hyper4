from hp4c import hp4c
from p4_hlir.main import HLIR

def arp_proxy():
  args = hp4c.parse_args(['-o', 'arp_proxy.hp4t', 'test/arp_proxy.p4'])
  hp4compiler = hp4c.HP4C(HLIR("test/arp_proxy.p4"), args)
  hp4compiler.gen_tset_control_entries()
  return True

def test_arp_proxy():
  assert arp_proxy()
