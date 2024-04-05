import argparse
import os
import sys
from lark import Lark, Transformer

root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)

from Assignment_2.Lexer import Lexer

default_folder = '../Assignment_6/test_cases'
grammar_file_path = "../Assignment_6/grammer.lark"  

with open(grammar_file_path, "r") as file:
    grammar = file.read()

parser = Lark(grammar, start='start', parser='lalr')

parser_argparse = argparse.ArgumentParser(description="Parse input files for test cases.")
parser_argparse.add_argument("-f", "--test_cases_folder", type=str, default="", help="Folder containing test cases.")
args = parser_argparse.parse_args()

if args.test_cases_folder:
    test_cases_folder = args.test_cases_folder
else:
    test_cases_folder = default_folder

# Get list of files in the folder
test_case_files = [f for f in os.listdir(test_cases_folder) if f.endswith('.cmm')]

for test_case_file in test_case_files:
    test_case_file_path = os.path.join(test_cases_folder, test_case_file)
    with open(test_case_file_path, "r") as file:
        test_cases_content = file.read().split('\n')
    
    print(f"Processing file: {test_case_file_path}")
    for i, case in enumerate(test_cases_content, start=1):
        if not case.strip():
            continue  
        print(f"Test Case {i}: {case}")
        try:
            tokens = list(parser.lex(case))
            print("Tokens:", [str(token) for token in tokens])
            parse_tree = parser.parse(case)
            print("Parse Tree:")
            print(parse_tree.pretty())

        except Exception as e:
            print(f"Error parsing Test Case {i}: {e}")
        print("\n" + "-"*50 + "\n")

class ASTTransformer(Transformer):
    # Program and statements handling
    def start(self, items):
        return {"type": "program", "body": items}

    def statements(self, items):
        return items

    # Function handling
    def functiondecl(self, items):
        _, name, _, args, _, return_type, body = items
        return {"type": "function_decl", "name": name, "args": args, "return_type": return_type, "body": body}

    def arguments(self, items):
        return items

    def argument(self, items):
        name, _, data_type = items
        return {"name": name, "data_type": data_type}

    # Variable and type declarations
    def variabledecl(self, items):
        # print(len(items))
        # for i in items:
        #     print(i)
        # name, _, data_type, _, value = items (incorrect)
        name, _, data_type, _, _, value, _ = items
        temp = str(data_type)
        lr = temp.split("'")
        check = lr[len(lr)-2]
        # print(check)
        # print(type(value))
        if(check == "integer" and (not isinstance(value, int))):
            raise Exception("Expected integer got ", type(value))

        if(check == "character" and (not isinstance(value, str))):
            if(isinstance(value, str) and len(value) == 1):
                raise Exception("Expected character got ", type(value))

        if(check == "floatpoint" and (not isinstance(value, float))):
            raise Exception("Expected floatpoint got ", type(value))

        if(check == "textwave" and (not isinstance(value, str))):
            raise Exception("Expected textwave got ", type(value))

        if(check == "flag" and (not isinstance(value, bool))):
            raise Exception("Expected flag got ", type(value))

        return {"type": "variable_decl", "name": name, "data_type": data_type, "value": value}

    def immutablevariabledecl(self, items):
        _, name, _, data_type, _, value = items
        # print("Hellooo", data_type)
        return {"type": "immutable_variable_decl", "name": name, "data_type": data_type, "value": value}

    # Loops
    def whileloop(self, items):
        _, condition, body = items
        return {"type": "while_loop", "condition": condition, "body": body}

    def iterateloop(self, items):
        _, _, variable, _, data_type, _, start, _, through, _, end, _, step, _, body = items
        return {"type": "iterate_loop", "variable": {"name": variable, "data_type": data_type}, "start": start, "through": through, "end": end, "step": step, "body": body}

    def rangeloop(self, items):
        _, _, variable, _, data_type, _, start, _, _, range_start, _, range_end, _, step, _, body = items
        return {"type": "range_loop", "variable": {"name": variable, "data_type": data_type}, "start": start, "range_start": range_start, "range_end": range_end, "step": step, "body": body}

    # Conditionals
    def conditional(self, items):
        clauses = []
        for item in items:
            if item['type'] in ['given_clause', 'elsegiven_clause', 'otherwise_clause']:
                clauses.append(item)
        return {"type": "conditional", "clauses": clauses}

    def givenclause(self, items):
        _, condition, body = items
        return {"type": "given_clause", "condition": condition, "body": body}

    def elsegivenclause(self, items):
        _, condition, body = items
        return {"type": "elsegiven_clause", "condition": condition, "body": body}

    def otherwiseclause(self, items):
        _, body = items
        return {"type": "otherwise_clause", "body": body}

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

    # Method calls and other specific nodes
    # Implement methods for method_call, array_methods, list_methods, etc., as per your grammar

    # Add methods for any other nodes you need to handle...

# Initialize the parser with the corrected grammar and the transformer
parser = Lark(grammar, start='start', parser='lalr', transformer=ASTTransformer())

# Example program text for parsing
program_text = [
    """x(integer) = 5.0;""",
    """x(character) = 5;""",
    """x(floatpoint) = 5;""",
    """x(textwave) = 5;""",
    """x(flag) = 5;""",
]

# Parse and transform the program text into an AST
for i in program_text:
    ast = parser.parse(i)
    print(ast)