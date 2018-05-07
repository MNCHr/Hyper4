parser start {
  return ingress;
}

action set_egr(egress_spec) {
    modify_field(standard_metadata.egress_spec, egress_spec);
}

table fwd {
    reads {
        standard_metadata.ingress_port : exact;
    }
    actions {
        set_egr;
    }
}

control ingress {
    apply(fwd);
}
