/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

switch_primitivetype.p4: Redirect execution to the control function appropriate
                         for the next primitive in the target P4 program
*/

#include "modify_field.p4"
#include "add_header.p4"
#include "copy_header.p4"
#include "remove_header.p4"
#include "push.p4"
#include "pop.p4"
#include "drop.p4"
#include "multicast.p4"
#include "math_on_field.p4"
#include "truncate.p4"

control switch_primitivetype_11 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_11();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_11();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_11();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_11();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_11();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_11();
  }
}

control switch_primitivetype_12 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_12();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_12();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_12();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_12();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_12();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_12();
  }
}

control switch_primitivetype_21 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_21();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_21();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_21();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_21();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_21();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_21();
  }
}

control switch_primitivetype_22 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_22();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_22();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_22();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_22();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_22();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_22();
  }
}

control switch_primitivetype_31 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_31();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_31();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_31();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_31();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_31();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_31();
  }
}

control switch_primitivetype_32 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_32();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_32();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_32();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_32();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_32();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_32();
  }
}

control switch_primitivetype_41 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_41();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_41();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_41();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_41();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_41();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_41();
  }
}

control switch_primitivetype_42 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_42();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_42();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_42();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_42();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_42();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_42();
  }
}

control switch_primitivetype_51 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_51();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_51();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_51();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_51();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_51();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_51();
  }
}

control switch_primitivetype_52 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_52();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_52();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_52();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_52();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_52();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_52();
  }
}

control switch_primitivetype_61 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_61();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_61();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_61();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_61();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_61();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_61();
  }
}

control switch_primitivetype_62 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_62();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_62();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_62();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_62();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_62();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_62();
  }
}

control switch_primitivetype_71 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_71();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_71();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_71();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_71();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_71();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_71();
  }
}

control switch_primitivetype_72 {
  if(meta_primitive_state.primitive == A_MODIFY_FIELD) {
    do_modify_field_72();
  }
  else if(meta_primitive_state.primitive == A_ADD_HEADER) {
    do_add_header_72();
  }
  else if(meta_primitive_state.primitive == A_TRUNCATE) {
    do_truncate_72();
  }
  else if(meta_primitive_state.primitive == A_DROP) {
    do_drop_72();
  }
  else if(meta_primitive_state.primitive == A_NO_OP) {
  }
  else if(meta_primitive_state.primitive == A_MULTICAST) {
    do_multicast_72();
  }
  else if(meta_primitive_state.primitive == A_MATH_ON_FIELD) {
    do_math_on_field_72();
  }
}
