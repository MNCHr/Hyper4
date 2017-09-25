#!/usr/bin/python

# Copyright 2013-present Barefoot Networks, Inc. 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep
import os
import subprocess
import random

import code

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))
_THRIFT_BASE_PORT = 22222

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=True)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--cli', help='Path to BM CLI',
                    type=str, action="store", required=True)
parser.add_argument('--commands', help='Path to initial CLI commands',
                    type=str, nargs='*', action="store", default=["commands.txt"])
parser.add_argument('--pcap', help='Turns on pcap generation',
                    action="store_true")
parser.add_argument('--scenario', help='Simulation scenario',
                    type=str, action="store")
parser.add_argument('--seed', help='Seed for pseudorandom numbers',
                    type=int, action="store")
parser.add_argument('--topo', help='Topology file',
                    type=str, action="store", default="topo.txt")
# Useful if we need to use runtime_CLI instead of sswitch_CLI:
#parser.add_argument('--p4factory', help='Use p4factory intead of standalone repos',
#                    action="store_true")

args = parser.parse_args()

class MyTopo(Topo):
    def __init__(self, sw_path, json_path, nb_hosts, nb_switches, links, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        for i in xrange(nb_switches):
            switch = self.addSwitch('s%d' % (i + 1),
                                    sw_path = sw_path,
                                    json_path = json_path,
                                    thrift_port = _THRIFT_BASE_PORT + i,
                                    pcap_dump = args.pcap,
                                    device_id = i)
        
        for h in xrange(nb_hosts):
            host = self.addHost('h%d' % (h + 1),
                                ip = "10.0.0.%d/24" % (h+1),
                                mac = '00:04:00:00:00:%02x' %h)

        for a, b in links:
            self.addLink(a, b)

class ArpTestTopo(Topo):
  def __init__(self, sw_path, json_path, nb_hosts, nb_switches, links, seed, **opts):
    Topo.__init__(self, **opts)

    random.seed(seed)

    assert(nb_hosts < 255)
    
    for i in xrange(nb_switches):
        switch = self.addSwitch('s%d' % (i + 1),
                                sw_path = sw_path,
                                json_path = json_path,
                                thrift_port = _THRIFT_BASE_PORT + i,
                                pcap_dump = args.pcap)

    ip_addrs = range(1, 255)
    for h in xrange(nb_hosts):
      ip_addr = ip_addrs.pop(random.randint(0, len(ip_addrs) - 1))
      host = self.addHost('h%d' % (h + 1),
                          ip = "10.0.0.%d/24" % (ip_addr),
                          mac = "00:04:00:00:00:%02x" %(h+1))

    for a, b in links:
      self.addLink(a, b)

def read_topo():
    nb_hosts = 0
    nb_switches = 0
    links = []
    with open("topo.txt", "r") as f:
        line = f.readline()[:-1]
        w, nb_switches = line.split()
        assert(w == "switches")
        line = f.readline()[:-1]
        w, nb_hosts = line.split()
        assert(w == "hosts")
        for line in f:
            if not f: break
            a, b = line.split()
            links.append( (a, b) )
    return int(nb_hosts), int(nb_switches), links
            

def send_commands(s_id, cmdfile):

  cmd = [args.cli, args.json, str(_THRIFT_BASE_PORT + s_id)]
  with open(cmdfile, "r") as f:
    print " ".join(cmd)
    try:
      output = subprocess.check_output(cmd, stdin = f)
      print output
    except subprocess.CalledProcessError as e:
      print e
      print e.output

def main():

    if args.scenario == 'arp':
      nb_hosts = 24
      nb_switches = 3
      links = []
      div = nb_hosts / nb_switches
      for j in xrange(1, nb_switches + 1):
        for i in xrange(div * (j - 1) + 1, div * j + 1):
          links.append(('h%d'%i, 's%d'%j))

      for j in xrange(1, nb_switches):
        for i in xrange(j + 1, nb_switches + 1):
          links.append(('s%d'%j, 's%d'%i))

      topo = ArpTestTopo(args.behavioral_exe,
                         args.json,
                         nb_hosts, nb_switches, links, args.seed)

    else:
      nb_hosts, nb_switches, links = read_topo()
      topo = MyTopo(args.behavioral_exe,
                    args.json,
                    nb_hosts, nb_switches, links)

    net = Mininet(topo = topo,
                  host = P4Host,
                  switch = P4Switch,
                  controller = None )
    net.start()

    for n in xrange(nb_hosts):
        h = net.get('h%d' % (n + 1))
        for off in ["rx", "tx", "sg"]:
            cmd = "/sbin/ethtool --offload eth0 %s off" % off
            print cmd
            h.cmd(cmd)
        print "disable ipv6"
        h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv4.tcp_congestion_control=reno")
        h.cmd("iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP")
        h.setDefaultRoute("dev eth0")

    sleep(1)

    for i in xrange(nb_switches):
        cmd = [args.cli, args.json,
               str(_THRIFT_BASE_PORT + i)]
        if i < len(args.commands):
          cmdfile = args.commands[i]
        else:
          cmdfile = args.commands[-1]
        with open(cmdfile, "r") as f:
            print " ".join(cmd)
            try:
                output = subprocess.check_output(cmd, stdin = f)
                print output
            except subprocess.CalledProcessError as e:
                print e
                print e.output
        s = net.get('s%d' % (i + 1))
        cmd = "ifconfig | grep -o -E \'s%d\-eth[0-9]*\'" % (i + 1)
        ifaces = (s.cmd(cmd)).split()
        for iface in ifaces:
          print("Disconnecting %s" % iface)
          s.cmd("nmcli dev disconnect iface %s" % iface)

    sleep(1)

    print "Ready !"

    CLI( net )

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
