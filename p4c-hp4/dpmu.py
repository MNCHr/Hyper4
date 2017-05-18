#!/usr/bin/python

import argparse
import sys
import json
import runtime_CLI
import socket
from subprocess import call
import os
import copy
import re
from cStringIO import StringIO
from hp4command import HP4_Match_Command
from hp4command import HP4_Primitive_Command

import code

FILENOTFOUND = 1
USERNOTFOUND = 2
INSTANCENOTFOUND = 3
validate_errors = {}
validate_errors[FILENOTFOUND] = 'FILENOTFOUND'
validate_errors[USERNOTFOUND] = 'USERNOTFOUND'
validate_errors[INSTANCENOTFOUND] = 'INSTANCENOTFOUND'

match_types = {'[DONE]':'0',
               '[EXTRACTED_EXACT]':'1',
               '[METADATA_EXACT]':'2',
               '[STDMETA_EXACT]':'3',
               '[EXTRACTED_VALID]':'4',
               '[STDMETA_INGRESS_PORT_EXACT]':'5',
               '[STDMETA_PACKET_LENGTH_EXACT]':'6',
               '[STDMETA_INSTANCE_TYPE_EXACT]':'7',
               '[STDMETA_EGRESS_SPEC_EXACT]':'8',
               '[MATCHLESS]':'99'}

primitive_types = {'[MODIFY_FIELD]':'0',
									 '[ADD_HEADER]':'1',
									 '[COPY_HEADER]':'2',
									 '[REMOVE_HEADER]':'3',
									 '[MODIFY_FIELD_WITH_HBO]':'4',
									 '[TRUNCATE]':'5',
									 '[DROP]':'6',
									 '[NO_OP]':'7',
									 '[PUSH]':'8',
									 '[POP]':'9',
									 '[COUNT]':'10',
									 '[METER]':'11',
									 '[GENERATE_DIGEST]':'12',
									 '[RECIRCULATE]':'13',
									 '[RESUBMIT]':'14',
									 '[CLONE_INGRESS_INGRESS]':'15',
									 '[CLONE_EGRESS_INGRESS]':'16',
									 '[CLONE_INGRESS_EGRESS]':'17',
									 '[CLONE_EGRESS_EGRESS]':'18',
									 '[MULTICAST]':'19',
									 '[MATH_ON_FIELD]':'20'}

MAX_PRIORITY = 2147483647

"""
Credit for Capturing class:
  username 'kindall' response to:
  http://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
"""
class Capturing(list):
  def __enter__(self):
    self._stdout = sys.stdout
    sys.stdout = self._stringio = StringIO()
    return self
  def __exit__(self, *args):
    self.extend(self._stringio.getvalue().splitlines())
    del self._stringio
    sys.stdout = self._stdout

class Rule():
  def __init__(self, rule_type, table, action, mparams, aparams):
    self.rule_type = rule_type
    self.table = table
    self.action = action
    self.mparams = mparams
    self.aparams = aparams

  def __str__(self):
    ret = self.rule_type + ' ' + self.table + ' ' + self.action
    for param in self.mparams:
      ret += ' ' + param
    if self.rule_type == 'table_add':
      ret += ' =>'
    elif self.rule_type != 'table_set_default':
      print("ERROR: incorrect table command %s, table %s" % (self.command, self.table))
      exit()
    for param in self.aparams:
      ret += ' ' + param
    return ret

