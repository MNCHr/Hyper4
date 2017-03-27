#!/usr/bin/python

import argparse
import sys
import json
import code
import bmpy_utils as utils
import runtime_CLI

def server(args):
  pass

def client(args):
  pass

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
  subparsers = parser.add_subparsers()

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

  parser_client = subparsers.add_parser('client')
  parser_client.add_argument('--port', help='port for DPMU',
                      type=int, action="store", default=33333)
  parser_client.add_argument('--load', help='P4 file to compile and load, \
                             optionally followed by list of instance names',
                             type=str, nargs=*, action="store")

  return parser.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])


if __name__ == '__main__':
  main()
