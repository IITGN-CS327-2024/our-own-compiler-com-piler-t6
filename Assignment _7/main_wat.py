class WATGenerator:
    def __init__(self, ast):
        self.ast = ast

    def generate(self):
        module_wat = '(module\n'
        module_wat += self._generate_wat(self.ast)
        module_wat += ')\n'
        return module_wat

    def _generate_wat(self, node):
        node_type = node['type']
        if node_type == 'program':
            return '\n'.join(self._generate_wat(child) for child in node['children'])
        elif node_type == 'statements':
            # Process each child in the body of the statements node
            return '\n'.join(self._generate_wat(child) for child in node['body'])
        elif node_type == 'function_decl':
            return self._handle_function_decl(node)
        elif node_type == 'block':
            return self._handle_block(node)
        elif node_type == 'return_statement':
            return self._handle_return_statement(node)
        elif node_type == 'arithmetic_expr':
            return self._handle_arithmetic_expr(node)
        else:
            raise ValueError(f"Unsupported node type: {node['type']}")

    def _handle_function_decl(self, node):
        func_name = node['name']
        args_wat = ' '.join(f"(param ${arg['name']} {self._data_type_wat(arg['data_type'])})" for arg in node['args']['names'])
        ret_type_wat = self._data_type_wat(node['return_type'])
        body_wat = self._generate_wat(node['body'])
        result_wat = f"(result {ret_type_wat})"
        func_definition = f"(func ${func_name} {args_wat} {result_wat}\n{body_wat}\n)"
        export_statement = f"(export \"{func_name}\" (func ${func_name}))"
        return func_definition + export_statement

    def _handle_block(self, node):
        return '\n'.join(self._generate_wat(stmt) for stmt in node['body'])

    def _handle_return_statement(self, node):
        expr_wat = self._generate_wat(node['value'])
        return f"(return {expr_wat})"

    def _handle_arithmetic_expr(self, node):
        left_wat = f"(local.get ${node['left']})"
        right_wat = f"(local.get ${node['right']})"
        operator = node['operator']
        op_wat = self._arithmetic_op_wat(operator, 'i32')
        return f"({op_wat} {left_wat} {right_wat})"

    def _data_type_wat(self, data_type):
        return {
            'integer': 'i32',
            'floatpoint': 'f32',
            'double': 'f64'
        }.get(data_type, 'i32')

    def _arithmetic_op_wat(self, operator, type_prefix):
        return {
            '+': f'{type_prefix}.add',
            '-': f'{type_prefix}.sub',
            '*': f'{type_prefix}.mul',
            '%': f'{type_prefix}.rem_s' if 'i32' in type_prefix else f'{type_prefix}.rem',
            '/': f'{type_prefix}.div_s' if 'i32' in type_prefix else f'{type_prefix}.div'
        }[operator]



import json

def main():

    # generator = WATGenerator(ast)
    # wat_code = generator.generate()
    # print(wat_code)
    input_filename = 'AST/arithmetic-test.json'  
    output_filename = 'wat/arithmetic-test.wat'  

    with open(input_filename, 'r') as file:
        ast = json.load(file)

    wat_generator = WATGenerator(ast)
    try:
        print("entered try")
        wat_code = wat_generator.generate()
        # print(wat_code)
        with open(output_filename, 'w') as file:
            file.write(wat_code)
        print(f"WAT code has been generated and saved to {output_filename}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
