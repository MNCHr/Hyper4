/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

add_header.p4: Carry out the add_header primitive
*/

action a_addh(sz, offset, msk, vbits) {
  modify_field(extracted.data, (extracted.data & ~msk) | (extracted.data >> (sz * 8)) & (msk >> (offset * 8)));
  modify_field(parse_ctrl.numbytes, parse_ctrl.numbytes + sz);
  modify_field(extracted.validbits, extracted.validbits | vbits);
}

table t_addh_11 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_12 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_21 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_22 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_31 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_32 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_41 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_42 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_51 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_52 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_61 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_62 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_71 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

table t_addh_72 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_addh;
  }
}

control do_add_header_11 {
  apply(t_addh_11);
}

control do_add_header_12 {
  apply(t_addh_12);
}

control do_add_header_21 {
  apply(t_addh_21);
}

control do_add_header_22 {
  apply(t_addh_22);
}

control do_add_header_31 {
  apply(t_addh_31);
}

control do_add_header_32 {
  apply(t_addh_32);
}

control do_add_header_41 {
  apply(t_addh_41);
}

control do_add_header_42 {
  apply(t_addh_42);
}

control do_add_header_51 {
  apply(t_addh_51);
}

control do_add_header_52 {
  apply(t_addh_52);
}

control do_add_header_61 {
  apply(t_addh_61);
}

control do_add_header_62 {
  apply(t_addh_62);
}

control do_add_header_71 {
  apply(t_addh_71);
}

control do_add_header_72 {
  apply(t_addh_72);
}
