control ingress {
  setup();
  // match-action...
  apply(
}

action a_set_context(program_ID) {
  modify_field(meta_ctrl.program, program_ID);
}

table tset_context {
  reads {
  }
  actions {
    a_set_context;
  }
}

action a_virt_ports_cleanup() {
  modify_field(meta_ctrl.virt_ingress_port, meta_ctrl.virt_egress_port);
  modify_field(meta_ctrl.virt_egress_port, 0);
}

table tset_in_virtnet {
  actions {
    a_virt_ports_cleanup;
  }
}

control setup {
  if (meta_ctrl.stage == INIT) {
    if (meta_ctrl.program == 0) {
      apply(tset_context);
    }
    if (meta_ctrl.virt_egress_port > 0) {
      apply(tset_in_virtnet);
    }
  }
  apply(tset_parse_control);
  if(parse_ctrl.next_action == INSPECT_SEB) {
    apply(tset_parse_select_SEB);
  }
  // and so forth...
  if(parse_ctrl.next_action == PROCEED) {
    apply(tset_pr_SEB);
    if(parse_ctrl.numbytes > 20) {
      apply(tset_pr_20_39);
      // and so forth...
    }
    apply(tset_pipeline_config);
  }
}

control egress {
  
}
