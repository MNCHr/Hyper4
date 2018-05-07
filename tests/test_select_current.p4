# define IN_1 0xF0
# define IN_2 0xF1

header_type ethernet_t {
    fields {
        dstAddr : 48;
        srcAddr : 48;
        etherType : 16;
    }
}  

header_type meta_t {
  fields {
    reslt : 8;
  }
}

header ethernet_t ethernet;
metadata meta_t meta;

parser start {
  return select(current(0, 8)) {
    IN_1: parse_one;
    IN_2: parse_two;
    default: ingress;
  }
}

parser parse_one {
  extract(ethernet);
  set_metadata(meta.reslt, 1);
  return ingress;
}

parser parse_two {
  extract(ethernet);
  set_metadata(meta.reslt, 2);
  return ingress;
}

action res_one() {
}

action res_two() {
}  

table check_reslt {
  reads {
    meta.reslt : exact;
  }
  actions {
    res_one;
    res_two;
  }
}

action a_mod_src_one() {
  modify_field(ethernet.srcAddr, 0x010101010101);
}

table mod_src_one {
  actions {
    a_mod_src_one;
  }
}

action a_mod_src_two() {
  modify_field(ethernet.srcAddr, 0x020202020202);
}

table mod_src_two {
  actions {
    a_mod_src_two;
  }
} 

control ingress {
  apply(check_reslt) {
    res_one {
      apply(mod_src_one);
    }
    res_two {
      apply(mod_src_two);
    }
  }
}
