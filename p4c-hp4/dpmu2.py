#!/usr/bin/python

import argparse
import sys
import json
import code
import bmpy_utils as utils
import runtime_CLI

def server(args):
  print("server")
  print(args)

def client_load(args):
  print("client_load")
  print(args)

def client_instance(args):
  print("client_instance")
  print(args)

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
  parser_client_instance.add_argument('instance-name', help='name of instance',
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
