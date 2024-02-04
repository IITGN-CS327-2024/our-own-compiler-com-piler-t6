# CMinusMinus/C--(.cmm)

# Programming Language Specification
- Our language is Case Sensitive.
  
## Entry Point of Code

- The program execution starts from the first line of the script and proceeds sequentially. (same as Python)

## End Point of a statement `;`
- The endpoint of a statement can be determined using semicolon notation. If the last character on a line is a semicolon, that line/statement ends.
  
  ```
  myInteger (integer) = 20;
  ```

## Comments
- **Single-line Comment**: `#`
  
  ```
  #This is a simple comment and it will be ignored by the compiler
  ```
- **Multi-line Comment**: `"""  """`
  
  ```
  """
  This is a simple comment.
  It spans multiple lines, so you can write whatever you want here.
  The compiler will ignore this entire block until the next """ or EOF.
  """
  ```

## Pendown Function

- To print data to the console. It allows the display of text messages, variables, or the results of expressions directly in the console using the `pendown` function as follows:
  
example -
```plaintext
#print a simple greeting message:
pendown("Hello, World!");
```

## Penup Function for User Input

- In our programming language, capturing user input from the console is facilitated through the `penup` function. This function is analogous to input mechanisms in other languages, designed to pause program execution and wait for the user to enter data, which is then returned as a string for further processing. Here's how you can use `penup` to capture and utilize user input in your programs:
  
```plaintext
# Example: Capturing a user's name and printing a greeting message
userName (textwave) = penup("Please enter your name: ");
pendown("Hello, " + userName + "!");
```

## Variables and datatypes
- **Syntax**: `variable_name (data_type) = literal`
- **Primitive Data Types**:
  - integer (`integer`)
  - character (`character`)
  - floatpoint (`floating point`)
  - doublepoint (`double`)
  - textwave (`string`)
  - flag (`bool`)
    
### Rules to Declare a Variable 
 - A variable name can consist of Capital letters A-Z, lowercase letters a-z digits 0-9, and two special characters such as _ underscore and $ dollar sign.
 - The first character must not be a digit.
 - Blank spaces cannot be used in variable names.
 - Java keywords cannot be used as variable names.
 - Variable names are case-sensitive.
 - There is no limit on the length of a variable name but by convention, it should be between 4 to 15 chars.
 - Variable names always should exist on the left-hand side of assignment operators.

## Examples of Variable Declarations in Our Programming Language

  This document provides examples of how to declare variables using different primitive data types in our programming language.

- ## Integer

  An integer variable declaration example:


  ```plaintext
  myInteger (integer) = 10;
  ```
- ## Character

  A character variable declaration example:


  ```plaintext
  myCharacter (character) = 'A';
  ```
- ## Floatpoint

  A floatpoint variable declaration example:


  ```plaintext
  myFloat (floatpoint) = 3.14;
  ```
- ## Doublepoint

  A doublepoint variable declaration example:


  ```plaintext
  myDouble (doublepoint) = 3.1415926535;
  ```
- ## Textwave (Strings)

  A textwave (string) variable declaration example:


  ```plaintext
  myString (textwave) = "Hello, World!";
  pendown(myString[1:5]); #The output would be "ello"
  pendown(myString[-1]); #The output would be "!"
  pendown(myString[::-1]); #The output would be "!dlroW ,olleH"

  myString2 (textwave) = "How are you?";
  pendown(myString + " " + myString2); #The output would be "Hello World! How are you?"
  ```
- ## Flag (True/False)

  A flag (boolean) variable declaration example, using 'True' for true:


  ```plaintext
  myFlag (flag) = True;
  ```

  And using 'False' for false:

  ```plaintext
  anotherFlag (flag) = False;
  ```

# Arithmetic Operations

## Unary Operations

Unary operations involve a single operand. Here are the basic unary arithmetic operations:
- **unary plus operator (+):** Returns the value of its operand
- **unary minus operator (-):** Returns the negative of the value of its operand.
- **Increment (++):** Increases the value of a variable by one. This can be pre-increment or post-increment.
- **Decrement (--):** Decreases the value of a variable by one. This can be pre-decrement or post-decrement.

### Unary Operations Examples

```plaintext
a (integer) = 10;
c (integer) = -a; # c = -10 (Negation)
c++; # c = -9 (Increment)
c--; # c = -10 (Decrement)
```

## Binary Operations

Binary operations involve two operands. Here are the basic binary arithmetic operations:

- **Addition (+):** Adds two numbers.
- **Subtraction (-):** Subtracts the second number from the first.
- **Multiplication (*):** Multiplies two numbers.
- **Division (/):** Divides the first number by the second. Note the distinction between integer division and floating-point division.
- **Modulus (%):** Returns the remainder of the division of the first number by the second.
- **Exponentiation (^):** Raises the first number to the power of the second.

### Binary Operations Examples

```plaintext
# Assuming variable declarations are similar to the syntax: variable_name (data_type) = literal;

 a (integer) = 10;
 b (integer) = 5;

# Addition
 sum (integer) = a + b; # sum = 15

# Subtraction
 difference (integer) = a - b; # difference = 5

# Multiplication
 product (integer) = a * b; # product = 50

# Division
 quotient (floatpoint) = a / b; # quotient = 2.0

# Modulus
 remainder (integer) = a % b; # remainder = 0

# Exponentiation
 power (doublepoint) = a ^ 2; # power = 100.0

```

# Comparison and Assignment Operators

## Comparison Operators

Comparison operators are used to compare two values, returning a boolean result (True or False).

### List of Comparison Operators

