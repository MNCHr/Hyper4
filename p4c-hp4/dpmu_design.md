# DPMU Design

Given:
- hp4t\_l2\_switch.p4
- UE1 table\_add dmac forward [MAC of h2] => [port of h1]

Need to produce entries for:
- t1\_extracted\_exact
- t\_mod\_11

We can use 'dmac' and 'forward' to form a key to look up relevant template entries.  We should expect a match table template, and potentially a number of primitive table templates.  The range of the number of primitive table templates has a minimum of 0, and a maximum equal to the number of primitives in the source action.

What is unclear is how to associate the source action parameters with their primitives.  It is easy enough to come up with some kind of mapping in the compiler: {primitive: ordinal number of source action parameter}.  Then we just have to include the ordinal number of the source action parameter in the template entry.

In p4c-hp4.py, focus on gen\_action\_entries and gen\_action\_aparams.  Basically in the p4\_call we can look at p4\_call[1][1] and if it is 'sig(n)' then the type will be p4\_hlir.hlir.p4\_imperatives.p4\_signature\_ref and it will have an idx attribute, which is the ordinal number of the source action parameter.

## t1\_extracted\_exact

- [program ID]: DPMU state initialized at startup via commandline arguments
- [val]: UE1 match parameter, [MAC of h2]
- [match ID]: DPMU state initialized at startup, updated with every user entry passed through the DPMU
- [DONE]: definitions file shared with hp4l
- [MODIFY_FIELD]: definitions file shared with hp4l

## t\_mod\_11

- [program ID]: DPMU state initialized at startup via commandline arguments
- [match ID]: DPMU state initialized at startup, updated with every user entry passed through the DPMU
- [val]: UE1 action parameter, [port of h1]
