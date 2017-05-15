# DPMU Implementation

Checkpoint: translate method
- I have recognized that when a source table matches on a standard_metadata
  field, there are two HP4\_Match\_Commands: tX\_stdmeta\_exact and
  tX\_stdmeta\_[field name].
- Need to pause DPMU implementation to review HP4 implementation: is there
  any benefit to separating the match into two tables?  If not, we can
  consolidate into one table in HP4, and simplify our effort in the DPMU.
  - IMPACT OF TWO TABLES:
    - Shortens the control functions match\_X
    - But incurs additional control functions switch\_stdmeta\_X
    - X additional tables tX\_stdmeta\_exact
    - Makes expansion of match type on standard metadata fields easier
  - Alternatives: consider latency, memory, ease of expansion
    - Remove intermediary tX\_stdmeta\_exact tables
    - Could copy all standard_metadata fields into one consolidated
      metadata field and do ternary match on that field just like we
      currently do for extracted (parsed representation) and metadata

A: Current
B: Remove tX\_stdmeta\_exact, add conditionals to match\_X
C: Copy stdmetadata fields into 1 metadata field, ternary match

latency:
For programs that use standard_metadata matching:
A: ~Y conds + ~Z conds + 1 table + 1 inst-action
B: ~Y conds + ~Z conds
C: ~Y conds + 1 table + Z inst-action
For programs that don't:
A: ~Y conds
B: ~Y conds (if all conds for non-stdmetadata match tables put first)
C: ~Y conds + 1 table (checking whether stdmetadata matching needed)

B wins

memory:
A: 1 control w/ Y conds + 1 control w/ Z conds + 1 table (1 entry / program ID) + 1 action + Z tables (1 entry / source entry)
B: 1 control w/ (Y + Z) conds + Z tables (1 entry / source entry)
C: 1 control w/ Y conds + 1 table (1 entry / source entry)

Close between B and C because each entry in C's table represents Z fields where B has Z tables, each representing 1 field.  C would appear to have the edge because of smaller control functions, but surely control functions are cheap in terms of memory.

ease of expansion:
A and B are both fairly simple, C is not.

B is best.

New!  See updated design at https://docs.google.com/presentation/d/1bntdi8gA0NhIPVTYo4pToTX5qwH_-jacIJEFcstEw00/edit?usp=sharing

First Iteration: Single User, no resource tracking, only instance tracking.
- [ ] redesign to support flowspaces, not just phys ingress port, for setting
      context for program ID
- [X] server: handle shutdown gracefully (release socket)
- [ ] client: ./dpmu client load source.p4 --instance `<instance-name>` [phys-ports]
  - [X] server handle compiling
  - [X] server handle loading prep (hp4l)
  - [X] server track vport:instance map
  - [X] server track instance attributes: prog ID, source, vports
  - [ ] Enforce phys-port:instance assignment
  - [X] server handle loading via sswitch_CLI
  - [X] server return success/fail to client
- [X] handle client populate ... step 1: check validity of instance
- [ ] handle client populate ... step 2: translate transaction
- [ ] handle client populate ... step 3: add table entries to running instance of HP4
- [ ] handle client populate ... step 4: return success/fail

./dpmu client populate `<instance name>` --port 33333 --command 'table_add dmac forward 00:AA:BB:00:00:01 => 1'

Second Iteration
- [ ] clarify port management
- [ ] Load userfile: track users, entry limits, and port assignments
- [ ] server: with each load and populate command received, track resource usage
- [ ] ./dpmu client user `<username>` returns resource status: total & per instance

# DPMU Design

Given:
- hp4t\_l2\_switch.p4
- a bmv2-style CLI command: table\_add dmac forward [MAC of h2] => [port of h1]

Need to produce entries for:
- t1\_extracted\_exact
- t\_mod\_11

We can use 'dmac' and 'forward' to form a key to look up relevant template entries.  We should expect a match table template, and potentially a number of primitive table templates.  The range of the number of primitive table templates has a minimum of 0, and a maximum equal to the number of primitives in the source action.

We have to associate the source action parameters with their primitives.  We perform the mapping in the compiler: {primitive: ordinal number of source action parameter}.  Then we include the ordinal number of the source action parameter in the template entry.  This is called src\_aparam\_id.

In p4c-hp4.py, focus on gen\_action\_entries and gen\_action\_aparams.  Basically in the p4\_call we can look at p4\_call[1][1] and if it is 'sig(n)' then the type will be p4\_hlir.hlir.p4\_imperatives.p4\_signature\_ref and it will have an idx attribute, which is the ordinal number of the source action parameter.

We add a new subclass of HP4\_Command called HP4\_Primitive\_Command, joining the other subclass, HP4\_Match\_Command.

## DPMU as a server

DPMU should be implemented as a server running in the background.

Basic client/server network programming in python: www.bogotobogo.com/python/python\_network\_programming\_server\_client.php.

