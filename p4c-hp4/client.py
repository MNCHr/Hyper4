#!/usr/bin/python

import argparse
import sys
import socket
import cmd

import code

def generic_send_request(host, port, data):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((host, port))
  s.send(data)
  resp = s.recv(1024)
  s.close()
  return resp

class Client(cmd.Cmd):
  prompt = 'HP4$ '
  intro = "Control utility for runtime HP4 management"

  def __init__(self, args):
    cmd.Cmd.__init__(self)
    self.user = args.user
    self.host = args.ip
    self.port = args.port
    self.debug = args.debug

  def do_EOF(self, line):
    print
    return True

  def send_request(self, data):
    return generic_send_request(self.host, self.port, data)

  def dbugprint(self, msg):
    if self.debug:
      print(msg)

class AdminClient(Client):
  prompt = 'HP4# '

  def do_add_user(self, line):
    "Add a user"
    resp = self.send_request(self.user + ' add_user ' + line)
    print(resp)

  def do_list_users(self, line):
    "List users"
    resp = self.send_request(self.user + ' list_users')
    print(resp)

  def do_add_device(self, line):
    "Add a device: add_device <ip> <port> " \
     + "<pre: \'SimplePre\'|\'SimplePreLAG\'|\'None\'> <name> <# entries> <ports>"
    resp = self.send_request(self.user + ' add_device ' + line)
    print(resp)

def client(args):
  if args.user == 'admin':
    c = AdminClient(args)
  else:
    c = Client(args)
  if args.startup:
    with open(args.startup) as commands:
      for command in commands:
        c.onecmd(command)
  c.cmdloop()

def parse_args(args):
  parser = argparse.ArgumentParser(description='HyPer4 Client')
  parser.add_argument('--debug', help='turn on debug mode',
                      action='store_true')
  parser.add_argument('--ip', help='ip of Controller',
                      type=str, action="store", default="localhost")
  parser.add_argument('--port', help='port for Controller',
                      type=int, action="store", default=33333)
  parser.add_argument('--startup', help='file with commands to run at startup',
                      type=str, action="store")
  parser.add_argument('user', help='username', type=str, action="store")
  parser.set_defaults(func=client)

  return parser.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  args.func(args)

if __name__ == '__main__':
  main()
