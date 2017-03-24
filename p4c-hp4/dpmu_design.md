# DPMU Design

Given:
- hp4t\_l2\_switch.p4
- UE1 table\_add dmac forward [MAC of h2] => [port of h1]

Need to produce entries for:
- t1\_extracted\_exact
- t\_mod\_11

Command line:
- ./dpmu -p 22222 -t hp4t\_l2\_switch.hp4mt -P 1 -c 'table_add dmac forward 00:AA:BB:00:00:01 => 1'

We can use 'dmac' and 'forward' to form a key to look up relevant template entries.  We should expect a match table template, and potentially a number of primitive table templates.  The range of the number of primitive table templates has a minimum of 0, and a maximum equal to the number of primitives in the source action.

What is unclear is how to associate the source action parameters with their primitives.  It is easy enough to come up with some kind of mapping in the compiler: {primitive: ordinal number of source action parameter}.  Then we just have to include the ordinal number of the source action parameter in the template entry.  UPDATE: This is called src\_aparam\_id.

In p4c-hp4.py, focus on gen\_action\_entries and gen\_action\_aparams.  Basically in the p4\_call we can look at p4\_call[1][1] and if it is 'sig(n)' then the type will be p4\_hlir.hlir.p4\_imperatives.p4\_signature\_ref and it will have an idx attribute, which is the ordinal number of the source action parameter.

But where do we store it?  Currently, we have HP4\_Match\_Command as the only subclass of HP4\_Command, but we should probably have a separate subclass, perhaps called HP4\_Primitive\_Command.

## t1\_extracted\_exact

- [program ID]: DPMU state initialized at startup via commandline arguments
  Let's flesh this out a bit.  Anticipated sequence of operation:
  1. (admin) Load P4 device with HP4
  2. (user) send request for service, include source.p4, pub key?, instance name(s)
  3. (admin) Compile source.p4 --p4c-hp4--> source.hp4t + source.hp4mt
  4. (admin) Prepare for loading: source.hp4t --hp4l--> source.hp4
   - Specify program ID
  5. (admin) Load HP4 with source.hp4
   - `<path to sswitch_CLI>` `<port of P4 device>` `<` source.hp4

- [val]: UE1 match parameter, [MAC of h2]
- [match ID]: DPMU state initialized at startup, updated with every user entry passed through the DPMU
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