- **Equal (==):** Checks if two values are equal.
- **Not Equal (!=):** Checks if two values are not equal.
- **Greater Than (>):** Checks if the left value is greater than the right value.
- **Less Than (<):** Checks if the left value is less than the right value.
- **Greater Than or Equal To (>=):** Checks if the left value is greater than or equal to the right value.
- **Less Than or Equal To (<=):** Checks if the left value is less than or equal to the right value.

### Comparison Operators Examples

```plaintext
 x (integer) = 10;
 y (integer) = 20;

# Equal
Given (x == y) {
    # Executes if x is equal to y
}

# Not Equal
Given (x != y) {
    # Executes if x is not equal to y
}

# Greater Than
Given (x > y) {
    # Executes if x is greater than y
}

# Less Than
Given (x < y) {
    # Executes if x is less than y
}

# Greater Than or Equal To
Given (x >= y) {
    # Executes if x is greater than or equal to y
}

# Less Than or Equal To
Given (x <= y) {
    # Executes if x is less than or equal to y
}

```

## Assignment Operators

Assignment operators are used to assign or update the value of a variable.

### List of Assignment Operators

- **Assignment (=):** Assigns a value to a variable.
- **Add and Assign (+=):** Adds the right operand to the left operand and assigns the result to the left operand.
- **Subtract and Assign (-=):** Subtracts the right operand from the left operand and assigns the result to the left operand.
- **Multiply and Assign (*=):** Multiplies the right operand with the left operand and assigns the result to the left operand.
- **Divide and Assign (/=):** Divides the left operand by the right operand and assigns the result to the left operand.
- **Modulus and Assign (%=):** Applies modulus operation between the two operands and assigns the result to the left operand.

### Assignment Operators Examples

```plaintext
 x (integer) = 10;

# Assignment
x = 5; # x is now 5

# Add and Assign
x += 3; # x is now 8

# Subtract and Assign
x -= 2; # x is now 6

# Multiply and Assign
x *= 2; # x is now 12

# Divide and Assign
x /= 4; # x is now 3

# Modulus and Assign
x %= 2; # x is now 1

```

## Logical Operators

Logical operators in our programming language allow for the combination of boolean expressions and the manipulation of boolean values. These operators are fundamental in constructing complex conditional statements and making decisions based on multiple conditions. The logical operators available are `and`, `or`, and `not`.

### `&&` Operator
The `&&` operator (same as `and` in Python) evaluates to True if both operands are True, and False otherwise.

```plaintext
# Example: Checking if two conditions are true
Given (x > 10 && y < 20) {
    pendown("Both conditions are true.");
}
```

### `$$` Operator
The `$$` operator (same as `or` in Python) evaluates to True if at least one of the operands is True.

```plaintext
# Example: Checking if at least one condition is true
Given (x > 10 $$ y < 5) {
    pendown("At least one condition is true.");
}
```

### `!` Operator
The `!` operator (same as `not` in python) inverts the boolean value of its operand.

```plaintext
# Example: Inverting a condition
Given (! x == 10) {
    pendown("x is not equal to 10.");
}
```

## **Immutability**: Variables are immutable.

- immute variable_name (data_type) = literal

## Array

- **Syntax**: `variable_name (data_type, size) = { }
- - **Predefined Functions**:
  - `.dim()`: Returns the dimension of the array.
  - `.exchange(index, element)`: Exchanges the element at the specified index.
  - `.getidx(value)`: Returns the index of the given value.
  - `.sort(asc/dsc)`: Sorts the array in ascending or descending order.
  - `.tail()`: return the tail of the array.
  - `.head()`: return the first element of the array.

## List

- **Syntax**: `[]`
- **Predefined Functions** (similar to Array with additional methods):
  - `.add(element)`: Adds an element to the list.
  - `.remove(index)`: Removes an element at the specified index; if no index is provided, removes the last element.

## Tuple

- **Syntax**: `()`
- **Predefined Functions** (similar to List without `.add()` and `.remove()` methods):
  - Tuples are immutable.

## Dictionary

- **Syntax**: `variable_name = { key : value }`

## Conditional Statements

- **Syntax**:
  ```plaintext
  Given (x > 10){
      # Code for x > 10
  }
  ElseGiven (x == 5) {
      # Code for x == 5
  }
  Otherwise {
      # Default code
  }
  ```

## Loops

The iterate construct in our programming language provides a powerful way to loop through collections like lists or ranges with specific initializations and steps. It serves a similar purpose to the for loop in many other languages but is tailored to the syntax and semantics of this language.

### Looping Through a List

To iterate over each element in a list/array, use the following syntax:

```plaintext
iterate (variable_name (int) = initialization; through list1;) {
    # Loop body where `variable_name` can be used
}
```

This loop initializes variable_name and iterates through each element in list1, allowing the loop body to execute with each element.

### Looping Through a Range

To loop through a numerical range, including the ability to specify a step (increment or decrement), use the syntax:

```plaintext
iterate (variable_name (int) = initialization; through range(start...end, step);) {
    # Loop body where `variable_name` is updated per the range and step
}
```

- start...end specifies the range of values to iterate through.
- step determines the increment/decrement for each iteration. A negative step value implies a decrement.

### Examples

Looping through a list of integers:

```plaintext
iterate (i (int) = 0; through myList;) {
    pendown(i);
}
```

Looping through a range with a positive step:

```plaintext
iterate (i (int) = 0; through range(0...10, 1);) {
    pendown(i);
}
```

Looping through a range with a negative step:

```plaintext
iterate (i (int) = 10; through range(10...0, -1);) {
    pendown(i);
}
```

## Function

- **Syntax**:
  ```plaintext
  fn function_name(data_type argument){
      # Function body
      exitwith 0;
  }
  ```

## Exception Handling

- **Syntax**:
  ```plaintext
  strive(){
      # Try block
  }
  capture(){
      # Catch block
  }
  ```
