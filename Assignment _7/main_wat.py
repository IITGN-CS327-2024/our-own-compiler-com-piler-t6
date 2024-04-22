import json 

class WATGenerator:
    def __init__(self):
        self.memory_index = 0
        self.variables = []
        print("WATGenerator initialized.")
        self.debug = True

    def log(self, message):
        if self.debug:
            print(message)

    def generate_wat(self, node):
        node_type = node['type']
        method_name = 'handle_' + node_type
        self.log(f"Processing node type: {node_type}")

        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(node)
        else:
            self.log(f"Warning: No handler for node type '{node_type}'")
            return f"; Unsupported node type: {node_type}\n"

    def handle_program(self, node):
        self.log("Building the module structure...")
        wat = '(module\n'
        for stmt in node['body']:
            statement_wat = self.generate_wat(stmt)
            if statement_wat:
                wat += statement_wat
        wat += ')\n'
        return wat

    def handle_variable_decl(self, node):
        name = node['name']
        value = node['value']
        self.variables.append(name)  # Track declared variables

        # Check if value is a simple integer or a complex expression
        if isinstance(value, dict) and 'type' in value:
            # Handle expressions differently
            computed_value = self.generate_wat(value)  # Evaluate the expression
            wat = f"(global ${name} (mut i32) \n  (i32.const 0)\n)  ; Initial dummy value\n"
            wat += f"(func (export \"init_{name}\")\n  (global.set ${name} \n    {computed_value}))\n"
        else:
            # Assume it's a simple integer
            wat = f"(global ${name} (mut i32) (i32.const {value}))\n"

        print(f"Variable {name} declared with value {value}")
        return wat


    def handle_function_decl(self, node):
        # Start function definition
        wat = f"(func ${node['name']} "
        # Add parameters and return type
        wat += ' '.join(f"(param ${param['name']} i32)" for param in node['args'])
        wat += " (result i32)\n"  # Assuming integer return type for simplicity
        for stmt in node['body']:
            wat += self.generate_wat(stmt)
        wat += ')\n'
        return wat

    def handle_function_call(self, node):
        # Construct function call WAT code
        args = ' '.join(f"(i32.const {arg})" for arg in node['args'])  # Simplified
        wat = f"(call ${node['name']} {args})\n"
        return wat

    def handle_arithmetic_expr(self, node):
        # Map arithmetic operations to WAT instructions
        left = self.generate_wat(node['left'])
        right = self.generate_wat(node['right'])
        op_map = {'+': 'i32.add', '-': 'i32.sub', '*': 'i32.mul', '/': 'i32.div_s'}
        operator = op_map[node['operator']]
        wat = f"{left} {right} {operator}\n"
        return wat

    def handle_logical_expr(self, node):
        left = self.generate_wat(node['left'])
        right = self.generate_wat(node['right'])
        operator = node['operator']

        if operator == 'AND':
            # Simulate logical AND with integer comparison
            return f"{left} {right} i32.and\n"
        elif operator == 'OR':
            # Simulate logical OR with integer comparison
            return f"{left} {right} i32.or\n"
        else:
            return f"; Unsupported logical operator {operator}\n"


    def handle_comparison_expr(self, node):
        left = self.generate_wat(node['left'])
        right = self.generate_wat(node['right'])
        operator = node['operator']

        op_map = {
            'SMALLERTHAN': 'i32.lt_s',
            'GREATERTHAN': 'i32.gt_s',
            'EQUALEQUAL': 'i32.eq',
            'NOTEQUALTO': 'i32.ne',
            'LESSTHANEQUALTO': 'i32.le_s',
            'GREATERTHANEQUALTO': 'i32.ge_s'
        }
        wat_operator = op_map.get(operator, '; Unsupported comparison operator')
        return f"{left} {right} {wat_operator}\n"


    def handle_while_loop(self, node):
        # Construct a WAT loop block
        condition = self.generate_wat(node['condition'])
        body = self.generate_wat(node['body'])
        wat = f"(loop {condition} {body} end)\n"
        return wat

    def handle_iterate_loop_range(self, node):
        var_name = node['variable']['name']
        range_start = node['range_start']
        range_end = node['range_end']
        step = node['step']
        body = node['body']

        wat = f"""
        (block
            (loop
                (local.set ${var_name} (i32.const {range_start}))
                (br_if 1 (i32.ge_s (local.get ${var_name}) (i32.const {range_end})))
                {self.generate_wat(body)}
                (local.set ${var_name} (i32.add (local.get ${var_name}) (i32.const {step})))
                (br 0)
            )
        )
        """
        return wat


    def handle_conditional(self, node):
        if_statements = []
        for clause in node['clauses']:
            condition = self.generate_wat(clause['condition'])
            body = self.generate_wat(clause['body'])
            if_statement = f"{condition} (if (then {body}))"
            if_statements.append(if_statement)

        return "\n".join(if_statements) + "\n"


    def handle_array_decl(self, node):
        # Example: Declare a memory segment for an array with initial values
        name = node['name']
        data_type = 'i32'  # Simplifying: assuming all data types are i32 for this example
        size = node['size']
        elements = ' '.join(f"(i32.const {elem})" for elem in node['elements'])
        
        # Store the array in memory and set a global index pointer for it
        wat = f"(global ${name} (mut i32) (i32.const {self.memory_index}))\n"
        wat += f"(data (i32.const {self.memory_index}) \"{elements}\")\n"
        self.memory_index += size * 4  # Assuming each i32 takes 4 bytes
        return wat

    def handle_list_decl(self, node):
        # Handling lists similarly to arrays for this example
        name = node['name']
        elements = ' '.join(f"(i32.const {elem})" for elem in node['elements'])
        
        wat = f"(global ${name} (mut i32) (i32.const {self.memory_index}))\n"
        wat += f"(data (i32.const {self.memory_index}) \"{elements}\")\n"
        self.memory_index += len(node['elements']) * 4
        return wat

    def handle_tuple_decl(self, node):
        # Tuples can be handled like lists/arrays
        name = node['name']
        elements = ' '.join(f"(i32.const {elem})" for elem in node['elements'])
        
        wat = f"(global ${name} (mut i32) (i32.const {self.memory_index}))\n"
        wat += f"(data (i32.const {self.memory_index}) \"{elements}\")\n"
        self.memory_index += len(node['elements']) * 4
        return wat

    def handle_dictionary_decl(self, node):
        # Dictionaries are more complex due to key-value pairs. This is a simple
        # version where we assume all keys are integers for simplification.
        name = node['name']
        wat = f"(global ${name} (mut i32) (i32.const {self.memory_index}))\n"
        for kv in node['keyValues']:
            key = kv['key']  # Assuming keys are integers
            value = kv['value']  # Assuming values are also integers
            wat += f"(data (i32.const {self.memory_index}) \"(i32.const {key}) (i32.const {value})\")\n"
            self.memory_index += 8  # Assuming 4 bytes each for key and value
        return wat

    # Assuming 'elements' and 'element' are utility functions to handle array/list contents
    def handle_elements(self, node):
        elements = ' '.join(f"(i32.const {elem})" for elem in node['elements'])
        return elements

    def handle_element(self, node):
        return f"(i32.const {node})\n"

    # Helper method to calculate address in memory
    def get_address(self, name):
        return f"${name}_addr"

    def handle_array_dim(self, node):
        # Assumes array length is stored at the start of the array
        array_name = node['array']
        return f"(i32.load {self.get_address(array_name)})\n"

    def handle_array_get_idx(self, node):
        array_name = node['array']
        index = node['index']
        # Calculate offset: Assuming 4 bytes per element and starting at 4 to skip length
        return f"(i32.load offset={4*index} {self.get_address(array_name)})\n"

    def handle_array_tail(self, node):
        array_name = node['array']
        # Get the address and skip the first element
        return f"(i32.load offset=4 {self.get_address(array_name)}) ; Tail of the array\n"

    def handle_array_head(self, node):
        array_name = node['array']
        # Get the address and load the first actual element (skip length)
        return f"(i32.load offset=4 {self.get_address(array_name)}) ; Head of the array\n"

    def handle_array_exchange(self, node):
        array_name = node['array']
        index = node['index']
        element = node['element']
        # Exchange operation
        return f"(i32.store offset={4*index} {self.get_address(array_name)} (i32.const {element}))\n"

    def handle_array_sort(self, node):
        array_name = node['array']
        order = node['order']
        # Sorting is complex and typically would require a custom sorting function
        return f"; Sorting the array {array_name} in {order} order not implemented\n"

    def handle_list_dim(self, node):
        list_name = node['list']
        # Assume list length is stored similarly to arrays
        return f"(i32.load {self.get_address(list_name)})\n"

    # More handlers as needed...

    # Handling block to encapsulate a sequence of instructions
    def handle_block(self, node):
        instructions = ""
        for statement in node['body']:
            instructions += self.generate_wat(statement)  # Recursively process each statement
        return instructions

    # Handling functions for input and print, though these require external calls in WebAssembly
    def handle_inputfunction(self, node):
        prompt = node.get('prompt', '')
        # WebAssembly does not support direct input; this would link to an external function
        return f"; External call to input function with prompt: {prompt}\n"

    def handle_printfunction(self, node):
        expression = node['expression']
        # Assume expression evaluation is handled elsewhere
        evaluated_expression = self.generate_wat(expression)
        return f"; External call to print function to output: {evaluated_expression}\n"

    def handle_unaryoperation(self, node):
        operator = node['operator']
        variable = node['variable']
        if operator == "++":
            return f"(i32.add (get_local ${variable}) (i32.const 1))\n"
        elif operator == "--":
            return f"(i32.sub (get_local ${variable}) (i32.const 1))\n"
        else:
            return f"; Unsupported unary operation {operator}\n"

def main():
    input_filename = 'output_ast.json'  
    output_filename = 'output.wat'  

    with open(input_filename, 'r') as file:
        ast = json.load(file)

    wat_generator = WATGenerator()
    try:
        print("entered try")
        wat_code = wat_generator.handle_program(ast)
        # print(wat_code)
        with open(output_filename, 'w') as file:
            file.write(wat_code)
        print(f"WAT code has been generated and saved to {output_filename}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
