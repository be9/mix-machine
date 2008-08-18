def disasm(word):
  """Returns (instruction_name, address, index, field)"""
  c = word[5]
  f = word[4]
  instruction_name = codes.get(c, codes.get((c,f), None))
  return (instruction_name, int(word[0:2]), word[3], word[4])

def disasm2str(word, separator):
  instr, _, ind, f = disasm(word)

  if instr is None:
    return None

  is_field_fixed = codes.get((word[5], f)) is not None

  # addr_str = str(int(word[0:2])) - this variant doesn't show "-0"
  addr_str = ("-" if word[0] == -1 else "") + str(abs(int(  word[1:2]  )))

  ind_str = ","+str(ind) if ind != 0 else ""

  if not is_field_fixed:
    if instr in instructions_with_field_spec:
      if instr == "stj" and f == 2: # 2 = (0:2)
        f_str = "" # don't show f_part for STJ, because it's default
      elif f == 5: # 5 = (0:5) - default for all but STJ
        f_str = "" # don't show f_part (it's default for this instruction)
      else:
        f_str = "(%i:%i)" % (f/8, f%8)

    else:
      f_str = "("+str(f)+")" if f != 0 else ""
  else:
    f_str = "" # don't show f_part for instructions with fixed field

  return "".join((separator,
                  instr.upper(),
                  separator,
                  addr_str,
                  ind_str,
                  f_str))


instructions_with_field_spec = ( # such as (3:4)
  "add",  "sub",  "mul",  "div",
  "lda",  "ld1",  "ld2",  "ld3",  "ld4",  "ld5",  "ld6",  "ldx",
  "ldan", "ld1n", "ld2n", "ld3n", "ld4n", "ld5n", "ld6n", "ldxn",
  "sta",  "st1",  "st2",  "st3",  "st4",  "st5",  "st6",  "stx",  "stj",  "stz",
  "cmpa", "cmp1", "cmp2", "cmp3", "cmp4", "cmp5", "cmp6", "cmpx"
)

codes = {
  ( 0   ) : "nop",
  ( 1   ) : "add",
  ( 2   ) : "sub",
  ( 3   ) : "mul",
  ( 4   ) : "div",
  ( 5, 0) : "num",
  ( 5, 1) : "char",
  ( 5, 2) : "hlt",
  ( 6, 0) : "sla",
  ( 6, 1) : "sra",
  ( 6, 2) : "slax",
  ( 6, 3) : "srax",
  ( 6, 4) : "slc",
  ( 6, 5) : "src",
  ( 7   ) : "move",
  ( 8   ) : "lda",
  ( 9   ) : "ld1",
  (10   ) : "ld2",
  (11   ) : "ld3",
  (12   ) : "ld4",
  (13   ) : "ld5",
  (14   ) : "ld6",
  (15   ) : "ldx",
  (16   ) : "ldan",
  (17   ) : "ld1n",
  (18   ) : "ld2n",
  (19   ) : "ld3n",
  (20   ) : "ld4n",
  (21   ) : "ld5n",
  (22   ) : "ld6n",
  (23   ) : "ldxn",
  (24   ) : "sta",
  (25   ) : "st1",
  (26   ) : "st2",
  (27   ) : "st3",
  (28   ) : "st4",
  (29   ) : "st5",
  (30   ) : "st6",
  (31   ) : "stx",
  (32   ) : "stj",
  (33   ) : "stz",
  (34   ) : "jbus",
  (35   ) : "ioc",
  (36   ) : "in_",
  (37   ) : "out",
  (38   ) : "jred",
  (39, 0) : "jmp",
  (39, 1) : "jsj",
  (39, 2) : "jov",
  (39, 3) : "jnov",
  (39, 4) : "jl",
  (39, 5) : "je",
  (39, 6) : "jg",
  (39, 7) : "jge",
  (39, 8) : "jne",
  (39, 9) : "jle",
  (40, 0) : "jan",
  (40, 1) : "jaz",
  (40, 2) : "jap",
  (40, 3) : "jann",
  (40, 4) : "janz",
  (40, 5) : "janp",
  (41, 0) : "j1n",
  (41, 1) : "j1z",
  (41, 2) : "j1p",
  (41, 3) : "j1nn",
  (41, 4) : "j1nz",
  (41, 5) : "j1np",
  (42, 0) : "j2n",
  (42, 1) : "j2z",
  (42, 2) : "j2p",
  (42, 3) : "j2nn",
  (42, 4) : "j2nz",
  (42, 5) : "j2np",
  (43, 0) : "j3n",
  (43, 1) : "j3z",
  (43, 2) : "j3p",
  (43, 3) : "j3nn",
  (43, 4) : "j3nz",
  (43, 5) : "j3np",
  (44, 0) : "j4n",
  (44, 1) : "j4z",
  (44, 2) : "j4p",
  (44, 3) : "j4nn",
  (44, 4) : "j4nz",
  (44, 5) : "j4np",
  (45, 0) : "j5n",
  (45, 1) : "j5z",
  (45, 2) : "j5p",
  (45, 3) : "j5nn",
  (45, 4) : "j5nz",
  (45, 5) : "j5np",
  (46, 0) : "j6n",
  (46, 1) : "j6z",
  (46, 2) : "j6p",
  (46, 3) : "j6nn",
  (46, 4) : "j6nz",
  (46, 5) : "j6np",
  (47, 0) : "jxn",
  (47, 1) : "jxz",
  (47, 2) : "jxp",
  (47, 3) : "jxnn",
  (47, 4) : "jxnz",
  (47, 5) : "jxnp",
  (48, 0) : "inca",
  (48, 1) : "deca",
  (48, 2) : "enta",
  (48, 3) : "enna",
  (49, 0) : "inc1",
  (49, 1) : "dec1",
  (49, 2) : "ent1",
  (49, 3) : "enn1",
  (50, 0) : "inc2",
  (50, 1) : "dec2",
  (50, 2) : "ent2",
  (50, 3) : "enn2",
  (51, 0) : "inc3",
  (51, 1) : "dec3",
  (51, 2) : "ent3",
  (51, 3) : "enn3",
  (52, 0) : "inc4",
  (52, 1) : "dec4",
  (52, 2) : "ent4",
  (52, 3) : "enn4",
  (53, 0) : "inc5",
  (53, 1) : "dec5",
  (53, 2) : "ent5",
  (53, 3) : "enn5",
  (54, 0) : "inc6",
  (54, 1) : "dec6",
  (54, 2) : "ent6",
  (54, 3) : "enn6",
  (55, 0) : "incx",
  (55, 1) : "decx",
  (55, 2) : "entx",
  (55, 3) : "ennx",
  (56   ) : "cmpa",
  (57   ) : "cmp1",
  (58   ) : "cmp2",
  (59   ) : "cmp3",
  (60   ) : "cmp4",
  (61   ) : "cmp5",
  (62   ) : "cmp6",
  (63   ) : "cmpx",
}
