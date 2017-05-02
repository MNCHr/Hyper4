#!/usr/bin/python

import argparse
import sys
import json
import code
import bmpy_utils as utils
import runtime_CLI
import socket
from subprocess import call

'''
potentially useful runtime_CLI methods:
table = runtime_CLI.TABLES['<table name>']
rta = runtime_CLI.RuntimeAPI('SimplePre', standard_client)
rta.do_table_dump('<table name>')
standard_client.bm_mt_get_entries(0, '<table name>')
entry = standard_client.bm_mt_get_entries(0, '<table name>')[<idx>]
'''

class DPMU_Server():
  def __init__(self, rta, entries, phys_ports, userfile):
    self.next_PID = 1
    self.instances = {}
    self.rta = rta
    self.total_entries = entries
    self.entries_remaining = entries
    self.phys_ports = phys_ports
    self.phys_ports_remaining = phys_ports.split()
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

  def do_load(self, command):
    srcfile = command.split()[1]
    srcname = srcfile.split('.')[0]
    instance = command.split()[2]
    pports = command.split()[3:]
    pport_str = ''
    front_sp = ''
    for port in pports:
      pport_str += front_sp
      pport_str += str(port)
      front_sp = ' '
    # compile
    # p4c-hp4 -o name.hp4t -m name.hp4mt -s 20 <srcfile>
    hp4t = srcname + '.hp4t'
    hp4mt = srcname + '.hp4mt'
    if call(["./p4c-hp4", "-o", hp4t, "-m", hp4mt, "-s 20", srcfile]) == 0:
      for instance in command.split()[2:]:
        self.instances[instance] = (self.next_PID, hp4t, {})
        # load
        # hp4l --input <hp4t> --output instancename+.hp4 --progID self.next_PID --phys_ports ... --virt_ports ...
        call(["../tools/hp4l", "--input", hp4t, "--output", instance+'.hp4',
              "--progID", str(self.next_PID), "--phys_ports", pport_str])
        self.next_PID += 1
    return 'DO_LOAD'

  def do_instance(self, command):
    # rta.do_table_add(...)
    return 'DO_INSTANCE'

def server(args):
  print("server")
  print(args)

  hp4_client, mc_client = runtime_CLI.thrift_connect(args.hp4_ip, args.hp4_port,
                              runtime_CLI.RuntimeAPI.get_thrift_services(args.pre))
  json = '/home/ubuntu/hp4-src/hp4/hp4.json'
  runtime_CLI.load_json_config(hp4_client, json)
  rta = runtime_CLI.RuntimeAPI('SimplePre', hp4_client)

  serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = socket.gethostname()
  serversocket.bind((host, args.port))
  serversocket.listen(5)
  # TODO: non-default parameters
  # def __init__(self, rta, entries, phys_ports, userfile):
  dserver = DPMU_Server(rta, 100, "1 2 3 4", None)

  while True:
    clientsocket,addr = serversocket.accept()
    print("Got a connection from %s" % str(addr))
    data = clientsocket.recv(1024)
    print(data)
    # TODO: create do_load(), do_instance()
    # In do_instance, we'll have rta.do_table_add(...)
    response = ''
    submode = data.split()[0]
    if submode == 'load':
      response = dserver.do_load(data)
    elif submode == 'instance':
      response = dserver.do_instance(data)
    clientsocket.sendall(response)
    clientsocket.close()

def client_load(args):
  print("client_load")
  print(args)
  data = 'load ' + args.source
  # At some point we may want a list of instances...
  """
  if args.instance_list == None:
    data += ' ' + args.source.split('.')[0]
  else:
    for inst in args.instance_list:
      data += ' ' + inst
  """
  # ...but for now:
  data += ' ' + args.instance
  for pport in args.pports:
    data += ' ' + str(pport)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = socket.gethostname()
  s.connect((host, args.port))
  s.send(data)
  resp = s.recv(1024)
  print(resp)
  s.close()

def process_command(port, iname, command):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = socket.gethostname()
  s.connect((host, port))
  s.send('instance ' + iname + ' ' + command)
  resp = s.recv(1024)
  print(resp)
  s.close()

def client_instance(args):
  print("client_instance")
  print(args)
  if args.file is not None:
    lines = [line.rstrip('\n') for line in open(args.file)]
    for line in lines:
      process_command(args.port, args.instance_name, line)
  elif args.command is not None:
    process_command(args.port, args.instance_name, args.command)
  else:
    print("ERROR client instance: require either --command or --file")
    exit()

'''
  client user <username>
  - return resource set associated w/ <username>
  client load source.p4 --user <username> --instance <instance name> [list of phys-ports]
  client populate <instance name> <[--command 'table_add dmac forward 00:AA:BB:00:00:01 => 1' | --file filename]>
  server --port 33333 --hp4-port 22222 --entries 1000 --phys-ports 4 --users userfile
'''
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
  subparsers = parser.add_subparsers(title='modes',
                                     description='valid modes',
                                     dest = 'mode')

  parser_server = subparsers.add_parser('server')
  parser_server.add_argument('--port', help='port for DPMU',
                      type=int, action="store", default=33333)
  parser_server.add_argument('--hp4-ip', help='IP address for HP4',
                             type=str, action="store", default='localhost')
  parser_server.add_argument('--hp4-port', help='port for HP4',
                             type=int, action="store", default=9090)
  parser_server.add_argument('--pre', help='Packet Replication Engine used by target',
                      type=str, choices=['None', 'SimplePre', 'SimplePreLAG'],
                      default=runtime_CLI.PreType.SimplePre, action=ActionToPreType)
  parser_server.set_defaults(func=server)

  parser_client = subparsers.add_parser('client')
  parser_client.add_argument('--port', help='port for DPMU',
                      type=int, action="store", default=33333)

  pc_subparsers = parser_client.add_subparsers(dest = 'subcommand')

  parser_client_load = pc_subparsers.add_parser('load', help='load P4 program')
  parser_client_load.add_argument('source', help='P4 file to compile and load',
                             type=str, action="store")
  parser_client_load.add_argument('--instance', help='instance \
                                  name to associate with the source P4 \
                                  program', type=str, action="store")
  parser_client_load.add_argument('pports', help='Physical ports to which \
                                  the instance should be assigned', type=int,
                                  nargs='+')
  parser_client_load.set_defaults(func=client_load)

  parser_client_instance = pc_subparsers.add_parser('instance',
                                  help='interact with an instance')
  parser_client_instance.add_argument('instance_name', help='name of instance',
                                  type=str, action="store")
  # file / command
  group = parser_client_instance.add_mutually_exclusive_group()
  group.add_argument('--command', help='single table command',
                                  type=str, action="store")
  group.add_argument('--file', help='file containing table commands',
                                  type=str, action="store")
  parser_client_instance.set_defaults(func=client_instance)

  return parser.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  args.func(args)

if __name__ == '__main__':
  main()
