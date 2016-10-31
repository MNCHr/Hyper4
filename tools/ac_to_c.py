#!/usr/bin/python

import argparse
import re

parser = argparse.ArgumentParser(description='HP4 Annotated Commands Converter')
parser.add_argument('--input', help='Annotated hp4 commands file',
                    type=str, action="store", required=True)
parser.add_argument('--output', help='Where to write hp4-ready commands file',
                    type=str, action="store", required=True)
parser.add_argument('--progID', help='Program ID',
                    type=str, action="store", default='1')
parser.add_argument('--phys_ports', help='Physical ports for which program applies',
                    type=str, nargs='*', action="store", default=['1'])
parser.add_argument('--virt_ports', help='Numbers to assign to virtual ports 0-3',
                    type=str, nargs='*', action="store", default=['65', '66', '67', '68'])

args = parser.parse_args()

f_ac = open(args.input, 'r')
f_c = open(args.output, 'w')

sr = {}

# TODO: read defines.p4 directly
sr['[program ID]'] = args.progID
sr['[VIRT_PORT_0]'] = args.virt_ports[0]
sr['[VIRT_PORT_1]'] = args.virt_ports[1]
sr['[VIRT_PORT_2]'] = args.virt_ports[2]
sr['[VIRT_PORT_3]'] = args.virt_ports[3]
sr['[PROCEED]'] = '0'
sr['[INSPECT_SEB]'] = '1'
sr['[INSPECT_20_29]'] = '2'
sr['[INSPECT_30_39]'] = '3'
sr['[INSPECT_40_49]'] = '4'
sr['[INSPECT_50_59]'] = '5'
sr['[INSPECT_60_69]'] = '6'
sr['[INSPECT_70_79]'] = '7'
sr['[INSPECT_80_89]'] = '8'
sr['[INSPECT_90_99]'] = '9'
sr['[EXTRACT_MORE]'] ='10'
sr['[DONE]'] = '0'
sr['[EXTRACTED_EXACT]'] = '1'
sr['[METADATA_EXACT]'] = '2'
sr['[STDMETA_EXACT]'] = '3'
sr['[EXTRACTED_VALID]'] = '4'
sr['[COMPLETE]'] = '1'
sr['[CONTINUE]'] = '2'
sr['[STDMETA_INGRESS_PORT]'] = '1'
sr['[MODIFY_FIELD]'] = '0'
sr['[DROP]'] = '6'
sr['[NO_OP]'] = '7'
sr['[MULTICAST]'] = '19'
sr['[MATH_ON_FIELD]'] = '20'
sr['[STDMETA_INGRESS_PORT]'] = '1'
sr['[STDMETA_PACKET_LENGTH]'] = '2'
sr['[STDMETA_INSTANCE_TYPE]'] = '3'
sr['[STDMETA_PARSERSTAT]'] = '4'
sr['[STDMETA_PARSERERROR]'] = '5'
sr['[STDMETA_EGRESS_SPEC]'] = '6'

found_sr = False

for line in f_ac:
  if line == '# SEARCH AND REPLACE\n':
    found_sr = True
    break

if(found_sr):
  line = f_ac.next()
  while line != '\n':
    linetoks = line.split()
    sr[linetoks[1]] = linetoks[3]
    line = f_ac.next()

f_ac.seek(0)

# WARNING this is not meant to be used as is... borrowed from p4t
def handle_loop(startmarker):
  body = []
  x = len(args.context)
  conditionalbreak = "\n"
  directive_a = startmarker.split("+")[1].strip().upper().split()

  while :
    line = self.lines[self.nextline]
    self.nextline += 1
    if line.strip().startswith("[+"):
      directive = line.split("+")[1].strip().upper()
      if directive == "ENDLOOP":
        break
      elif self.nextline == len(self.lines):
        print("Error: missing ENDLOOP directive")
        exit()
    body.append(line)
    
  linebreak = ""
  for i in range(1, x + 1):
    self.out += linebreak
    linebreak = conditionalbreak
    for line in body:
      line = line.replace("[+X+]", str(i))
      line = line.replace("[+ X +]", str(i))
      self.out += line

for line in f_ac:
  # strip out comments and white space
  if line[0] == '#' or line[0] == '\n':
    continue
  i = line.find('#')
  if i != -1:
    line = line[0:i]
    while line.endswith(' '):
      line = line[0:-1]
    line += '\n'

  for key in sr.keys():
    line = line.replace(key, sr[key])
  for token in re.findall("\[.*?\]", line):
    replace = ""
    if re.search("\[[0-9]*x00s\]", token):
      numzeros = int(re.search("[0-9]+", token).group())
      for i in range(numzeros):
        replace += "00"   
      line = line.replace(token, replace)
  # Another pass for PPORT, VPORT, other markers producing multiple lines:
  lines = []
  # TODO: 
  # 1. add line to lines[]
  # 2. while done == FALSE:
  #      done = TRUE
  #      for every line in lines[]:
  #        look for marker ([PPORT] | [VPORT]); if found:
  #          replace line with multiple lines, where each new line has the marker
  #           substituted for one of the values in the corresponding args object
  #          done = FALSE
  for token in re.findall("\[.*?\]", line):
    if re.search("\[[pP][pP][oO][rR][tT]\]", token):

      for i in range(len(args.phys_ports)):
        lines.add( line.replace( token, str(args.phys_ports[i]) ) )
    elif re.search("\[[vV][pP][oO][rR][tT]\]", token):

      
    else:
      print("Unrecognized token: %s" % token)
      exit()
  f_c.write(line)

f_c.close()
f_ac.close()
