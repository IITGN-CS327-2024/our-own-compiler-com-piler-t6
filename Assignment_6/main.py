import os
import sys
from lark import Lark, Transformer, Tree, Token


root_dir = os.path.join(os.path.dirname(_file_), '..')
sys.path.insert(0, root_dir)

from Assignment_2.Lexer import Lexer

default_folder = 'Assignment_5/test_cases'
grammar_file_path = "Assignment_5/grammer.lark"  

with open(grammar_file_path, "r") as file:
    grammar = file.read()

def print_ast(node, indent="", last=True):
    # Handle Lark Tree
    if isinstance(node, Tree):
        name = node.data
        children = node.children
        print(f"{indent}{'└── ' if last else '├── '}{name}")
        new_indent = indent + ("    " if last else "│   ")
        for i, child in enumerate(children):
            print_ast(child, new_indent, i == len(children) - 1)
    
    # Handle Lark Token
    elif isinstance(node, Token):
        print(f"{indent}{'└── ' if last else '├── '}{node.type}({node.value})")
    
    # Handle dictionary (custom AST nodes)
    elif isinstance(node, dict):
        name = node.get("type", "Dict")
        print(f"{indent}{'└── ' if last else '├── '}{name}")
        new_indent = indent + ("    " if last else "│   ")
        for key, value in node.items():
            if key == "type":
                continue
            print(f"{new_indent}├── {key}:")
            print_ast(value, new_indent + "│   ", last=True)
    
    # Handle lists and tuples
    elif isinstance(node, (list, tuple)):
        print(f"{indent}{'└── ' if last else '├── '}['list' if isinstance(node, list) else 'tuple']")
        new_indent = indent + ("    " if last else "│   ")
        for i, item in enumerate(node):
            print_ast(item, new_indent, i == len(node) - 1)
    
    # Handle simple data types (leaves)
    else:
        print(f"{indent}{'└── ' if last else '├── '}{repr(node)}")

# Example usage:
# print_ast(ast)







