# HyPer4 Tools

## EvalRun

This tool accepts the run number as a command line parameter and assumes there exist two pcap files named 'run<run #>-<iface>.pcap'.  It associates packets between the two pcap files and measures the latency between each pair.  From this list of latencies, it produces a PDF, CDF, and percentile chart.

### Evaluating P4 Latency

We want to measure the latency of the program itself and do as much as we can to avoid measuring other latencies on the system.  The problem with Wireshark and other packet sniffing software:
  Packet arrives
  |
  NIC issues interrupt
  |
  Host responds to the interrupt
  |
  Packet handed to capture mechanism
  |
  Capture mechanism timestamps the packet
Between each event we have some latency which can vary and throw off what we actually want to measure.  It is not clear to me at what point the P4 program engages, either: before, in parallel with, or after the handoff to the capture mechanism?

The recommendation from Barefoot Networks is to use the INT approach, which consists of a VXLAN-GPE driver written in C doing the timestamping.  It is not clear to me why this approach was recommended.  Antonin Bas: "You may want to look for a P4-way of measuring latency and look into doing some form of inband network telemetry (see http://p4.org/p4/inband-network-telemetry).  IMO, this is the only approach that will remain valid and meaningful for hardware switches."  Well but will I always be able to load the VXLAN-GPE driver on all hardware switches?  Somehow I doubt it.  And P4 itself doesn't have a mechanism for getting timestamps.

Unless the driver approach works for all switches, we are not going to be able to compare software vs hardware.  But we can evaluate alternatives within each domain.



Until we figure that out completely, we are doing mininet simulations with bmv2 and capturing iperf traffic via wireshark.  There is a problem with iperf3 vs iperf when using bmv2.  I'm not sure whether it shows up for all P4 programs, but with parse\_L5\_and\_forward, there is a 20x difference between UDP bandwidth tests for iperf (~70 Mbps before packet loss) and iperf3 (~3.5 Mbps before significant packet loss).  We see that iperf sends packets with 1470 byte payloads, while iperf3 uses packets 8192 bytes in payload size.  There is no option listed in the iperf3 man page to change the payload size.  Note, we see no such discrepancy when using mininet's default OVS switch.  This suggests some buffer for bmv2 is improperly sized, or the effect is produced by a quirk with the P4 program it is running.

Therefore we stick with iperf.
