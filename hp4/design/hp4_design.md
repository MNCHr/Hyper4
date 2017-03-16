## TODO

- [ ] p4c-hp4 test: arp-proxy
- [ ] p4c-hp4 test: firewall
- [ ] p4c-hp4 test: router
- [ ] p4c-hp4 test: l2 switch
- [ ] ADE: setup.p4: [link](#parsed-representation-to-HP4-metadata) copy ext header stack elements to extracted.data BEFORE doing the matching on the parsed representation, so we do it against extracted.data instead of ext elements, allowing us to do everything with one table that has a ternary match against extracted.data

ADE: Alternative Design Evaluation

-----

## HyPer4 Subsystems

### Ingress

#### context setting

table *tset_context*

When a packet is received from a physical port, we must assign the program ID and the virtual ingress port.  The virtual ingress port assignment removes the need to think about the physical ingress port as a possible match field when managing any of the virtual program's tables that, when run natively, would match on the standard_metadata.ingress_port.  Virtual programs may not even be connected to any physical ports directly.  This virtual ingress port assignment therefore makes the HP4 virtual network easier to manage - we can rewire virtual programs without worrying about the physical ingress ports.

The match fields should include standard_metadata fields.  We don't look at the parsed representation fields here, but the tset_parse_select_XX_YY tables provide the chance to change the program ID based on the parsed representation.

#### inbound virtual networking

table *tset_in_virtnet*

When a packet is handed over to another virtual program after having been processed by a virtual program already (we know this because the virtual egress port is non-zero), we need to copy the virtual egress port to the virtual ingress port and reset the virtual egress port in order to adopt the correct perspective of the current virtual program.

#### parsing

table *tset_parse_control*
table *tset_parse_select_XX_YY*

This subsystem handles parsing.  It provides the mechanisms for inspecting parsed representation values to determine whether a resubmit is required to extract more bytes.  At the end we are left with a header stack that contains the parsed representation.  

#### parsed representation to HP4 metadata

table *tset_pr_XX_YY*

Once we have the parsed representation in a header stack, we copy all elements of the stack to a single metadata field to make arbitrary matching feasible.

DESIGN OPTIONS:
- Option #1: Let this happen after tset_parse_select tables when parse_ctrl.next_action == PROCEED.  Advantage is that it is only invoked once, after the packet has been fully parsed.  Disadvantage is that tset_parse_select tables must examine the ext header stack, and we've broken up the process in groups of ten stack elements / bytes to inspect at a time.  In other words, the tset_parse_select process is awkward.
- Option #2: Do it first, before even tset_context.  Advantage: simplifies tset_parse_select to a single table, and tset_context also can read the extracted.data metadata field to determine how to set the program ID instead of handling this in tset_parse_select.  In terms of development effort, this is the way to go.  Disadvantage: for packets that must be resubmitted more than once in order to fully parse them, this copying process is invoked in every iteration of that loop.

We like option 2 but out of concern for performance we should evaluate it first.  Evaluation plan:

- Create a simple, non-HP4 program that parses up to the transport layer and simply forwards the packet.
- Create a program that uses the HP4 parser and relevant setup tables, but functionally does nothing but forwards the packet.  Use option 1.
- Same but option 2.
- For each, measure these things:
  - Throughput: via iperf
  - Latency: wireshark: time between appearing one interface and the other.  Do percentile distribution charts.
    - light load
    - moderate load
    - heavy load

- pipeline configuration
  - tset_pipeline

This subsystem prepares HP4 to handle the virtual program's ingress pipeline.  Based on the program ID and the final parse_ctrl.state, we identify the tableID corresponding to the type of matching that must be performed first.  We also set the validbits bitmap indicating which headers are logically present in the parsed representation.

#### match-action

This subsystem handles the core functionality of the virtual program, performing equivalent matches and executing actions as chained instances of single primitives.

#### egress_spec to port

table *thp4_handle_egress_spec*

We need to handle the egress_spec.  Two options:
- [NOT SELECTED] Option #1: The compiler reinterprets modify_field calls where the dest field is the egress_spec, as modify_field calls where the dest field is meta_ctrl.virt_egress_port.  At the end of ingress, we have a table thp4_handle_egress that matches on program ID and virt_egress_port.  IF the virt_egress_port is linked to a physical port, the triggered action should set the egress_spec accordingly.  Otherwise the virt_egress_port is linked to another program's logical virt_ingress_port, and we set egress_spec to ingress_port because egress activities must be handled at some port.
- [SELECTED] Option #2: The compiler does not reinterpret modify_field calls where egress_spec is the dest field.  At the end of ingress, we have a table thp4_handle_egress that matches on the program ID and the egress_spec.  Now depending on how the HP4 device administrator has configured the virtual program, the egress_spec may correspond directly with a physical port, in which case we do nothing, or it may correspond with a virtual port for this program that is linked to the virtual port of another program, in which case, we need to set the virt_egress_port according to the egress_spec->virt_egress_port map, while the egress_spec is set to the ingress_port (because the packet has to be handled by some port).

In option 1, consider a program in which, natively, we have some forwarding table where the entries commonly trigger an action that modifies the egress_spec according to an action parameter.  Now we host this program in HP4.  Each time the program's admin wants to populate the forwarding table, the DPMU has to convert egress_spec values to the corresponding virtual egress port values.  And there might be multiple such tables in a given program hosted in HP4.  On the other hand, with option 1, the DPMU does not have to do the translation.  Rather, only the HP4 admin has to maintain thp4_handle_egress entries to indicate how a virtual program's egress_spec values map either to physical ports or to other virtual program's virtual ingress ports.

Either way, the program admin can remain oblivious to the actual port correspondence.  For the HP4 admin, option 1 leads to editing a config file that the DPMU reads to do the substitutions properly, in addition to managing the thp4_handle_egress table.  Option 2 can be handled the same way, but doesn't have to be: it allows managing port correspondence via entries in the thp4_handle_egress table.

The real challenge is that, in an arbitrary program, the egress_spec can be set in a number of ways: the source value can be from an action parameter, another field (user-defined metadata, standard metadata, parsed representation), or a constant.  With option 1, we have to implement compiler support for each possibility.  This actually may not be too difficult though it will involve modifying HP4 as well as the compiler.

All things considered, option 2 seems the best approach for simplicity of implementation and management.

### Egress

#### multicast to virtual programs

#### egress filtering

#### outbound virtual networking

#### checksum

#### resize parsed representation

#### HP4 metadata to parsed representation

-----

## HyPer4 Design (Possibly Obsolete)

v0.1 Features
- 4 primitive types:
  - modify_field
    - target metadata <- standard metadata
    - target metadata <- constant
    - standard metadata <- target metadata
    - standard metadata <- constant
  - drop
  - no_op
  - truncate

v0.2 Features
- 2 Additional matching types: ternary, lpm
- 5 Additional primitive types:
  - add_header
  - copy_header
  - remove_header
  - push
  - pop
- Python script to generate p4 code
  - support user-specified max number of matches
  - support user-specified max number of primitives to execute per match
  - etc.

Outstanding Issues

- We have a potential problem with the initialization process.  Currently, we have a check_init table that has no entries and two possible default actions: init and no_op.  During normal operation the default action is no_op, and when the operator wants to trigger reinitialization, he changes the default action to init.  The problem is keeping initialization under control: we only want to execute initialization once, but it is triggered by the arrival of a packet in the dataplane, and while the switch initializes, other packets could arrive before we have a chance to revert the default action in the control plane.

How might we change this to ensure initialization happens only once?

We could use two registers and form a semaphore.  Assume both registers must be true in order to carry out initialization.  During normal operation, reg A is set to true and reg B is set to false.  Check_init default action is no_op until controller changes it to set_reg_B_true.  The first action taken by the intialization action is to set reg A to false.  The last actions taken by the intialization action is to set reg B to false and then set reg A to true.  Meanwhile, all subsequent packets should be held somehow (recirculated?) while reg B is true.

Double check this solution with existing semaphore implementations e.g. Peterson's Algorithm or Dekker's algorithm.