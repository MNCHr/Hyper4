#!/usr/bin/python

import argparse
import sys
import json
import code

def parse_args(args):
  parser = argparse.ArgumentParser(description='Data Plane Management Unit')
  parser.add_argument('-p', '--port', help='Thrift port for HyPer4',
                      type=int, action="store", default=9090)
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
  code.interact(local=locals())
  if args.file is not None:
    pass
  elif args.command is not None:
  else:
    print("ERROR: Require either -c: single command, or -f: file including one or more commands")
    exit()

if __name__ == '__main__':
  main()
