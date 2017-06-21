#!/usr/bin/python

import argparse
import sys
import socket
import cmd

import code

class Client(cmd.Cmd):
  prompt = 'HP4: '
  intro = "Control utility for runtime HP4 management"


  def __init__(self, args):
    cmd.Cmd.__init__(self)
    self.user = args.user
    self.port = args.port
    self.debug = args.debug

  def do_EOF(self, line):
    print
    return True

  def send_request(self, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.connect((host, self.port))
    s.send(data)
    resp = s.recv(1024)
    s.close()
    return resp

  def do_beep(self, line):
    "Simple test"
    data = 'beep'
    resp = self.send_request(data)
    self.dbugprint(resp)

  def do_add_user(self, line):
    "Add a user"
    resp = self.send_request(self.user + ' ' + 'add_user ' + line)
    print(resp)

  def dbugprint(self, msg):
    if self.debug:
      print(msg)

def client(args):
  #c = Client(args)
  #c.beep()
  Client(args).cmdloop()

def parse_args(args):
  parser = argparse.ArgumentParser(description='HyPer4 Client')
  parser.add_argument('--debug', help='turn on debug mode',
                      action='store_true')
  parser.add_argument('--port', help='port for Controller',
                      type=int, action="store", default=33333)
  parser.add_argument('user', help='username', type=str, action="store")
  parser.set_defaults(func=client)

  return parser.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  args.func(args)

if __name__ == '__main__':
  main()
