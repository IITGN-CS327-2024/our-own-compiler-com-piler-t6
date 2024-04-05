import os
import sys
from lark import Lark, Transformer, Tree, Token


root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)

from Assignment_2.Lexer import Lexer

def print_ast(node, indent="", last=True):
    # Handle Lark Tree instances
    if isinstance(node, Tree):
        name = node.data
        children = node.children
        print(f"{indent}{'└── ' if last else '├── '}{name}")
        new_indent = indent + ("    " if last else "│   ")
        for i, child in enumerate(children):
            print_ast(child, new_indent, i == len(children) - 1)

    # Handle Lark Token instances
    elif isinstance(node, Token):
        print(f"{indent}{'└── ' if last else '├── '}{node.type}({node.value})")

    # Handle dictionary (custom AST nodes) instances
    elif isinstance(node, dict):
        # Only process if "type" field exists; otherwise, directly print children
        if "type" in node:
            name = node["type"]
            print(f"{indent}{'└── ' if last else '├── '}{name}")
            new_indent = indent + ("    " if last else "│   ")
            for key, value in node.items():
                if key != "type":
                    print(f"{new_indent}├── {key}:")
                    print_ast(value, new_indent + "│   ", True)
        else:
            # Directly print children without introducing an extra layer
            for value in node.values():
                print_ast(value, indent, last)

    # Handle lists and tuples
    elif isinstance(node, (list, tuple)):
        new_indent = indent + ("    " if last else "│   ")
        for i, item in enumerate(node):
            print_ast(item, new_indent, i == len(node) - 1)

    # Handle simple data types (leaves)
    else:
        print(f"{indent}{'└── ' if last else '├── '}{repr(node)}")




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
        return_type = items[6]
        body = items[7]
        return {"type": "function_decl", "name": name, "args": args, "return_type": return_type, "body": body}

    def arguments(self, items):
        if len(items) == 0:
            return []
        name = items[0]
        data_type = items[2]
        return {"name": name, "data_type": data_type}
    
    def argument(self, items):
        name = items[0]
        data_type = items[2]
        return {"name": name, "data_type": data_type}
    
    def functioncall1(self, items):
        name = items[0]
        args = items[2]
        return {"type": "function_call", "name": name, "args": args}
        

    def variabledecl(self, items):
        name = items[0]  
        datatype = items[2] 
        expression = items[5] 
    
        return {
        "type": "variable_decl",
        "name": str(name),
        "value": expression
    }

    def arithmeticexpr(self, items):
        # As arithmeticexpr is now directly linked to simpleexpression, simply pass through
        return items[0]

    def simpleexpression(self, items):
        # Handles term ((PLUS|MINUS) term)*
        if len(items) == 1:
            return items[0]
        else:
            # Construct a binary expression tree for each operation
            expr = items[0]
            for i in range(1, len(items), 2):
                operator = items[i]
                right = items[i + 1]
                expr = {"type": "arithmetic_expr", "operator": operator, "left": expr, "right": right}
            return expr

    def term(self, items):
        # Handles factor ((STAR|SLASH|PERCENT) factor)*
        if len(items) == 1:
            return items[0]
        else:
            expr = items[0]
            for i in range(1, len(items), 2):
                operator = items[i]
                right = items[i + 1]
                expr = {"type": "arithmetic_expr", "operator": operator, "left": expr, "right": right}
            return expr

    def factor(self, items):
        # Handles base (CARET factor)?
        if len(items) == 1:
            return items[0]
        else:
            return {"type": "arithmetic_expr", "operator": "^", "left": items[0], "right": items[2]}

    def base(self, items):
        # Handles parentheses and simple tokens
        if len(items) == 1:
            # Directly return the item if it's a simple token
            return items[0]
        else:
            # If the item is an expression in parentheses, return it directly
            return items[1]
        

    def logicalexpr(self, items):
        # Process the left side of the logical expression
        # Check if the item is a Tree and needs transforming
        left = self.transform(items[0]) if isinstance(items[0], Tree) else items[0]

        # Extracting the operator assuming it's a Token
        operator = items[1].value if isinstance(items[1], Token) else items[1]

        # Process the right side of the logical expression
        # Check if the item is a Tree and needs transforming
        right = self.transform(items[2]) if isinstance(items[2], Tree) else items[2]

        return {"type": "logical_expr", "operator": operator, "left": left, "right": right}

    def comparisonexpr(self, items):
        # Since the debug output shows the structure of items in this method,
        # you should directly access the value of tokens and handle integers appropriately.
        left = items[0].value if isinstance(items[0], Token) else items[0]  # Handle left operand
        operator = items[1].value if isinstance(items[1], Token) else items[1]  # Extract operator
        right = items[2]  # Right operand seems to be an integer based on the debug output

        return {"type": "comparison_expr", "operator": operator, "left": left, "right": right}

    def string(self, items):
        value = str(items[0][1:-1]) 
        return {"type": "string", "textwave": value}

    def number(self, items):
        value = int(items[0])
        return {"type": "number",  "INTEGER": value}

    def floatnumber(self, items):
        # This method handles floating-point numbers.
        # Assuming items[0] is the string representation of the float
        value = float(items[0])
        return {"type": "number",  "FLOATPOINT": value}


    def immutablevariabledecl(self, items):
        name = items[1]  
        datatype = items[3] 
        expression = items[6]
        return {"type": "immutable_variable_decl", "name": name, "value": expression}
    
    def whileloop(self, items):
    # No changes; this appears correct.
        return {"type": "while_loop", "condition": items[2], "body": items[4]}

    def rangeloop(self, items):
        var_name = items[2]  # VARIABLENAME
        var_type = items[4]  # datatype
        range_start = items[9]  # expression before DOTDOT
        range_end = items[11]  # expression after DOTDOT
        step = items[13]  # expression after COMMA

        return {
            "type": "iterate_loop_range",
            "variable": {"name": var_name, "data_type": var_type},
            "range_start": range_start,
            "range_end": range_end,
            "step": step,
            "body": items[-1]  # The last item is assumed to be the 'block'
        }

    def iterateloop(self, items):
        var_name = items[2]  # VARIABLENAME
        var_type = items[4]  # datatype
        list_name = items[7]  # VARIABLENAME after THROUGH

        return {
            "type": "iterate_loop_list",
            "variable": {"name": var_name, "data_type": var_type},
            "through": list_name,
            "body": items[-1]  # The last item is assumed to be the 'block'
        }


    # Conditionals
    def conditional(self, items):
        clauses = []
        for item in items:
            if item is not None:
                # Check if the item is a Tree object before transforming
                if isinstance(item, Tree):
                    transformed_item = self.transform(item)
                    clauses.append(transformed_item)
                elif isinstance(item, dict):
                    # If the item is already a dict, use it directly
                    clauses.append(item)
                else:
                    # Handle other types appropriately, depending on your needs
                    pass
        return {"type": "conditional", "clauses": clauses}


    def givenclause(self, items):
        # Check if the condition is a Tree and needs transforming
        condition = self.transform(items[1]) if isinstance(items[1], Tree) else items[2]

        # Check if the body is a Tree and needs transforming
        # The body is more likely to be a Tree, but we still check to be safe
        body = self.transform(items[4]) if isinstance(items[4], Tree) else items[4]

        # Since the error indicates you might have a Token, you need to decide how to handle it
        # For a condition or body that's a Token, extracting its value is one approach
        if isinstance(condition, Token):
            condition = condition.value  # Or some appropriate handling
        if isinstance(body, Token):
            body = body.value  # Or some appropriate handling

        return {"type": "given_clause", "condition": condition, "body": body}

    def elsegivenclause(self, items):
        if(len(items) != 0):
            return {"type": "elsegiven_clause", "condition": items[2], "body": items[4]}
        

    def otherwiseclause(self, items):
        if(len(items) != 0):
            return {"type": "otherwise_clause", "body": items[1]}

    # Expressions
    

    def arraydecl(self, items):
        name = items[0].value  # Extracting the name of the array

        # Extracting the data type directly from the Tree structure
        data_type = items[2].children[0].value

        # Extracting the size of the array
        size = items[4]['INTEGER']

        # Extracting the elements. Assuming items[8] contains the elements directly as a list.
        elements_list = items[8]
        elements = []
        for elem in elements_list:
            # Handle dictionaries representing numbers
            if isinstance(elem, dict) and 'type' in elem and elem['type'] == 'number':
                number_value = elem['INTEGER']  # Assuming all numbers are keyed by 'INTEGER'
                elements.append(number_value)
            elif isinstance(elem, Tree):
                # For elements that are Trees (possibly complex structures or expressions), transform them
                transformed_elem = self.transform(elem)
                elements.append(transformed_elem)
            elif isinstance(elem, Token):
                # Handle Tokens directly, especially for simple data types like strings
                if elem.type == 'STRING':
                    elements.append(elem.value[1:-1])  # Removing quotation marks from strings
                elif elem.type == 'NUMBER':
                    elements.append(float(elem.value) if '.' in elem.value else int(elem.value))
            else:
                print(f"Element type not handled in array declaration: {type(elem)} {elem}")

        return {"type": "ArrayDeclaration", "name": name, "dataType": data_type, "size": size, "elements": elements}

    def listdecl(self, items):
        name = items[0].value  # Extracting the list's name
        elements_list = items[3]  # Assuming items[3] is the list of elements
        elements = []
        for elem in elements_list:
            # Skipping commas
            if isinstance(elem, Token) and elem.type == 'COMMA':
                continue
            if isinstance(elem, Tree):
                transformed_elem = self.transform(elem)
                elements.append(transformed_elem)
            else:
                elements.append(elem)

        return {"type": "ListDeclaration", "name": name, "elements": elements}

    def tupledecl(self, items):
        name = items[0].value  # Extracting the tuple's name
        elements_list = items[3]  # Assuming items[3] is the list of elements
        elements = []
        for elem in elements_list:
            # Skipping commas
            if isinstance(elem, Token) and elem.type == 'COMMA':
                continue
            if isinstance(elem, Tree):
                transformed_elem = self.transform(elem)
                elements.append(transformed_elem)
            else:
                elements.append(elem)

        return {"type": "TupleDeclaration", "name": name, "elements": elements}

    def dictionarydecl(self, items):
        name = items[0].value  # Extracting the dictionary name directly from the Token
        key_values = []  # This will hold the formatted key-value pairs

        # Assuming kv_pairs is directly accessible and each kv pair is a list or similar structure
        # that directly contains the key and value as its first two elements
        kv_pairs = items[3:-2][0]  # Adjust this indexing based on actual items' structure

        for kv in kv_pairs:
            # We skip structural elements (like commas, braces) directly
            if isinstance(kv, Token) and kv.type in ['COMMA', 'LCURL', 'RCURL']:
                continue

            # Handling a key-value pair encapsulated in a Tree or dict
            if isinstance(kv, Tree) and kv.data == 'key_value':
                key = self.transform(kv.children[0])  # Transforming or directly accessing the key
                value = self.transform(kv.children[1])  # Transforming or directly accessing the value
                # Append the transformed key-value pair
                key_values.append({'key': key, 'value': value})
            elif isinstance(kv, dict) and 'key' in kv and 'value' in kv:
                # If kv is already a dict with 'key' and 'value', we assume it's already in the desired format
                key_values.append(kv)

        return {"type": "DictionaryDeclaration", "name": name, "keyValues": key_values}
    
    def elements(self, items):
        elements = [items[0]]
        if len(items) > 1:
            for i in range(1, len(items), 2):
                elements.append(items[i])
        return {"type": "elements", "elements": elements}
    
    def element(self, items):
        return items[0]

    # Array Methods
    def array_dim(self, items):
        return {"type": "ArrayDim", "array": items[0]}

    def array_get_idx(self, items):
        return {"type": "ArrayGetIndex", "array": items[0], "index": items[4]}

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
        return {"type": "ListAdd", "list": items[0], "element": items[4]}

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
        dictionary_name = items[0] if isinstance(items[0], str) else self.transform(items[0])
        
        # Directly creating a key-value pair structure, similar to dictionary declarations
        key_value = {
            "key": self.transform(items[4]) if isinstance(items[4], Tree) else items[4],
            "value": self.transform(items[6]) if isinstance(items[6], Tree) else items[6]
        }
        
        # Using "keyValues" to align with the structure in dictionary declarations
        return {
            "type": "DictionarySet",
            "dictionary": dictionary_name,
            "keyValues": [key_value]  # Wrapping the single key-value pair in a list for consistency
        }


    def elements(self, items):
        return items

    def key_values(self, items):
        return items

    def key_value(self, items):
        return {"key": items[0], "value": items[2]}
    
    def inputfunction(self, items):
        prompt = None if not items else items[2]
        return {"type": "input_function", "prompt": prompt}

    def printfunction(self, items):
        return {"type": "print_function", "expresion": items[2]}

    def unaryoperation(self, items):
        operator, variable = items[1], items[0]
        return {"type": "unary_operation", "operator": operator, "variable": variable}

    def striveblock(self, items):
        return {"type": "try_block", "body": items[3]}
    
    def block(self, items):
        # Filter out LCURL and RCURL tokens, keeping only meaningful statements or expressions
        statements = [item for item in items if not isinstance(item, Token) or item.type not in ['LCURL', 'RCURL']]
        
        # Process each statement with transform if they are Trees, directly include otherwise
        processed_statements = [self.transform(statement) if isinstance(statement, Tree) else statement for statement in statements]

        return {
            "type": "block",
            "body": processed_statements
        }
    
    def accessexpression(self, items):
        # Transform the variable part (assuming it's the first item and always a Token or Tree requiring transformation)
        variable = self.transform(items[0]) if isinstance(items[0], Tree) else items[0].value

        # Extracting the index directly from the 'accessoperator' tree
        # Ensure that we are accessing the Tree correctly and safely extract the index value
        if isinstance(items[1], Tree) and items[1].data == 'accessoperator':
            # Find the actual index value, which should be the dictionary with the 'type': 'number'
            # Assuming the second child is the index value (skipping the LSQUARE token)
            index_structure = items[1].children[1]
            if isinstance(index_structure, dict):
                # If the index is directly given as a dictionary (from previous transformation)
                index_value = index_structure.get('INTEGER')
            elif isinstance(index_structure, Tree):
                # If the index is wrapped in a Tree, further transformation might be needed
                index_value = self.transform(index_structure)
            else:
                # Handle other cases as needed, for instance, direct Token handling
                index_value = None
        else:
            index_value = None

        return {
            "type": "accessexpression",
            "variable": variable,
            "index": index_value
        }


    def captureblock(self, items):
        
        return {"type": "catch_block", "body": items[-1]}

    def throwexception(self, items):
        return {"type": "throw_exception", "message": items[2]}

    def loopinterrupt(self, items):
        return {"type": "loop_interrupt"}

    def loopresume(self, items):
        return {"type": "loop_continue"}

    def return_statement(self, items):
        return {"type": "return_statement", "value": items[1]}