class DPMU_Server():
  def __init__(self, rta, entries, phys_ports, userfile, debug):
    self.next_PID = 1

    # map instances (strs) to tuples (e.g., (prog ID, source, [vports]))
    self.instances = {}

    # map (instances, source tables) to ints (counter for match_ID)
    self.match_counters = {}

    self.rta = rta
    self.total_entries = entries
    self.entries_remaining = entries
    self.phys_ports = phys_ports
    self.phys_ports_remaining = phys_ports.split()

    # 64 vports w/ 4 vports / vfunc = 16 vfuncs supported
    self.virt_ports_remaining = range(65, 129)

    # map vports (ints) to instances (strs)
    self.virt_ports_instances = {}

    # key: username
    # value: (entries, [phys_ports], [instances])
    self.users = {}

    if userfile is None:
      uports = list(self.phys_ports_remaining)
      self.users['default'] = (self.entries_remaining, uports, [])
      self.entries_remaining = 0
      self.phys_ports_remaining[:] = []
    else:
      lines = [line.rstrip('\n') for line in open(userfile)]
      for line in lines:
        uname = line.split()[0]
        uentries = int(line.split()[1])
        uports = [int(port) for port in line.split()[2:]]
        if uentries > self.entries_remaining:
          print("ERROR: userfile %s: requested %i entries for user %s, %i \
              available" % (userfile, uentries, uname, self.entries_remaining))
          exit()
        for port in uports:
          if port in self.phys_ports_remaining:
            self.phys_ports_remaining.remove(port)
          else:
            print("ERROR: userfile %s: requested port %i not available" % \
                (userfile, port))
            exit()
        self.entries_remaining = self.entries_remaining - uentries
        self.users[uname] = (uentries, uports, [])

    self.debug = debug

  def handle_request(self, data):
    response = ''
    submode = data.split()[1]
    if submode == 'load':
      response = self.handle_load_request(data)
    elif submode == 'instance':
      response = self.handle_rule_request(data)
    return response

  def parse_load_request(self, request):
    uname = request.split()[0]
    fp4 = request.split()[2]
    fname = fp4.split('.')[0]
    fhp4t = fname + '.hp4t'
    fhp4mt = fname + '.hp4mt'
    finst_name = request.split()[3]
    context = request.split()[4:]
    return uname, fp4, fhp4t, fhp4mt, finst_name, context

  def validate_load_request(self, uname, fname, context):
    if uname not in self.users:
      print('USERNOTFOUND: ' + uname)
      return USERNOTFOUND
    if os.path.isfile(fname) == False:
      return FILENOTFOUND
    # TODO: validate context
    return 0

  def load_load_request(self, finst_name):
    with open(finst_name+'.hp4', 'r') as f:
      for line in f:
        if line.split()[0] == 'table_add':
          self.rta.do_table_add(line.split('table_add ')[1])
        elif line.split()[0] == 'table_set_default':
          self.rta.do_table_set_default(line.split('table_set_default ')[1])

  def handle_load_request(self, request):
    if (self.debug):
      print("handle_load_request: " + request)

    uname, \
    fp4, \
    fhp4t, \
    fhp4mt, \
    finst_name, \
    context = self.parse_load_request(request)

    # validate
    validate = self.validate_load_request(uname, fp4, context)
    if validate != 0:
      return 'ERROR: request failed validation with error: ' + validate_errors[validate]

    # compile
    # p4c-hp4 -o name.hp4t -m name.hp4mt -s 20 <srcfile>
    if call(["./p4c-hp4", "-o", fhp4t, "-m", fhp4mt, "-s 20", fp4]) != 0:
      return 'ERROR: could not compile ' + fp4

    # link... TODO: refine handling of context
    if call(["../tools/hp4l", "--input", fhp4t, "--output", finst_name+'.hp4',
            "--progID", str(self.next_PID), "--phys_ports"] + context) != 0:
      return 'ERROR: could not link ' + fhp4t

    # track
    self.instances[finst_name] = (self.next_PID, fhp4t, fhp4mt, [])
    for i in range(4):
      vport = self.virt_ports_remaining.pop(0)
      self.virt_ports_instances[vport] = finst_name
      self.instances[finst_name][3].append(vport)
    self.next_PID += 1

    # load
    self.load_load_request(finst_name)
    
    return 'OK'

  # TODO: implement this in an API-agnostic way (i.e., this method assumes bmv2)
  def parse_rule_request(self, request):
    uname = request.split()[0]
    finst_name = request.split()[2]
    rule_type = request.split()[3]
    table = request.split()[4]
    action = request.split()[5]
    mparams = []
    aparams = []
    if rule_type == 'table_set_default':
      aparams = request.split()[6:]
    elif rule_type == 'table_add':
      args = re.split('\s*=>\s*', request)
      mparams = args[0].split()[6:]
      if len(args) > 1:
        aparams = args[1].split()[0:]
    #mparams = request.split(' => ')[0].split()[6:]
    #aparams = request.split(' => ')[1].split()[0:]
    rule = Rule(rule_type, table, action, mparams, aparams)
    if self.debug:
      print('rule parsed: %s' % str(rule))
    return uname, finst_name, rule

  def validate_rule_request(self, uname, finst_name, rule):
    if uname not in self.users:
      print('USERNOTFOUND: ' + uname)
      return USERNOTFOUND
    if finst_name not in self.instances:
      print('INSTANCENOTFOUND: ' + finst_name)
      return INSTANCENOTFOUND
    # TODO: validate rule
    return 0

  def parse_json(self, finst_name, rule):
    templates_match = {}
    templates_prims = {}
    hp4mt = self.instances[finst_name][2]
    with open(hp4mt) as json_data:
      d = json.load(json_data)
      for hp4_command in d:
        src_table = hp4_command['source_table']
        src_action = hp4_command['source_action']
        key = (src_table, src_action)
        command = hp4_command['command']
        table = hp4_command['table']
        action = hp4_command['action']
        match_params = hp4_command['match_params']
        action_params = hp4_command['action_params']
        if hp4_command['__class__'] == 'HP4_Match_Command':
          templates_match[key] = HP4_Match_Command(src_table, src_action,
                                                   command, table, action,
                                                   match_params, action_params)
        elif hp4_command['__class__'] == 'HP4_Primitive_Command':
          src_aparam_id = hp4_command['src_aparam_id']
          if templates_prims.has_key(key) == False:
            templates_prims[key] = []
          templates_prims[key].append(HP4_Primitive_Command(src_table,
                                                    src_action, command, table,
                                                    action, match_params,
                                                    action_params, 
                                                    src_aparam_id))
        else:
          print("ERROR: Unrecognized class: %s" % hp4_command['__class__'])
    templates = {}
    for key in templates_match:
      templates[key] = {'match': templates_match[key], 'primitives': []}
      if templates_prims.has_key(key):
        templates[key]['primitives'] = templates_prims[key]
    return templates[(rule.table, rule.action)]

  def translate(self, finst_name, templates, rule):
    rules = []
    key = (finst_name, templates['match'].source_table)
    if self.match_counters.has_key(key) == False:
      self.match_counters[key] = 1
    match_ID = self.match_counters[key]
    self.match_counters[key] += 1

    # handle the match rule
    ## match parameters
    mrule = copy.copy(templates['match'])
    for i in range(len(mrule.match_params)):
      if mrule.match_params[i] == '[program ID]':
        mrule.match_params[i] = str(self.instances[finst_name][0])
      if rule.rule_type == 'table_add':
        if '[val]' in mrule.match_params[i]:
          # ERROR! Need to detect hex, convert to hex if not
          if '0x' in rule.mparams[0]:
            leftside = rule.mparams[0]
          elif ':' in rule.mparams[0]:
            print("Not yet supported: %s" % rule.mparams[0])
            exit()
          else:
            leftside = format(int(rule.mparams[0]), '#x')
          code.interact(local=locals())
          # leftside = rule.mparams[0]
          if re.search("\[[0-9]*x00s\]", mrule.match_params[i]):
            to_replace = re.search("\[[0-9]*x00s\]", mrule.match_params[i]).group()
            numzeros = int(re.search("[0-9]+", to_replace).group())
            replace = ""
            for j in range(numzeros):
              replace += "00"   
            mrule.match_params[i] = \
                    mrule.match_params[i].replace(to_replace, replace)
            leftside += replace
          mrule.match_params[i] = \
                  mrule.match_params[i].replace('[val]', leftside)
        elif '[valid]' in mrule.match_params[i]:
          # handle valid matching; 0 = 0, 1 = everything right of &&&
          if rule.mparams[0] == '1':
            mrule.match_params[i] = \
                    mrule.match_params[i].replace('[valid]',
                                         mrule.match_params[i].split('&&&')[1])
          elif rule.mparams[0] == '0':
            mrule.match_params[i] = \
                    mrule.match_params[i].replace('[valid]', '0x0')
          else:
            print("ERROR: Unexpected value in rule.mparams[0]: %s" % rule.mparams[0])
            exit()
      elif rule.rule_type == 'table_set_default':
        if ('[val]' in mrule.match_params[i] or
            '[valid]' in mrule.match_params[i]):
          mrule.match_params[i] = '0&&&0' # don't care

    ## action parameters
    for i in range(len(mrule.action_params)):
      if mrule.action_params[i] == '[match ID]':
        mrule.action_params[i] = str(match_ID)
      elif mrule.action_params[i] == '[PRIORITY]':
        if rule.rule_type == 'table_set_default':
          mrule.action_params[i] = str(MAX_PRIORITY)
        else:
          mrule.action_params[i] = '0'
      elif mrule.action_params[i] in match_types:
        mrule.action_params[i] = match_types[mrule.action_params[i]]
      elif mrule.action_params[i] in primitive_types:
        mrule.action_params[i] = primitive_types[mrule.action_params[i]]

    rules.append(mrule)

    # handle the primitives rules
    for entry in templates['primitives']:
      arule = copy.copy(entry)
      ## match parameters
      for i in range(len(arule.match_params)):
        if arule.match_params[i] == '[program ID]':
          arule.match_params[i] = str(self.instances[finst_name][0])
        elif '[match ID]' in arule.match_params[i]:
          arule.match_params[i] = arule.match_params[i].replace('[match ID]',
                                                                 str(match_ID))
      ## action parameters
      for i in range(len(arule.action_params)):
        if arule.action_params[i] == '[val]':
          a_idx = int(arule.src_aparam_id)
          arule.action_params[i] = str(rule.aparams[a_idx])
        if re.search("\[[0-9]*x00s\]", arule.action_params[i]):
          to_replace = re.search("\[[0-9]*x00s\]", arule.action_params[i]).group()
          numzeros = int(re.search("[0-9]+", to_replace).group())
          replace = ""
          for j in range(numzeros):
            replace += "00"   
          arule.action_params[i] = \
                            arule.action_params[i].replace(to_replace, replace)
      
      rules.append(arule)

    return rules

  def handle_rule_request(self, request):
    # parse request
    uname, finst_name, rule = self.parse_rule_request(request)

    # validate
    validate = self.validate_rule_request(uname, finst_name, rule)
    if validate != 0:
      return 'ERROR: request failed validation with error: ' + validate_errors[validate]

    # parse json: return dict w/ keys 'match' and 'primitives'
    # value for 'match': an HP4_Match_Command
    # value for 'primitives': a list of HP4_Primitive_Commands
    templates = self.parse_json(finst_name, rule)

    # translate
    rules = self.translate(finst_name, templates, rule)
    #code.interact(local=locals())
    # push to hp4
    for rule in rules:
      if(self.debug):
        print(rule)
      if rule.command == 'table_add':
        with Capturing() as output:
          self.rta.do_table_add(str(rule).split('table_add ')[1])
        for line in output:
          print(line)
          # TODO: detect error and return error message
          if 'Entry has been added' in line:
            handle = int(line.split('handle ')[1])
        # TODO: figure out how to track entry handles properly per instance
      elif rule.command == 'table_set_default':
        self.rta.do_table_set_default(str(rule).split('table_set_default ')[1])
    return 'OK'

  def handle_composition_request(self, request):
    pass
  def handle_ralloc_request(self, request):
    pass
  def handle_status_request(self, request):
    pass

