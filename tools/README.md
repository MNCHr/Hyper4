# HyPer4 Tools

## EvalRun

This tool accepts the run number as a command line parameter and assumes there exist two pcap files named 'run<run #>-<iface>.pcap'.  It associates packets between the two pcap files and measures the latency between each pair.  From this list of latencies, it produces a PDF, CDF, and percentile chart.

### Evaluating P4 Latency

The recommendation from Barefoot Networks is to use the INT approach.  It should apply to software and hardware P4 devices alike.

Until we figure that out completely, we are doing mininet simulations with bmv2 and capturing iperf traffic via wireshark.  There is a problem with iperf3 vs iperf when using bmv2.  I'm not sure whether it shows up for all P4 programs, but with parse\_L5\_and\_forward, there is a 20x difference between UDP bandwidth tests for iperf (~70 Mbps before packet loss) and iperf3 (~3.5 Mbps before significant packet loss).  We see that iperf sends packets with 1470 byte payloads, while iperf3 uses packets 8192 bytes in payload size.  There is no option listed in the iperf3 man page to change the payload size.  Note, we see no such discrepancy when using mininet's default OVS switch.  This suggests some buffer for bmv2 is improperly sized, or the effect is produced by a quirk with the P4 program it is running.

Therefore we stick with iperf.
