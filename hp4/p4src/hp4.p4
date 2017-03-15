/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

hp4.p4: Define the ingress and egress pipelines, including multicast support.
*/

#include "includes/defines.p4"
#include "includes/headers.p4"
#include "includes/parser.p4"
#include "includes/deparse_prep.p4"
#include "includes/setup.p4"
#include "includes/stages.p4"
#include "includes/checksums.p4"
#include "includes/resize_pr.p4"
//#include "includes/debug.p4"

metadata meta_ctrl_t meta_ctrl;
metadata meta_primitive_state_t meta_primitive_state;
metadata extracted_t extracted;
metadata tmeta_t tmeta;
metadata csum_t csum;

metadata intrinsic_metadata_t intrinsic_metadata;

action a_handle_egress_virt(port) {
  modify_field(standard_metadata.egress_spec, standard_metadata.ingress_port);
  modify_field(meta_ctrl.virt_egress_port, port);
}

action a_handle_egress_phys(port) {
  modify_field(standard_metadata.egress_spec, port);
}

table thp4_handle_egress {
  reads {
    meta_ctrl.program : exact;
    standard_metadata.egress_spec : exact;
  }
  actions {
    a_handle_egress_virt;
    a_handle_egress_phys;
    _no_op;
  }
}

control ingress {
  setup();

  if (meta_ctrl.stage == NORM) {
    if (meta_ctrl.next_table != DONE and meta_ctrl.next_stage == 1) {
      stage1(); // stages.p4
    }

    if (meta_ctrl.next_table != DONE and meta_ctrl.next_stage == 2) {
      stage2(); // stages.p4
    }

    if (meta_ctrl.next_table != DONE and meta_ctrl.next_stage == 3) {
      stage3(); // stages.p4
    }

    if (meta_ctrl.next_table != DONE and meta_ctrl.next_stage == 4) {
      stage4(); // stages.p4
    }
    apply(thp4_handle_egress);
  }
}

field_list clone_fl {
  standard_metadata;
  meta_ctrl;
  extracted;
}

table thp4_egress_filter_case1 { actions { a_drop; }}
table thp4_egress_filter_case2 { actions { a_drop; }}

field_list fl_virtnet {
  meta_ctrl.program;
  meta_ctrl.virt_egress_port;
  standard_metadata;
}

action a_virtnet_forward(next_prog) {
  modify_field(meta_ctrl.program, next_prog);
  recirculate(fl_virtnet);
}

table thp4_out_virtnet {
  reads {
    meta_ctrl.program : exact;
    meta_ctrl.virt_egress_port : exact;
  }
  actions {
    _no_op;
    a_virtnet_forward;
  }
}

control egress {
  // egress filtering, recirculation
  if(standard_metadata.egress_port == standard_metadata.ingress_port) {
    if(meta_ctrl.virt_egress_port == 0) {
      apply(thp4_egress_filter_case1);
    }
    else {
      apply(thp4_out_virtnet);
    }
  }
  if(meta_ctrl.virt_egress_port == meta_ctrl.virt_ingress_port) {
    if(standard_metadata.egress_spec == standard_metadata.ingress_port) {
      apply(thp4_egress_filter_case2);
    }
  }

  apply(t_checksum);          // checksums.p4
  apply(t_resize_pr);         // resize_pr.p4
  apply(t_prep_deparse_SEB);  // deparse_prep.p4
  if(parse_ctrl.numbytes > 20) {
    apply(t_prep_deparse_20_39);
    if(parse_ctrl.numbytes > 40) {
      apply(t_prep_deparse_40_59);
      if(parse_ctrl.numbytes > 60) {
        apply(t_prep_deparse_60_79);
        if(parse_ctrl.numbytes > 80) {
          apply(t_prep_deparse_80_99);
        }
      }
    }
  }

}
