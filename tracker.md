# HP4 Development Tracker

## hp4.p4

### P4 Language Coverage

- [ ] Support stateful memory

Adding support for stateful memory objects will lead to support for:
- DISCLOSURE (Detecting Botnet Command and Control Servers Through Large-Scale NetFlow Analysis)
- PaxOS made Switchy / NetPaxOS
- INT

- [ ] Additional primitives (TODO: identify & prioritize)

### Features

- [ ] Multicasting: Support arbitrary combinations of physical and virtual ports

Required if we want seamless abstraction regardless of actual topology

- [ ] Flowspaces: not just phys ingress port but flowspaces as defined in
      FlowVisor paper, for setup.p4::tset_context.
      May have to set a metadata field to the hash of the parsed representation
       and match on that field instead of trying to match on all possible fields.
      Implement both ways and compare, report as optimization if hashed is better
