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

action a_handle_egress_virt(port) {
  modify_field(meta_ctrl.virt_egress_port, port);
  modify_field(standard_metadata.egress_spec, standard_metadata.ingress_port);
}

action a_handle_egress_phys(port) {
  modify_field(standard_metadata.egress_spec, port);
}

table thp4_handle_egress {
  reads {
    meta_ctrl.program : exact;
    standard_metadata.egress_spec : exact;
  }
  actions {
    a_handle_egress_virt;
    a_handle_egress_phys;
    _no_op;
  }
}

control ingress {
  setup();
  // match-action...
  apply(thp4_set_egress_spec);
}

field_list clone_fl {
  standard_metadata;
  meta_ctrl;
  extracted;
}

action a_multicast(port) {
  modify_field(meta_ctrl.mcast_current_egress, port);
  clone_egress_pkt_to_egress(port, clone_fl);
}

table thp4_multicast {
  reads {
    meta_ctrl.program : exact;
    meta_ctrl.mcast_grp : exact;
    meta_ctrl.mcast_current_egress : exact;
  }
  actions {
    a_multicast;
    _no_op;
  }
}

table thp4_egress_filter_case1 { actions { _drop; }}
table thp4_egress_filter_case2 { actions { _drop; }}

control egress {
  if(meta_ctrl.mc_flag == 1) {
    apply(thp4_multicast);
  }

  // egress filtering
  if(standard_metadata.egress_spec == standard_metadata.ingress_port) {
    if(meta_ctrl.virt_egress_port == 0) {
      apply(thp4_egress_filter_case1);
    }
  }
  if(meta_ctrl.virt_egress_port == meta_ctrl.virt_ingress_port) {
    if(standard_metadata.egress_spec == standard_metadata.ingress_port) {
      apply(thp4_egress_filter_case2);
    }
  }
}
