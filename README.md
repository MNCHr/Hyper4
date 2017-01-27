# HyPer4

Some basic HyPer4 background is provided here, but refer to the
[CoNEXT 2016 paper](http://dl.acm.org/citation.cfm?id=2999607) for more
details.

This README also includes step-by-step instructions for running two demos
described in the paper illustrating the interesting properties of virtualized
programmable data planes.

## Background

HyPer4 is a P4 program that acts as a hypervisor, in that it is capable of
emulating other (simple) P4 programs.

Conceptually, we think of P4 programs as having *structure* -- the .P4
source -- and *state* -- the runtime-supplied table entries and default
actions that may govern flow of execution within the framework provided by the
structure.

HyPer4 aims to provide a generalized structure to allow arbitrary packet processing
activities, as directed by state, where a collection of such activities can represent
entire P4 programs.  Thus .p4 source is converted ("compiled") into table operations
consumable by HyPer4.

We have converted four P4 programs this way:
- A simple L2 switch program
  - based on dest MAC address, it forwards out a specific port, or does a multicast
- A simple router
  - based on dest IP address, it forwards out a specific port, rewrites the source
    MAC address, decrements the TTL, and recomputes the IPv4 checksum
- An ARP proxy
  - responds to ARP requests on behalf of the target of the request
- A firewall
  - blocks specified TCP or UDP source or destination ports

These four programs are used in two demos, all in the /hp4 directory.

## Commands

### Demos

run\_demo\_one.sh: This demo includes three switches in a line
s1 <-> s2 <-> s3, and four hosts, with h1 and h2 both connected to s1, and h3
and h4 both connected to s3.  The demo involves three phases: A, B, and C.

Phase A:
* s1: arp proxy
* s2: l2 switch
* s3: arp proxy
Phase B:
* s1: l2 switch
* s2: firewall
* s3: l2 switch
Phase C:
* s1: l2 switch
* s2: arp proxy -> firewall -> router
* s3: l2 switch

Conceptually, when you execute this demo, the switches are first loaded with
HyPer4.  But each instance of HyPer4 does not perform a function until its
tables are populated.  You then run a script to populate the tables such
that each instance virtually contains all of the functions necessary for
each phase, with the function for Phase A left active.  You run some tests
to verify expected behavior and switch to the next phase, repeating this
process until phase C has been evaluated.

Execution as follows:

1. Invoke the demo:
   ```
   cd [path to repo]/hp4
   ./run\_demo\_one.sh
   ```
2. Try h1 ping h2 in the mininet terminal; observe failure.  The switches have
   been loaded with HyPer4 but the tables have not been populated to provide
   HyPer4 any functionality.
3. In a separate terminal (referred to hereafter as "the second terminal"),
   load the switches with configurations for A, B and C.  It is also
   recommended to disable the sources of non-relevant IPv6 traffic by
   running the iface\_down script at this time:
   ```
   cd [path to repo]/hp4/targets/demo\_one
   ./iface\_down.sh
   ./load\_s1\_s2\_s3.sh
   ```
4. Back in the mininet terminal, try pinging between all hosts; observe
   success (though in some cases duplicate packets are sent; this is an
   error.  It should be fixed, but in any case, the error disappears once
   we move from phase A to phase B, so it is useful for quick evidence
   that invoking the script to change phases actually changes the
   configuration of the switches.)
5. Use xterms and wireshark to observe that the outer switches are acting
   as ARP proxies:
   ```
   xterm s2
   ```
   The node for which we spawn the xterm is s2 here, but it actually doesn't
   matter as long as it is s1, s2, or s3.  From the xterm:
   ```
   wireshark
   ```
   Select interfaces to monitor.  To show that the ARP proxy is working, we
   might plan to send a ping from h1 to h3 after flushing the arp cache
   (```h1 ip -s -s neigh flush all```) and see whether the ARP traffic is
   ever carried on the s2-facing interface in s1, and for good measure
   whether the ARP traffic ever appears on the s1-facing interface in s2.
   In this case select s1-eth1, s1-eth3, and s2-eth1 and start sniffing.
   Then, in the mininet terminal:
   ```
   h1 ping h3 -c 1 -W 1
   ```
   Observe in wireshark that the ARP traffic initiated by h1 appears on
   s1-eth1 and is sent back out s1-eth1 and never appears on s1-eth3 or
   s2-eth1.
6. Switch phases from A to B.  In the second terminal:
   ```
   ./swap\_to\_B\_s1\_s2\_s3.sh
   ```
7. Back in the mininet terminal, try pinging between all hosts; observe
   success.
8. Use xterms and iperf to observe that s2 is acting as a firewall:
   ```
   xterm h1
   xterm h3
   ```
   In xterm for h3, start a server:
   ```
   iperf -s
   ```
   The default is a TCP server on port 5001.  The firewall in s2 blocks
   TCP traffic with a source port of 4000, and UDP traffic with
   a destination port of 5000.  So TCP traffic sent to h3 from h1 now
   should work.  In the xterm for h1, give it a try:
   ```
   iperf -c 10.0.0.3
   ```
   Now stop the server on h3 (CTRL-C) and try the configurations that
   are blocked.  Both commands shown together (for xterm for h3):
   ```
   iperf -s -p 4000
   iperf -s -p 5000 -u
   ```
   The corresponding commands for h1:
   ```
   iperf -c 10.0.0.3 -p 4000
   iperf -c 10.0.0.3 -p 5000 -u
   ```
   Of course, you can try any combination of server / client so long
   as either h1 or h2 plays one of the roles while h3 or h4 plays the
   other role.  But feel free to try iperf between h1 and h2, and
   between h3 and h4, to see that traffic is not blocked because the
   firewall is at s2, not s1 or s3.
9. Switch phases from B to C.  In the second terminal:
   ```
   ./swap\_to\_C\_s1\_s2\_s3.sh
   ```
10. Back in the mininet terminal, run the source command with a script that
    reconfigures the hosts with different IP addresses and gateways:
   ```
   source targets/demo\_one/chg\_ips
   ```
11. Verify, via ifconfig, that hosts h1 and h2 are on a different subnet than
    h3 and h4 and can only communicate through a router.  Try pinging between
    all hosts.  Use xterms and iperf as in step 8 to observe that s2 also
    employs a firewall function.  Use xterms and wireshark on interfaces
    s2-eth1, s2-eth2, and s3-eth1 as in step 5 to see that s2 also employs
    an ARP proxy function.

run\_demo\_two.sh: This demo includes one switch s1, and four hosts h1, h2,
h3, and h4 connected to it.  The switch runs HyPer4 and is initially devoid
of function.  When the load.sh script is run, the switch adopts a simple
l2 switch behavior for hosts h1 and h2, and a firewall -> router composite
behavior for hosts h3 and h4.

Execution as follows:

1. Invoke the demo:
   ```
   cd [path to repo]/hp4
   ./run\_demo\_two.sh
   ```
2. Try pinging between any two hosts in the mininet terminal; observe failure.
   The switches have been loaded with HyPer4 but the tables have not been
   populated to provide HyPer4 any functionality.
3. In a separate terminal (referred to hereafter as "the second terminal"),
   load the switch with configurations for the h1, h2 side and for the h3,
   h4 side.  It is also recommended to disable the sources of non-relevant
   IPv6 traffic by running the iface\_down script at this time:
   ```
   cd [path to repo]/hp4/targets/demo\_two
   ./iface\_down.sh
   ./load.sh
   ```
4. Back in the mininet terminal, change the network configuration for h3
   and h4 using a provided script as follows:
   ```
   source targets/demo\_two/chg_ips
   ```
   Ping between h1 and h2, and between h3 and h4 and observe success. You
   may also try pinging between h1 or h2 and h3 or h4 to observe failure
   as there is no bridge between the two sides.  The switch has been sliced
   according to physical ingress ports.
5. Use xterm and iperf to verify the firewall functions for traffic passing
   between h3 and h4.  Follow the pattern shown in step 8 of the instructions
   for demo one, but use xterms for h3 and h4, and use the correct IP address
   depending on which host is selected to act as the server:
   * h3: 10.0.1.3
   * h4: 10.0.2.4

### Utilities

#### run_nano.sh

This runs a modified version of Barefoot Networks' nano message
client, which connects to bmv2's nano service and outputs events (packet
ingress events, table matches, actions, et cetera).  Some of the demos
employ multiple switches, so by adding the appropriate integer as a command
line argument, we can specify which switch to connect to:
```
./run\_nano.sh [switch ID]
```
where switch ID corresponds to the integer to the right of the 's' in the
name used in mininet (e.g., 1 for s1).
Typical usage involves redirecting stdout to a file:
```
./run\_nano.sh [switch ID] > nano\_out.txt
```
We then fire a packet in mininet (e.g., h1 ping h2 -c 1 -W 1), return to the
terminal running nano, and CTRL-C to stop it.  At this point we can open
the text file for analysis.

It is recommend that you invoke the iface_down.sh script first (see below)
to minimize the possibility of non-relevant traffic cluttering up the
output.  As an additional measure, it is recommended that from the mininet
terminal, you start an xterm for the node of interest and run wireshark,
so that you can see what packets have been received that correspond to
the events collected by the nano message client.

#### cleanup.sh

This script kills all running bmv2 processes and cleans up corrupt mininet
and bmv2 state.  This fixes incorrect behaviors that sometimes occur after
mininet was not shut down cleanly (the usual but not exclusive cause of
such behaviors).

#### iface_down.sh

This script "disconnects" interfaces to mute IPv6 traffic, though connectivity
in mininet remains intact.  This script helps nano- and wireshark-based
analysis by eliminating traffic that is not relevant to the HyPer4 scenario.
