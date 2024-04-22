import os
import sys
from lark import Lark, Transformer, Tree, Token, Visitor
import operator
import logging
import json

class SymbolTable:
    def __init__(self):
        self.stack = [{}]

    def enter_scope(self):
        self.stack.append({})

    def exit_scope(self):
        if self.stack:
            current_scope = self.stack.pop()
            # print(f"Exiting scope, variables in this scope are: {list(current_scope.keys())}")
            return current_scope
        return None

    def define_symbol(self, name, info):
        if name in self.stack[-1]:
            # print(f"Error: Variable '{name}' is declared multiple times in the same scope.")
            return False  # Already declared in the current scope
        self.stack[-1][name] = info
        # print(f"Variable '{name}' added to scope with info: {info}")
        return True
    
    def update_symbol(self, name, new_value):
        for scope in reversed(self.stack):
            if name in scope:
                old_info = scope[name]
                old_info['value'] = new_value  # Update the value while preserving the type
                # print(f"Variable '{name}' updated in scope with new value: {new_value}")
                return True
        # print(f"Error: Variable '{name}' is accessed before declaration.")
        return False


    def lookup_symbol(self, name):
        for scope in reversed(self.stack):
            if name in scope:
                return scope[name]
        return None  # Symbol not found

    def lookup_symbol_in_current_scope(self, name):
        return name in self.stack[-1]

    def print_symbol_table(self):
        for i, scope in enumerate(self.stack):
            print(f"Scope level {i}: {scope}")

