/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

parser.p4: Define various parse functions allowing us to extract a specified
           number of bits from the received packet.
*/

metadata parse_ctrl_t parse_ctrl;
header ext_t ext[100];

parser start {
  set_metadata(parse_ctrl.next_action, PROCEED);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return select(parse_ctrl.numbytes) {
    0 : ingress;
    64 : ingress;
    65 : pr01;
    66 : pr02;
    67 : pr03;
    68 : pr04;
    69 : pr05;
    default : p70;
  }
}

parser pr01 {
  extract(ext[next]);
  return ingress;
}

parser pr02 {
  extract(ext[next]);
  extract(ext[next]);
  return ingress;
}

parser pr03 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return ingress;
}

parser pr04 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return ingress;
}

parser pr05 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return ingress;
}

parser pr06 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return ingress;
}

parser pr07 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return ingress;
}

parser pr08 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return ingress;
}

parser pr09 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return ingress;
}

parser p70 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return select(parse_ctrl.numbytes) {
    70 : ingress;
    71 : pr01;
    72 : pr02;
    73 : pr03;
    74 : pr04;
    75 : pr05;
    76 : pr06;
    77 : pr07;
    78 : pr08;
    79 : pr09;
    default : p80;
  }
}

parser p80 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return select(parse_ctrl.numbytes) {
    80 : ingress;
    81 : pr01;
    82 : pr02;
    83 : pr03;
    84 : pr04;
    85 : pr05;
    86 : pr06;
    87 : pr07;
    88 : pr08;
    89 : pr09;
    default : p90;
  }
}

parser p90 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return select(parse_ctrl.numbytes) {
    90 : ingress;
    91 : pr01;
    92 : pr02;
    93 : pr03;
    94 : pr04;
    95 : pr05;
    96 : pr06;
    97 : pr07;
    98 : pr08;
    99 : pr09;
    default : p100;
  }
}

parser p100 {
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  extract(ext[next]);
  return ingress;
}
