from .. import hp4c

def func():
  hp4compiler = HP4C(HLIR(firewall.p4))
  return True

def test_test():
  assert func()
