# Define maximum sizes
NMax = 400  # Maximum input length
RMax = 400  # Maximum number of non-terminals

# Initialize dynamic programming table
dp = [[[False for _ in range(RMax)] for _ in range(NMax)] for _ in range(NMax)]

# Map for non-terminal symbols
mp = {
  'S': 1, 
  'VD_Content': 2, 
  'X1': 3, 
  'X2': 4, 
  'X3': 5, 
  'X4': 6, 
  'X5': 7, 
  'X6': 8, 
  'X7': 9, 
  'X8': 10, 
  'X9': 11, 
  'DataType': 12, 
  'Expression': 13, 
  'GivenBlock': 14, 
  'Y1': 15,
  'OtherwiseBlock': 16, 
  'ElseGivenBlock': 17,
  'GivenCondition': 18, 
  'Block': 19,
  'ElseGivenCondition': 20, 
  'Y3': 21, 
  'Y2': 22, 
  'Y4': 23, 
  'Y5': 24, 
  'COND': 25, 
  'Y6': 26, 
  'Y7': 27, 
  'Y8': 28, 
  'Y9': 29, 
  'Operators': 30,
  'Y10': 31, 
  'Z1': 32, 
  'Z2': 33, 
  'Z3': 34, 
  'Z4': 35, 
  'Y11': 36
}

# CFG rules
R = {
  1: [["VD_Content", "X6"], ["GivenBlock", "Y1"], ["GivenBlock", "OtherwiseBlock"]],
  2: [["X1", "Expression"]],
  3: [["X2", "X7"]],
  4: [['X3', 'X8']],
  5: [['X4', 'DataType']],
  6: [['X5', 'X9']],
  7: [["Identifier"]],
  8: [["SEMICOLON"]],
  9: [["EQUALS"]],
  10: [["RPAREN"]],
  11: [["LPAREN"]],
  12: [['integer'], ['floatpoint'] , ['doublepoint']],
  13: [['integer_literal'] , ['float_literal'], ['True'], ['False']],
  14: [["GivenCondition", "Block"]],
  15: [["ElseGivenBlock", "OtherwiseBlock"], ["ElseGivenBlock", "Y1"]],
  16: [["Y11", "Block"]],
  17: [["ElseGivenCondition", "Block"]],
  18: [["Y3", "Y2"]],
  19: [["Z1", "Z2"]],
  20: [["Y4", "Y2"]],
  21: [["GIVEN"]],
  22: [["Y5", "COND"]],
  23: [["ELSEGIVEN"]],
  24: [["LPAREN"]],
  25: [['Y6', 'Y7']],
  26: [['Y8', 'Y9'], ['True'], ['False']],
  27: [['RPAREN']],
  28: [['Identifier']],
  29: [['Operators', 'Y10']],
  30: [['=='], ['>='], ['!=']],
  31: [['integer_literal'], ['float_literal']],
  32: [['Z3', 'Z4']],
  33: [['RCURLY']],
  34: [['LCURLY']],
  35: [['VD_Content', 'X6']],
  36: [['OTHERWISE']]
}


def parser_Conds(inp):
  # Initialize dynamic programming table
  dp = [[[False for _ in range(RMax)] for _ in range(NMax)] for _ in range(NMax)]

  n = len(inp)  # Input length
  m = len(mp)  # Number of non-terminals

  # CYK Algorithm
  # Fill dp table for substrings of length 1 (base case)
  for s in range(1, n+1):
    for v in range(1, m+1):
      for e in R[v]:
        if e[0] == inp[s-1]:  
          dp[1][s][v] = True
          break

  for L in range(2, n+1):
    for s in range(1, n-L+2):
      for p in range(1, L):
        for a in range(1, m+1):
          for e in R[a]:
            if len(e) == 1:  # Skip terminals
              continue
            b = mp[e[0]]
            c = mp[e[1]]
            if dp[p][s][b] and dp[L-p][s+p][c]:
              dp[L][s][a] = True
              break

  # Check if the input stream is in the language
  print("Input Stream Received: ", inp)
  print("Output: Accepted" if dp[n][1][1] else "Syntax Error")

# Input stream of tokens
inp = [
  ["Identifier", "LPAREN", "floatpoint", "RPAREN", "EQUALS", "float_literal"],
  ["Identifier", "LPAREN", "floatpoint", "RPAREN", "EQUALS", "float_literal", "SEMICOLON"],
  [
    "GIVEN", "LPAREN", "True", "RPAREN", "LCURLY", 
    "Identifier", "LPAREN", "floatpoint", "RPAREN", "EQUALS", "float_literal", "SEMICOLON","RCURLY", 
    "ELSEGIVEN", "LPAREN", "False", "RPAREN", "LCURLY", 
    "Identifier", "LPAREN", "floatpoint", "RPAREN", "EQUALS", "float_literal", "SEMICOLON", "RCURLY",
    "OTHERWISE", "LCURLY", 
    "Identifier", "LPAREN", "floatpoint", "RPAREN", "EQUALS", "float_literal", "SEMICOLON", "RCURLY"
  ],
  [
    "GIVEN", "LPAREN", "True", "RPAREN", "LCURLY", 
    "Identifier", "LPAREN", "floatpoint", "RPAREN", "EQUALS", "float_literal", "SEMICOLON","RCURLY", 
    "ELSEGIVEN", "LPAREN", "False", "RPAREN", "LCURLY", 
    "Identifier", "LPAREN", "floatpoint", "RPAREN", "EQUALS", "float_literal", "SEMICOLON", "RCURLY",
    "OTHERWISE", "LCURLY", 
    "Identifier", "LPAREN", "floatpoint", "RPAREN", "EQUALS", "float_literal", "SEMICOLON", 
  ],
]

for i in inp:
  parser_Conds(i)
  print()