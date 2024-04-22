import json 

class WATGenerator:
    def __init__(self):
        self.memory_index = 0  
        self.variables = []


    def handle_statements(self, node):
        wat = ""
        
        for stmt in node['body']:
            wat += self.generate_wat(stmt) + "\n"
        return wat

    def generate_wat(self, node):
        node_type = node['type']
        method_name = 'handle_' + node_type

        # Dynamic method lookup with error handling
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(node)
        elif hasattr(self, 'handle_' + node_type):
            # Directly calling specific handlers if not caught by dynamic lookup
            return getattr(self, 'handle_' + node_type)(node)
        else:
            # Unified error handling if no method exists for the node type
            raise ValueError(f"Unsupported node type: {node_type}")

    
    def handle_program(self, node):
        wat = '(module\n'
        for stmt in node['body']:
            wat += self.generate_wat(stmt)
        
        # Assuming you want to return the value of the last declared variable in the main function
        if self.variables:
            last_var = self.variables[-1]
            wat += f"""
            (func $main (export "main") (result i32)
            (global.get ${last_var})
            )
            """
            wat += ')\n'
            return wat



    def handle_variable_decl(self, node):
        # Example: handle integer variables as mutable globals in WAT
        wat = f"(global ${node['name']} (mut i32) (i32.const {node['value']}))\n"
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
        # Example: increment or decrement
        if operator == "++":
            return f"(i32.add (get_local ${variable}) (i32.const 1))\n"
        elif operator == "--":
            return f"(i32.sub (get_local ${variable}) (i32.const 1))\n"
        else:
            return f"; Unsupported unary operation {operator}\n"

    # Implement more methods as necessary

def main():
    input_filename = 'output_ast.json'  # JSON file containing the AST
    output_filename = 'output.wat'      # File to save the generated WAT code

    # Load the AST from JSON file
    with open(input_filename, 'r') as file:
        ast = json.load(file)

    # Create an instance of your WAT generator
    wat_generator = WATGenerator()
   

    try:

        wat_code = wat_generator.handle_program(ast)
        print(wat_code)
        with open(output_filename, 'w') as file:
            file.write(wat_code)
        print(f"WAT code has been generated and saved to {output_filename}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
