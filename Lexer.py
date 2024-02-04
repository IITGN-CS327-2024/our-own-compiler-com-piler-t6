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

import re, os

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
    


def main(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.cmm')]

    for input_file in input_files:
        input_file_path = os.path.join(input_folder, input_file)
        output_file_path = os.path.join(output_folder, input_file.replace('.cmm', '_output.txt'))

        with open(input_file_path, 'r') as file:
            code = file.read()

        lexer = Lexer()
        tokens = lexer.tokenize(code)

        formatter = LexerOutputFormatter()
        formatted_output = formatter.format(tokens)

        with open(output_file_path, 'w') as file:
            for token in formatted_output:
                file.write(token + '\n')

if __name__ == "__main__":
    input_folder = 'our-own-compiler-com-piler-t6/lexer_testcases'
    output_folder = 'our-own-compiler-com-piler-t6/lexer_output'
    main(input_folder, output_folder)
