/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

math_on_field.p4: Implements HP4 support for doing math to a field.
*/

// emask ensures change is isolated to the desired field
action a_add2f_extracted_const_s(leftshift, emask, val) {
  modify_field(extracted.data, (extracted.data & ~emask) | ( extracted.data + (val << leftshift) ));
}

// faster and easier, but no protection
action a_add2f_extracted_const_u(leftshift, val) {
  modify_field(extracted.data, extracted.data + (val << leftshift) );
}

// emask ensures change is isolated to the desired field
action a_subff_extracted_const_s(leftshift, emask, val) {
  modify_field(extracted.data, (extracted.data & ~emask) | ( extracted.data + (val << leftshift) ));
}

// faster and easier, but no protection
action a_subff_extracted_const_u(leftshift, val) {
  modify_field(extracted.data, extracted.data - (val << leftshift) );
}

table t_math_on_field_11 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_12 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_21 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_22 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_31 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_32 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_41 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_42 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_51 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_52 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_61 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_62 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_71 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

table t_math_on_field_72 {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.subtype : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.match_ID : ternary;
  }
  actions {
    a_add2f_extracted_const_s;
    a_add2f_extracted_const_u;
    a_subff_extracted_const_s;
    a_subff_extracted_const_u;
  }
}

control do_math_on_field_11 {
  apply(t_math_on_field_11);
}

control do_math_on_field_12 {
  apply(t_math_on_field_12);
}

control do_math_on_field_21 {
  apply(t_math_on_field_21);
}

control do_math_on_field_22 {
  apply(t_math_on_field_22);
}

control do_math_on_field_31 {
  apply(t_math_on_field_31);
}

control do_math_on_field_32 {
  apply(t_math_on_field_32);
}

control do_math_on_field_41 {
  apply(t_math_on_field_41);
}

control do_math_on_field_42 {
  apply(t_math_on_field_42);
}

control do_math_on_field_51 {
  apply(t_math_on_field_51);
}

control do_math_on_field_52 {
  apply(t_math_on_field_52);
}

control do_math_on_field_61 {
  apply(t_math_on_field_61);
}

control do_math_on_field_62 {
  apply(t_math_on_field_62);
}

control do_math_on_field_71 {
  apply(t_math_on_field_71);
}

control do_math_on_field_72 {
  apply(t_math_on_field_72);
}
