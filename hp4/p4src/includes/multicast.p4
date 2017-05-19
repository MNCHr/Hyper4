/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

multicast.p4: Provide multicast support.  The method is less efficient than
              a switch-specific mechanism, but it is portable.  The code
              here sets up multicasting, while hp4.p4 is where it is carried
              out.
*/

action a_multicast(grp_id, highport) {
  modify_field(meta_ctrl.mcast_grp_id, grp_id);
  modify_field(meta_ctrl.mcast_current_egress, highport);
  modify_field(meta_ctrl.mc_flag, 1);
  modify_field(standard_metadata.egress_spec, highport);
}

table t_multicast_11 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_12 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_21 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_22 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_31 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_32 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_41 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_42 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_51 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_52 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_61 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_62 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_71 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

table t_multicast_72 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_multicast;
  }
}

control do_multicast_11 {
  apply(t_multicast_11);
}

control do_multicast_12 {
  apply(t_multicast_12);
}

control do_multicast_21 {
  apply(t_multicast_21);
}

control do_multicast_22 {
  apply(t_multicast_22);
}

control do_multicast_31 {
  apply(t_multicast_31);
}

control do_multicast_32 {
  apply(t_multicast_32);
}

control do_multicast_41 {
  apply(t_multicast_41);
}

control do_multicast_42 {
  apply(t_multicast_42);
}

control do_multicast_51 {
  apply(t_multicast_51);
}

control do_multicast_52 {
  apply(t_multicast_52);
}

control do_multicast_61 {
  apply(t_multicast_61);
}

control do_multicast_62 {
  apply(t_multicast_62);
}

control do_multicast_71 {
  apply(t_multicast_71);
}

control do_multicast_72 {
  apply(t_multicast_72);
}