class ASTTransformer(Transformer):
    
    def start(self, items):
        return {"type": "program", "body": items[0]}

    def statements(self, items):
        return {"type": "statements", "body": items}

    # Function handling
    def functiondecl(self, items):
        # Accessing items by index
        name = items[1]
        args = items[3]
        return_type = items[5]
        body = items[7]
        return {"type": "function_decl", "name": name, "args": args, "return_type": return_type, "body": body}

    def argument(self, items):
        # Fixed issue: Directly accessing items by index
        name = items[0]
        data_type = items[2]
        return {"name": name, "data_type": data_type}

    def variabledecl(self, items):
        name = items[0]  
        datatype = items[2] 
        expression = items[5] 
    
        return {
        "type": "variable_decl",
        "name": str(name),
        "data_type": datatype,
        "value": expression
    }

    def immutablevariabledecl(self, items):
        name = items[1]  
        datatype = items[3] 
        expression = items[6]
        return {"type": "immutable_variable_decl", "name": name, "data_type": datatype, "value": expression}
    
    def whileloop(self, items):
    # No changes; this appears correct.
        return {"type": "while_loop", "condition": items[1], "body": items[2]}

    def iterateloop(self, items):
        # This method now needs to differentiate between a list and a range.
        if "list" in str(items[8]):  # Assuming items[8] indicates whether it's a list or a range.
            # List iteration
            return {"type": "iterate_loop_list", 
                    "variable": {"name": items[2], "data_type": items[4]}, 
                    "start": items[6], 
                    "through": items[8],  # This would be the list's name
                    "body": items[9]}  # Adjust index as needed
        else:
            # Range iteration
            return {"type": "iterate_loop_range", 
                    "variable": {"name": items[2], "data_type": items[4]}, 
                    "start": items[6], 
                    "range_start": items[8], 
                    "range_end": items[10], 
                    "step": items[12], 
                    "body": items[13]}  # Adjust index as needed

    # Conditionals
    def conditional(self, items):
        clauses = []
        for item in items:
            # Check if item is None before accessing 'type'
            if item is not None and item['type'] in ['given_clause', 'elsegiven_clause', 'otherwise_clause']:
                clauses.append(item)
        return {"type": "conditional", "clauses": clauses}

    def givenclause(self, items):
        # Directly accessing condition and body by index
        return {"type": "given_clause", "condition": items[1], "body": items[2]}

    def elsegivenclause(self, items):
        if(len(items) != 0):
            return {"type": "elsegiven_clause", "condition": items[1], "body": items[2]}
        

    def otherwiseclause(self, items):
        if(len(items) != 0):
            return {"type": "otherwise_clause", "body": items[1]}

    # Expressions
    def arithmeticexpr(self, items):
        left, operator, right = items
        return {"type": "arithmetic_expr", "operator": operator, "left": left, "right": right}

    def logicalexpr(self, items):
        left, operator, right = items
        return {"type": "logical_expr", "operator": operator, "left": left, "right": right}

    def comparisonexpr(self, items):
        left, operator, right = items
        return {"type": "comparison_expr", "operator": operator, "left": left, "right": right}

    # Basic types handling
    def number(self, items):
        return int(items[0])

    def floatnumber(self, items):
        return float(items[0])

    def string(self, items):
        # Removing quotation marks
        return str(items[0][1:-1])

    def array_decl(self, items):
        name, data_type, size, elements = items
        return {"type": "ArrayDeclaration", "name": name, "dataType": data_type, "size": size, "elements": elements}

    def list_decl(self, items):
        name, elements = items
        return {"type": "ListDeclaration", "name": name, "elements": elements}

    def tuple_decl(self, items):
        name, elements = items
        return {"type": "TupleDeclaration", "name": name, "elements": elements}

    def dictionary_decl(self, items):
        name, key_values = items
        return {"type": "DictionaryDeclaration", "name": name, "keyValues": key_values}

    # Array Methods
    def array_dim(self, items):
        return {"type": "ArrayDim", "array": items[0]}

    def array_get_idx(self, items):
        return {"type": "ArrayGetIndex", "array": items[0], "index": items[1]}

    def array_tail(self, items):
        return {"type": "ArrayTail", "array": items[0]}

    def array_head(self, items):
        return {"type": "ArrayHead", "array": items[0]}

    def array_exchange(self, items):
        return {"type": "ArrayExchange", "array": items[0], "index": items[1], "element": items[2]}

    def array_sort(self, items):
        return {"type": "ArraySort", "array": items[0], "order": items[1]}

    # List Methods
    def list_dim(self, items):
        return {"type": "ListDim", "list": items[0]}

    def list_exchange(self, items):
        return {"type": "ListExchange", "list": items[0], "index": items[1], "element": items[2]}

    def list_get_idx(self, items):
        return {"type": "ListGetIndex", "list": items[0], "index": items[1]}

    def list_sort(self, items):
        return {"type": "ListSort", "list": items[0], "order": items[1]}

    def list_tail(self, items):
        return {"type": "ListTail", "list": items[0]}

    def list_head(self, items):
        return {"type": "ListHead", "list": items[0]}

    def list_add(self, items):
        return {"type": "ListAdd", "list": items[0], "element": items[1]}

    def list_remove(self, items):
        return {"type": "ListRemove", "list": items[0], "index": items[1]}


    # Tuple Methods
    def tuple_dim(self, items):
        return {"type": "TupleDim", "tuple": items[0]}

    def tuple_get_idx(self, items):
        return {"type": "TupleGetIndex", "tuple": items[0], "index": items[1]}

    def tuple_tail(self, items):
        return {"type": "TupleTail", "tuple": items[0]}

    def tuple_head(self, items):
        return {"type": "TupleHead", "tuple": items[0]}

    # Dictionary Methods
    def dictionary_set(self, items):
        return {"type": "DictionarySet", "dictionary": items[0], "key": items[1], "value": items[2]}

    def elements(self, items):
        return items

    def key_values(self, items):
        return items

    def key_value(self, items):
        return {"key": items[0], "value": items[1]}


