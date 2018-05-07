#!/usr/bin/python

# Run all tests
#
# David Hancock
# Flux Research Group
# University of Utah

import os
import subprocess
import importlib

def source_env():
  command = ['bash', '-c', 'set -a && source ../env.sh && env']
  proc = subprocess.Popen(command, stdout = subprocess.PIPE)
  for line in proc.stdout:
    (key, _, value) = line.partition("=")
    os.environ[key] = value
  proc.communicate()

def compile_p4_files():
  tests = []
  files = []
  for f in filter(os.path.isfile, os.listdir( os.curdir ) ):
    if f.endswith(".p4") and f.startswith("test"):
      files.append(f)

  for f in files:
    f_name = f.split('.p4')[0]
    command = ['bash', '-c', '%s/p4c_bm/__main__.py %s --json %s.json' %
                              (os.environ['P4C_BM_PATH'].rstrip(), f, f_name)]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = proc.communicate()
    success = True
    for line in output:
      if 'error' in line:
        success = False
        print(output)
      break
    if success:
      tests.append(f_name)
  return tests

def main():
  source_env()
  tests = compile_p4_files()
  for test in tests:
    testlib = None
    if os.path.isfile(test+'.py'):
      testlib = importlib.import_module(test)
    else:
      testlib = importlib.import_module("test_mininet")
    testlib.main()

if __name__ == '__main__':
  main()
