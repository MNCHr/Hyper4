/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

drop.p4: Implements the drop primitive.
*/

action a_drop() {
  drop();
}

table t_drop_11 {
  actions {
    a_drop;
  }
}

table t_drop_12 {
  actions {
    a_drop;
  }
}

table t_drop_21 {
  actions {
    a_drop;
  }
}

table t_drop_22 {
  actions {
    a_drop;
  }
}

table t_drop_31 {
  actions {
    a_drop;
  }
}

table t_drop_32 {
  actions {
    a_drop;
  }
}

table t_drop_41 {
  actions {
    a_drop;
  }
}

table t_drop_42 {
  actions {
    a_drop;
  }
}

table t_drop_51 {
  actions {
    a_drop;
  }
}

table t_drop_52 {
  actions {
    a_drop;
  }
}

table t_drop_61 {
  actions {
    a_drop;
  }
}

table t_drop_62 {
  actions {
    a_drop;
  }
}

table t_drop_71 {
  actions {
    a_drop;
  }
}

table t_drop_72 {
  actions {
    a_drop;
  }
}

control do_drop_11 {
  apply(t_drop_11);
}

control do_drop_12 {
  apply(t_drop_12);
}

control do_drop_21 {
  apply(t_drop_21);
}

control do_drop_22 {
  apply(t_drop_22);
}

control do_drop_31 {
  apply(t_drop_31);
}

control do_drop_32 {
  apply(t_drop_32);
}

control do_drop_41 {
  apply(t_drop_41);
}

control do_drop_42 {
  apply(t_drop_42);
}

control do_drop_51 {
  apply(t_drop_51);
}

control do_drop_52 {
  apply(t_drop_52);
}

control do_drop_61 {
  apply(t_drop_61);
}

control do_drop_62 {
  apply(t_drop_62);
}

control do_drop_71 {
  apply(t_drop_71);
}

control do_drop_72 {
  apply(t_drop_72);
}
