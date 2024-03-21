import argparse
import os
import sys
from lark import Lark

root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)

from Assignment_2.Lexer import Lexer

default_folder = 'Assignment_5/test_cases'
grammar_file_path = "Assignment_5/grammer.lark"  

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
