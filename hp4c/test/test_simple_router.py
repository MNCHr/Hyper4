from hp4c import hp4c
from p4_hlir.main import HLIR
import pytest

class TestSimpleRouter:
  args = hp4c.parse_args(['-o', 'simple_router.hp4t', 'test/simple_router/simple_router.p4'])
  hp4compiler = hp4c.HP4C(HLIR('test/simple_router/simple_router.p4'), args)
  hp4compiler.build()
  expected = []
  fin = open('test/expected_outputs/simple_router.hp4t', 'r')
  for line in fin:
    expected.append(line[:-1])
  testflags = [False]*len(expected)
  for command in hp4compiler.commands:
    try:
      testflags[expected.index(str(command))] = True
    except ValueError:
      pass

  @pytest.mark.parametrize("test_input", range(len(expected)))
    
  def test_all_expected_commands_present(self, test_input):
    print(self.expected[test_input])
    assert self.testflags[test_input]

  def test_no_extra_commands_present(self):
    assert len(self.hp4compiler.commands) == len(self.expected)
