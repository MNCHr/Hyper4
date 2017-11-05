/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

match.p4: Support various types of matching used by the target P4 program.
*/

action init_program_state(action_ID, match_ID, next_stage, next_table, primitive, primitive_subtype) {
  modify_field(meta_primitive_state.action_ID, action_ID);
  modify_field(meta_primitive_state.match_ID, match_ID);
  modify_field(meta_ctrl.next_stage, next_stage);
  modify_field(meta_primitive_state.primitive_index, 1);
  modify_field(meta_ctrl.next_table, next_table);
  modify_field(meta_primitive_state.primitive, primitive);
  modify_field(meta_primitive_state.subtype, primitive_subtype);
}

table t1_matchless {
  reads {
    meta_ctrl.vdev_ID : exact;
  }
  actions {
    init_program_state;
  }
}

table t1_extracted_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t1_metadata_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t1_metadata_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t1_extracted_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t1_extracted_valid {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.validbits : ternary;
  }
  actions {
    init_program_state;
  }
}

// TODO: change match type for stdmetadata field to ternary, all tables
// Reason: supports table_set_default by allowing 0&&&0 while we still do exact
// matching on the program ID
table t1_stdmeta_ingress_port_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_ingress_port : ternary;
  }
  actions {
    init_program_state;
  }
}

table t1_stdmeta_packet_length_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.packet_length : ternary;
  }
  actions {
    init_program_state;
  }
}

table t1_stdmeta_instance_type_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.instance_type : ternary;
  }
  actions {
    init_program_state;
  }
}

table t1_stdmeta_egress_spec_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_egress_spec : ternary;
  }
  actions {
    init_program_state;
  }
}

table t2_matchless {
  reads {
    meta_ctrl.vdev_ID : exact;
  }
  actions {
    init_program_state;
  }
}

table t2_extracted_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t2_metadata_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t2_metadata_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t2_extracted_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t2_extracted_valid {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.validbits : ternary;
  }
  actions {
    init_program_state;
  }
}

// TODO: change match type for stdmetadata field to ternary, all tables
// Reason: supports table_set_default by allowing 0&&&0 while we still do exact
// matching on the program ID
table t2_stdmeta_ingress_port_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_ingress_port : ternary;
  }
  actions {
    init_program_state;
  }
}

table t2_stdmeta_packet_length_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.packet_length : ternary;
  }
  actions {
    init_program_state;
  }
}

table t2_stdmeta_instance_type_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.instance_type : ternary;
  }
  actions {
    init_program_state;
  }
}

table t2_stdmeta_egress_spec_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_egress_spec : ternary;
  }
  actions {
    init_program_state;
  }
}

table t3_matchless {
  reads {
    meta_ctrl.vdev_ID : exact;
  }
  actions {
    init_program_state;
  }
}

table t3_extracted_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t3_metadata_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t3_metadata_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t3_extracted_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t3_extracted_valid {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.validbits : ternary;
  }
  actions {
    init_program_state;
  }
}

// TODO: change match type for stdmetadata field to ternary, all tables
// Reason: supports table_set_default by allowing 0&&&0 while we still do exact
// matching on the program ID
table t3_stdmeta_ingress_port_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_ingress_port : ternary;
  }
  actions {
    init_program_state;
  }
}

table t3_stdmeta_packet_length_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.packet_length : ternary;
  }
  actions {
    init_program_state;
  }
}

table t3_stdmeta_instance_type_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.instance_type : ternary;
  }
  actions {
    init_program_state;
  }
}

table t3_stdmeta_egress_spec_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_egress_spec : ternary;
  }
  actions {
    init_program_state;
  }
}

table t4_matchless {
  reads {
    meta_ctrl.vdev_ID : exact;
  }
  actions {
    init_program_state;
  }
}

table t4_extracted_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t4_metadata_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t4_metadata_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t4_extracted_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t4_extracted_valid {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.validbits : ternary;
  }
  actions {
    init_program_state;
  }
}

// TODO: change match type for stdmetadata field to ternary, all tables
// Reason: supports table_set_default by allowing 0&&&0 while we still do exact
// matching on the program ID
table t4_stdmeta_ingress_port_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_ingress_port : ternary;
  }
  actions {
    init_program_state;
  }
}

