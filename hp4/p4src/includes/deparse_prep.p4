/*
David Hancock
FLUX Research Group
University of Utah
dhancock@cs.utah.edu

HyPer4: A P4 Program to Run Other P4 Programs

deparse_prep.p4: Prepare packet for deparsing
*/

action a_prep_deparse_SEB() {
  modify_field(ext_first.data, (extracted.data >> 288));
}

table t_prep_deparse_SEB {
  actions {
    a_prep_deparse_SEB;
  }
}

action a_prep_deparse_64_79() {
  modify_field(ext[0].data, (extracted.data >> 280) & 0xFF);
  modify_field(ext[1].data, (extracted.data >> 272) & 0xFF);
  modify_field(ext[2].data, (extracted.data >> 264) & 0xFF);
  modify_field(ext[3].data, (extracted.data >> 256) & 0xFF);
  modify_field(ext[4].data, (extracted.data >> 248) & 0xFF);
  modify_field(ext[5].data, (extracted.data >> 240) & 0xFF);
  modify_field(ext[6].data, (extracted.data >> 232) & 0xFF);
  modify_field(ext[7].data, (extracted.data >> 224) & 0xFF);
  modify_field(ext[8].data, (extracted.data >> 216) & 0xFF);
  modify_field(ext[9].data, (extracted.data >> 208) & 0xFF);
  modify_field(ext[10].data, (extracted.data >> 200) & 0xFF);
  modify_field(ext[11].data, (extracted.data >> 192) & 0xFF);
  modify_field(ext[12].data, (extracted.data >> 184) & 0xFF);
  modify_field(ext[13].data, (extracted.data >> 176) & 0xFF);
  modify_field(ext[14].data, (extracted.data >> 168) & 0xFF);
  modify_field(ext[15].data, (extracted.data >> 160) & 0xFF);
}

table t_prep_deparse_64_79{
  actions {
    a_prep_deparse_64_79;
  }
}

action a_prep_deparse_80_99() {
  modify_field(ext[16].data, (extracted.data >> 152) & 0xFF);
  modify_field(ext[17].data, (extracted.data >> 144) & 0xFF);
  modify_field(ext[18].data, (extracted.data >> 136) & 0xFF);
  modify_field(ext[19].data, (extracted.data >> 128) & 0xFF);
  modify_field(ext[20].data, (extracted.data >> 120) & 0xFF);
  modify_field(ext[21].data, (extracted.data >> 112) & 0xFF);
  modify_field(ext[22].data, (extracted.data >> 104) & 0xFF);
  modify_field(ext[23].data, (extracted.data >> 96) & 0xFF);
  modify_field(ext[24].data, (extracted.data >> 88) & 0xFF);
  modify_field(ext[25].data, (extracted.data >> 80) & 0xFF);
  modify_field(ext[26].data, (extracted.data >> 72) & 0xFF);
  modify_field(ext[27].data, (extracted.data >> 64) & 0xFF);
  modify_field(ext[28].data, (extracted.data >> 56) & 0xFF);
  modify_field(ext[29].data, (extracted.data >> 48) & 0xFF);
  modify_field(ext[30].data, (extracted.data >> 40) & 0xFF);
  modify_field(ext[31].data, (extracted.data >> 32) & 0xFF);
  modify_field(ext[32].data, (extracted.data >> 24) & 0xFF);
  modify_field(ext[33].data, (extracted.data >> 16) & 0xFF);
  modify_field(ext[34].data, (extracted.data >> 8) & 0xFF);
  modify_field(ext[35].data, (extracted.data >> 0) & 0xFF);
}

table t_prep_deparse_80_99{
  actions {
    a_prep_deparse_80_99;
  }
}