class ASTTransformer(Transformer):
    def __init__(self, symbol_table):
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '^': operator.pow,
            'AND': operator.and_,  
            'OR': operator.or_,    
            '<': operator.lt,
            '>': operator.gt,
            '==': operator.eq,
            '!=': operator.ne,
            '<=': operator.le,
            '>=': operator.ge
        }
        self.symbol_table = symbol_table
        self.errors = []

    def evaluate_expression(self, node, path=''):
        try:
            # Check if the node is a simple type or already evaluated
            if isinstance(node, int):
                return node
            elif isinstance(node, dict) and 'type' in node:
                if node['type'] == 'number':
                    return int(node['INTEGER'])

                elif node['type'] == 'arithmetic_expr':
                    # Construct the path for debugging
                    new_path = f"{path} -> {node['operator']}"

                    # Recursively evaluate the left and right expressions
                    left_val = self.evaluate_expression(node['left'], path=new_path + " (left)")
                    right_val = self.evaluate_expression(node['right'], path=new_path + " (right)")
                    
                    # Check if operators and their application have been defined properly
                    if node['operator'] in self.operators:
                        return self.operators[node['operator']](left_val, right_val)
                    else:
                        raise ValueError(f"Unsupported operator: {node['operator']}")

                else:
                    raise ValueError(f"Unsupported expression type: {node['type']} at path {path}")
            else:
                # If the node does not match expected patterns, raise an error
                raise TypeError(f"Node of unexpected type or structure: {node}")

        except Exception as e:
            # Log the error with detailed node information
            logging.error(f"Failed to evaluate node at path {path}: {node}")
            raise TypeError(f"Error evaluating expression at {path}: {e}") from e


    def start(self, items):
        return {"type": "program", "body": items[0]}

    def statements(self, items):
        return {"type": "statements", "body": items}
    
    def variabledecl(self, items):
        name = items[0]
        datatype_tree = items[2]
        expression = items[5]

        datatype = datatype_tree.children[0].value
        
        return {
            "type": "variable_decl",
            "name": str(name),
            "value": expression
        }
    
    def functiondecl(self, items):
        name = items[1]
        args = items[3]
        return_type = items[6]
        body = items[7]
        return {"type": "function_decl", "name": name, "args": args, "return_type": return_type, "body": body}

    def assignment(self, items):
        name = items[0]
        assignmentoperator = items[1]   
        expression = items[2]
        return {"type": "assignmentoperator", "name": name, "value": expression}
   

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
    
    def functioncall2(self, items):
        name = items[0]
        args = items[2]
        return {"type": "function_call", "name": name, "args": args}
    
    def functionargs(self, items):
        # This will filter out commas and return only meaningful items
        return [self.functionarg(item) for item in items if not isinstance(item, Token) or item.type != 'COMMA']

    def functionarg(self, items):
        # Assuming 'items' is a list where each item could be a single token or another structure
        # If the item is a token, it might be a variable name, a number, or another single value
        if isinstance(items, Token):
            return {'type': 'Token', 'token_type': items.type, 'value': items.value}
        # If the item is a more complex expression, it needs deeper handling
        elif isinstance(items, Tree):
            return self.construct_ast_dictionary(items)
        # If it's already a dictionary (possibly from previous processing), return as is
        elif isinstance(items, dict):
            return items
        # Otherwise, just return the item as it might be a primitive or already processed value
        else:
            return items
    
    def expression(self, items):
        return items[0]

    def arithmeticexpr(self, items):
        return self.evaluate_expression(items[0])

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
        if len(items) == 1:
            return items[0]
        else:
            return items[1]
        
    

    def evaluate_expressionlc(self, node, path=''):
        try:
            if isinstance(node, int):
                return node
            elif isinstance(node, dict) and 'type' in node:
                if node['type'] in ['logicalexpr', 'comparisonexpr']:
                    # Evaluate left and right recursively and then apply the logical or comparison operator
                    left_val = self.evaluate_expressionlc(node['left'], path=path + " (left)")
                    right_val = self.evaluate_expressionlc(node['right'], path=path + " (right)")
                    
                    # Extract operator from token if it's a Token object, otherwise use as is
                    operator = node['operator'].value if isinstance(node['operator'], Token) else node['operator']
                    
                    print(f"Evaluating {node['type']} with operator {operator}")

                    # Check if the operator is supported and perform the operation
                    if operator in self.operators:
                        result = self.operators[operator](left_val, right_val)
                        return 1 if result else 0
                    else:
                        raise ValueError(f"Unsupported operator {operator} in {node['type']} at path {path}")

                elif node['type'] == 'arithmetic_expr':
                    # Process arithmetic expression similarly but return the computed value directly
                    left_val = self.evaluate_expressionlc(node['left'], path=path + " (left)")
                    right_val = self.evaluate_expressionlc(node['right'], path=path + " (right)")
                    
                    # Extract operator from token if it's a Token object, otherwise use as is
                    operator = node['operator'].value if isinstance(node['operator'], Token) else node['operator']

                    print(f"Evaluating {node['type']} with operator {operator}")

                    return self.operators[operator](left_val, right_val)
                else:
                    raise ValueError(f"Unsupported node type for expression evaluation: {node['type']} at path {path}")
            else:
                raise TypeError(f"Unexpected node type or structure: {node}")
        except Exception as e:
            logging.error(f"Failed to evaluate node at path {path}: {node}")
            raise TypeError(f"Error evaluating expression at {path}: {e}")

    def arithmeticexpr(self, items):
        if len(items) == 1:
            return self.evaluate_expressionlc(items[0])
        else:
            expr = items[0]
            for i in range(1, len(items), 2):
                operator = items[i]
                right_expr = items[i + 1]
                expr = {"type": "arithmetic_expr", "operator": operator, "left": expr, "right": right_expr}
            return self.evaluate_expressionlc(expr)

    def logicalexpr(self, items):
        return self.evaluate_expressionlc(self.logicalexpr_constructor(items))

    def comparisonexpr(self, items):
        return self.evaluate_expressionlc(self.comparisonexpr_constructor(items))

    def logicalexpr_constructor(self, items):
        if len(items) == 1:
            return items[0]
        else:
            expr = items[0]
            for i in range(1, len(items), 2):
                operator = items[i]
                right_expr = items[i + 1]
                expr = {"type": "logicalexpr", "operator": operator, "left": expr, "right": right_expr}
            return expr

    def comparisonexpr_constructor(self, items):
        if len(items) == 1:
            return items[0]
        else:
            expr = items[0]
            for i in range(1, len(items), 2):
                operator = items[i]
                right_expr = items[i + 1]
                expr = {"type": "comparisonexpr", "operator": operator, "left": expr, "right": right_expr}
            return expr

    def conditional(self, items):
        clauses = []
        for item in items:
            if item is not None:
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
        condition = items[1:5]
        body = items[4]
        print(condition)
        return {"type": "given_clause", "condition": condition, "body": body}

    def elsegivenclause(self, items):
        if(len(items) != 0):
            return {"type": "elsegiven_clause", "condition": items[2], "body": items[4]}
        

    def otherwiseclause(self, items):
        if(len(items) != 0):
            return {"type": "otherwise_clause", "body": items[1]}

    def STRING(self, items):
        value = str(items[1:-1]) 
        print(value)
        return value

    def number(self, items):
        value = int(items[0])
        return value

    def floatnumber(self, items):
        value = float(items[0])
        return value


    def immutablevariabledecl(self, items):
        name = items[1]  
        datatype = items[3] 
        expression = items[6]
        return {"type": "immutable_variable_decl", "name": name, "datatype":datatype,   "value": expression}
    
    def whileloop(self, items):
        return {"type": "while_loop", "condition": items[2], "body": items[4]}

    def rangeloop(self, items):
        var_name = items[2]  
        var_type = items[4]  
        range_start = items[9]  
        range_end = items[11]  
        step = items[13] 

        return {
            "type": "iterate_loop_range",
            "variable": {"name": var_name, "data_type": var_type},
            "range_start": range_start,
            "range_end": range_end,
            "step": step,
            "body": items[-1]  
        }

    def iterateloop(self, items):
        var_name = items[2]  
        var_type = items[4] 
        list_name = items[7]  

        return {
            "type": "iterate_loop_list",
            "variable": {"name": var_name, "data_type": var_type},
            "through": list_name,
            "body": items[-1]  
        }
    
    def elements(self, items):
        elements = []
        for item in items:
            if isinstance(item, int):  # Directly handle integer values
                elements.append(item)
            elif isinstance(item, float):  # Handle float values
                elements.append(item)
            elif isinstance(item, Token):  
                if item.type == 'STRING' or item.type == 'CHARACTER':
                    # Remove quotation marks for strings or characters
                    elements.append(item.value.strip('"').strip("'"))
                elif item.type == 'NUMBER':
                    # Convert numbers to float or int
                    elements.append(float(item.value) if '.' in item.value else int(item.value))
            elif isinstance(item, Tree):
                # For Trees, call a specific function that can handle complex structures
                # Assuming a function `transform_tree_to_value` exists to handle Trees
                transformed_value = self.transform_tree_to_value(item)
                elements.append(transformed_value)
            else:
                # Log or handle unexpected types
                print(f"Unhandled item type in elements list: {type(item)} {item}")
        return {"type": "elements", "elements": elements}

    def arraydecl(self, items):
        name = items[0].value  # Extracting the name of the array

        # Extracting the data type directly from the Tree structure
        data_type = items[2].children[0].value

        # Extracting the size of the array
        size = items[4]

        # Assuming items[8] contains the list of elements directly; modifying if needed based on actual structure
        elements_list = items[8]  # Assuming items[3] is the list of elements
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
    
    def listdecl(self, items):
        name = items[0].value  # Extracting the list's name
        elements_list = items[5]  # Assuming items[3] is the list of elements
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
        return {"type": "print_function", "value": items[2]}


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
        variable = self.transform(items[0]) if isinstance(items[0], Tree) else items[0].value


        if isinstance(items[1], Tree) and items[1].data == 'accessoperator':

            index_structure = items[1].children[1]
            if isinstance(index_structure, dict):

                index_value = index_structure.get('INTEGER')
            elif isinstance(index_structure, Tree):
                index_value = self.transform(index_structure)
            else:
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
    
    def construct_ast_dictionary(self, tree):
        if isinstance(tree, Tree):
            # Convert Tree to a dictionary
            return {
                'type': tree.data,
                'children': [self.construct_ast_dictionary(child) for child in tree.children]
            }
        elif isinstance(tree, Token):
            # Convert Token to a dictionary
            return {'type': 'Token', 'token_type': tree.type, 'value': tree.value}
        else:
            return tree  # Return as is if it's already a basic type

  

