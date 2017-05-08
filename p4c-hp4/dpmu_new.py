#!/usr/bin/python

import argparse
import sys
import json
import runtime_CLI
import socket
from subprocess import call

import code

class DPMU_Server():
  def __init__(self, rta, entries, phys_ports, userfile, debug):
    self.next_PID = 1

    # map instances (strs) to tuples (e.g., (prog ID, source, [vports]))
    self.instances = {}

    self.rta = rta
    self.total_entries = entries
    self.entries_remaining = entries
    self.phys_ports = phys_ports
    self.phys_ports_remaining = phys_ports.split()

    # 64 vports w/ 4 vports / vfunc = 16 vfuncs supported
    self.virt_ports_remaining = range(65, 129)

    # map vports (ints) to instances (strs)
    self.virt_ports_instances = {}

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

    self.debug = debug

  def handle_request(self, data):
    response = ''
    submode = data.split()[0]
    if submode == 'load':
      response = self.handle_load_request(data)
    elif submode == 'instance':
      response = dserver.handle_rule_request(data)
    return response

  def handle_load_request(self, request):
    if (self.debug):
      print("handle_load_request: " + request)
    srcfile = request.split()[1]
    srcname = srcfile.split('.')[0]
    instance = request.split()[2]
    pports = request.split()[3:]
    # compile
    # p4c-hp4 -o name.hp4t -m name.hp4mt -s 20 <srcfile>
    hp4t = srcname + '.hp4t'
    hp4mt = srcname + '.hp4mt'
    if call(["./p4c-hp4", "-o", hp4t, "-m", hp4mt, "-s 20", srcfile]) != 0:
      return 'ERROR: could not compile ' + srcfile

    # link
    if call(["../tools/hp4l", "--input", hp4t, "--output", instance+'.hp4',
            "--progID", str(self.next_PID), "--phys_ports"] + pports) != 0:
      return 'ERROR: could not link ' + hp4t

    # track
    self.instances[instance] = (self.next_PID, hp4t, [])
    for i in range(4):
      vport = self.virt_ports_remaining.pop(0)
      self.virt_ports_instances[vport] = instance
      self.instances[instance][2].append(vport)
    self.next_PID += 1

    # load
    code.interact(local=locals())
    # self.rta.do_table_add(...)


  def handle_rule_request(self, request):
    pass
  def handle_composition_request(self, request):
    pass
  def handle_ralloc_request(self, request):
    pass
  def handle_status_request(self, request):
    pass

def server(args):
  if(args.debug):
    print("server")
    print(args)
  hp4_client, mc_client = runtime_CLI.thrift_connect(args.hp4_ip,
                          args.hp4_port,
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
  dserver = DPMU_Server(rta, 100, "1 2 3 4", None, args.debug)

  while True:
    clientsocket = None
    try:
      clientsocket,addr = serversocket.accept()
      if(args.debug):
        print("Got a connection from %s" % str(addr))
      data = clientsocket.recv(1024)
      if(args.debug):
        print(data)
      # In do_instance, we'll have rta.do_table_add(...)
      response = dserver.handle_request(data)
      clientsocket.sendall(response)
      clientsocket.close()
    except KeyboardInterrupt:
      if clientsocket:
        clientsocket.close()
      break

def load(args):
  if(args.debug):
    print("client load")
    print(args)
  data = 'load ' + args.source
  data += ' ' + args.instance
  for pport in args.pports:
    data += ' ' + str(pport)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = socket.gethostname()
  s.connect((host, args.port))
  s.send(data)
  resp = s.recv(1024)
  if(args.debug):
    print(resp)
  s.close()

def rule(args):
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
  parser.add_argument('--debug', help='turn on debug mode',
                      action='store_true')
  subparsers = parser.add_subparsers(title='modes',
                                     description='valid modes',
                                     dest='mode')
  parser_server = subparsers.add_parser('server')
  parser_client = subparsers.add_parser('client')

  # server
  parser_server.add_argument('--port', help='port for DPMU',
                      type=int, action="store", default=33333)
  parser_server.add_argument('--hp4-ip', help='IP address for HP4',
                             type=str, action="store", default='localhost')
  parser_server.add_argument('--hp4-port', help='port for HP4',
                             type=int, action="store", default=9090)
  parser_server.add_argument('--pre', help='Packet Replication Engine used by \
                 target',
                 type=str, choices=['None', 'SimplePre', 'SimplePreLAG'],
                 default=runtime_CLI.PreType.SimplePre, action=ActionToPreType)
  parser_server.set_defaults(func=server)

  # client
  parser_client.add_argument('--port', help='port for DPMU',
                             type=int, action="store", default=33333)
  pc_subparsers = parser_client.add_subparsers(dest = 'subcommand')
  parser_client_load = pc_subparsers.add_parser('load', help='load P4 program')
  parser_client_inst = pc_subparsers.add_parser('instance',
                                              help='interact with an instance')

  ## client load
  parser_client_load.add_argument('source', help='P4 file to compile and load',
                                  type=str, action="store")
  parser_client_load.add_argument('--instance', help='instance \
                                  name to associate with the source P4 \
                                  program', type=str, action="store")
  parser_client_load.add_argument('pports', help='Physical ports to which \
                                  the instance should be assigned', type=int,
                                  nargs='+')
  parser_client_load.set_defaults(func=load)

  ## client instance
  parser_client_inst.add_argument('instance_name', help='name of instance',
                                  type=str, action="store")
  ### file / command
  group = parser_client_inst.add_mutually_exclusive_group()
  group.add_argument('--command', help='single table command',
                                  type=str, action="store")
  group.add_argument('--file', help='file containing table commands',
                                  type=str, action="store")

  parser_client_inst.set_defaults(func=rule)
  
  return parser.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  args.func(args)

if __name__ == '__main__':
  main()
