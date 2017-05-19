/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

stages.p4: Each control function executes a single match-action stage of a
           target P4 program.

           The set_program_state tables guide execution from one primtive to
           the next.
*/

#include "match.p4"
#include "switch_primitivetype.p4"

action update_state(primitive, primitive_subtype) {
  modify_field(meta_primitive_state.primitive_index, 
               meta_primitive_state.primitive_index + 1);
  modify_field(meta_primitive_state.primitive, primitive);
  modify_field(meta_primitive_state.subtype, primitive_subtype);
}

action finish_action(next_stage) {
  modify_field(meta_ctrl.next_stage, next_stage);
  modify_field(meta_ctrl.stage_state, COMPLETE);
}

table tstg11_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg12_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg21_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg22_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg31_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg32_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg41_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg42_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg51_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg52_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg61_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg62_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg71_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg72_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

control stage1 {
  match_1(); // match.p4
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_11(); // switch_primitivetype.p4
    apply(tstg11_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_12(); // switch_primitivetype.p4
      apply(tstg12_update_state);
    }
  }
}

control stage2 {
  match_2(); // match.p4
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_21(); // switch_primitivetype.p4
    apply(tstg21_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_22(); // switch_primitivetype.p4
      apply(tstg22_update_state);
    }
  }
}

control stage3 {
  match_3(); // match.p4
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_31(); // switch_primitivetype.p4
    apply(tstg31_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_32(); // switch_primitivetype.p4
      apply(tstg32_update_state);
    }
  }
}

control stage4 {
  match_4(); // match.p4
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_41(); // switch_primitivetype.p4
    apply(tstg41_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_42(); // switch_primitivetype.p4
      apply(tstg42_update_state);
    }
  }
}

control stage5 {
  match_5(); // match.p4
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_51(); // switch_primitivetype.p4
    apply(tstg51_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_52(); // switch_primitivetype.p4
      apply(tstg52_update_state);
    }
  }
}

control stage6 {
  match_6(); // match.p4
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_61(); // switch_primitivetype.p4
    apply(tstg61_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_62(); // switch_primitivetype.p4
      apply(tstg62_update_state);
    }
  }
}

control stage7 {
  match_7(); // match.p4
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_71(); // switch_primitivetype.p4
    apply(tstg71_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_72(); // switch_primitivetype.p4
      apply(tstg72_update_state);
    }
  }
}

