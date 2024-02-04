# keywords = {
#     'pendown', 'penup', 'integer', 'character', 'floatpoint', 'doublepoint', 'textwave', 'flag',
#     'True', 'False', 'given', 'elsegiven', 'otherwise', 'iterate', 'through', 'fn', 'exitwith', 
#     'strive', 'capture', 'immute', 'interrupt', 'resume', 'dim', 'sort','while', 'add', 'remove', 
#     'exchange', 'getidx', 'asc', 'dsc','tail', 'head',
# }

# binary_operators = {
#     '+', '-', '*', '/', '%', '^', '==', '!=', '>', '<', '>=', '<=', '=', '+=', '-=', 
#     '*=', '/=', '%=', '&&', '$$', '!'
# }

# unary_operators = {
#     '++', '--'
# }

# whitespace = {
#     ' ', '\n', '\t'
# }

# parenthesis = {
#     '(', ')', '[', ']', '{', '}'
# }

# delimiters = {
#     ';', ',', '.',':'
# }
import re

class Lexer:
    def __init__(self):
        self.token_patterns = {
            # Comments
            'single_line_comment': r'#.*',
            'multi_line_comment': r'"""[\s\S]*?"""',
            # Keywords
            'keywords': r'\b(pendown|penup|integer|character|floatpoint|doublepoint|textwave|flag|True|False|given|elsegiven|otherwise|iterate|through|fn|exitwith|strive|capture|immute|interrupt|resume|dim|sort)\b',
            # Operators
            'unary_operators': r'(\+\+|--)',
            'binary_operators': r'(\+|\-|\*|\/|%|\^|==|!=|>|<|>=|<=|=|\+=|\-=|\*=|\/=|%=|&&|\$\$|!)',
            # Brackets and Parentheses
            'parenthesis': r'([\(\)\[\]\{\}])',
            # Floating point numbers  
            'float_literal': r'\b-?\d+\.\d*\b|\b-?\.\d+\b',
            # Integer literals
            'integer_literal': r'\b\d+\b',
            # Delimiters (excluding the dot as it's handled in float_literal)
            'delimiters': r'(;|,|:|\.)',
            # String literals
            'string_literal': r'"[^"]*"',
            # Boolean literals
            'boolean_literal': r'\b(True|False)\b',
            # Identifiers
            'identifier': r'\b[a-zA-Z_][a-zA-Z_0-9]*\b',
            
        }
        # Combine patterns, prioritizing float_literal and integer_literal correctly
        self.combined_pattern = '|'.join(f'(?P<{k}>{v})' for k, v in self.token_patterns.items())

    def tokenize(self, code):
        tokens = []
        for match in re.finditer(self.combined_pattern, code):
            token_type = match.lastgroup
            token_value = match.group()
            if token_type not in ['single_line_comment', 'multi_line_comment']:
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

def main(input_file, output_file):
    with open(input_file, 'r') as file:
        code = file.read()

    lexer = Lexer()
    tokens = lexer.tokenize(code)
    
    formatter = LexerOutputFormatter()
    formatted_output = formatter.format(tokens)
    
    with open(output_file, 'w') as file:
        for token in formatted_output:
            file.write(token + '\n')

if __name__ == "__main__":
    input_file = 'test_cases.txt'  
    output_file = 'lexer_output.txt' 
    main(input_file, output_file)