# Token Classes

"""
keywords = {
    'pendown', 'penup', 'integer', 'character', 'floatpoint', 'doublepoint', 'textwave', 'flag',
    'true', 'false', 'given', 'elsegiven', 'otherwise', 'iterate', 'through', 'fn', 'exitwith', 
    'strive', 'capture', 'immute', 'interrupt', 'resume', 'dim', 'sort','while', 'add', 'remove', 
    'exchange', 'getidx', 'asc', 'dsc','tail', 'head', 'range', 'throwexception'
}

binary_operators = {
    '+', '-', '*', '/', '%', '^', '==', '!=', '>', '<', '>=', '<=', '=', '+=', '-=', 
    '*=', '/=', '%=', '&&', '$$', '!'
}

unary_operators = {
    '++', '--'
}

whitespace = {
    ' ', '\n', '\t'
}

parentheses = {
    '(', ')', '[', ']', '{', '}'
}

delimiters = {
    ';', ',' , '.' , ':'
}

range_delimiters = {
   ...
}

float_literal = { 
1.5, 0.4, 
}

integer_literal = {
e.g. 1,2,3
}

string_literal = {
e.g. "hello"
}

char_literal = {
e.g. 'a'
}


identifier = {
e.g. var1, var2, var3
}

"""

import re, os, argparse

class Lexer:
    def __init__(self):
        self.token_patterns = {
            'single_line_comment': r'#.*',
            'multi_line_comment': r'"""[\s\S]*?"""',
            'string_literal': r'"(?:\\.|[^"\\])*"',
            'char_literal': r"'(?:\\.|[^'\\])'",
            'range_delimiter': r'\.\.\.',
            'keywords': r'\b(pendown|penup|integer|character|floatpoint|doublepoint|textwave|flag|true|false|given|elsegiven|otherwise|iterate|through|fn|exitwith|strive|capture|immute|interrupt|resume|dim|sort|while|add|remove|exchange|getidx|asc|dsc|tail|head|range|throwexception)\b',
            'float_literal': r'-?\b\d+\.\d*\b|-?\b\d+\.\b',
            'integer_literal': r'-?\b\d+\b',
            'unary_operators': r'(\+\+|--)',
            'binary_operators': r'(\+|\-|\|\/|%|\^|==|!=|>|<|>=|<=|=|\+=|\-=|\=|\/=|%=|&&|\$\$|!)',
            'parentheses': r'([\(\)\[\]\{\}])',
            'delimiters': r'(;|,|:|\.)',
            'identifier': r'\b[a-zA-Z_][a-zA-Z_0-9]*\b',
            'whitespace': r'[ \n\t]+',
        }
        self.combined_pattern = '|'.join(f'(?P<{k}>{v})' for k, v in self.token_patterns.items())

    def tokenize(self, code):
        tokens = []
        for match in re.finditer(self.combined_pattern, code):
            token_type = match.lastgroup
            token_value = match.group()
            if token_type not in ['single_line_comment', 'multi_line_comment', 'whitespace']:
                tokens.append((token_type, token_value))
        return tokens

class LexerOutputFormatter:
    @staticmethod
    def format(tokens):
        formatted_output = []
        for token_type, token_value in tokens:
            if token_type == 'string_literal':
                formatted_output.append(f'<string, {token_value}>')
            else:
                formatted_output.append(f'<{token_type}, "{token_value}">')
        return formatted_output
    
def prcoess_File(file_path, lexer, output_folder):
    with open(file_path, 'r') as file:
        content = file.read()
    tokens = lexer.tokenize(content)

    formatted_output = LexerOutputFormatter.format(tokens)

    base_name = os.path.basename(file_path)
    output_file_name = os.path.splitext(base_name)[0] + '_tokens.txt'
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(output_file_path, 'w') as output_file:
        for token in formatted_output:
            output_file.write(token + '\n')

def main():
    parser = argparse.ArgumentParser(description='Lexer for processing files')
    parser.add_argument('input_files', nargs='*', help='Input files to process')
    parser.add_argument('--output', '-o', default='Assignment_2\lexer_output', help = 'Output directory for lexer output') 
    args = parser.parse_args()

    output_folder = args.output
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    lexer = Lexer()

    if args.input_files:
        for input_file in args.input_files:
            prcoess_File(input_file, lexer, args.output)   
    else:
        input_folder = 'Assignment_2\lexer_testcases'
        output_folder = 'Assignment_2\lexer_output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        input_files = [f for f in os.listdir(input_folder) if f.endswith('.cmm')]

        for input_file in input_files:
            input_file_path = os.path.join(input_folder, input_file)
            prcoess_File(input_file_path, lexer, output_folder)

        
if __name__ == "__main__":
    main()