def main():
    test_cases_folder = 'our-own-compiler-com-piler-t6/Assignment_6/test_cases'
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
            | accessexpression
            | dictionaryaccess
            | list
            | listaccess
            | negation
            | method_call
            
            

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

    
    ?comparisonoperator: SMALLERTHAN | GREATERTHAN | EQUALEQUAL | NOTEQUALTO | LESSTHANEQUALTO | GREATERTHANEQUALTO


    arithmeticexpr: simpleexpression
   
    ?logicalexpr: comparisonexpr
              | logicalexpr logicaloperator comparisonexpr -> logicaloperation

    ?comparisonexpr: arithmeticexpr
                 | comparisonexpr comparisonoperator arithmeticexpr -> comparisonoperation


    
    logicaloperator: AND | OR


    ?simpleexpression: term ((PLUS|MINUS) term)*  

    ?term: factor ((STAR|SLASH|PERCENT) factor)*

    ?factor: base (CARET factor)?  

    ?base: LPAREN expression RPAREN
        | VARIABLENAME
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
    floatnumber: (PLUS | MINUS)? /[0-9]*\.[0-9]+/

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
    rangeloop: ITERATE LPAREN VARIABLENAME LPAREN datatype RPAREN THROUGH RANGE LPAREN expression DOTDOTDOT expression COMMA expression RPAREN RPAREN block
    iterateloop: ITERATE LPAREN VARIABLENAME LPAREN datatype RPAREN THROUGH VARIABLENAME RPAREN block
    loopinterrupt: INTERRUPT ENDOST
    loopresume: RESUME ENDOST

    exceptionhandling: striveblock captureblock
    striveblock: STRIVE LPAREN RPAREN block
    captureblock: CAPTURE (LPAREN [VARIABLENAME] RPAREN)? block 
    throwexception: THROWEXCEPTION LPAREN STRING RPAREN ENDOST

    unaryoperation: VARIABLENAME INCREMENT ENDOST | VARIABLENAME DECREMENT ENDOST
    assignment: VARIABLENAME EQUALTO expression ENDOST | VARIABLENAME assignmentoperator expression ENDOST
    assignmentoperator: PLUSEQUAL | MINUSEQUAL | TIMESEQUAL | DIVIDEEQUAL | MODEQUAL

    arraydecl: VARIABLENAME LPAREN datatype COMMA number RPAREN EQUALTO LCURL elements RCURL ENDOST 
    listdecl: VARIABLENAME EQUALTO LSQUARE elements RSQUARE ENDOST 
    tupledecl: VARIABLENAME EQUALTO LPAREN elements RPAREN ENDOST 
    dictionarydecl: VARIABLENAME EQUALTO LCURL key_values RCURL ENDOST

    elements: element (COMMA element)* | 
    element: expression

    key_values: key_value (COMMA key_value)* | 
    key_value: key COLON value

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

if __name__ == "__main__":
    main()