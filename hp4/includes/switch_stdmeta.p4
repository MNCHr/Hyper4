#include "defines.p4"

table t1_stdmeta_ingressport {
  reads {
    standard_metadata.ingress_port : exact;
  }
  actions {
    set_program_state;
  }
}

table t1_stdmeta_packetlength {
  reads {
    standard_metadata.packet_length : exact;
  }
  actions {
    set_program_state;
  }
}

table t1_stdmeta_insttype {
  reads {
    standard_metadata.instance_type : exact;
  }
  actions {
    set_program_state;
  }
}

table t1_stdmeta_parserstat {
  reads {
    standard_metadata.parser_status : exact;
  }
  actions {
    set_program_state;
  }
}

table t1_stdmeta_parsererror {
  reads {
    standard_metadata.parser_error_location : exact;
  }
  actions {
    set_program_state;
  }
}

table t2_stdmeta_ingressport { reads { standard_metadata.ingress_port : exact; }
  actions { set_program_state; } }

table t2_stdmeta_packetlength { reads { standard_metadata.packet_length : exact; }
  actions { set_program_state; } }

table t2_stdmeta_insttype { reads { standard_metadata.instance_type : exact; }
  actions { set_program_state; } }

table t2_stdmeta_parserstat { reads { standard_metadata.parser_status : exact; }
  actions { set_program_state; } }

table t2_stdmeta_parsererror { reads { standard_metadata.parser_error_location : exact; }
  actions { set_program_state; } }

table t3_stdmeta_ingressport { reads { standard_metadata.ingress_port : exact; }
  actions { set_program_state; } }

table t3_stdmeta_packetlength { reads { standard_metadata.packet_length : exact; }
  actions { set_program_state; } }

table t3_stdmeta_insttype { reads { standard_metadata.instance_type : exact; }
  actions { set_program_state; } }

table t3_stdmeta_parserstat { reads { standard_metadata.parser_status : exact; }
  actions { set_program_state; } }

table t3_stdmeta_parsererror { reads { standard_metadata.parser_error_location : exact; }
  actions { set_program_state; } }

control switch_stdmeta {
  if(stdmeta_match.stdmeta_ID == STDMETA_INGRESSPORT) {
    apply(t1_stdmeta_ingressport);
  }
  else if(stdmeta_match.stdmeta_ID == STDMETA_PACKETLENGTH) {
    apply(t1_stdmeta_packetlength);
  }
  else if(stdmeta_match.stdmeta_ID == STDMETA_INSTTYPE) {
    apply(t1_stdmeta_insttype);
  }
  else if(stdmeta_match.stdmeta_ID == STDMETA_PARSERSTAT) {
    apply(t1_stdmeta_parserstat);
  }
  else if(stdmeta_match.stdmeta_ID == PARSERERROR) {
    apply(t1_stdmeta_parsererror);
  }
}

control switch_stdmeta_2 {
  if(stdmeta_match.stdmeta_ID == STDMETA_INGRESSPORT) {
    apply(t2_stdmeta_ingressport);
  }
  else if(stdmeta_match.stdmeta_ID == STDMETA_PACKETLENGTH) {
    apply(t2_stdmeta_packetlength);
  }
  else if(stdmeta_match.stdmeta_ID == STDMETA_INSTTYPE) {
    apply(t2_stdmeta_insttype);
  }
  else if(stdmeta_match.stdmeta_ID == STDMETA_PARSERSTAT) {
    apply(t2_stdmeta_parserstat);
  }
  else if(stdmeta_match.stdmeta_ID == PARSERERROR) {
    apply(t2_stdmeta_parsererror);
  }
}

control switch_stdmeta_3 {
  if(stdmeta_match.stdmeta_ID == STDMETA_INGRESSPORT) {
    apply(t3_stdmeta_ingressport);
  }
  else if(stdmeta_match.stdmeta_ID == STDMETA_PACKETLENGTH) {
    apply(t3_stdmeta_packetlength);
  }
  else if(stdmeta_match.stdmeta_ID == STDMETA_INSTTYPE) {
    apply(t3_stdmeta_insttype);
  }
  else if(stdmeta_match.stdmeta_ID == STDMETA_PARSERSTAT) {
    apply(t3_stdmeta_parserstat);
  }
  else if(stdmeta_match.stdmeta_ID == PARSERERROR) {
    apply(t3_stdmeta_parsererror);
  }
}