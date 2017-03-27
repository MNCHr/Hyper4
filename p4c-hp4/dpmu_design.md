# DPMU Design

Given:
- hp4t\_l2\_switch.p4
- UE1 table\_add dmac forward [MAC of h2] => [port of h1]

Need to produce entries for:
- t1\_extracted\_exact
- t\_mod\_11

We can use 'dmac' and 'forward' to form a key to look up relevant template entries.  We should expect a match table template, and potentially a number of primitive table templates.  The range of the number of primitive table templates has a minimum of 0, and a maximum equal to the number of primitives in the source action.

We have to associate the source action parameters with their primitives.  We perform the mapping in the compiler: {primitive: ordinal number of source action parameter}.  Then we include the ordinal number of the source action parameter in the template entry.  This is called src\_aparam\_id.

In p4c-hp4.py, focus on gen\_action\_entries and gen\_action\_aparams.  Basically in the p4\_call we can look at p4\_call[1][1] and if it is 'sig(n)' then the type will be p4\_hlir.hlir.p4\_imperatives.p4\_signature\_ref and it will have an idx attribute, which is the ordinal number of the source action parameter.

We add a new subclass of HP4\_Command called HP4\_Primitive\_Command, joining the other subclass, HP4\_Match\_Command.

## DPMU as a server

It has become clear that the DPMU should be implemented as a server running in the background, especially because this is easier than initially thought.

Basic client/server network programming in python is found at www.bogotobogo.com/python/python\_network\_programming\_server\_client.php.  There are only a handful of key lines to worry about.

Pattern of communication:
  0. Admin loads P4 device with HP4 and starts DPMU server
     ./dpmu --server --port 33333 --hp4-port 22222 &
     
  1. (user) send request for service, include source.p4, instance name(s)
     ./dpmu --client --port 33333 --load source.p4
     With no instance name(s) supplied, the default is to create a single instance with the same name as the source P4 program, without the .p4 extension.
     ./dpmu --client --port 33333 --load source.p4 --instance-list "src1 src2 src3"

  2. (dpmu) Compile source.p4 --p4c-hp4--> source.hp4t + source.hp4mt
  3. (dpmu) Prepare for loading: source.hp4t --hp4l--> `<instance name>`.hp4
   - Create program ID per instance and maintain map `<instance name>: [program ID]`
  4. (dpmu) Load HP4 with `<instance name>`.hp4
   - `<path to sswitch_CLI> <port of P4 device> < <instance name>.hp4`
  5. (dpmu) return success/fail for each requested instance
  6. (user) send table transaction formatted for source.p4, designated for a certain instance
     ./dpmu --client --port 33333 --instance `<instance name>` --command 'table_add dmac forward 00:AA:BB:00:00:01 => 1'

  7. (dpmu) check validity of instance, translate transaction, return success/fail

## t1\_extracted\_exact

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

standard\_client, mc\_client = thrift\_connect(args.thrift_ip, args.thrift\_port, RuntimeAPI.get\_thrift\_services(args.pre))

load\_json\_config(standard\_client, args.json)

RuntimeAPI(args.pre, standard\_client, mc\_client).cmdloop()

thrift\_connect:
- wrapper method in runtime\_CLI.py: return utils.thrift\_connect(...)

- [X] Need: import bmpy\_utils as utils
- [ ] RuntimeAPI::do\_table\_set\_default
      - [ ] Need RuntimeAPI::parse\_runtime\_data
      - [ ] Need runtime_CLI.py::parse\_runtime\_data
- [ ] RuntimeAPI::do\_table\_add
