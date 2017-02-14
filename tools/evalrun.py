#!/usr/bin/python

# Takes two pcap files, extracts timestamps, and calculates and plots the
# histogram and CDF of the differences between timestamps
#
# Assumption is that file 1 includes timestamps of packets received on the inbound
# switch interface; file 2 includes timestamps of the corresponding packets sent
# out the outbound switch interface.
#
# DAVID HANCOCK
# University of Utah

import sys
import os
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt

# get run#
if len(sys.argv) < 2:
  print("usage: %s <run #>\n" % sys.argv[0])
  exit()

# construct filenames (1 for eth1, 1 for eth2)
filestart1 = "run" + sys.argv[1] + "-eth1"
filestart2 = "run" + sys.argv[1] + "-eth2"

file1pcap = filestart1 + ".pcap"
file2pcap = filestart2 + ".pcap"
file1txt = filestart1 + ".txt"
file2txt = filestart2 + ".txt"

# use tcpdump -r to convert .pcap files to .txt
execstr1 = "tcpdump -r " + file1pcap + " > " + file1txt
execstr2 = "tcpdump -r " + file2pcap + " > " + file2txt
os.system(execstr1)
os.system(execstr2)

times1 = []
times2 = []
diffs = []

# process the two files
with open(file1txt, 'r') as f1:
  for line in f1:
    # store the time in an array
    t = datetime.datetime.strptime( line.split()[0], "%H:%M:%S.%f" )
    times1.append( time.mktime(t.timetuple()) + (t.microsecond / 1000000.0) )
    
with open(file2txt, 'r') as f2:
  for line in f2:
    # store the time in an array
    t = datetime.datetime.strptime( line.split()[0], "%H:%M:%S.%f" )
    times2.append( time.mktime(t.timetuple()) + (t.microsecond / 1000000.0) )

# - calculate difference between corresponding timestamps
for t1, t2 in zip(times1, times2):
  diffs.append( abs(round( (t2 - t1) * 1000, 3)) )

arr = np.array(diffs)

density, bins = np.histogram(arr, density=True)
unity_density = density / density.sum()
pbins = np.arange(0, 104, 4)
#pbins = np.array([0, 25, 50, 90, 100])
pindices = np.arange(len(pbins))
percentile = np.zeros(len(pbins))
for i in range(len(pbins)):
  percentile[i] = np.percentile(arr, pbins[i])

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, sharex=False, figsize=(12,4))
widths = bins[:-1] - bins[1:]
ax1.bar(bins[1:], unity_density, width=widths)
ax2.bar(bins[1:], unity_density.cumsum(), width = widths)
#ax3.plot(pindices, percentile)
ax3.plot(pbins, percentile)
#ax3.xaxis.set_ticks(pindices)
#ax3.xaxis.set_ticklabels(pbins)
ax1.set_xlabel('PDF')
ax2.set_xlabel('CDF')
ax3.set_xlabel('Percentiles')
fig.tight_layout()
plt.show()
