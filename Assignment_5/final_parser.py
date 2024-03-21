# Define maximum sizes
NMax = 400  # Maximum input length
RMax = 400  # Maximum number of non-terminals

# Initialize dynamic programming table
dp = [[[False for _ in range(RMax)] for _ in range(NMax)] for _ in range(NMax)]

mp = {
  'Program': 1,
 'Statements': 2,
 'MoreStatements': 3,
 'Statement': 4,
 'VariableDecl': 5,
 'VariableDecl1': 6,
 'VariableDecl2': 7,
 'VariableDecl3': 8,
 'VariableDecl4': 9,
 'VariableDecl5': 10,
 'VariableDecl6': 11,
 'ImmutableVariableDecl': 12,
 'ImmutableVariableDecl1': 13,
 'ImmutableVariableDecl2': 14,
 'ImmutableVariableDecl3': 15,
 'ImmutableVariableDecl4': 16,
 'ImmutableVariableDecl5': 17,
 'ImmutableVariableDecl6': 18,
 'ImmutableVariableDecl7': 19,
 'Expression': 20,
 'SimpleExpression': 21,
 'BinaryExpression': 22,
 'BinaryOperatorTerm': 23,
 'Term': 24,
 'Term1': 25,
 'Term2': 26,
 'Term3': 27,
 'Term4': 28,
 'Factor': 29,
 'Anytext1': 30,
 'Anytext2': 31,
 'Anytext3': 32,
 'Anytext4': 33,
 'AnyText': 34,
 'AnyChar': 35,
 'LogicalExpr': 36,
 'LogicalExpr1': 37,
 'LogicalOperator': 38,
 'Number': 39,
 'FloatNumber': 40,
 'FloatNumber1': 41,
 'Literal': 42,
 'Literal1': 43,
 'AccessExpression': 44,
 'AccessOperator': 45,
 'LNUMBERR': 46,
 'LNUMBERCNUMBERR': 47,
 'LNUMBERR1': 48,
 'LNUMBERR2': 49,
 'LNUMBERR3': 50,
 'LNUMBERCNUMBERR1': 51,
 'LN': 52,
 'LN1': 53,
 'LNUMBERCNUMBERR2': 54,
 'DictionaryAccess': 55,
 'DictionaryAccess1': 56,
 'DictionaryAccess2': 57,
 'DictionaryAccess3': 58,
 'DictionaryAccess4': 59,
 'FunctionDecl': 60,
 'FunctionDecl1': 61,
 'FunctionDecl2': 62,
 'FunctionDecl3': 63,
 'FunctionDecl4': 64,
 'FunctionName': 65,
 'Arguments': 66,
 'ArgumentsRest': 67,
 'COMMAArgument': 68,
 'Argument': 69,
 'Argument1': 70,
 'Argument2': 71,
 'Argument3': 72,
 'Conditional': 73,
 'Conditional1': 74,
 'GivenClause': 75,
 'GivenClause1': 76,
 'GivenClause2': 77,
 'GivenClause3': 78,
 'ElseGivenClause': 79,
 'ElseGivenClause1': 80,
 'ElseGivenClause2': 81,
 'ElseGivenClause3': 82,
 'OtherwiseClause': 83,
 'Loop': 84,
 'WhileLoop': 85,
 'WhileLoop1': 86,
 'WhileLoop2': 87,
 'WhileLoop3': 88,
 'WhileLoop4': 89,
 'IterateLoop': 90,
 'IterateLoop1': 91,
 'IterateLoop2': 92,
 'IterateLoop3': 93,
 'IterateLoop4': 94,
 'IterateLoop5': 95,
 'IterateLoop6': 96,
 'IterateLoop7': 97,
 'IterateLoop8': 98,
 'IterateLoop9': 99,
 'IterateLoop10': 100,
 'IterateLoop11': 101,
 'IterateLoop12': 102,
 'RangeLoop': 103,
 'RangeLoop1': 104,
 'RangeLoop2': 105,
 'RangeLoop3': 106,
 'RangeLoop4': 107,
 'RangeLoop5': 108,
 'RangeLoop6': 109,
 'RangeLoop7': 110,
 'RangeLoop8': 111,
 'RangeLoop9': 112,
 'RangeLoop10': 113,
 'RangeLoop11': 114,
 'RangeLoop12': 115,
 'RangeLoop13': 116,
 'RangeLoop14': 117,
 'RangeLoop15': 118,
 'RangeLoop16': 119,
 'RangeLoop17': 120,
 'RangeLoop18': 121,
 'LoopStatements': 122,
 'LoopStatement': 123,
 'LoopInterrupt': 124,
 'LoopResume': 125,
 'ExceptionHandling': 126,
 'StriveBlock': 127,
 'CaptureBlock': 128,
 'CaptureBlockOption': 129,
 'CaptureWithParentheses': 130,
 'CaptureWithoutParentheses': 131,
 'VariableNameBlock': 132,
 'RPARENBlock': 133,
 'UnaryOperation': 134,
 'UnaryOperation1': 135,
 'UnaryOperationEnd': 136,
 'Assignment': 137,
 'Assignment1': 138,
 'Assignment2': 139,
 'AssignmentOperator': 140,
 'ArrayDecl': 141,
 'ArrayDecl1': 142,
 'ArrayDecl2': 143,
 'ArrayDecl3': 144,
 'ArrayDecl4': 145,
 'ArrayDecl5': 146,
 'ArrayDecl6': 147,
 'ArrayDecl7': 148,
 'ArrayDecl8': 149,
 'ArrayDecl9': 150,
 'ListDecl': 151,
 'ListDecl1': 152,
 'ListDecl2': 153,
 'ListDecl3': 154,
 'ListDecl4': 155,
 'TupleDecl': 156,
 'TupleDecl1': 157,
 'TupleDecl2': 158,
 'TupleDecl3': 159,
 'TupleDecl4': 160,
 'DictionaryDecl': 161,
 'DictionaryDecl1': 162,
 'DictionaryDecl2': 163,
 'DictionaryDecl3': 164,
 'DictionaryDecl4': 165,
 'Elements': 166,
 'ElementsRest': 167,
 'COMMAElement': 168,
 'KeyValues': 169,
 'KeyValuesRest': 170,
 'COMMAKeyValue': 171,
 'Element': 172,
 'KeyValue': 173,
 'KeyValue1': 174,
 'ArrayMethods': 175,
 'ListMethods': 176,
 'TupleMethods': 177,
 'DictionaryMethods': 178,
 'ArrayDim': 179,
 'ArrayExchange': 180,
 'ArrayGetIdx': 181,
 'ArraySort': 182,
 'ArrayTail': 183,
 'ArrayHead': 184,
 'ListAdd': 185,
 'ListRemove': 186,
 'DictionarySet': 187,
 'SortOrder': 188,
 'Key': 189,
 'Value': 190,
 'PrintFunction': 191,
 'PrintFunction1': 192,
 'PrintFunction2': 193,
 'PrintFunction3': 194,
 'InputFunction': 195,
 'InputFunction1': 196,
 'InputFunction2': 197,
 'InputFunction3': 198,
 'FunctionArgs': 199,
 'FunctionArgsRest': 200,
 'COMMAFunctionArg': 201,
 'Epsilon': 202,
 'Block': 203,
 'VariableName': 204,
 'LPAREN': 205,
 'DataType': 206,
 'RPAREN': 207,
    'EQUALTO': 208,
    'ENDOST': 209,
    'IMMUTE': 210,
    'INTEGER': 211,
    'CHARACTER': 212,
    'FLOATPOINT': 213,
    'TEXTWAVE': 214,
    'FLAG': 215,
    'PLUS': 216,
    'MINUS': 217,
    'STAR': 218,
    'SLASH': 219,
    'PERCENT': 220,
    'CARET': 221,
    'OR': 223,
    'NOT': 224,
    'TRUE': 225,
    'FALSE': 226,
    'QUOTE': 227,
    'LSQUARE': 228,
    'RSQUARE': 229,
    'COLON': 230,
    'DOT': 231,
    'FN': 232,
    'COMMA': 233,
    'WHILE': 234,
    'ITERATE': 235,
    'THROUGH': 236,
    'RANGE': 237,
    'DOTDOTDOT': 238,
    'INTERRUPT': 239,
    'RESUME': 240,
    'STRIVE': 241,
    'CAPTURE': 242,
    'INCREMENT': 243,
    'DECREMENT': 244,
    'PLUSEQUAL': 245,
    'MINUSEQUAL': 246,
    'TIMESEQUAL': 247,
    'DIVIDEEQUAL': 248,
    'MODEQUAL': 249,
    'GIVEN': 250,
    'ELSEGIVEN': 251,
    'OTHERWISE': 252,
    'PENDOWN': 253,
    'PENUP': 254,
    'UNDERSCORE': 255,
    'Epsilon': 256,
    'Letter': 257,
    'Digit': 258,
    'AnyChar': 259,
    'space': 260,
    'AnySymbol': 261,
    'AnyText': 262,
    'BinaryOperator': 263,
    'LogicalOperator': 264,
    'ArrayDim1': 265,
    'ArrayDim2': 266,
    'ArrayDim3': 267,
    'ArrayDim4': 268,
    'ArrayExchange1': 269,
    'ArrayExchange2': 270,
    'ArrayExchange3': 271,
    'ArrayExchange4': 272,
    'ArrayExchange5': 273,
    'ArrayExchange6': 274,
    'ArrayGetIdx1': 275,
    'ArrayGetIdx2': 276,
    'ArrayGetIdx3': 277,
    'ArrayGetIdx4': 278,
    'ArraySort1': 279,
    'ArraySort2': 280,
    'ArraySort3': 281,
    'ArraySort4': 282,
    'ArrayTail1': 283,
    'ArrayTail2': 284,
    'ArrayHead1': 285,
    'ArrayHead2': 286,
    'ListAdd1': 287,
    'ListAdd2': 288,
    'ListAdd3': 289,
    'ListAdd4': 290,
    'ListRemove1': 291,
    'ListRemove2': 292,
    'ListRemove3': 293,
    'ListRemove4': 294,
    'DictionarySet1': 295,
    'DictionarySet2': 296,
    'DictionarySet3': 297,
    'DictionarySet4': 298,
    'COMMAValue': 299,
    'RPARENENDOST': 300,
    'LPARENRPARENENDOST': 301,
    'C': 302,
    'Identifier': 303,
    'IdentifierDigits': 304,
    'SET': 305,
    'GETIDX': 306,
    'DIM': 307,
    'EXCHANGE': 308,
    'SORT': 309,
    'TAIL': 310,
    'HEAD': 311,
    'ADD': 312,
    'REMOVE': 313,
    'Liternal2': 314,
    'Liternal3': 315,
    'LCURL': 316,
    'RCURL': 317,
    'ValueRPARENENDOST': 318,
    'Block1': 319,

}