class MyASTTransformer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errors = []

    def block(self, tokens):
        keywords = {
            "immute", "integer", "character", "floatpoint", "textwave", "flag", "True", "False",
            "fn", "while", "iterate", "through", "range", "interrupt", "resume", "strive",
            "capture", "Given", "ElseGiven", "Otherwise", "throwexception", "array_dim",
            "array_get_idx", "array_tail", "array_head", "array_exchange", "array_sort",
            "list_dim", "list_exchange", "list_get_idx", "list_tail", "list_head", "list_sort",
            "list_add", "list_remove", "tuple_dim", "tuple_get_idx", "tuple_tail", "tuple_head",
            "dictionary_set", "pendown", "penup", "asc", "desc", "exitwith"
        }

        # print("Starting block function...")
        self.symbol_table.enter_scope()
        i = 0
        while i < len(tokens):
            token = tokens[i]
            # print(f"Processing token: {token.type} with value: {token.value}")
            if token.type == 'LCURL':
                self.symbol_table.enter_scope()
                # print("Entered new scope")
            elif token.type == 'RCURL':
                self.symbol_table.exit_scope()
                # print("Exiting current scope")
            elif token.type == 'FN': 
                function_name = tokens[i+1].value
                i += 3  
                parameters = []
                self.symbol_table.enter_scope()
                while tokens[i].type != 'RPAREN':
                    param_name = tokens[i].value
                    if tokens[i+1].type != 'LPAREN' or tokens[i+3].type != 'RPAREN':
                        raise Exception("Syntax Error in parameter declaration")
                    param_type = tokens[i+2].value
                    parameters.append((param_name, param_type))
                    self.symbol_table.define_symbol(param_name, {'type': param_type, 'value': None})
                    i += 4  # Move past param_name(LPAREN param_type RPAREN)
                    if tokens[i].type == 'COMMA':
                        i += 1 
                i += 1
                if tokens[i].type != 'ARROW':
                    # print(tokens[i].type)
                    raise Exception("Syntax Error: Expected '->' after parameters")
                return_type = tokens[i+1].value
                i += 2
                self.symbol_table.define_symbol(function_name, {
                    'type': 'function', 'parameters': parameters, 'return_type': return_type,
                })
            elif token.type == 'VARIABLENAME':
                if token.value in keywords:
                    self.errors.append(f"Semantic Error: '{token.value}' is a reserved keyword and cannot be used as a variable name.")
                else:
                    next_token = tokens[i+1]
                    if next_token.type == 'LPAREN':  # Start of a declaration or a function call
                        if (i+4) < len(tokens) and tokens[i+4].type == 'EQUALTO':  # Declaration
                            type_info = tokens[i+2].value
                            if tokens[i+3].type == 'RPAREN':
                                value_info = tokens[i+5].value
                                if not self.symbol_table.lookup_symbol_in_current_scope(token.value):
                                    self.symbol_table.define_symbol(token.value, {'type': type_info, 'value': value_info})
                                    i += 5  # Advance index past the declaration
                                else:
                                    self.errors.append(f"Error: Redefinition of '{token.value}' in the same scope is not allowed.")
                        else:
                            i += 2  # Move to the first argument or to ')'
                            args = []
                            arg_types = []
                            while tokens[i].type != 'RPAREN':
                                if tokens[i].type == 'VARIABLENAME':
                                    arg_value = tokens[i].value
                                    args.append(arg_value)
                                    var_info = self.symbol_table.lookup_symbol(arg_value)
                                    if var_info:
                                        arg_types.append(var_info['type'])
                                    else:
                                        self.errors.append(f"Error: Variable '{arg_value}' used as argument not declared.")
                                i += 1  # Move to ',' or ')'
                                if tokens[i].type == 'COMMA':
                                    i += 1  # Skip ','
                          
                            i += 1  # Skip past ')'
                            if tokens[i].type == 'ENDOST':
                                # Confirm it's a function call by the presence of ';'
                                func_info = self.symbol_table.lookup_symbol(token.value)
                                if func_info:
                                    # Validate the number and types of arguments
                                    param_types = [param[1] for param in func_info['parameters']]
                                    if len(func_info['parameters']) == len(args) and param_types == arg_types:
                                        # print(f"Function call to {token.value} is valid with arguments {args}.")
                                        pass
                                    else:
                                        mismatch_detail = " or incorrect types of arguments." if len(func_info['parameters']) == len(args) else " or incorrect number of arguments."
                                        self.errors.append(f"Function '{token.value}' called with incorrect arguments" + mismatch_detail)
                                else:
                                    self.errors.append(f"Function '{token.value}' called but not declared.")
                                i += 1  # Move past ';'
                            else:
                                self.errors.append(f"Syntax error near {token.value}, expected ';'.")
                    elif next_token.type == 'EQUALTO':
                        if self.symbol_table.lookup_symbol(token.value):
                            value_info = tokens[i+2].value
                            self.symbol_table.update_symbol(token.value, value_info) 
                            i += 2  
                        else:
                            self.errors.append(f"Error: Variable '{token.value}' is accessed before declaration.")
                    
            i += 1
        # print("Exiting top scope")
        if self.errors:
            for error in self.errors:
                print(error)
        # print("Symbol table state at end of block:", self.symbol_table.stack)


