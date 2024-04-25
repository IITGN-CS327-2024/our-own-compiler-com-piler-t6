# Arithmetic Expression Compiler

This project demonstrates a simple arithmetic expression compiler written in Python, converting arithmetic expressions into WebAssembly (WASM) format and executing them in JavaScript.

## Prerequisites

Ensure you have the following software installed on your system:

- Python 3.x
- Node.js
- `wat2wasm` (WebAssembly binary toolkit)

## Instructions

### 1. Generate AST (Abstract Syntax Tree)

Run the `main.py` file to generate the AST (Abstract Syntax Tree) from arithmetic expressions.

```
python main.py
```

### 2. Convert AST to WAT (WebAssembly Text Format)
```
python main_wat.py
```
### 3. Convert WAT to WASM (WebAssembly Binary Format):
```
python wat2wasm.py
```

### 4. Run the WebAssembly Module in JavaScript:
```
node arithmetic-test
```

### 5. run all testcase
```
sh test.sh
```
