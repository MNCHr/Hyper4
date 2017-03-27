#!/usr/bin/python

import argparse
import sys
import json
import code
import bmpy_utils as utils
import runtime_CLI

hp4_commands = []

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

  parser.add_argument('--port', help='port for DPMU',
                      type=int, action="store", default=33333)
  parser.add_argument('--hp4-ip', help='IP address for HP4',
                      type=str, action="store", default='localhost')
  parser.add_argument('--hp4-port', help='port for HyPer4',
                      type=int, action="store", default=9090)
  parser.add_argument('--pre', help='Packet Replication Engine used by target',
                      type=str, choices=['None', 'SimplePre', 'SimplePreLAG'],
                      default=runtime_CLI.PreType.SimplePre, action=ActionToPreType)
  parser.add_argument('--server', help='flag starts DPMU as a server',
                      action="store_true")

  group = parser.add_mutually_exclusive_group()
  group.add_argument('--command', help='single table command',
                     type=str, action="store")
  group.add_argument('--file', help='file containing table commands',
                      type=str, action="store")
  return parser.parse_args(args)

def process_command(template, command):
  src_table = command.split()[1]
  src_action = command.split()[2]
  # TODO...

def write_output(args):
  standard_client, mc_client = runtime_CLI.thrift_connect(args.hp4_ip, args.hp4_port,
      runtime_CLI.RuntimeAPI.get_thrift_services(args.pre)
  )
  json = '../hp4/hp4.json'
  runtime_CLI.load_json_config(standard_client, json)
  #for command in hp4_commands:
    

def main():
  args = parse_args(sys.argv[1:])
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
  with open(args.template) as template_file:
    template = json.load(template_file)

  if args.file is not None:
    lines = [line.rstrip('\n') for line in open(args.file)]
    for line in lines:
      process_command(template, line)
  elif args.command is not None:
    process_command(template, args.command)
  else:
    print("ERROR: Require either -c: single command, or -f: file including one or more commands")
    exit()

  #write_output(args)
  #code.interact(local=locals())

if __name__ == '__main__':
  main()
