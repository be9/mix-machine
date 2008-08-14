
# tables are copied from mdk manual (10, 20, 21 = delta, sigma, pi)
ord_table = {
    " ":  0,      "A":  1,      "B":  2,      "C":  3,
    "D":  4,      "E":  5,      "F":  6,      "G":  7,
    "H":  8,      "I":  9,      "~":  10,     "J":  11,
    "K":  12,     "L":  13,     "M":  14,     "N":  15,
    "O":  16,     "P":  17,     "Q":  18,     "R":  19,
    "[":  20,     "#":  21,     "S":  22,     "T":  23,
    "U":  24,     "V":  25,     "W":  26,     "X":  27,
    "Y":  28,     "Z":  29,     "0":  30,     "1":  31,
    "2":  32,     "3":  33,     "4":  34,     "5":  35,
    "6":  36,     "7":  37,     "8":  38,     "9":  39,
    ".":  40,     ",":  41,     "(":  42,     ")":  43,
    "+":  44,     "-":  45,     "*":  46,     "/":  47,
    "=":  48,     "$":  49,     "<":  50,     ">":  51,
    "@":  52,     ";":  53,     ":":  54,     "'":  55
}
chr_table = [x for x in " ABCDEFGHI~JKLMNOPQR[#STUVWXYZ0123456789.,()+-*/=$<>@;:'"]
charset_len = len(chr_table)

def ord(char, default = None):
  """Char -> Int"""
  return ord_table.get(char, default)

def chr(num, default = None):
  """Int -> Char"""
  return chr_table[num] if 0 <= num < charset_len else default
