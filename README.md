# our-own-compiler-com-piler-t6

# Programming Language Specification

## Entry Point of Code
- Same as Python
- The program will automatically identify an `entry` block or `main` function as the starting point for execution.

## Comments
- **Single-line Comment**: `#`
- **Multi-line Comment**: 
  ```
  plaintext
  Multi-line
  Comment
  ```


## Variables
- **Syntax**: `variable_name <data_type> = literal`
- **Primitive Data Types**:
  - integer (`int`)
  - character (`char`)
  - floatpoint (`float`)
  - doublepoint (`double`)
  - textwave (`Strings`)
  - Flag (`T/F`)
  - Null (`null`)


## **Immutability**: Variables are immutable.
 - immute variable_name <data_type> = literal

## Array
- **Syntax**: `variable_name <data_type, size> = 
- **Predefined Functions**:
  - `.dim()`: Returns the dimension of the array.
  - `.exchange(index, element)`: Exchanges the element at the specified index.
  - `.getidx(value)`: Returns the index of the given value.
  - `.sort(asc/dsc)`: Sorts the array in ascending or descending order.
  - `variable_name[ : , jump]`: Slicing and jumping through elements.

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
      // Code for x > 10
  }
  ElseGiven (x == 5) {
      // Code for x == 5
  }
  Otherwise {
      // Default code
  }
  ```

## Loops
- **Syntax**: `iterate (data_type variable_name; through list1;){}`

## Function
- **Syntax**: 
  ```plaintext
  fn function_name(data_type argument){
      // Function body
      exitwith 0;
  }
  ```

## Exception Handling
- **Syntax**:
  ```plaintext
  strive(){
      // Try block
  }
  capture(){
      // Catch block
  }
  ```
