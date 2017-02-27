header_type ethernet_t {
    fields {
        dstAddr : 48;
        srcAddr : 48;
        etherType : 16;
    }
}

header_type intrinsic_metadata_t {
  fields {
        mcast_grp : 4;
        egress_rid : 4;
        mcast_hash : 16;
        lf_field_list : 32;
        resubmit_flag : 16;
        recirculate_flag : 16;
  }
}

header ethernet_t ethernet;
metadata intrinsic_metadata_t intrinsic_metadata;

parser start {
  extract(ethernet);
  return ingress;
}

// .hp4 ACTION_ID: 1
action _drop() {
  drop();
}

// .hp4 ACTION_ID: 2
action forward(port) {
  modify_field(standard_metadata.egress_spec, port);
}

// .hp4 ACTION_ID: 3
action broadcast(mcast) {
  modify_field(intrinsic_metadata.mcast_grp, mcast);
}

table dmac {
  reads {
      ethernet.dstAddr : exact;
  }
  actions {
      forward;
      broadcast;
      _drop;
  }
  size : 512;
}

control ingress {
  apply(dmac);
}

table filter_egress {
  actions {
    _drop;
  }
}

control egress {
  if(standard_metadata.egress_port == standard_metadata.ingress_port) {
    apply(filter_egress);
  }
}
