import argparse
import os, sys

root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_dir)

from Assignment_2.Lexer import Lexer
default_folder = 'Assignment_2/lexer_testcases'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        for token_type, token_value in self.tokens:
            print(f'<{token_type}, "{token_value}">')

def process_file(file_path):
    print(f"\nProcessing tokens for: {os.path.basename(file_path)}\n--->")
    with open(file_path, 'r') as file:
        code = file.read()

    lexer = Lexer()
    tokens = lexer.tokenize(code)
    parser = Parser(tokens)
    parser.parse()

def main(input_folder, input_file):
    if input_file:
        process_file(input_file)
    else:
        if not input_folder:
            input_folder = default_folder
        input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.cmm')]
        for file_path in input_files:
            process_file(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process .cmm files or a specific file.")
    parser.add_argument('--input_folder', type=str, help="Input folder containing .cmm files")
    parser.add_argument('--input_file', type=str, help="Specific .cmm file to process")
    
    args = parser.parse_args()
    main(args.input_folder, args.input_file)
