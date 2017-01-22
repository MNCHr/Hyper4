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

header ethernet_t ethernet;
header ipv4_t ipv4;
header tcp_t tcp;
header udp_t udp;

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
action tcp_not_present() {
}

// action ID: 4
action udp_present() {
}

// action ID: 5
action udp_not_present() {
}

table is_tcp_valid {
  reads {
    tcp : valid;
  }
  actions {
    tcp_present;
    tcp_not_present;
    _no_op;
  }
}

table is_udp_valid {
  reads {
    udp : valid;
  }
  actions {
    udp_present;
    udp_not_present;
    _no_op;
  }
}

// action ID: 6
action _drop() {
  drop();
}

table tcp_src_block {
  reads {
    tcp.src_port : exact;
  }
  actions {
    _drop;
    _no_op;
  }
}

table tcp_dst_block {
  reads {
    tcp.dst_port : exact;
  }
  actions {
    _drop;
    _no_op;
  }
}

table udp_src_block {
  reads {
    udp.src_port : exact;
  }
  actions {
    _drop;
    _no_op;
  }
}

table udp_dst_block {
  reads {
    udp.dst_port : exact;
  }
  actions {
    _drop;
    _no_op;
  }
}

// action ID: 7
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
  apply(is_tcp_valid) {
    tcp_present {
      // stage 3
      apply(tcp_src_block) {
        _no_op {
          // stage 4
          apply(tcp_dst_block);
        }
      }
    }
    tcp_not_present {
      // stage 5
      apply(is_udp_valid) {
        udp_present {
          // stage 6
          apply(udp_src_block) {
            _no_op {
              // stage 7
              apply(udp_dst_block);
            }
          }
        }
      }
    }
  }
}