table t4_stdmeta_packet_length_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.packet_length : ternary;
  }
  actions {
    init_program_state;
  }
}

table t4_stdmeta_instance_type_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.instance_type : ternary;
  }
  actions {
    init_program_state;
  }
}

table t4_stdmeta_egress_spec_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_egress_spec : ternary;
  }
  actions {
    init_program_state;
  }
}

table t5_matchless {
  reads {
    meta_ctrl.vdev_ID : exact;
  }
  actions {
    init_program_state;
  }
}

table t5_extracted_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t5_metadata_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t5_metadata_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t5_extracted_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t5_extracted_valid {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.validbits : ternary;
  }
  actions {
    init_program_state;
  }
}

// TODO: change match type for stdmetadata field to ternary, all tables
// Reason: supports table_set_default by allowing 0&&&0 while we still do exact
// matching on the program ID
table t5_stdmeta_ingress_port_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_ingress_port : ternary;
  }
  actions {
    init_program_state;
  }
}

table t5_stdmeta_packet_length_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.packet_length : ternary;
  }
  actions {
    init_program_state;
  }
}

table t5_stdmeta_instance_type_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.instance_type : ternary;
  }
  actions {
    init_program_state;
  }
}

table t5_stdmeta_egress_spec_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_egress_spec : ternary;
  }
  actions {
    init_program_state;
  }
}

table t6_matchless {
  reads {
    meta_ctrl.vdev_ID : exact;
  }
  actions {
    init_program_state;
  }
}

table t6_extracted_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t6_metadata_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t6_metadata_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t6_extracted_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t6_extracted_valid {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.validbits : ternary;
  }
  actions {
    init_program_state;
  }
}

// TODO: change match type for stdmetadata field to ternary, all tables
// Reason: supports table_set_default by allowing 0&&&0 while we still do exact
// matching on the program ID
table t6_stdmeta_ingress_port_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_ingress_port : ternary;
  }
  actions {
    init_program_state;
  }
}

table t6_stdmeta_packet_length_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.packet_length : ternary;
  }
  actions {
    init_program_state;
  }
}

table t6_stdmeta_instance_type_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.instance_type : ternary;
  }
  actions {
    init_program_state;
  }
}

table t6_stdmeta_egress_spec_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_egress_spec : ternary;
  }
  actions {
    init_program_state;
  }
}

table t7_matchless {
  reads {
    meta_ctrl.vdev_ID : exact;
  }
  actions {
    init_program_state;
  }
}

table t7_extracted_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t7_metadata_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t7_metadata_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    tmeta.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t7_extracted_ternary {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.data : ternary;
  }
  actions {
    init_program_state;
  }
}

table t7_extracted_valid {
  reads {
    meta_ctrl.vdev_ID : exact;
    extracted.validbits : ternary;
  }
  actions {
    init_program_state;
  }
}

// TODO: change match type for stdmetadata field to ternary, all tables
// Reason: supports table_set_default by allowing 0&&&0 while we still do exact
// matching on the program ID
table t7_stdmeta_ingress_port_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_ingress_port : ternary;
  }
  actions {
    init_program_state;
  }
}

table t7_stdmeta_packet_length_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.packet_length : ternary;
  }
  actions {
    init_program_state;
  }
}

table t7_stdmeta_instance_type_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    standard_metadata.instance_type : ternary;
  }
  actions {
    init_program_state;
  }
}

table t7_stdmeta_egress_spec_exact {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_egress_spec : ternary;
  }
  actions {
    init_program_state;
  }
}

