/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

defines.p4: Define constants
*/

// extracted.data field width
#define EXTRACTED_SIZE	800

// value for sm.egress_spec indicating virt net
#define VIRT_NET 65

// parse_ctrl.next_action
#define PROCEED				0
#define PARSE_SELECT_00_19 1
#define PARSE_SELECT_20_29 2
#define PARSE_SELECT_30_39 3
#define PARSE_SELECT_40_49 4
#define PARSE_SELECT_50_59 5
#define PARSE_SELECT_60_69 6
#define PARSE_SELECT_70_79 7
#define PARSE_SELECT_80_89 8
#define PARSE_SELECT_90_99 9
#define EXTRACT_MORE	10

// meta_ctrl.stage
#define INIT	0
#define NORM	1
#define VFWD  2

// meta_ctrl.next_table
#define DONE            0
#define EXTRACTED_EXACT	1
#define METADATA_EXACT	2
#define STDMETA_EXACT	  3 // deprecated
#define EXTRACTED_VALID 4
#define STDMETA_INGRESS_PORT_EXACT 	5
#define STDMETA_PACKET_LENGTH_EXACT 6
#define STDMETA_INSTANCE_TYPE_EXACT 7
#define STDMETA_EGRESS_SPEC_EXACT		8
#define METADATA_TERNARY						9
#define EXTRACTED_TERNARY						10
#define MATCHLESS				99

// meta_ctrl.stdmeta_ID
#define STDMETA_INGRESS_PORT	1
#define STDMETA_PACKET_LENGTH	2
#define STDMETA_INSTANCE_TYPE	3
#define STDMETA_PARSERSTAT	  4
#define STDMETA_PARSERERROR	  5
#define STDMETA_EGRESS_SPEC	  6

// meta_primitive_state.primitive
#define A_ADD_HEADER		        1
#define A_COPY_HEADER		        2
#define A_REMOVE_HEADER		      3
#define A_MODIFY_FIELD_WITH_HBO	4
#define A_TRUNCATE		          5
#define A_DROP			            6
#define A_NO_OP			            7
#define A_PUSH			            8
#define A_POP			              9
#define A_COUNT			            10
#define A_METER			            11
#define A_GENERATE_DIGEST	      12
#define A_RECIRCULATE		        13
#define A_RESUBMIT		          14
#define A_CLONE_INGRESS_INGRESS	15
#define A_CLONE_EGRESS_INGRESS	16
#define A_CLONE_INGRESS_EGRESS	17
#define A_CLONE_EGRESS_EGRESS	  18
#define A_MULTICAST		          19
#define A_MATH_ON_FIELD		      20
#define A_MODIFY_FIELD	      	21
#define A_MODIFY_FIELD_RNG_U		22
#define A_BIT_XOR								23
