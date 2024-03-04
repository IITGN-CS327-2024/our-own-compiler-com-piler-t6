# Parser.py Documentation

This document serves as the guide for the `parser.py` file within the our-own-compiler-com-piler-t6 project.

## Prerequisites

Before running `parser.py`, ensure the following components are present and correctly placed as per the structure outlined in our GitHub repository:

- `Lexer.py`: The lexer script required for tokenizing the input, which is present in Assignment 2 folder.
- `text_cases` folder: Contains the `.cmm` files to be parsed, located within the Assignment 2 folder.

## Features

The `parser.py` script is designed to perform the following operations:

- Retrieve tokens generated by the lexer.
- Display these tokens on the console.

## Command-Line Arguments Support

`parser.py` is equipped to handle command-line arguments for flexible file processing:

### Processing a Single File

To parse a single `.cmm` file, use the following command, replacing `path/to/your_file.cmm` with the actual path to your file
```sh
python parser.py --input_file path/to/your_file.cmm
```

### Processing Multiple Files in a Directory

To parse all `.cmm` files in a directory, use the following command, replacing `path/to/your_directory` with the path to your directory:

```sh
python parser.py --input_folder path/to/your_directory
```

## Note:
### We have worked on the feedback provided in Assignment 02 and have made the following changes:
- We have added the support for command-line arguments for flexible file processing in Lexer.py file.