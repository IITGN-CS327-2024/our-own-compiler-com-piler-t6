# Define maximum sizes
NMax = 300  # Maximum input length
RMax = 30  # Maximum number of non-terminals

# Map for non-terminal symbols
mp = {
  'S': 1, 'VD_Content': 2, 
  'X1': 3, 'X2': 4, 
  'X3': 5, 'X4': 6, 
  'X5': 7, 'X6': 8, 
  'X7': 9, 'X8': 10, 
  'X9': 11, 'DataType': 12, 
  'Expression': 13
}

# CFG rules
R = {
  1: [["VD_Content", "X6"]],
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
}

def parser_VD(inp):
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
  ["Identifier", "LPAREN", "floatpoint", "RPAREN", "EQUALS", "float_literal", "SEMICOLON"]
]

for i in inp:
  parser_VD(i)
  print()