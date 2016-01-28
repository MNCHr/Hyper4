/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

setup.p4:
- Check the need to initialize local metadata for the current packet
  - this includes the parse width; after this is set, we resubmit so we can
    extract the proper number of bits
- Normalize extracted data to a standard width bitfield (e.g. 256 -> 768)
- Set program and first table
*/

// ------ Normalize data to 768-bit bitfield
action a_norm_256() {
  modify_field(extracted.data, bitfield_256.data);
}

action a_norm_512() {
  modify_field(extracted.data, bitfield_512.data);
}

action a_norm_768() {
  modify_field(extracted.data, bitfield_768.data);
}

table t_norm {
  reads {
    meta_ctrl.program : exact;
  }
  actions {
    a_norm_256;
    a_norm_512;
    a_norm_768;
  }
}

// ------ Initialize local metadata and resubmit
field_list f_packet_init {
  meta_parse;
  meta_ctrl;
  standard_metadata;
}

// ------ Set program and first table and parse width
action set_program(program, table_ID, parse_width) {
  modify_field(meta_ctrl.program, program);
  modify_field(meta_ctrl.next_table, table_ID);
  modify_field(meta_parse.parse_width, parse_width);
  resubmit(f_packet_init);
}

table t_prog_select {
  reads {
    standard_metadata.ingress_port : exact; // range not yet supported by bmv2
    //standard_metadata.packet_length : exact; // range not yet supported by bmv2
    //standard_metadata.instance_type : exact; // range not yet supported by bmv2
    //extracted.data : ternary;
  }
  actions {
    set_program;
  }
}

// ------ Setup
control setup {
  if (meta_ctrl.stage == INIT) { //_condition_0
    apply(t_prog_select);
  }
  else if ( meta_ctrl.stage == NORM ) { //_condition_1
    apply(t_norm);
  }
}
