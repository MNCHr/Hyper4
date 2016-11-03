/* simple firewall:
   block by
   (ipv4.srcAddr <&&|"||"> ipv4.dstAddr)
   <&&|"||">
   ( (udp.src_port <&&|"||"> udp.dst_port)
    ||
     (tcp.src_port <&&|"||"> tcp.dst_port) )

   EDIT: Let's keep it simple to start with and simply do TCP/UDP
*/

header_type ethernet_t {
  fields {
    dst : 48;
    src : 48;
    etherType : 16;
  } // 14 B / 112 b
}

header_type ipv4_t {
    fields {
        version : 4;
        ihl : 4;
        diffserv : 8;
        totalLen : 16;
        identification : 16;
        flags : 3;
        fragOffset : 13;
        ttl : 8;
        protocol : 8;
        hdrChecksum : 16;
        srcAddr : 32;
        dstAddr: 32;
    } // 20 B / 160 b
}

header_type tcp_t {
  fields {
    src_port : 16;
    dst_port : 16;
    seq_num : 32;
    ack_num : 32;
    data_offset : 4;
    rsvd : 3;
    flags : 9;
    window_sz : 16;
    checksum : 16;
    urgent_ptr : 16;
  } // 20 B / 160 b
}

header_type udp_t {
  fields {
    src_port : 16;
    dst_port : 16;
    len : 16;
    checksum : 16;
  } // 8 B / 64 b
}
/*
header_type meta_t {
  fields {
    cond_block : 8;  // when block requires match on both ipv4 as well as
                     // tcp/udp fields
  }
}
*/

header ethernet_t ethernet;
header ipv4_t ipv4;
header tcp_t tcp;
header udp_t udp;
// metadata meta_t meta;

parser start {
    extract(ethernet);
    return select(ethernet.etherType) {
      0x0800 : parse_ipv4;
      default : ingress;
  }
}

parser parse_ipv4 {
  extract(ipv4);
  return select(ipv4.protocol) {
    0x06 : parse_tcp;
    0x11 : parse_udp;
    default : ingress;
  }
}

parser parse_tcp {
  extract(tcp);
  return ingress;
}

parser parse_udp {
  extract(udp);
  return ingress;
}

// action ID: 1
action _no_op() {
}

// action ID: 2
action tcp_present() {
}

// action ID: 3
action udp_present() {
}

table is_tcp_or_udp_valid {
  reads {
    tcp : valid;
    udp : valid;
  }
  actions {
    tcp_present;
    udp_present;
    _no_op;
  }
}

// action ID: 4
action _drop() {
  drop();
}
/*
action conditional_block(val) {
  modify_field(meta.cond_block, val);
}
*/
table tcp_block {
  reads {
    tcp.src_port : ternary;
    tcp.dst_port : ternary;
  }
  actions {
    _drop;
    _no_op;
    // conditional_block;
  }
}

table udp_block {
  reads {
    udp.src_port : ternary;
    udp.dst_port : ternary;
  }
  actions {
    _drop;
    _no_op;
    // conditional_block;
  }
}
/*
action ipv4_present() {
}

table is_ipv4_valid {
  reads {
    ipv4 : valid;
  }
  actions {
    ipv4_present;
    _no_op;
  }
}

table ipv4_block {
  reads {
    ipv4.srcAddr : ternary;
    ipv4.dstAddr : ternary;
    meta.cond_block : ternary;
  }
  actions {
    _drop;
    _no_op;
  }
}
*/

// action ID: 5
action a_fwd(port) {
  modify_field(standard_metadata.egress_spec, port);
}

table fwd {
  reads {
    standard_metadata.ingress_port : exact;
  }
  actions {
    a_fwd;
  }
}

control ingress {
  // stage 1
  apply(fwd);
  // stage 2
  apply(is_tcp_or_udp_valid) {
    tcp_present {
      // stage 3
      apply(tcp_block);
    }
    udp_present {
      // stage 4
      apply(udp_block);
    }
  }
/* let's keep it simple for now
  apply(is_ipv4_valid) {
    ipv4_present {
      apply(ipv4_block);
    }
  }
*/
}