def main():
    test_cases_folder = 'Assignment_5/test_cases'

    # Specify the grammar directly in the script or load it from a file
    grammar = """
    ?start: program
    program: statements
    ?statements: statement*
    ?statement: variabledecl
               | immutablevariabledecl
               | functiondecl
               | loop
               | conditional
               | exceptionhandling
               | assignment
               | unaryoperation
               | printfunction
               | block
               | loopinterrupt  
               | loopresume
               | throwexception
               | arraydecl
               | listdecl
               | tupledecl
               | dictionarydecl
               | method_call
               | methods_type_2
               | return_statement  
               | functioncall1

    return_statement: EXITWITH expression ENDOST
    variabledecl: VARIABLENAME LPAREN datatype RPAREN EQUALTO expression ENDOST
    immutablevariabledecl: IMMUTABLE VARIABLENAME LPAREN datatype RPAREN EQUALTO literal ENDOST 
    datatype: INTEGER | CHAR | FLOATPOINT | TEXTWAVE | FLAG


    ?expression: inputfunction
               | logicalexpr
               | comparisonexpr
               | accessexpression
               | dictionaryaccess
               | list
               | listaccess
               | negation
               | method_call
               | term
               | arithmeticexpr

    method_call: (array_methods
               | list_methods
               | tuple_methods
               | dictionary_methods)


    negation: NOT factor
    list: LSQUARE elements RSQUARE
    listaccess: expression LSQUARE expression RSQUARE

    dictionaryaccess: VARIABLENAME LSQUARE key RSQUARE

    matrix: LSQUARE matrix_elements RSQUARE
    matrix_elements: matrix_element (COMMA matrix_element)* | 
    matrix_element: list

    comparisonexpr: expression comparisonoperator expression
    ?comparisonoperator: SMALLERTHAN | GREATERTHAN | EQUALEQUAL | NOTEQUALTO | LESSTHANEQUALTO | GREATERTHANEQUALTO


    arithmeticexpr: expression binaryoperator expression
    binaryoperator: PLUS | MINUS | STAR | SLASH | PERCENT | CARET

    logicalexpr: expression logicaloperator expression
    logicaloperator: AND | OR


    ?simpleexpression: term (binaryoperator term)*
    ?term: factor
         | LPAREN expression RPAREN  

    ?factor: VARIABLENAME
           | number
           | floatnumber
           | CHARACTER  
           | STRING    
           | TRUE
           | FALSE
           | functioncall2



    accessexpression: VARIABLENAME accessoperator
    accessoperator: LSQUARE number RSQUARE | LSQUARE number COLON number RSQUARE


    number: (PLUS | MINUS)? /[0-9]+/
    floatnumber: (PLUS | MINUS)? /[0-9]+\.[0-9]+/

    literal: number | floatnumber | CHARACTER | TRUE | FALSE | STRING


    conditional: givenclause elsegivenclause otherwiseclause
    givenclause: GIVEN LPAREN [expression] RPAREN block 
    elsegivenclause: ELSEGIVEN LPAREN [expression] RPAREN block | 
    otherwiseclause: OTHERWISE block | 

    functiondecl: FN functionname LPAREN arguments RPAREN ARROW datatype block
    functionname: VARIABLENAME
    ?arguments: argument (COMMA argument)* |
    ?argument: VARIABLENAME LPAREN datatype RPAREN


    functioncall1: VARIABLENAME LPAREN [functionargs] RPAREN ENDOST

    functioncall2: VARIABLENAME LPAREN [functionargs] RPAREN 

    ?functionargs: functionarg (COMMA functionarg)* 
    functionarg: expression



    loop: whileloop | iterateloop | rangeloop
    whileloop: WHILE LPAREN expression RPAREN block
    iterateloop: ITERATE LPAREN VARIABLENAME LPAREN datatype RPAREN EQUALTO expression ENDOST THROUGH VARIABLENAME ENDOST RPAREN block
    rangeloop: ITERATE LPAREN VARIABLENAME LPAREN datatype RPAREN EQUALTO expression ENDOST THROUGH RANGE LPAREN expression DOTDOTDOT expression COMMA expression RPAREN ENDOST RPAREN block
    loopinterrupt: INTERRUPT ENDOST
    loopresume: RESUME ENDOST

    exceptionhandling: striveblock captureblock
    striveblock: STRIVE LPAREN RPAREN block
    captureblock: CAPTURE (LPAREN [VARIABLENAME] RPAREN)? block 
    throwexception: THROWEXCEPTION LPAREN STRING RPAREN ENDOST

    unaryoperation: VARIABLENAME INCREMENT ENDOST | VARIABLENAME DECREMENT ENDOST
    assignment: VARIABLENAME EQUALTO expression ENDOST | VARIABLENAME assignmentoperator expression ENDOST
    assignmentoperator: PLUSEQUAL | MINUSEQUAL | TIMESEQUAL | DIVIDEEQUAL | MODEQUAL

    elements: element (COMMA element)* | 
    element: expression

    key_values: key_value (COMMA key_value)* | 
    key_value: key COLON value

    arraydecl: VARIABLENAME LPAREN datatype COMMA number RPAREN EQUALTO LCURL elements RCURL ENDOST 
    listdecl: VARIABLENAME EQUALTO LSQUARE elements RSQUARE ENDOST 
    tupledecl: VARIABLENAME EQUALTO LPAREN elements RPAREN ENDOST 
    dictionarydecl: VARIABLENAME EQUALTO LCURL key_values RCURL ENDOST

    array_methods: array_dim
                 | array_get_idx
                 | array_tail
                 | array_head


    list_methods: list_dim
                | list_get_idx
                | list_tail
                | list_head


    tuple_methods: tuple_dim
                 | tuple_get_idx
                 | tuple_tail
                 | tuple_head

    methods_type_2: array_exchange
                    | array_sort
                    | list_exchange
                    | list_sort
                    | list_add
                    | list_remove

    dictionary_methods: dictionary_set

    // Array methods
    array_dim: VARIABLENAME DOT ARRAYDIM PAREN 
    array_get_idx: VARIABLENAME DOT ARRAYINDEX LPAREN element RPAREN 
    array_tail: VARIABLENAME DOT ARRAYTAIL PAREN
    array_head: VARIABLENAME DOT ARRAYHEAD PAREN

    // Array method1
    array_exchange: VARIABLENAME DOT ARRAYEXCHANGE LPAREN number COMMA element RPAREN ENDOST
    array_sort: VARIABLENAME DOT ARRAYSORT LPAREN sort_order RPAREN ENDOST

    // List methods
    list_dim: VARIABLENAME DOT LISTDIM PAREN
    list_exchange: VARIABLENAME DOT LISTEXCHANGE LPAREN number COMMA element RPAREN ENDOST
    list_get_idx: VARIABLENAME DOT LISTINDEX LPAREN element RPAREN 
    list_sort: VARIABLENAME DOT LISTSORT LPAREN sort_order RPAREN ENDOST
    list_tail: VARIABLENAME DOT LISTTAIL PAREN
    list_head: VARIABLENAME DOT LISTHEAD PAREN 
    list_add: VARIABLENAME DOT LISTADD LPAREN element RPAREN ENDOST
    list_remove: VARIABLENAME DOT LISTREMOVE LPAREN number RPAREN ENDOST 

    // Tuple methods
    tuple_dim: VARIABLENAME DOT TUPLEDIM PAREN 
    tuple_get_idx: VARIABLENAME DOT TUPLEINDEX LPAREN element RPAREN 
    tuple_tail: VARIABLENAME DOT TUPLETAIL PAREN 
    tuple_head: VARIABLENAME DOT TUPLEHEAD PAREN 

    // Dictionary method
    dictionary_set: VARIABLENAME DOT DICTSET LPAREN key COMMA value RPAREN ENDOST

    // Sort order definition
    sort_order: ASC | DESC


    printfunction: PENDOWN LPAREN expression RPAREN ENDOST 
    inputfunction: PENUP LPAREN [STRING] RPAREN 


    block: LCURL statements RCURL

    LPAREN: "(" 
    RPAREN: ")"
    ENDOST: ";"
    EQUALTO: "="
    LCURL: "{"
    RCURL: "}"
    LSQUARE: "["
    RSQUARE: "]"
    IMMUTE: "immute"
    INTEGER: "integer"
    CHAR: "character"
    FLOATPOINT: "floatpoint"
    TEXTWAVE: "textwave"
    FLAG: "flag"
    PLUS: "+"
    MINUS: "-"
    STAR: "*"
    SLASH: "/"
    PERCENT: "%"
    CARET: "^"
    AND: "&&"
    OR: "||"
    NOT: "!"
    TRUE: "True"
    FALSE: "False"
    COLON: ":"
    DOT: "."
    FN: "fn"
    COMMA: ","
    WHILE: "while"
    ITERATE: "iterate"
    THROUGH: "through"
    RANGE: "range"
    DOTDOTDOT: "..."
    INTERRUPT: "interrupt"
    RESUME: "resume"
    STRIVE: "strive"
    CAPTURE: "capture"
    INCREMENT: "++"
    DECREMENT: "--"
    PLUSEQUAL: "+="
    MINUSEQUAL: "-="
    TIMESEQUAL: "*="
    DIVIDEEQUAL: "/="
    MODEQUAL: "%="
    GREATERTHAN: ">"
    SMALLERTHAN: "<"
    EQUALEQUAL: "=="
    NOTEQUALTO: "!="
    LESSTHANEQUALTO: "<="
    GREATERTHANEQUALTO: ">="
    ARROW: "->"
    GIVEN: "Given"
    ELSEGIVEN: "ElseGiven"
    OTHERWISE: "Otherwise"
    THROWEXCEPTION: "throwexception"
    PAREN: "()"
    ARRAYDIM: "array_dim"
    ARRAYINDEX: "array_get_idx"
    ARRAYTAIL: "array_tail"
    ARRAYHEAD: "array_head"
    ARRAYEXCHANGE: "array_exchange"
    ARRAYSORT: "array_sort"
    LISTDIM: "list_dim"
    LISTEXCHANGE: "list_exchange"
    LISTINDEX: "list_get_idx"
    LISTTAIL: "list_tail"
    LISTHEAD: "list_head"
    LISTSORT: "list_sort"
    LISTADD: "list_add"
    LISTREMOVE: "list_remove"
    TUPLEDIM: "tuple_dim"
    TUPLEINDEX: "tuple_get_idx"
    TUPLETAIL: "tuple_tail"
    TUPLEHEAD: "tuple_head"
    DICTSET: "dictionary_set"
    PENDOWN: "pendown"
    PENUP: "penup"
    ASC: "asc"
    DESC: "desc"
    EXITWITH: "exitwith"
    IMMUTABLE: "immute"



    DIGIT: "0".."9"
    VARIABLENAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    key: expression
    value: expression
    anytext: /(?:[^"\\]|\\.)?/
    STRING: /"(?:[^"\\\\]|\\\\.)*"/
    CHARACTER: /'.'/ 
    %ignore " "
    %ignore /\s+/
    """

     # Initialize the parser with the grammar and the transformer
    parser = Lark(grammar, start='start', parser='lalr')
    transformer = ASTTransformer()

    # Get list of .cmm files in the folder
    test_case_files = [f for f in os.listdir(test_cases_folder) if f.endswith('.cmm')]

    for test_case_file in test_case_files:
        test_case_file_path = os.path.join(test_cases_folder, test_case_file)
        with open(test_case_file_path, "r") as file:
            test_cases_content = file.read()
        
        print(f"Processing file: {test_case_file_path}")
        try:
            parse_tree = parser.parse(test_cases_content)
            ast = transformer.transform(parse_tree)  # Transform parse tree into AST
            print("AST Output:")
            print_ast(ast)  # Use the updated print_ast function
        except Exception as e:
            print(f"Error parsing file {test_case_file_path}: {e}")

if _name_ == "_main_":
    main()