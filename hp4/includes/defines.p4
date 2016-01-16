// meta_ctrl.stage
#define INIT	0
#define NORM	1

// meta_ctrl.next_table
#define EXTRACTED_EXACT	1
#define METADATA_EXACT	2
#define STDMETA_EXACT	3

// size of tmeta_8_r, tmeta_16_r registers
#define TMETA_8_CAPACITY	1000
#define TMETA_16_CAPACITY	1000

// meta_ctrl.stage_state
#define COMPLETE	1
#define CONTINUE	2

// stdmeta_match.stdmeta_ID
#define STDMETA_INGRESSPORT	1
#define STDMETA_PACKETLENGTH	2
#define STDMETA_INSTTYPE	3
#define STDMETA_PARSERSTAT	4
#define STDMETA_PARSERERROR	5

// meta_primitive_metadata.type
#define A_MODIFY_FIELD		0
#define A_ADD_HEADER		1
#define A_COPY_HEADER		2
#define A_REMOVE_HEADER		3
#define A_MODIFY_FIELD_WITH_HBO	4
#define A_TRUNCATE		5
#define A_DROP			6
#define A_NO_OP			7
#define A_PUSH			8
#define A_POP			9
#define A_COUNT			10
#define A_METER			11
#define A_GENERATE_DIGEST	12
#define A_RECIRCULATE		13
#define A_RESUBMIT		14
#define A_CLONE_INGRESS_INGRESS	15
#define A_CLONE_EGRESS_INGRESS	16
#define A_CLONE_INGRESS_EGRESS	17
#define A_CLONE_EGRESS_EGRESS	18