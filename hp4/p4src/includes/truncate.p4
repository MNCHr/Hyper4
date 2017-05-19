/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

truncate.p4: Implements the truncate primitive
*/

action a_truncate(val) {
  truncate(val);
}

table t_truncate_11 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_12 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_21 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_22 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_31 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_32 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_41 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_42 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_51 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_52 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_61 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_62 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_71 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

table t_truncate_72 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_truncate;
  }
}

control do_truncate_11 {
  apply(t_truncate_11);
}

control do_truncate_12 {
  apply(t_truncate_12);
}

control do_truncate_21 {
  apply(t_truncate_21);
}

control do_truncate_22 {
  apply(t_truncate_22);
}

control do_truncate_31 {
  apply(t_truncate_31);
}

control do_truncate_32 {
  apply(t_truncate_32);
}

control do_truncate_41 {
  apply(t_truncate_41);
}

control do_truncate_42 {
  apply(t_truncate_42);
}

control do_truncate_51 {
  apply(t_truncate_51);
}

control do_truncate_52 {
  apply(t_truncate_52);
}

control do_truncate_61 {
  apply(t_truncate_61);
}

control do_truncate_62 {
  apply(t_truncate_62);
}

control do_truncate_71 {
  apply(t_truncate_71);
}

control do_truncate_72 {
  apply(t_truncate_72);
}
