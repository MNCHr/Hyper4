#!/usr/bin/python

import argparse
import sys
import socket

import code

class Client():
  def __init__(self, args):
    self.args = args
    self.port = args.port
    self.debug = args.debug

  def send_request(self, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.connect((host, self.port))
    s.send(data)
    resp = s.recv(1024)
    s.close()
    return resp

  def beep(self):
    data = 'beep'
    self.send_request(data)
    

  def dbugprint(msg):
    if self.debug:
      print(msg)

def client(args):
  c = Client(args)
  c.beep()

def parse_args(args):
  parser = argparse.ArgumentParser(description='HyPer4 Client')
  parser.add_argument('--debug', help='turn on debug mode',
                      action='store_true')
  parser.add_argument('--port', help='port for Controller',
                      type=int, action="store", default=33333)
  parser.set_defaults(func=client)

  return parser.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  args.func(args)

if __name__ == '__main__':
  main()
