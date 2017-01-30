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

action update_state(action_ID, primitive, primitive_subtype) {
  modify_field(meta_primitive_state.action_ID, action_ID);
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
    meta_primitive_state.primitive_index : exact;
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
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg13_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg14_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg15_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg16_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg17_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg18_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg19_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
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
    meta_primitive_state.primitive_index : exact;
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
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg23_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg24_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg25_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg26_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg27_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg28_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg29_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
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
    meta_primitive_state.primitive_index : exact;
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
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg33_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg34_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg35_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg36_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg37_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg38_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg39_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
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
    meta_primitive_state.primitive_index : exact;
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
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg43_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg44_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg45_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg46_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg47_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg48_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

table tstg49_update_state {
  reads {
    meta_ctrl.program : exact;
    meta_primitive_state.action_ID : exact;
    meta_primitive_state.primitive_index : exact;
  }
  actions {
    update_state;
    finish_action;
  }
}

control stage1 {
  match_1();
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_11();
    apply(tstg11_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_12();
      apply(tstg12_update_state);
      if(meta_ctrl.stage_state != COMPLETE) {
        switch_primitivetype_13();
        apply(tstg13_update_state);
        if(meta_ctrl.stage_state != COMPLETE) {
          switch_primitivetype_14();
          apply(tstg14_update_state);
          if(meta_ctrl.stage_state != COMPLETE) {
            switch_primitivetype_15();
            apply(tstg15_update_state);
            if(meta_ctrl.stage_state != COMPLETE) {
              switch_primitivetype_16();
              apply(tstg16_update_state);
              if(meta_ctrl.stage_state != COMPLETE) {
                switch_primitivetype_17();
                apply(tstg17_update_state);
                if(meta_ctrl.stage_state != COMPLETE) {
                  switch_primitivetype_18();
                  apply(tstg18_update_state);
                  if(meta_ctrl.stage_state != COMPLETE) {
                    switch_primitivetype_19();
                    apply(tstg19_update_state);
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

control stage2 {
  match_2();
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_21();
    apply(tstg21_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_22();
      apply(tstg22_update_state);
      if(meta_ctrl.stage_state != COMPLETE) {
        switch_primitivetype_23();
        apply(tstg23_update_state);
        if(meta_ctrl.stage_state != COMPLETE) {
          switch_primitivetype_24();
          apply(tstg24_update_state);
          if(meta_ctrl.stage_state != COMPLETE) {
            switch_primitivetype_25();
            apply(tstg25_update_state);
            if(meta_ctrl.stage_state != COMPLETE) {
              switch_primitivetype_26();
              apply(tstg26_update_state);
              if(meta_ctrl.stage_state != COMPLETE) {
                switch_primitivetype_27();
                apply(tstg27_update_state);
                if(meta_ctrl.stage_state != COMPLETE) {
                  switch_primitivetype_28();
                  apply(tstg28_update_state);
                  if(meta_ctrl.stage_state != COMPLETE) {
                    switch_primitivetype_29();
                    apply(tstg29_update_state);
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

control stage3 {
  match_3();
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_31();
    apply(tstg31_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_32();
      apply(tstg32_update_state);
      if(meta_ctrl.stage_state != COMPLETE) {
        switch_primitivetype_33();
        apply(tstg33_update_state);
        if(meta_ctrl.stage_state != COMPLETE) {
          switch_primitivetype_34();
          apply(tstg34_update_state);
          if(meta_ctrl.stage_state != COMPLETE) {
            switch_primitivetype_35();
            apply(tstg35_update_state);
            if(meta_ctrl.stage_state != COMPLETE) {
              switch_primitivetype_36();
              apply(tstg36_update_state);
              if(meta_ctrl.stage_state != COMPLETE) {
                switch_primitivetype_37();
                apply(tstg37_update_state);
                if(meta_ctrl.stage_state != COMPLETE) {
                  switch_primitivetype_38();
                  apply(tstg38_update_state);
                  if(meta_ctrl.stage_state != COMPLETE) {
                    switch_primitivetype_39();
                    apply(tstg39_update_state);
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

control stage4 {
  match_4();
  if(meta_ctrl.stage_state != COMPLETE) {
    switch_primitivetype_41();
    apply(tstg41_update_state);
    if(meta_ctrl.stage_state != COMPLETE) {
      switch_primitivetype_42();
      apply(tstg42_update_state);
      if(meta_ctrl.stage_state != COMPLETE) {
        switch_primitivetype_43();
        apply(tstg43_update_state);
        if(meta_ctrl.stage_state != COMPLETE) {
          switch_primitivetype_44();
          apply(tstg44_update_state);
          if(meta_ctrl.stage_state != COMPLETE) {
            switch_primitivetype_45();
            apply(tstg45_update_state);
            if(meta_ctrl.stage_state != COMPLETE) {
              switch_primitivetype_46();
              apply(tstg46_update_state);
              if(meta_ctrl.stage_state != COMPLETE) {
                switch_primitivetype_47();
                apply(tstg47_update_state);
                if(meta_ctrl.stage_state != COMPLETE) {
                  switch_primitivetype_48();
                  apply(tstg48_update_state);
                  if(meta_ctrl.stage_state != COMPLETE) {
                    switch_primitivetype_49();
                    apply(tstg49_update_state);
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

