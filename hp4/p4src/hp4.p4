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
metadata temp_t temp;
metadata tmeta_t tmeta;
metadata csum_t csum;

metadata intrinsic_metadata_t intrinsic_metadata;

action do_phys_fwd_only(spec, filter) {
  modify_field(standard_metadata.egress_spec, spec);
  modify_field(meta_ctrl.efilter, filter);
}

action do_bmv2_mcast(mcast_grp, filter) {
  modify_field(intrinsic_metadata.mcast_grp, mcast_grp);
  modify_field(meta_ctrl.efilter, filter);
}

action do_virt_fwd() {
  modify_field(standard_metadata.egress_spec, standard_metadata.ingress_port);
  modify_field(meta_ctrl.virt_fwd_flag, 1);
}

table t_virtnet {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_egress_spec : exact;
  }
  actions {
    a_drop;
    do_phys_fwd_only;
    do_bmv2_mcast;
    do_virt_fwd;
  }
}

control ingress {
  setup();

  if (meta_ctrl.stage == NORM) { // 15?
    if (meta_ctrl.next_table != DONE and meta_ctrl.next_stage == 1) { // ?|?|?|...
      stage1(); // stages.p4
    }

    if (meta_ctrl.next_table != DONE and meta_ctrl.next_stage == 2) { // ?|?|?|...
      stage2(); // stages.p4
    }

    if (meta_ctrl.next_table != DONE and meta_ctrl.next_stage == 3) { // ?|?|?|...
      stage3(); // stages.p4
    }

    if (meta_ctrl.next_table != DONE and meta_ctrl.next_stage == 4) { // ?|?|?|...
      stage4(); // stages.p4
    }

    if (meta_ctrl.next_table != DONE and meta_ctrl.next_stage == 5) { // ?|?|?|...
      stage5(); // stages.p4
    }
    if (meta_ctrl.dropped == 0) {
      apply(t_virtnet);
    }
  }
}

field_list fl_recirc {
  standard_metadata;
  meta_ctrl.vdev_ID;
  meta_ctrl.next_vdev_ID;
  meta_ctrl.virt_ingress_port;
  meta_ctrl.stage;
  meta_ctrl.virt_egress_spec;
  meta_ctrl.orig_virt_ingress_port;
}

field_list fl_clone {
  standard_metadata;
  meta_ctrl.vdev_ID;
  meta_ctrl.next_vdev_ID;
  meta_ctrl.virt_ingress_port;
  meta_ctrl.virt_egress_spec;
  meta_ctrl.virt_fwd_flag;
}

action vfwd(vdev_ID, vingress) {
  modify_field(meta_ctrl.next_vdev_ID, vdev_ID);
  modify_field(meta_ctrl.virt_ingress_port, vingress);
  modify_field(meta_ctrl.stage, VFWD);
  recirculate(fl_recirc);
}

action vmcast(vdev_ID, vingress) {
  modify_field(meta_ctrl.next_vdev_ID, vdev_ID);
  modify_field(meta_ctrl.virt_ingress_port, vingress);
  modify_field(meta_ctrl.virt_egress_spec, meta_ctrl.virt_egress_spec + 1);
  modify_field(meta_ctrl.stage, VFWD);
  recirculate(fl_recirc);
  clone_egress_pkt_to_egress(standard_metadata.egress_port, fl_clone);
}

action vmcast_phys(vdev_ID, vingress, phys_spec) {
  modify_field(meta_ctrl.next_vdev_ID, vdev_ID);
  modify_field(meta_ctrl.virt_ingress_port, vingress);
  modify_field(meta_ctrl.virt_egress_spec, meta_ctrl.virt_egress_spec + 1);
  modify_field(meta_ctrl.stage, VFWD);
  recirculate(fl_recirc);
  clone_egress_pkt_to_egress(phys_spec, fl_clone);
}

action pmcast(phys_spec) {
  modify_field(meta_ctrl.virt_egress_spec, meta_ctrl.virt_egress_spec + 1);
  clone_egress_pkt_to_egress(phys_spec, fl_clone);
}

table t_egr_virtnet {
  reads {
    meta_ctrl.vdev_ID : exact;
    meta_ctrl.virt_egress_spec : exact;
  }
  actions {
    vfwd;
    vmcast;
    vmcast_phys;
    pmcast;
    a_drop;
  }
}

table egress_filter { actions { a_drop; } }

control egress {

  if(meta_ctrl.virt_fwd_flag == 1) { // 850
    apply(t_egr_virtnet); // recirculate, maybe clone_e2e
  }

  else if((standard_metadata.egress_port == standard_metadata.ingress_port) and
          (meta_ctrl.efilter == 1)) { // 851
    apply(egress_filter);
  }

  apply(t_checksum);          // checksums.p4
  apply(t_resize_pr);         // resize_pr.p4
  if(parse_ctrl.numbytes < 40) { // 852
    apply(t_prep_deparse_00_38);  // deparse_prep.p4
  }
  else {
    apply(t_prep_deparse_SEB);
    if(parse_ctrl.numbytes > 40) { // 853
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
