parser start {
  return ingress;
}

action ingr_one() {
}

action ingr_two() {
}

action ingr_three() {
}

table read_ingress {
  reads {
    standard_metadata.ingress_port : exact;
  }
  actions {
    ingr_one;
    ingr_two;
    ingr_three;
  }
}

action a_fwd_one() {
  modify_field(standard_metadata.egress_spec, 1);
}

table fwd_one {
  actions {
    a_fwd_one;
  }
}

action a_fwd_two() {
  modify_field(standard_metadata.egress_spec, 2);
}

table fwd_two {
  actions {
    a_fwd_two;
  }
}

action _drop() {
  drop();
}

table t_drop {
  actions {
    _drop;
  }
}

control ingress {
  apply(read_ingress) {
    ingr_one {
      apply(fwd_two);
    }
    ingr_two {
      apply(fwd_one);
    }
    ingr_three {
      apply(t_drop);
    }
  }
}
