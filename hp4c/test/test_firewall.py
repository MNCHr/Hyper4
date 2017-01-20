from hp4c import hp4c
from p4_hlir.main import HLIR
import pytest

class TestFirewall:
  function = 'firewall'
  args = hp4c.parse_args(['-o', function+'.hp4t', 'test/'+function+'.p4'])
  hp4compiler = hp4c.HP4C(HLIR('test/'+function+'.p4'), args)
  hp4compiler.build()
  expected = []
  fin = open('test/expected_outputs/'+function+'.hp4t', 'r')
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
    # hack to handle non-deterministic order of state handling though still correct:
    if test_input == 15 or test_input == 17:
      if self.testflags[test_input] == False:
        if self.hp4compiler.commands[15].action_params == '0xe0000000000000000000':
          if self.hp4compiler.commands[17].action_params == '0xd0000000000000000000':
            assert True
          else:
            assert False
        elif self.hp4compiler.commands[15].action_params == '0xd0000000000000000000':
          if self.hp4compiler.commands[17].action_params == '0xe0000000000000000000':
            assert True
          else:
            assert False
        else:
          assert False
    assert self.testflags[test_input]

  def test_no_extra_commands_present(self):
    assert len(self.hp4compiler.commands) == len(self.expected)
