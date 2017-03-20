#!/usr/bin/python

import argparse
import sys
import json
import code
import bmpy_utils as utils
import runtime_CLI

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
  parser.add_argument('-p', '--port', help='Thrift port for HyPer4',
                      type=int, action="store", default=9090)
  parser.add_argument('--thrift-ip', help='Thrift IP address for table updates',
                      type=str, action="store", default='localhost')
  parser.add_argument('--pre', help='Packet Replication Engine used by target',
                      type=str, choices=['None', 'SimplePre', 'SimplePreLAG'],
                      default=runtime_CLI.PreType.SimplePre, action=ActionToPreType)
  parser.add_argument('-i', '--initialize', help='initialize DPMU state',
                      action="store_true")
  parser.add_argument('-t', '--template', help='template file (.hp4mt)',
                      type=str, action="store")
  parser.add_argument('-P', '--pid', help='program ID',
                      type=str, action="store")
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-c', '--command', help='single table command',
                     type=str, action="store")
  group.add_argument('-f', '--file', help='file containing table commands',
                      type=str, action="store")
  return parser.parse_args(args)

def write_output():
  pass

def main():
  args = parse_args(sys.argv[1:])
  # code.interact(local=locals())
  '''
  standard_client, mc_client = thrift_connect(args.thrift_ip, args.thrift_port,
      RuntimeAPI.get_thrift_services(args.pre)
  )
  json = '/home/ubuntu/hp4-src/hp4/hp4.json'
  runtime_CLI.load_json_config(standard_client, json)
  #table = runtime_CLI.TABLES['<table name>']
  #rta = runtime_CLI.RuntimeAPI('SimplePre', standard_client)
  #rta.do_table_dump('<table name>')
  #standard_client.bm_mt_get_entries(0, '<table name>')
  #entry = standard_client.bm_mt_get_entries(0, '<table name>')[<idx>]
  #rta.do_table_add('<table name> <action name> <match fields> => <action parameters> [priority]')
  '''
  if args.file is not None:
    pass
  elif args.command is not None:
    print(args.command)
  else:
    print("ERROR: Require either -c: single command, or -f: file including one or more commands")
    exit()

if __name__ == '__main__':
  main()
