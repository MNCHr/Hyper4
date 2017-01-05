/*
Copyright 2013-present Barefoot Networks, Inc. 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#include "includes/headers.p4"
#include "includes/parser.p4"

// 1
action _drop() {
    drop();
}

header_type routing_metadata_t {
    fields {
        nhop_ipv4 : 32;
    }
}

header_type meta_t {
  fields {
    temp : 32;
    do_process : 8;
    //csmask : 768;
  }
}

metadata routing_metadata_t routing_metadata;
metadata meta_t meta;

// 2
action set_nhop(nhop_ipv4, port) {
    modify_field(routing_metadata.nhop_ipv4, nhop_ipv4);
    modify_field(standard_metadata.egress_spec, port);
    add_to_field(ipv4.ttl, -1);
}

table ipv4_lpm {
    reads {
        ipv4.dstAddr : lpm;
    }
    actions {
        set_nhop;
        _drop;
    }
    size: 1024;
}

// 3
action set_dmac(dmac) {
    modify_field(ethernet.dstAddr, dmac);
}

table forward {
    reads {
        routing_metadata.nhop_ipv4 : exact;
    }
    actions {
        set_dmac;
        _drop;
    }
    size: 512;
}

// 4
action rewrite_mac(smac) {
    modify_field(ethernet.srcAddr, smac);
}

table send_frame {
    reads {
        standard_metadata.egress_spec: exact;
    }
    actions {
        rewrite_mac;
        _drop;
    }
    size: 256;
}
/*
action a_is_icmp() {
}

table is_icmp {
  reads {
    meta.do_process : exact;
  }
  actions {
    a_is_icmp;
    _drop;
  }
}
*/

control ingress {
//    apply(is_icmp) {
//      a_is_icmp {
        apply(ipv4_lpm);
        apply(forward);
        apply(send_frame);
//      }
//    }
}

action a_csum() {
  modify_field(meta.temp, ((ipv4.version << 12) + (ipv4.ihl << 8) + ipv4.diffserv));
  modify_field(meta.temp, meta.temp + ipv4.totalLen);
  modify_field(meta.temp, meta.temp + ipv4.identification);
  modify_field(meta.temp, meta.temp + (ipv4.flags << 13 + ipv4.fragOffset));
  modify_field(meta.temp, meta.temp + ((ipv4.ttl << 8) + ipv4.protocol));
  modify_field(meta.temp, meta.temp + (ipv4.srcAddr >> 16));
// This doesn't work; trying to get rid of high bits and just add low bits...
// But high bits are still preserved:
//  modify_field(meta.temp, meta.temp + ((ipv4.srcAddr << 16) >> 16));
  modify_field(meta.temp, meta.temp + (ipv4.srcAddr & 0xFFFF));
  modify_field(meta.temp, meta.temp + (ipv4.dstAddr >> 16));
  modify_field(meta.temp, meta.temp + (ipv4.dstAddr & 0xFFFF));
  modify_field(meta.temp, meta.temp + ((meta.temp >> 16) & 0xFFFF)); // add carry
  modify_field(ipv4.hdrChecksum, ~meta.temp);
  // This works:
//  modify_field(meta.csmask, 0xFFFF << 6);
  // But this doesn't:
  //modify_field(meta.csmask, 0xFFFF000000000000);
}

table csum {
  actions {
    a_csum;
  }
}

control egress {
  apply(csum);
}
