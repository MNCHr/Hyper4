class HP4_Command:
  def __init__(self, command, table, action, mparams, aparams):
    self.command = command
    self.table = table
    self.action = action
    self.match_params = mparams
    self.action_params = aparams
  def __str__(self):
    ret = self.command + ' ' + self.table + ' ' + self.action
    for param in self.match_params:
      ret += ' ' + param
    if self.command == 'table_add':
      ret += ' =>'
    elif self.command != 'table_set_default':
      print("ERROR: incorrect table command %s, table %s" % (self.command, self.table))
      exit()
    for param in self.action_params:
      ret += ' ' + param
    return ret

class TICS(HP4_Command):
  def __init__(self):
    HP4_Command.__init__(self, '', '', '', [], [])
    self.curr_pc_state = 0
    self.next_pc_state = 0
    self.next_parse_state = ''
    self.priority = 0

class HP4_Match_Command(HP4_Command):
  def __init__(self, source_table, source_action, command, table, action, mparams, aparams):
    HP4_Command.__init__(self, command, table, action, mparams, aparams)
    self.source_table = source_table
    self.source_action = source_action

class HP4_Primitive_Command(HP4_Command):
  def __init__(self, source_table, source_action, command, table, action, mparams, aparams, src_aparam_id):
    HP4_Command.__init__(self, command, table, action, mparams, aparams)
    self.source_table = source_table
    self.source_action = source_action
    self.src_aparam_id = src_aparam_id