control match_1 {
  if(meta_ctrl.next_table == EXTRACTED_EXACT) { // 17|118|...
    apply(t1_extracted_exact);
  }
  else if(meta_ctrl.next_table == METADATA_EXACT) { // 18|119|...
    apply(t1_metadata_exact);
  }
  else if(meta_ctrl.next_table == EXTRACTED_VALID) { // 19|120|...
    apply(t1_extracted_valid);
  }
  else if(meta_ctrl.next_table == MATCHLESS) {
    apply(t1_matchless);
  }
  else if(meta_ctrl.next_table == STDMETA_INGRESS_PORT_EXACT) {
    apply(t1_stdmeta_ingress_port_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_PACKET_LENGTH_EXACT) { // 22|...
    apply(t1_stdmeta_packet_length_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_INSTANCE_TYPE_EXACT) { // 23|...
    apply(t1_stdmeta_instance_type_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_EGRESS_SPEC_EXACT) { // 24|...
    apply(t1_stdmeta_egress_spec_exact);
  }
  else if(meta_ctrl.next_table == METADATA_TERNARY) { // 25|...
    apply(t1_metadata_ternary);
  }
  else if(meta_ctrl.next_table == EXTRACTED_TERNARY) { // 26|...
    apply(t1_extracted_ternary);
  }
}

control match_2 {
  if(meta_ctrl.next_table == EXTRACTED_EXACT) { // 17|118|...
    apply(t2_extracted_exact);
  }
  else if(meta_ctrl.next_table == METADATA_EXACT) { // 18|119|...
    apply(t2_metadata_exact);
  }
  else if(meta_ctrl.next_table == EXTRACTED_VALID) { // 19|120|...
    apply(t2_extracted_valid);
  }
  else if(meta_ctrl.next_table == MATCHLESS) {
    apply(t2_matchless);
  }
  else if(meta_ctrl.next_table == STDMETA_INGRESS_PORT_EXACT) {
    apply(t2_stdmeta_ingress_port_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_PACKET_LENGTH_EXACT) { // 22|...
    apply(t2_stdmeta_packet_length_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_INSTANCE_TYPE_EXACT) { // 23|...
    apply(t2_stdmeta_instance_type_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_EGRESS_SPEC_EXACT) { // 24|...
    apply(t2_stdmeta_egress_spec_exact);
  }
  else if(meta_ctrl.next_table == METADATA_TERNARY) { // 25|...
    apply(t2_metadata_ternary);
  }
  else if(meta_ctrl.next_table == EXTRACTED_TERNARY) { // 26|...
    apply(t2_extracted_ternary);
  }
}

control match_3 {
  if(meta_ctrl.next_table == EXTRACTED_EXACT) { // 17|118|...
    apply(t3_extracted_exact);
  }
  else if(meta_ctrl.next_table == METADATA_EXACT) { // 18|119|...
    apply(t3_metadata_exact);
  }
  else if(meta_ctrl.next_table == EXTRACTED_VALID) { // 19|120|...
    apply(t3_extracted_valid);
  }
  else if(meta_ctrl.next_table == MATCHLESS) {
    apply(t3_matchless);
  }
  else if(meta_ctrl.next_table == STDMETA_INGRESS_PORT_EXACT) {
    apply(t3_stdmeta_ingress_port_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_PACKET_LENGTH_EXACT) { // 22|...
    apply(t3_stdmeta_packet_length_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_INSTANCE_TYPE_EXACT) { // 23|...
    apply(t3_stdmeta_instance_type_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_EGRESS_SPEC_EXACT) { // 24|...
    apply(t3_stdmeta_egress_spec_exact);
  }
  else if(meta_ctrl.next_table == METADATA_TERNARY) { // 25|...
    apply(t3_metadata_ternary);
  }
  else if(meta_ctrl.next_table == EXTRACTED_TERNARY) { // 26|...
    apply(t3_extracted_ternary);
  }
}

control match_4 {
  if(meta_ctrl.next_table == EXTRACTED_EXACT) { // 17|118|...
    apply(t4_extracted_exact);
  }
  else if(meta_ctrl.next_table == METADATA_EXACT) { // 18|119|...
    apply(t4_metadata_exact);
  }
  else if(meta_ctrl.next_table == EXTRACTED_VALID) { // 19|120|...
    apply(t4_extracted_valid);
  }
  else if(meta_ctrl.next_table == MATCHLESS) {
    apply(t4_matchless);
  }
  else if(meta_ctrl.next_table == STDMETA_INGRESS_PORT_EXACT) {
    apply(t4_stdmeta_ingress_port_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_PACKET_LENGTH_EXACT) { // 22|...
    apply(t4_stdmeta_packet_length_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_INSTANCE_TYPE_EXACT) { // 23|...
    apply(t4_stdmeta_instance_type_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_EGRESS_SPEC_EXACT) { // 24|...
    apply(t4_stdmeta_egress_spec_exact);
  }
  else if(meta_ctrl.next_table == METADATA_TERNARY) { // 25|...
    apply(t4_metadata_ternary);
  }
  else if(meta_ctrl.next_table == EXTRACTED_TERNARY) { // 26|...
    apply(t4_extracted_ternary);
  }
}

control match_5 {
  if(meta_ctrl.next_table == EXTRACTED_EXACT) { // 17|118|...
    apply(t5_extracted_exact);
  }
  else if(meta_ctrl.next_table == METADATA_EXACT) { // 18|119|...
    apply(t5_metadata_exact);
  }
  else if(meta_ctrl.next_table == EXTRACTED_VALID) { // 19|120|...
    apply(t5_extracted_valid);
  }
  else if(meta_ctrl.next_table == MATCHLESS) {
    apply(t5_matchless);
  }
  else if(meta_ctrl.next_table == STDMETA_INGRESS_PORT_EXACT) {
    apply(t5_stdmeta_ingress_port_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_PACKET_LENGTH_EXACT) { // 22|...
    apply(t5_stdmeta_packet_length_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_INSTANCE_TYPE_EXACT) { // 23|...
    apply(t5_stdmeta_instance_type_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_EGRESS_SPEC_EXACT) { // 24|...
    apply(t5_stdmeta_egress_spec_exact);
  }
  else if(meta_ctrl.next_table == METADATA_TERNARY) { // 25|...
    apply(t5_metadata_ternary);
  }
  else if(meta_ctrl.next_table == EXTRACTED_TERNARY) { // 26|...
    apply(t5_extracted_ternary);
  }
}

control match_6 {
  if(meta_ctrl.next_table == EXTRACTED_EXACT) { // 17|118|...
    apply(t6_extracted_exact);
  }
  else if(meta_ctrl.next_table == METADATA_EXACT) { // 18|119|...
    apply(t6_metadata_exact);
  }
  else if(meta_ctrl.next_table == EXTRACTED_VALID) { // 19|120|...
    apply(t6_extracted_valid);
  }
  else if(meta_ctrl.next_table == MATCHLESS) {
    apply(t6_matchless);
  }
  else if(meta_ctrl.next_table == STDMETA_INGRESS_PORT_EXACT) {
    apply(t6_stdmeta_ingress_port_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_PACKET_LENGTH_EXACT) { // 22|...
    apply(t6_stdmeta_packet_length_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_INSTANCE_TYPE_EXACT) { // 23|...
    apply(t6_stdmeta_instance_type_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_EGRESS_SPEC_EXACT) { // 24|...
    apply(t6_stdmeta_egress_spec_exact);
  }
  else if(meta_ctrl.next_table == METADATA_TERNARY) { // 25|...
    apply(t6_metadata_ternary);
  }
  else if(meta_ctrl.next_table == EXTRACTED_TERNARY) { // 26|...
    apply(t6_extracted_ternary);
  }
}

control match_7 {
  if(meta_ctrl.next_table == EXTRACTED_EXACT) { // 17|118|...
    apply(t7_extracted_exact);
  }
  else if(meta_ctrl.next_table == METADATA_EXACT) { // 18|119|...
    apply(t7_metadata_exact);
  }
  else if(meta_ctrl.next_table == EXTRACTED_VALID) { // 19|120|...
    apply(t7_extracted_valid);
  }
  else if(meta_ctrl.next_table == MATCHLESS) {
    apply(t7_matchless);
  }
  else if(meta_ctrl.next_table == STDMETA_INGRESS_PORT_EXACT) {
    apply(t7_stdmeta_ingress_port_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_PACKET_LENGTH_EXACT) { // 22|...
    apply(t7_stdmeta_packet_length_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_INSTANCE_TYPE_EXACT) { // 23|...
    apply(t7_stdmeta_instance_type_exact);
  }
  else if(meta_ctrl.next_table == STDMETA_EGRESS_SPEC_EXACT) { // 24|...
    apply(t7_stdmeta_egress_spec_exact);
  }
  else if(meta_ctrl.next_table == METADATA_TERNARY) { // 25|...
    apply(t7_metadata_ternary);
  }
  else if(meta_ctrl.next_table == EXTRACTED_TERNARY) { // 26|...
    apply(t7_extracted_ternary);
  }
}