Pattern of communication:
  0. Admin loads P4 device with HP4 and starts DPMU server
     ./dpmu server --port 33333 --hp4-port 22222 --entries 1000 --phys-ports 4 --users userfile 2>&1 &
   - userfile format:
     username max\_table\_entries phys-port1 ... phys-portN
     ...
     If no userfile supplied, single user named 'default' created, with all --entries and --phys-ports

  1. (user) send a request for resource status
     ./dpmu client user `<username>`
  2. (dpmu) return resource set associated w/ `<username>`:
   - total table entry space
   - physical port assignment
     Provide update on current set of instances, current table space usage
     (total and per instance), and current port assignments (per instance).

  3. (user) send request for loading, triggering port assignments
     ./dpmu client load source.p4 --user `<username>` --instance `<instance-name>` [phys-ports]
     TODO: Get clarity on what if we want multiple instances now or later, and how to do fine-grained function assignment properly.  Remember we can do direct interaction w/ HP4 via CLI if we have to and it isn't essential for paper objectives.

  4. (dpmu) Compile source.p4 --p4c-hp4--> source.hp4t + source.hp4mt
  5. (dpmu) Prepare for loading: source.hp4t --hp4l--> `<instance name>`.hp4
   - Create program ID per instance and maintain map `<instance name>: [program ID]`
   - Maintain instance -> program map `<instance name>`: `<source name>` where source name
     can be appended with .hp4mt to yield the hp4 match template file name or .hp4t to
     yield the file supplied to the loader to produce the .hp4
   - Maintain virtual ports map `<instance name: [vport1, vport2, vport3, vport4]>`
     where vportX is automatically determined by DPMU
  6. (dpmu) Load HP4 with `<instance name>`.hp4
   - `<path to sswitch_CLI> <port of P4 device> < <instance name>.hp4`
  7. (dpmu) return success/fail for each requested instance

  8. (user) send table transaction formatted for source.p4, designated for a certain instance
     ./dpmu client populate `<instance name>` --port 33333 --command 'table_add dmac forward 00:AA:BB:00:00:01 => 1'
     ./dpmu client populate `<instance name>` --port 33333 --file `<path to file with commands>`
  9. (dpmu) check validity of instance, translate transaction, return success/fail

## t1\_extracted\_exact

When translating a population request, the task is to replace all bracketed fields in the template with actual values. The following identifies where the values come from for each such template field:
- [program ID]: DPMU creates and tracks program ID for each requested instance
- [val]: UE1 match parameter, [MAC of h2]
- [match ID]: DPMU state initialized upon receiving request for new instance, updated with every user entry passed through the DPMU
- [DONE]: definitions file shared with hp4l
- [MODIFY_FIELD]: definitions file shared with hp4l

## t\_mod\_11

- [program ID]: DPMU state initialized at startup via commandline arguments
- [match ID]: DPMU state initialized at startup, updated with every user entry passed through the DPMU
- [val]: UE1 action parameter, [port of h1]

## Connecting to bmv2 CLI

Ref: p4lang/behavioral-model/tools/runtime_CLI.py

import bmpy\_utils as utils
import runtime\_CLI

standard\_client, mc\_client = thrift\_connect(args.thrift\_ip, args.thrift\_port, runtime\_CLI.RuntimeAPI.get\_thrift\_services(args.pre))
json = '../hp4/hp4.json'
runtime\_CLI.load\_json\_config(standard\_client, json)
rta = runtime\_CLI.RuntimeAPI('SimplePre', standard\_client)
rta.do\_table\_add(`<table name> <action name> <match fields> => <action parameters [priority]`)

Other useful commands:
- table = runtime\_CLI.TABLES`[<table name>]`
- rta.do\_table\_dump(`<table name>`)
- entry = standard\_client.bm\_mt\_get\_entries(0, `<table name>`)`[<idx>]`

## port management

The issues:
- properly setting the program ID when the physical port is used for this purpose
- translating use of physical ports in the source program
  - source program matches on physical port
    - standard\_metadata.ingress\_port
    - standard\_metadata.egress\_spec
  - source program uses physical port as source in modify_field primitive
  - source program uses physical port as dest in modify_field primitive

### properly setting the program ID
The loader, hp4l, expects, as a command line argument, a list of physical ports to which the virtual program applies.

When a client first connects to the DPMU server, he should receive a list of physical resources (number of virtual programs he is allowed and total table space usable by all virtual programs, list of physical ports, and list of virtual ports) associated with some kind of cryptographic token.  In later transactions, he presents the token to authenticate any requests to use those resources.

We previously considered SSL to secure transactions between the client and the server, and decided the actual use of SSL was not necessary for this research system because it adds nothing of research value.  Similarly, we can decide that actual cryptographic authentication is not necessary for resource management.

Nevertheless, we do have a basic requirement to support user management.  This adds an argument to the client mode at a minimum and a {username: resource_set} dictionary to track for the server.

In any case, the compiler generates a template entry:
- table\_add tset\_context a\_set\_context [PPORT] => [program ID]
The load prep hp4l takes this and generates one entry for every port in args.phys\_ports.

This requirement is currently implemented.

### translating use of physical ports in the source program

Source program matches on physical port: this is handled in p4c-hp4 in gen\_tX\_templates.  A template entry is created with [STDMETA\_INGRESS\_PORT] as the read field.  hp4l converts this to '1', matching the code in defines.p4 for meta\_ctrl.stdmeta\_ID.

## client user `<username>`

./dpmu client user `<username>`

Provide status of resource allocation.  Resources must be allocated when the server is invoked.
