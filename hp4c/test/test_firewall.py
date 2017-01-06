from hp4c import hp4c
from p4_hlir.main import HLIR

class TestFirewall:
  def test_tset_control_entry_A(self):
    args = hp4c.parse_args(['-o', 'firewall.hp4t', 'test/firewall.p4'])
    hp4compiler = hp4c.HP4C(HLIR("test/firewall.p4"), args)
    hp4compiler.gen_tset_control_entries()
    passed = False
    for command in hp4compiler.commands:
      if (command.command == 'table_add' and
          command.table == 'tset_control' and
          command.action == 'set_next_action' and
          command.match_params == ['[program ID]', '0'] and
          command.action_params == ['[INSPECT_SEB]', '1']):
        passed = True
        break
    assert passed

"""
def test_firewall():
  args = hp4c.parse_args(['-o', 'firewall.hp4t', 'test/firewall.p4'])
  hp4compiler = hp4c.HP4C(HLIR("test/firewall.p4"), args)
  hp4compiler.gen_tset_control_entries()
  passed = 0
  for command in hp4compiler.commands:
    if (command.table == 'tset_control' and
        command.action == 'set_next_action' and
        command.match_params == ['[program ID]', '0'] and
        command.action_params == ['[INSPECT_SEB]', '1']):
      passed += 1
    elif (command.table == 'tset_control' and
          command.action == 'set_next_action' and
          command.match_params == ['[program ID]', '2'] and
          command.action_params == ['[INSPECT_20_29]', '2']):
      passed += 1
    elif (command.table == 'tset_control' and
          command.action == 'set_next_action' and
          command.match_params == ['[program ID]', '3'] and
          command.action_params == ['[PROCEED]', '3']):
      passed += 1
    elif (command.table == 'tset_control' and
          command.action == 'set_next_action' and
          command.match_params == ['[program ID]', '4'] and
          command.action_params == ['[PROCEED]', '4']):
      passed += 1
  assert passed == 4

def tset_control_entry_A(hp4compiler):
  cmd_type = 'table_add'
  table = 'tset_control'
  action = 'set_next_action'
  mparams = ['[program ID]', '0']
  aparams = ['[INSPECT_SEB]', '1']
  command = hp4c.HP4_Command(cmd_type, table, action, mparams, aparams)
  assert command in hp4compiler.commands
"""

#def test_firewall():
#  assert firewall()

"""
def test_parsing():
  args = hp4c.parse_args(['-o', 'firewall.hp4t', 'test/firewall.p4'])
  hp4compiler = hp4c.HP4C(HLIR("test/firewall.p4"), args)
  passed = [0, 0, 0, 0]
  for key in hp4compiler.bits_needed_total.keys():
    if key[0].name == 'start':
      if key[1] == ():
        if hp4compiler.bits_needed_total[key] == 112:
          passed[0] = 1
    elif key[0].name == 'parse_ipv4':
      if len(key[1]) == 1:
        if key[1][0].name == 'start':
          if hp4compiler.bits_needed_total[key] == 272:
            passed[1] = 1
    elif key[0].name == 'parse_tcp':
      if len(key[1]) == 2:
        if key[1][0].name == 'start' and key[1][1].name == 'parse_ipv4':
          if hp4compiler.bits_needed_total[key] == 432:
            passed[2] = 1
    elif key[0].name == 'parse_udp':
      if len(key[1]) == 2:
        if key[1][0].name == 'start' and key[1][1].name == 'parse_ipv4':
          if hp4compiler.bits_needed_total[key] == 336:
            passed[3] = 1
  assert passed == [1, 1, 1, 1]
"""
