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

table t_math_on_field_13 {
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

table t_math_on_field_14 {
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

table t_math_on_field_15 {
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

table t_math_on_field_16 {
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

table t_math_on_field_17 {
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

table t_math_on_field_18 {
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

table t_math_on_field_19 {
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

table t_math_on_field_23 {
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

table t_math_on_field_24 {
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

table t_math_on_field_25 {
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

table t_math_on_field_26 {
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

table t_math_on_field_27 {
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

table t_math_on_field_28 {
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

table t_math_on_field_29 {
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

table t_math_on_field_33 {
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

table t_math_on_field_34 {
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

table t_math_on_field_35 {
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

table t_math_on_field_36 {
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

table t_math_on_field_37 {
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

table t_math_on_field_38 {
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

table t_math_on_field_39 {
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

table t_math_on_field_43 {
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

table t_math_on_field_44 {
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

table t_math_on_field_45 {
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

table t_math_on_field_46 {
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

table t_math_on_field_47 {
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

table t_math_on_field_48 {
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

table t_math_on_field_49 {
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

table t_math_on_field_53 {
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

table t_math_on_field_54 {
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

table t_math_on_field_55 {
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

table t_math_on_field_56 {
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

table t_math_on_field_57 {
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

table t_math_on_field_58 {
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

table t_math_on_field_59 {
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

table t_math_on_field_63 {
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

table t_math_on_field_64 {
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

table t_math_on_field_65 {
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

table t_math_on_field_66 {
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

table t_math_on_field_67 {
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

table t_math_on_field_68 {
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

table t_math_on_field_69 {
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

table t_math_on_field_73 {
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

table t_math_on_field_74 {
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

table t_math_on_field_75 {
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

table t_math_on_field_76 {
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

table t_math_on_field_77 {
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

table t_math_on_field_78 {
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

table t_math_on_field_79 {
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

control do_math_on_field_13 {
  apply(t_math_on_field_13);
}

control do_math_on_field_14 {
  apply(t_math_on_field_14);
}

control do_math_on_field_15 {
  apply(t_math_on_field_15);
}

control do_math_on_field_16 {
  apply(t_math_on_field_16);
}

control do_math_on_field_17 {
  apply(t_math_on_field_17);
}

control do_math_on_field_18 {
  apply(t_math_on_field_18);
}

control do_math_on_field_19 {
  apply(t_math_on_field_19);
}

control do_math_on_field_21 {
  apply(t_math_on_field_21);
}

control do_math_on_field_22 {
  apply(t_math_on_field_22);
}

control do_math_on_field_23 {
  apply(t_math_on_field_23);
}

control do_math_on_field_24 {
  apply(t_math_on_field_24);
}

control do_math_on_field_25 {
  apply(t_math_on_field_25);
}

control do_math_on_field_26 {
  apply(t_math_on_field_26);
}

control do_math_on_field_27 {
  apply(t_math_on_field_27);
}

control do_math_on_field_28 {
  apply(t_math_on_field_28);
}

control do_math_on_field_29 {
  apply(t_math_on_field_29);
}

control do_math_on_field_31 {
  apply(t_math_on_field_31);
}

control do_math_on_field_32 {
  apply(t_math_on_field_32);
}

control do_math_on_field_33 {
  apply(t_math_on_field_33);
}

control do_math_on_field_34 {
  apply(t_math_on_field_34);
}

control do_math_on_field_35 {
  apply(t_math_on_field_35);
}

control do_math_on_field_36 {
  apply(t_math_on_field_36);
}

control do_math_on_field_37 {
  apply(t_math_on_field_37);
}

control do_math_on_field_38 {
  apply(t_math_on_field_38);
}

control do_math_on_field_39 {
  apply(t_math_on_field_39);
}

control do_math_on_field_41 {
  apply(t_math_on_field_41);
}

control do_math_on_field_42 {
  apply(t_math_on_field_42);
}

control do_math_on_field_43 {
  apply(t_math_on_field_43);
}

control do_math_on_field_44 {
  apply(t_math_on_field_44);
}

control do_math_on_field_45 {
  apply(t_math_on_field_45);
}

control do_math_on_field_46 {
  apply(t_math_on_field_46);
}

control do_math_on_field_47 {
  apply(t_math_on_field_47);
}

control do_math_on_field_48 {
  apply(t_math_on_field_48);
}

control do_math_on_field_49 {
  apply(t_math_on_field_49);
}

control do_math_on_field_51 {
  apply(t_math_on_field_51);
}

control do_math_on_field_52 {
  apply(t_math_on_field_52);
}

control do_math_on_field_53 {
  apply(t_math_on_field_53);
}

control do_math_on_field_54 {
  apply(t_math_on_field_54);
}

control do_math_on_field_55 {
  apply(t_math_on_field_55);
}

control do_math_on_field_56 {
  apply(t_math_on_field_56);
}

control do_math_on_field_57 {
  apply(t_math_on_field_57);
}

control do_math_on_field_58 {
  apply(t_math_on_field_58);
}

control do_math_on_field_59 {
  apply(t_math_on_field_59);
}

control do_math_on_field_61 {
  apply(t_math_on_field_61);
}

control do_math_on_field_62 {
  apply(t_math_on_field_62);
}

control do_math_on_field_63 {
  apply(t_math_on_field_63);
}

control do_math_on_field_64 {
  apply(t_math_on_field_64);
}

control do_math_on_field_65 {
  apply(t_math_on_field_65);
}

control do_math_on_field_66 {
  apply(t_math_on_field_66);
}

control do_math_on_field_67 {
  apply(t_math_on_field_67);
}

control do_math_on_field_68 {
  apply(t_math_on_field_68);
}

control do_math_on_field_69 {
  apply(t_math_on_field_69);
}

control do_math_on_field_71 {
  apply(t_math_on_field_71);
}

control do_math_on_field_72 {
  apply(t_math_on_field_72);
}

control do_math_on_field_73 {
  apply(t_math_on_field_73);
}

control do_math_on_field_74 {
  apply(t_math_on_field_74);
}

control do_math_on_field_75 {
  apply(t_math_on_field_75);
}

control do_math_on_field_76 {
  apply(t_math_on_field_76);
}

control do_math_on_field_77 {
  apply(t_math_on_field_77);
}

control do_math_on_field_78 {
  apply(t_math_on_field_78);
}

control do_math_on_field_79 {
  apply(t_math_on_field_79);
}
