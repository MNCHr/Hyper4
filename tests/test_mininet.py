#!/usr/bin/python

#
# David Hancock
# Flux Research Group
# University of Utah

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

import argparse
from time import sleep
import os
import subprocess

import unittest

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))
_THRIFT_BASE_PORT = 22222

class TestTopo(Topo):
  def __init__(self, **opts):
    self.json = opts.pop('json')
    super(TestTopo, self).__init__(**opts)
    links = [ ('h1', 's1'),
              ('h2', 's1'),
              ('h3', 's1')]
    behavioral = os.environ['BMV2_PATH'].rstrip() + \
                                     '/targets/simple_switch/simple_switch'
    switch = self.addSwitch('s1', sw_path = behavioral,
                            json_path = self.json,
                            thrift_port = _THRIFT_BASE_PORT,
                            pcap_dump = False,
                            device_id = 0)
    for h in xrange(3):
      host = self.addHost('h%d' % (h + 1),
                          ip = '10.0.0.%d/24' % (h+1),
                          mac = '00:04:00:00:00:%02x' %h)

    for a, b in links:
      self.addLink(a, b)

# https://stackoverflow.com/questions/11380413/python-unittest-passing-arguments/20702984
class TestLoaderWithKwargs(unittest.TestLoader):
    """A test loader which allows to parse keyword arguments to the
       test case class."""
    def loadTestsFromTestCase(self, testCaseClass, **kwargs):
        """Return a suite of all tests cases contained in 
           testCaseClass."""
        if issubclass(testCaseClass, unittest.suite.TestSuite):
            raise TypeError("Test cases should not be derived from "\
                            "TestSuite. Maybe you meant to derive from"\
                            " TestCase?")
        testCaseNames = self.getTestCaseNames(testCaseClass)
        if not testCaseNames and hasattr(testCaseClass, 'runTest'):
            testCaseNames = ['runTest']

        # Modification here: parse keyword arguments to testCaseClass.
        test_cases = []
        for test_case_name in testCaseNames:
            test_cases.append(testCaseClass(test_case_name, **kwargs))
        loaded_suite = self.suiteClass(test_cases)

        return loaded_suite 

class TestPings(unittest.TestCase):

    def __init__(self, *args, **kwargs):
      self.net = kwargs.pop('mn')
      super(TestPings, self).__init__(*args, **kwargs)

    @staticmethod
    def get_loss(ping_res):
      _TRANSMITTED = 0
      _RECEIVED = 1
      _LOSS = 2
      _TIME = 3
      res_lines = ping_res.split('\n')
      for line in res_lines:
        if 'packet loss' in line:
          return line.split(', ')[_LOSS]
      return 'error; packet loss not found'

    def test_good_ping(self):
        h1 = self.net.get('h1')
        res = h1.cmd("ping 10.0.0.2 -c 1 -W 1")
        print('good_ping: ' + res)
        ans = self.get_loss(res)
        self.assertEqual(ans, '0% packet loss')

    def test_bad_ping(self):
      h1 = self.net.get('h1')
      res = h1.cmd("ping 10.0.0.3 -c 1 -W 1")
      print('bad_ping: ' + res)
      ans = self.get_loss(res)
      self.assertEqual(ans, '100% packet loss')

def mn_start(project):
  jsonpath = project + '.json'
  cmdfile = project + '.commands'
  topo = TestTopo(json=jsonpath)
  net = Mininet(topo = topo,
                host = P4Host,
                switch = P4Switch,
                controller = None)
  net.start()

  for n in xrange(3):
      h = net.get('h%d' % (n + 1))
      for off in ["rx", "tx", "sg"]:
          cmd = "/sbin/ethtool --offload eth0 %s off" % off
          print cmd
          h.cmd(cmd)
      h.cmd("sysctl -w net.ipv4.tcp_congestion_control=reno")
      h.cmd("iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP")
      h.setDefaultRoute("dev eth0")

  cli = os.environ['BMV2_PATH'].rstrip() + '/targets/simple_switch/sswitch_CLI'
  cmd = [cli, jsonpath, str(_THRIFT_BASE_PORT)]
  if os.path.isfile(cmdfile):
    with open(cmdfile, "r") as f:
      print " ".join(cmd)
      try:
        output = subprocess.check_output(cmd, stdin = f)
        print output
      except subprocess.CalledProcessError as e:
        print e
        print e.output
  else:
    print(cmdfile + " not found")

  sleep(1)
  print("ready!")

  return net

def main(project='test_hub'):
    net = mn_start(project)
    loader = TestLoaderWithKwargs()
    suite = loader.loadTestsFromTestCase(TestPings, mn=net)
    unittest.TextTestRunner(verbosity=2).run(suite)
    net.stop()

if __name__ == '__main__':
  command = ['bash', '-c', 'set -a && source ../env.sh && env']
  proc = subprocess.Popen(command, stdout = subprocess.PIPE)
  for line in proc.stdout:
    (key, _, value) = line.partition("=")
    os.environ[key] = value
  proc.communicate()

  import sys
  sys.path.append(os.environ['BMV2_PATH'].rstrip() + '/mininet/')
  from p4_mininet import P4Switch, P4Host

  main()
