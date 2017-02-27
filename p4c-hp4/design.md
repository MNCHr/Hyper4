# HP4C (HyPer4 Compiler) Design

## Current Effort

Need to revise the design to account for parse function return statements that include selection criteria.  We need a dictionary of the form {(pc\_state, fieldname): offset} mapping offsets to every field for every parse control state.  This is required for tset\_control because set\_next\_action needs the next\_action parameter, which is one of INSPECT\_SEB | INSPECT\_20\_29 | ... | INSPECT\_90\_99.  

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
* tset\_context
* tset\_virtnet
* tset\_recirc
* tset\_control
* tset\_inspect\_SEB
* tset\_inspect\_20\_29
* ...
* tset\_pr\_SEB
* tset\_pr\_20\_39
* ...
* tset\_pipeline

Let's look at the inputs/outputs for each table separately.

tset\_context:
- input:
  - We don't know which ports should be assigned to this program at compile time; output [PPORT] and let the loader (hp4l) handle replicating commands for every physical port that applies.
  - The virtual ingress port used by this program should also be supplied at load time; output [VPORT_0] and let the loader substitute the actual number.  We *could* change this to VPORT_INGRESS and let the loader pick from any of the virtual ports available via comman option.  That seems unnecessary though.
  - Program ID also.
- output:
  table\_add tset\_context set\_program [PPORT] => [program ID] [virt\_ingress\_port]

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

- SKIP FOR NOW: set\_next\_action\_chg\_program and extract\_more\_chg\_program
- input:
  - We must assign at least one, but perhaps more than one, pc.state to each P4 parse state.  '0' for start.  Within the set of pc.states associated with a parse state, each corresponds to a different path taken through the parse tree to arrive at the parse state.
  - Determine byte requirements for each path (inc. partial paths) through the parse tree:
    explicit = {(pc.state, [start, ..., state immediately preceding pc.state]): numbytes}
    total = {(pc.state, [start, ..., state immediately preceding pc.state]): numbytes}
    # 'total' includes current(X, Y)-imposed extraction requirements.
    # Do in two steps.  First, explicit, then total.
  - Use total to populate {(pc.state, numbytes): next\_numbytes} dictionary.
  - 

- tasks
  1. Figure out whether output is set\_next\_action or extract\_more.
- output:

  table\_add tset\_control set\_next\_action [program ID] [numbytes] [pc.state] => [next\_action] [next pc.state]
  OR
  table\_add tset\_control extract\_more [program ID] [numbytes] [pc.state] => [next numbytes]

  - We need to produce one table entry for every possible number of bytes that could have been extracted before arriving at this parse state.  Each entry will either have action = set\_next\_action or action = extract\_more as follows:
      If the parse state does not include extraction nor current(X,Y) beyond what has been extracted:
        If the parse state includes a select expression in the return statement:
          action: set\_next\_action; [next\_action]: INSPECT
        Else:
          action: set\_next\_action; [next\_action]: PROCEED
      Else:
        action: extract\_more;
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
