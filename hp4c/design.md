# HP4C (HyPer4 Compiler) Design

## Contents
* [Overview](#Overview)
* [Data Structures](#Data Structures)
* [Parsing and Setup](#Parsing and Setup)
* Stages

More sections will be added as the work progresses.  The strategy is to tackle all of the commands associated with the tables in pieces, according to the header file in which the tables are defined.

## Overview

HP4C accepts a .p4 and converts it to a .hp4t, or a template file preparatory to the final instantiation of a set of commands (a .hp4) to send to a switch running HyPer4.  It is the job of HP4L ('L' for 'Loader') to convert the .hp4t to the .hp4.

### Workflow

1. Initialize data structures
2. Build the HLIR
3. Collect all parse states  
   Associate a UID with every parse state in the HLIR
4. Collect all actions  
   Associate a UID with every action in the HLIR
5. Collect all tables  
   Associate a UID with every table in the HLIR and establish a sequential order for table emulation in HyPer4.
6. Parsing and Setup  
   a. Identify _parse control_ states (not to be confused with _parse states_ in the HLIR - each HLIR _parse state_ may be associated with multiple _parse control_ states, as a _parse control_ state identifies not only a specific _parse state_, but how the parser arrived at that state) required.  This activity prepares HP4C to generate tset\_control and tset\_inspect\_XX commands.  
   b. Output tset\_control and tset\_inspect\_XX commands?
7. ...

### Limitations

HP4C does not yet have a clear path for:
* conditionals in control functions
* multiple match fields in tables

## Data Structures

### actionUIDs
Dictionary associating each action in the .p4 with a unique number referred to in HP4 source as the _action\_ID_ field in the _meta\_primitive\_state_ metadata header (set by match::tXX\_\[match type\]->init\_program\_state and stages::tstgXY\_update\_state->update\_state, read by stages::tstgXY\_update\_state).

### parseStateUIDs
Dictionary associating each parser function in the .p4 with a unique number referred to in HP4 source as the _state_ field in the _parse\_ctrl_ metadata header (set and read by setup::tset\_control|tset\_inspect\_XX->set\_next\_action|set\_next\_action\_chg\_program, also read by setup::tset\_pipeline).

### tableUIDs
Ordered dictionary associating each table in the .p4 with a unique number.  This is being populated but it is not clear how it will be used.

### bits\_needed\_local
Dictionary associating each parse state in the .p4 with a (numbits, maxcurr) tuple.  This dictionary stores the local bit requirement for the parse state, where maxcurr tracks the number of bits required by all uses of the 'current' function, and numbits is the total, including maxcurr as well as bits required by all invocations of 'extract'.

### bits\_needed\_total
Dictionary associating each possible (parse state, tuple of preceding states) tuple in the .p4 with a total number of bits that should be extracted from the packet to handle the parse state.  Inuitively, every path that ends up at the parse state could have a different bit extraction requirement as identified in bits\_needed\_local.

### tset\_control\_state\_nextbits

### commands

## Parsing and Setup

Tables:
* tset_context
* tset_virtnet
* tset_recirc
* tset_control
* tset_inspect_SEB
* tset_inspect_20_29
* ...
* tset_pr_SEB
* tset_pr_20_39
* ...
* tset_pipeline

Let's look at the inputs/outputs for each table separately.

tset_context:
- input:
  - Need to know which ports should be assigned to this program.  But we should not require this set of ports to be specified at compile time.  This will be supplied at load time.  Our requirement is to produce a line in hp4t that may become multiple lines, one for every ingress port specified at load time (just like the program ID).
  - The virtual ingress port used by this program should also be supplied at load time.
  - Program ID also.
- output:
  [+ dup sm.ingress_port, program ID, virt_ingress_port +]
  table_add tset_context set_program [sm.ingress_port] => [program ID] [virt_ingress_port]
  [+ enddup +]

tset_virtnet: SKIP FOR NOW

tset_recirc: SKIP FOR NOW

tset_control:

	table tset_control {
	  reads {
	    meta_ctrl.program : exact;
	    parse_ctrl.numbytes : exact;
	    parse_ctrl.state : exact;
	  }
	  actions {
	    set_next_action;
	    set_next_action_chg_program;
	    extract_more;
	    extract_more_chg_program;
	  }
	}

- SKIP FOR NOW: set_next_action_chg_program and extract_more_chg_program
- input:
  - We must assign a pc.state to each parse function.  '0' for start.
  - Determine byte requirements for each path (inc. partial paths) through the parse tree:
    explicit = {(pc.state, [start, ..., state immediately preceding pc.state]): numbytes}
    total = {(pc.state, [start, ..., state immediately preceding pc.state]): numbytes}
    # 'total' includes current(X, Y)-imposed extraction requirements.
    # Do in two steps.  First, explicit.
    def exp_parse_tree_traverse(pc.state, list_of_preceding_states, so_far):
      if pc.state == 'ingress':
        return
      numbytes = so_far
      for extract_statement in call_sequence:
        numbytes += extract_statement.header.total_width (e.g., for field in header, += field.width)
      explicit[(pc.state, list_of_preceding_states)] = numbytes
      for next_state in pc.state.return_select_exp:
        exp_parse_tree_traverse(next_state, list_of_preceding_states.append(pc.state), numbytes)
    def total_parse_tree_traverse(pc.state, list_of_preceding_states):
      if pc.state == 'ingress':
        return
      numbytes = explicit[(pc.state, list_of_preceding_states)]

      maxcurr = 0
      for current_exp in return statement:
        if current_exp.offset + current_exp.width > maxcurr:
          maxcurr = current_exp.offset + current_exp.width
      numbytes += maxcurr

      total[(pc.state, list_of_preceding_states)] = numbytes
      for next_state in pc.state.return_select_exp:
        total_parse_tree_traverse(next_state, list_of_preceding_states.append(pc.state))
    # Start at 'start'.  E.g., exp_parse_tree_traverse(h.p4_parse_states['start'], [], 0)
    # Then total_parse_tree_traverse(h.p4_parse_states['start'], [], 0)
  - Use total to populate {(pc.state, numbytes): next_numbytes} dictionary

- tasks
  1. Figure out whether output is set_next_action or extract_more.
- output:

  table_add tset_control set_next_action [program ID] [numbytes] [pc.state] => [next_action] [next pc.state]
  OR
  table_add tset_control extract_more [program ID] [numbytes] [pc.state] => [next numbytes]

  - We need to produce one table entry for every possible number of bytes that could have been extracted before arriving at this parse state.  Each entry will either have action = set_next_action or action = extract_more as follows:
      If the parse state does not include extraction nor current(X,Y) beyond what has been extracted:
        If the parse state includes a select expression in the return statement:
          action: set_next_action; [next_action]: INSPECT
        Else:
          action: set_next_action; [next_action]: PROCEED
      Else:
        action: extract_more;
		[next numbytes]: (pc.state, numbytes) should be used as a key to look up the value

At the end, we could have multiple possible offsets into extracted.data where a particular field may be stored.  This could multiply the number of table entries required where such table entries include a match for such a field.  And it would mean the validbits or final parse_ctrl.state must be included in the reads sections of tables implementing the ingress pipeline.

tset_inspect_SEB:
- input:
  parser p {
    // ...
    return select(ext.field) {
      0x0800: return q;
      0x0801: return r;
      default: return ingress;
    }
  }
  or
  parser p {
    // ...
    return select(current(0, 16)) {
      0x0800: return q;
      0x0801: return r;
      default: return ingress;
    }
  - the field_or_data_ref in the select expression (e.g., ext.field or current(0, 16) above) must be mapped to the ext[] 
- output:
  table_add tset_inspect_SEB
