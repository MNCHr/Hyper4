# HyPer4

## Commands

### Demos

run\_demo\_one.sh: This demo includes three switches in a line
s1 <-> s2 <-> s3, and four hosts, with h1 and h2 both connected to s1, and h3
and h4 both connected to s3.  The demo involves three phases: A, B, and C.
Execution as follows:

1. Invoke the demo:
   ```
   ./run_demo_one.sh
   ```
2. Try h1 ping h2 in the mininet terminal; observe failure.  The switches have
   been loaded with HyPer4 but the tables have not been populated to provide
   HyPer4 any functionality.
3. In a separate terminal (referred to hereafter as "the second terminal"),
   load the switches with configurations for A, B and C:
   ```
   cd [path to repo]/hp4/targets/demo_one
   ./load_s1_s2_s3.sh
   ```
4. Back in the mininet terminal, try pinging between all hosts; observe
   success (though in some cases duplicate packets are sent; this is an
   error we will eventually fix.  In any case, the error disappears once
   we move from phase A to phase B so it is useful for quick evidence
   that invoking the script to change phases actually changes the
   configuration of the switches.)
5. Use xterms and wireshark to observe that the outer switches are acting
   as ARP proxies (TODO: provide details on how to do this).
6. Switch phases from A to B.  In the second terminal:
   ```
   ./swap_to_B_s1_s2_s3.sh
   ```
7. Back in the mininet terminal, try pinging between all hosts; observe
   success.
8. Use xterms and iperf to observe that s2 is acting as a firewall (TODO:
   provide details on how to do this).
9. Switch phases from B to C.  In the second terminal:
   ```
   ./swap_to_C_s1_s2_s3.sh
   ```
10. Back in the mininet terminal, run the source command with a script that
    reconfigures the hosts with different IP addresses and gateways:
   ```
   source targets/demo_one/chg_ips
   ```
11. Verify, via ifconfig, that hosts h1 and h2 are on a different subnet than
    h3 and h4 and can only communicate through a router.  Try pinging between
    all hosts (TODO: fix the bug that currently prevents traffic from routing
    between subnets).  Use xterms and iperf to observe that s2 also employs
    a firewall function.

run\_demo\_two.sh
run\_demo\_three.sh

### Utilities

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

We have converted two P4 programs this way:
- A simple L2 switch program
  - based on dest MAC address, it forwards out a specific port, or does a multicast
- A simple router
  - based on dest IP address, it forwards out a specific port, rewrites the source
    MAC address, decrements the TTL, and recomputes the IPv4 checksum

An IPv4 checksum routine has been implemented directly in HyPer4, but in the future,
general checksums (i.e. using arbitrary portions of the packet for the calculation)
will be possible.

These two programs are used in four demos, all in the /hp4 directory:

1. Run the L2 switch program via HyPer4:  
   ```
   run_l2_switch_demo.sh  
   ```   
   From the mininet prompt, you may verify connectivity between the three hosts.

2. Run the simple router program via HyPer4:
   ```
   run_simple_router_demo.sh
   ```
   From the mininet prompt, you may verify connectivity between h1<->h2, but  
   adding connectivity to/from h3 is left as an exercise.  (This may be  
   difficult to do until I add some information about the HyPer4 table operations  
   required, but the file to edit is in ./targets/simple_router/commands.txt)
   
3. Initialize HyPer4 to contain the L2 switch program as well as an extended  
   version of the same program; swap between the two at will, observing the impact  
   on connectivity: see two_progs_sequential_demo.txt for detailed instructions.

4. Run both the L2 switch program AND the simple router program simultaneously,  
   each taking action on a different set of packets (separated by ingress port):
   ```
   run_two_progs_demo.sh
   ```
   From the mininet prompt, you may verify connectivity between h1, h2, and h3  
   (these are using the L2 switch program), and between h4 and h5 (these are  
   using the simple router program).  h6 is grouped with h4 and h5 but, just  
   as in demo #2, we have not supplied the table entries required to establish  
   connectivity to/from h6.  You are welcome to give it a try; edit  
   ./targets/two_progs_parallel.

There is much work to be done (templatizing HyPer4, making a "compiler" as well
as a control plane translator, expanding the coverage of HyPer4 over more
primitives, table match types, etc.).  But hopefully, these demos provide an idea
of what HyPer4 might be capable of some day.
