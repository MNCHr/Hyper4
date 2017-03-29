#!/usr/bin/python

import argparse
import sys
import json
import code
import bmpy_utils as utils
import runtime_CLI
import socket

'''
potentially useful runtime_CLI methods:
table = runtime_CLI.TABLES['<table name>']
rta = runtime_CLI.RuntimeAPI('SimplePre', standard_client)
rta.do_table_dump('<table name>')
standard_client.bm_mt_get_entries(0, '<table name>')
entry = standard_client.bm_mt_get_entries(0, '<table name>')[<idx>]
'''

def do_load():
  pass

def do_instance():
  pass

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

  while True:
    clientsocket,addr = serversocket.accept()
    print("Got a connection from %s" % str(addr))
    data = clientsocket.recv(1024)
    print(data)
    # TODO: create do_load(), do_instance()
    # In do_instance, we'll have rta.do_table_add(...)
    clientsocket.sendall('response')
    clientsocket.close()

def client_load(args):
  print("client_load")
  print(args)
  

def process_command(port, iname, command):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = socket.gethostname()
  s.connect((host, port))
  s.send(iname + ' ' + command)
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
  parser_client_load.add_argument('--instance-list', help='list of instance \
                                  names to associate with the source P4 \
                                  program', nargs='*')
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
