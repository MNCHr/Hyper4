from hp4c import hp4c
from p4_hlir.main import HLIR
import pytest

class TestFirewall:
  args = hp4c.parse_args(['-o', 'firewall.hp4t', 'test/firewall.p4'])
  hp4compiler = hp4c.HP4C(HLIR("test/firewall.p4"), args)
  hp4compiler.gen_tset_context_entry()
  hp4compiler.gen_tset_control_entries()
  expected = []
  fin = open('test/expected_outputs/firewall.hp4t', 'r')
  for line in fin:
    expected.append(line[:-1])
  testflags = [False]*len(expected)
  for command in hp4compiler.commands:
    try:
      testflags[expected.index(str(command))] = True
    except ValueError:
      pass
  @pytest.mark.parametrize("test_input", range(len(expected)))
    
  def test_tset_control_entry(self, test_input):
    print(self.expected[test_input])
    assert self.testflags[test_input]