def collect_tokens(node, tokens=None):
    if tokens is None:
        tokens = []

    if isinstance(node, Tree):
        for child in node.children:
            collect_tokens(child, tokens)
    elif isinstance(node, Token):
        tokens.append(node)
    elif isinstance(node, (list, tuple)):
        for item in node:
            collect_tokens(item, tokens)
    return tokens



def save_ast_to_file(ast_dict, filename):
    # Check if the filename contains a directory path
    directory = os.path.dirname(filename)
    
    # If the directory is not empty, ensure it exists
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    # Now, save the file
    with open(filename, 'w') as file:
        json.dump(ast_dict, file, indent=4)

def main():
    test_cases_folder = 'test_cases'
    ggrammar = """
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
            | STRING
            | CHARACTER
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
              | logicalexpr logicaloperator comparisonexpr 

    ?comparisonexpr: arithmeticexpr
                 | comparisonexpr comparisonoperator arithmeticexpr 


    
    logicaloperator: AND | OR


    ?simpleexpression: term ((PLUS|MINUS) term)*  

    ?term: factor ((STAR|SLASH|PERCENT) factor)*

    ?factor: base (CARET factor)?  

    ?base: LPAREN expression RPAREN
        | VARIABLENAME
        | number
        | floatnumber   
        | TRUE
        | FALSE
        | functioncall2 


    accessexpression: VARIABLENAME accessoperator
    accessoperator: LSQUARE number RSQUARE | LSQUARE number COLON number RSQUARE


    number: (PLUS | MINUS)? /[0-9]+/
    floatnumber: (PLUS | MINUS)? /[0-9]*\.[0-9]+/

    literal: number | floatnumber | CHARACTER | TRUE | FALSE | STRING


    conditional: givenclause elsegivenclause otherwiseclause
    givenclause: GIVEN LPAREN [logicalexpr | comparisonexpr] RPAREN block
    elsegivenclause: ELSEGIVEN LPAREN [logicalexpr | comparisonexpr] RPAREN block | 
    otherwiseclause: OTHERWISE block | 

    functiondecl: FN functionname LPAREN arguments RPAREN ARROW datatype block
    ?arguments: argument (COMMA argument)* |
    ?argument: augumentname LPAREN datatype RPAREN

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


    printfunction: PENDOWN LPAREN (expression | STRING) RPAREN ENDOST
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
    functionname: /[a-zA-Z_][a-zA-Z0-9_]*/
    augumentname: /[a-zA-Z_][a-zA-Z0-9_]*/
    key: expression
    value: expression
    anytext: /(?:[^"\\]|\\.)?/     
    STRING: /"(?:[^"\\\\]|\\\\.)*"/
    CHARACTER: /'.'/ 
    %ignore " "
    %ignore /\s+/
"""
    parser = Lark(ggrammar, start='start', parser='lalr')
    symbol_table = SymbolTable()
    # transformer1 = MyASTTransformer(symbol_table)
    transformer = ASTTransformer(symbol_table)

    test_case_files = [f for f in os.listdir(test_cases_folder) if f.endswith('.cmm')]

    for test_case_file in test_case_files:
        test_case_file_path = os.path.join(test_cases_folder, test_case_file)
        with open(test_case_file_path, "r") as file:
            test_cases_content = file.read()

    parse_tree = parser.parse(test_cases_content)
    ast = transformer.transform(parse_tree)
    tokens_list = collect_tokens(parse_tree)  
    print(ast)
    # transformer1.block(tokens_list)
    if ast:
        output_path = 'output_ast.json'
        ast_dict = transformer.construct_ast_dictionary(ast)  # Double-check conversion
        print("AST Dictionary:")
        print(ast_dict)
        save_ast_to_file(ast_dict, output_path)
    else:
        print("No AST generated.")
if __name__ == "__main__":
    main()