def server(args):
  if(args.debug):
    print("server")
    print(args)
  hp4_client, mc_client = runtime_CLI.thrift_connect(args.hp4_ip,
                          args.hp4_port,
                          runtime_CLI.RuntimeAPI.get_thrift_services(args.pre))
  json = '/home/ubuntu/hp4-src/hp4/hp4.json'
  runtime_CLI.load_json_config(hp4_client, json)
  rta = runtime_CLI.RuntimeAPI('SimplePre', hp4_client)

  serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  host = socket.gethostname()
  serversocket.bind((host, args.port))
  serversocket.listen(5)
  # TODO: non-default parameters
  # def __init__(self, rta, entries, phys_ports, userfile):
  dserver = DPMU_Server(rta, 100, "1 2 3 4", None, args.debug)

  while True:
    clientsocket = None
    try:
      clientsocket,addr = serversocket.accept()
      if(args.debug):
        print("Got a connection from %s" % str(addr))
      data = clientsocket.recv(1024)
      if(args.debug):
        print(data)
      # In do_instance, we'll have rta.do_table_add(...)
      response = dserver.handle_request(data)
      clientsocket.sendall(response)
      clientsocket.close()
    except KeyboardInterrupt:
      if clientsocket:
        clientsocket.close()
      serversocket.close()
      if(args.debug):
        print('Keyboard Interrupt, sockets closed')
      break