R = {
1: [['Statements', 'MoreStatements']],
2: [['Statements', 'MoreStatements']],
3: [['Statements', 'MoreStatements']],
4: [['VariableDecl'], ['ImmutableVariableDecl'], ['FunctionDecl'], ['Loop'], ['Conditional'], ['ExceptionHandling'], ['UnaryOperation'], ['Assignment'], ['PrintFunction'], ['InputFunction'], ['ArrayDecl'], ['ListDecl'], ['TupleDecl'], ['DictionaryDecl'], ['Block']],
5: [['VariableName', 'VariableDecl1']],
6: [['LPAREN', 'VariableDecl2']],
7: [['DataType', 'VariableDecl3']],
8: [['RPAREN', 'VariableDecl4']],
9: [['EQUALTO', 'VariableDecl5']],
10: [['Expression', 'VariableDecl6']],
11: [['ENDOST']],
12: [['IMMUTE', 'ImmutableVariableDecl1']],
13: [['VariableName', 'ImmutableVariableDecl2']],
14: [['LPAREN', 'ImmutableVariableDecl3']],
15: [['DataType', 'ImmutableVariableDecl4']],
16: [['RPAREN', 'ImmutableVariableDecl5']],
17: [['EQUALTO', 'ImmutableVariableDecl6']],
18: [['Literal', 'ImmutableVariableDecl7']],
19: [['ENDOST']],
20: [['SimpleExpression'], ['LogicalExpr'], ['AccessExpression'], ['DictionaryAccess']],
21: [['Term'], ['BinaryExpression']],
22: [['SimpleExpression', 'BinaryOperatorTerm']],
23: [['BinaryOperator', 'Term']],
24: [['Factor'], ['Term1']],
25: [['Term2'], ['Term3']],
26: [['LPAREN']],
27: [['Expression', 'Term4']],
28: [['RPAREN']],
29: [['VariableName'], ['Number'], ['FloatNumber'], ['Anytext1'], ['TRUE'], ['FALSE']],
30: [['Anytext2', 'Anytext3']],
31: [['QUOTE']],
32: [['AnyText', 'Anytext4']],
33: [['QUOTE']],
34: [['AnyChar', 'AnyText']],
35: [['AnyChar'], ['Digit'], ['AnySymbol'], ['space', 'space']],
263: [['PLUS'], ['MINUS'], ['STAR'], ['SLASH'], ['PERCENT'], ['CARET']],
36: [['LogicalExpr1'], ['Expression']],
37: [['Expression', 'LogicalOperator']],
38: [['AND'], ['OR'], ['NOT']],
39: [['Digit', 'Number'], ['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
40: [['FloatNumber1', 'Number']],
41: [['Number', 'DOT']],
42: [['Number'], ['FloatNumber'], ['Literal1'], ['TRUE'], ['FALSE']],
43: [['Liternal3', 'LCURL']],
315: [['QUOTE']],
316: [['AnyText', 'QUOTE']],
44: [['VariableName', 'AccessOperator']],
45: [['LNUMBERR'], ['LNUMBERCNUMBERR']],
46: [['LNUMBERR1', 'LNUMBERR2']],
47: [['LNUMBERCNUMBERR1', 'LNUMBERCNUMBERR2']],
48: [['LSQUARE']],
49: [['Number', 'LNUMBERR3']],
50: [['RSQUARE']],
51: [['LN', 'Identifier']],
52: [['LN1', 'LSQUARE']],
53: [['LSQUARE']],
54: [['Number', 'LNUMBERR3']],
55: [['VariableName', 'DictionaryAccess1']],
56: [['DictionaryAccess2', 'DictionaryAccess3']],
57: [['DictionaryAccess4'], ['Key']],
58: [['RSQUARE']],
59: [['LSQUARE']],
204: [['UNDERSCORE'], ['IdentifierDigits', 'SET'], ['a'], ['b'], ['C'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z']],
304: [['UNDERSCORE'], ['IdentifierDigits', 'SET'], ['a'], ['b'], ['C'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z']],
305: [['IdentifierDigits', 'Digit'], ['Letter', 'IdentifierDigits']],
206: [['INTEGER'], ['CHARACTER'], ['FLOATPOINT'], ['TEXTWAVE'], ['FLAG']],
60: [['FN', 'FunctionDecl1']],
61: [['FunctionName', 'FunctionDecl2']],
62: [['LPAREN', 'FunctionDecl3']],
63: [['Arguments', 'FunctionDecl4']],
64: [['RPAREN', 'Block']],
65: [['VariableName']],
66: [['Argument', 'Argument1']],
67: [['COMMAArgument', 'ArgumentsRest']],
68: [['COMMA', 'Argument']],
69: [['VariableName', 'Argument1']],
70: [['LPAREN', 'Argument2']],
71: [['DataType', 'Argument3']],
72: [['RPAREN']],
73: [['GivenClause', 'Conditional1']],
74: [['GivenClause1', 'GivenClause2']],
75: [['GIVEN', 'GivenClause1']],
76: [['LPAREN', 'GivenClause2']],
77: [['Expression', 'Block']],
78: [['RPAREN', 'Block']],
79: [['ElseGivenClause1', 'ElseGivenClause2']],
80: [['LPAREN', 'ElseGivenClause2']],
81: [['Expression', 'ElseGivenClause3']],
82: [['RPAREN', 'Block']],
83: [['OTHERWISE', 'Block']],
84: [['WhileLoop'], ['IterateLoop'], ['RangeLoop']],
85: [['WHILE', 'WhileLoop1']],
86: [['LPAREN', 'WhileLoop2']],
87: [['Expression', 'WhileLoop3']],
88: [['RPAREN', 'WhileLoop4']],
89: [['Block', 'LoopStatements']],
90: [['ITERATE', 'IterateLoop1']],
91: [['LPAREN', 'IterateLoop2']],
92: [['VariableName', 'IterateLoop3']],
93: [['LPAREN', 'IterateLoop4']],
94: [['DataType', 'IterateLoop5']],
95: [['RPAREN', 'IterateLoop6']],
96: [['EQUALTO', 'IterateLoop7']],
97: [['Expression', 'IterateLoop8']],
98: [['ENDOST', 'IterateLoop9']],
99: [['THROUGH', 'IterateLoop10']],
100: [['VariableName', 'IterateLoop11']],
101: [['ENDOST', 'IterateLoop12']],
102: [['RPAREN', 'Block']],
103: [['ITERATE', 'RangeLoop1']],
104: [['LPAREN', 'RangeLoop2']],
105: [['VariableName', 'RangeLoop3']],
106: [['LPAREN', 'RangeLoop4']],
107: [['DataType', 'RangeLoop5']],
108: [['RPAREN', 'RangeLoop6']],
109: [['EQUALTO', 'RangeLoop7']],
110: [['Expression', 'RangeLoop8']],
111: [['DOTDOTDOT', 'RangeLoop9']],
112: [['THROUGH', 'RangeLoop10']],
113: [['RANGE', 'RangeLoop11']],
114: [['LPAREN', 'RangeLoop12']],
115: [['Expression', 'RangeLoop13']],
116: [['DOTDOTDOT', 'RangeLoop14']],
117: [['Expression', 'RangeLoop15']],
118: [['COMMA', 'RangeLoop16']],
119: [['Expression', 'RangeLoop17']],
120: [['DOTDOTDOT', 'RangeLoop18']],
121: [['RPAREN', 'Block']],
122: [['LoopStatement', 'LoopStatements']],
123: [['Statement'], ['LoopInterrupt'], ['LoopResume']],
124: [['INTERRUPT', 'ENDOST']],
125: [['RESUME', 'ENDOST']],
126: [['StriveBlock', 'CaptureBlock']],
127: [['STRIVE', 'Block']],
128: [['CAPTURE', 'CaptureBlockOption']],
129: [['CaptureWithParentheses'], ['CaptureWithoutParentheses']],
130: [['LPAREN', 'VariableNameBlock']],
131: [['CAPTURE', 'Block']],
132: [['VariableName', 'RPARENBlock']],
133: [['RPAREN', 'Block']],
134: [['VariableName', 'UnaryOperation1']],
135: [['INCREMENT', 'ENDOST'], ['DECREMENT', 'UnaryOperationEnd']],
136: [['ENDOST']],
137: [['VariableName', 'Assignment1']],
138: [['EQUALTO', 'Assignment2'], ['AssignmentOperator', 'Assignment2']],
139: [['Expression', 'ENDOST']],
140: [['BinaryOperator'], ['PLUSEQUAL'], ['MINUSEQUAL'], ['TIMESEQUAL'], ['DIVIDEEQUAL'], ['MODEQUAL']],
141: [['VariableName', 'ArrayDecl1']],
142: [['LPAREN', 'ArrayDecl2']],
143: [['DataType', 'ArrayDecl3']],
144: [['COMMA', 'ArrayDecl4']],
145: [['Number', 'ArrayDecl5']],
146: [['RPAREN', 'ArrayDecl6']],
147: [['EQUALTO', 'ArrayDecl7']],
148: [['RCURL', 'ArrayDecl8']],
149: [['Elements', 'ArrayDecl9']],
150: [['ValueRPARENENDOST', 'ENDOST']],
151: [['VariableName', 'ListDecl1']],
152: [['EQUALTO', 'ListDecl2']],
153: [['LSQUARE', 'ListDecl3']],
154: [['Elements', 'ListDecl4']],
155: [['RSQUARE', 'ENDOST']],
156: [['VariableName', 'TupleDecl1']],
157: [['EQUALTO', 'TupleDecl2']],
158: [['LPAREN', 'TupleDecl3']],
159: [['Elements', 'TupleDecl4']],
160: [['RPAREN', 'ENDOST']],
161: [['VariableName', 'DictionaryDecl1']],
162: [['EQUALTO', 'DictionaryDecl2']],
163: [['RCURL', 'DictionaryDecl3']],
164: [['KeyValues', 'DictionaryDecl4']],
165: [['ValueRPARENENDOST', 'ENDOST']],
166: [['Element', 'ElementsRest']],
167: [['COMMAElement', 'ElementsRest']],
168: [['COMMA', 'Element']],
169: [['KeyValue', 'KeyValuesRest']],
170: [['COMMAKeyValue', 'KeyValuesRest']],
171: [['COMMA', 'KeyValue']],
172: [['Expression']],
173: [['Expression', 'KeyValue1']],
174: [['COLON', 'Expression']],
175: [['ArrayDim'], ['ArrayExchange'], ['ArrayGetIdx'], ['ArraySort'], ['ArrayTail'], ['ArrayHead'], ['ListAdd'], ['ListRemove'], ['DictionarySet']],
176: [['ArrayDim'], ['ArrayExchange'], ['ArrayGetIdx'], ['ArraySort'], ['ArrayTail'], ['ArrayHead'], ['ListAdd'], ['ListRemove']],
177: [['ArrayDim'], ['ArrayExchange'], ['ArrayGetIdx'], ['ArraySort'], ['ArrayTail'], ['ArrayHead'], ['ListAdd'], ['ListRemove']],
178: [['DictionarySet']],
179: [['VariableName', 'ArrayDim2']],
266: [['DOT', 'ArrayDim3']],
267: [['EXCHANGE', 'ArrayDim4']],
268: [['LPAREN', 'ArrayExchange1']],
269: [['RPAREN', 'ENDOST']],
180: [['VariableName', 'ArrayExchange2']],
270: [['DOT', 'ArrayExchange3']],
271: [['SORT', 'ArrayExchange4']],
272: [['LPAREN', 'ArrayExchange5']],
273: [['Number', 'ArrayExchange6']],
274: [['COMMA', 'ArrayGetIdx1']],
275: [['RPAREN', 'ENDOST']],
181: [['VariableName', 'ArrayGetIdx2']],
276: [['DOT', 'ArrayGetIdx3']],
277: [['DIM', 'ArrayGetIdx4']],
278: [['LPAREN', 'ArraySort1']],
279: [['Element', 'LPARENRPARENENDOST']],
182: [['VariableName', 'ArraySort2']],
280: [['DOT', 'ArraySort3']],
281: [['TAIL', 'ArraySort4']],
282: [['LPAREN', 'ArrayTail1']],
283: [['SortOrder', 'LPARENRPARENENDOST']],
183: [['VariableName', 'ArrayTail2']],
284: [['DOT', 'ArrayHead1']],
285: [['HEAD', 'C']],
184: [['VariableName', 'ArrayHead2']],
286: [['DOT', 'ListAdd1']],
287: [['ADD', 'C']],
185: [['VariableName', 'ListAdd2']],
288: [['DOT', 'ListAdd3']],
289: [['REMOVE', 'ListAdd4']],
290: [['LPAREN', 'ListRemove1']],
291: [['Element', 'LPARENRPARENENDOST']],
186: [['VariableName', 'ListRemove2']],
292: [['DOT', 'ListRemove3']],
293: [['GETIDX', 'ListRemove4']],
294: [['LPAREN', 'DictionarySet1']],
295: [['Key', 'RPARENENDOST']],
187: [['VariableName', 'ListRemove2']],
300: [['COMMA', 'Block1']],
319: [['Value', 'LPARENRPARENENDOST']],
301: [['RPAREN', 'ENDOST']],
189: [['Expression']],
190: [['Expression']],
191: [['PENDOWN', 'PrintFunction1']],
192: [['LPAREN', 'PrintFunction2']],
193: [['FunctionArgs', 'PrintFunction3']],
194: [['RPAREN', 'ENDOST']],
195: [['PENUP', 'InputFunction1']],
196: [['LPAREN', 'InputFunction2']],
197: [['FunctionArgs', 'InputFunction3']],
198: [['RPAREN', 'ENDOST']],
199: [['FunctionArgs', 'FunctionArgsRest']],
200: [['COMMAFunctionArg', 'FunctionArgsRest']],
201: [['COMMA', 'FunctionArgs']],
203: [['RCURL', 'Block1']],
259: [['Letter'], ['Digit'], ['AnySymbol'], ['space', 'space'], ['!'], ['@'], ['#'], ['$'], ['%'], ['^'], ['&'], ['*'], ['('], [')'], ['-'], ['_'], ['+'], ['='], ['{'], ['}'], ['['], [']'], ['|'], ['\\'], [':'], [';'], ["'"], ['"'], [','], ['<'], ['>'], ['.'], ['?'], ['/'], ['`'], ['~'], ['a'], ['b'], ['C'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z'], ['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
260: [['"']],
261: [['space', 'space'], ['!'], ['@'], ['#'], ['$'], ['%'], ['^'], ['&'], ['*'], ['('], [')'], ['-'], ['_'], ['+'], ['='], ['{'], ['}'], ['['], [']'], ['|'], ['\\'], [':'], [';'], ["'"], ['"'], [','], ['<'], ['>'], ['.'], ['?'], ['/'], ['`'], ['~'], ['a'], ['b'], ['C'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z'], ['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
188: [['Asc'], ['Dsc']],
    253: [["pendown"]],
    254: [["penup"]],
205: [['(']],
207: [[')']],
233: [[',']],
209: [[';']],
257: [['a'], ['b'], ['C'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z']],
258: [['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
255: [['_']],
202: [['ε']],
208: [['=']],
    210: [["immute"]],
    211: [["integer"]],
    212:[ ["character"]],
    213: [["floatpoint"]],
    214: [["textwave"]],
    215: [["flag"]],
    216:[ ["+"]],
    217: [["-"]],
    218: [["*"]],
    219: [["/"]],
    220: [["%"]],
    221: [["^"]],
    222: [["&&"]],
    223:[ ["$$"]],
    224: [["!"]],
    225: [["True"]],
    226: [["False"]],
227: [['"']],
228: [['[']],
229: [[']']],
230: [[':']],
231: [['.']],
 232: [["fn"]],
    234: [["while"]],
    235: [["iterate"]],
    236: [["through"]],
    237: [["range"]],
    238: [["..."]],
    239: [["interrupt"]],
    240: [["resume"]],
    241: [["strive"]],
    242: [["capture"]],
    243: [["++"]],
    244: [["--"]],
    245: [["+="]],
    246: [["-="]],
    247: [["*="]],
    248: [["/="]],
    249: [["%="]],
250: [["Given"]],
251: [["ElseGiven"]],
252: [["Otherwise"]],

256: [['ε']],
262: [['AnyChar', 'AnyText']],
264: [['&&'], ['||']],
265: [['PLUS'], ['MINUS'], ['STAR'], ['SLASH'], ['PERCENT'], ['CARET']],
269: [['DOT'], ['DIM']],
270: [['EXCHANGE']],
296: [['SET', 'DictionarySet3']],
297: [['LPAREN', 'DictionarySet4']],
298: [['Key', 'COMMAValue']],
299: [['COMMA', 'ValueRPARENENDOST']],
302: [['COLON']],
303: [['underscore'], ['Identifier', 'IdentifierDigits'],['a'], ['b'], ['C'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z']],
306: [['getidx']],
307: [['dim']],
308: [['exchange']],
309: [['sort']],
310: [['tail']],
311: [['head']],
312: [['add']],
313: [['remove']],
314: [['QUOTE']],
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
                if len(e) == 1 and e[0] == inp[s-1]:
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
    
    # Print DP table
    print("\nDP Table:")
    for L in range(1, n+1):
        print(f"Length {L}:")
        for s in range(1, n-L+2):
            for v in range(1, m+1):
                if dp[L][s][v]:
                    print(f"dp[{L}][{s}][{v}] = {dp[L][s][v]} ", end='')
            print()  # Newline for readability
        print("--------")  # Separator for different lengths

inp = [
    ['VariableName', 'EQUALTO', 'INTEGER', 'LPAREN', 'Number', 'RPAREN', 'ENDOST']
]

for i in inp:
    parser_Conds(i)
    print()
