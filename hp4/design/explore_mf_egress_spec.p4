// Handle modify_field(standard_metadata.egress_spec, [val])

// OPTION 1: Compiler changes destination field to meta_ctrl.virt_egress_spec:

action mod_stdmeta_egressspec_const(val) {
  

table mod_XY {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    // ...
    mod_stdmeta_egressspec_meta;
    mod_stdmeta_egressspec_const;
    mod_stdmeta_egressspec_stdmeta_ingressport;
    // ...
}

table t_link {
  reads {
    meta_ctrl.program : exact;
    
  }
}

control ingress {
  setup();
  // match-action...
  apply(t_link);
}