def load(args):
  if(args.debug):
    print("client load")
    print(args)
  data = args.user + ' load ' + args.source
  data += ' ' + args.instance
  for pport in args.pports:
    data += ' ' + str(pport)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = socket.gethostname()
  s.connect((host, args.port))
  s.send(data)
  resp = s.recv(1024)
  if(args.debug):
    print(resp)
  s.close()

def instance(args):
  if(args.debug):
    print("client instance")
    print(args)
  def handle_command(command):
    data = args.user + ' instance ' + args.instance_name + ' ' + command
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.connect((host, args.port))
    s.send(data)
    resp = s.recv(1024)
    if(args.debug):
      print(resp)
    s.close()
  if args.command:
    handle_command(args.command)
  elif args.file:
    with open(args.file) as cmd_file:
      for line in cmd_file:
        handle_command(line)

def parse_args(args):
  class ActionToPreType(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
      if nargs is not None:
        raise ValueError("nargs not allowed")
      super(ActionToPreType, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
      assert(type(values) is str)
      setattr(namespace, self.dest, PreType.from_str(values))

  parser = argparse.ArgumentParser(description='Data Plane Management Unit')
  parser.add_argument('--debug', help='turn on debug mode',
                      action='store_true')
  subparsers = parser.add_subparsers(title='modes',
                                     description='valid modes',
                                     dest='mode')
  parser_server = subparsers.add_parser('server')
  parser_client = subparsers.add_parser('client')

  # server
  parser_server.add_argument('--port', help='port for DPMU',
                      type=int, action="store", default=33333)
  parser_server.add_argument('--hp4-ip', help='IP address for HP4',
                             type=str, action="store", default='localhost')
  parser_server.add_argument('--hp4-port', help='port for HP4',
                             type=int, action="store", default=9090)
  parser_server.add_argument('--pre', help='Packet Replication Engine used by \
                 target',
                 type=str, choices=['None', 'SimplePre', 'SimplePreLAG'],
                 default=runtime_CLI.PreType.SimplePre, action=ActionToPreType)
  parser_server.set_defaults(func=server)

  # client
  parser_client.add_argument('user', help='username', type=str, action="store")
  parser_client.add_argument('--port', help='port for DPMU',
                             type=int, action="store", default=33333)
  pc_subparsers = parser_client.add_subparsers(dest = 'subcommand')
  parser_client_load = pc_subparsers.add_parser('load', help='load P4 program')
  parser_client_inst = pc_subparsers.add_parser('instance',
                                              help='interact with an instance')

  ## client load
  parser_client_load.add_argument('source', help='P4 file to compile and load',
                                  type=str, action="store")
  parser_client_load.add_argument('--instance', help='instance \
                                  name to associate with the source P4 \
                                  program', type=str, action="store")
  parser_client_load.add_argument('pports', help='Physical ports to which \
                                  the instance should be assigned', type=int,
                                  nargs='+')
  parser_client_load.set_defaults(func=load)

  ## client instance
  parser_client_inst.add_argument('instance_name', help='name of instance',
                                  type=str, action="store")
  ### file / command
  group = parser_client_inst.add_mutually_exclusive_group()
  group.add_argument('--command', help='single table command',
                                  type=str, action="store")
  group.add_argument('--file', help='file containing table commands',
                                  type=str, action="store")

  parser_client_inst.set_defaults(func=instance)
  
  return parser.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  args.func(args)

if __name__ == '__main__':
  main()
