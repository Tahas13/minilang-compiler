# MiniLang Compiler Project Report

**Course:** CS-4031 – Compiler Construction  
**Instructor:** Syed Zain Ul Hassan  
**Semester:** Fall 2025  
**Group Members:** Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)  
**Date:** December 2, 2025

## Executive Summary

This report presents the complete implementation of a compiler for MiniLang, a simple programming language designed to demonstrate fundamental compiler construction principles. The project successfully implements all three major phases of compilation: lexical analysis, syntax analysis, and semantic analysis. The compiler is capable of processing MiniLang source code, performing comprehensive error detection, and generating detailed diagnostic information.

## 1. Introduction

### 1.1 Project Objectives
The primary objective of this project was to design and implement a complete compiler for MiniLang that demonstrates:
- Lexical analysis techniques for tokenizing source code
- Syntax analysis using recursive descent parsing
- Semantic analysis for type checking and error detection
- Comprehensive error reporting and recovery mechanisms

### 1.2 Language Design Goals
MiniLang was designed to be:
- **Simple**: Easy to understand and implement
- **Complete**: Includes essential programming constructs
- **Educational**: Demonstrates key compiler concepts
- **Robust**: Provides comprehensive error detection

## 2. Language Specification

### 2.1 MiniLang Features
MiniLang supports the following language constructs:

**Data Types:**
- `int`: 32-bit integers
- `float`: Floating-point numbers
- `bool`: Boolean values (true/false)

**Operators:**
- Arithmetic: `+`, `-`, `*`, `/`
- Relational: `>`, `<`, `==`, `!=`
- Logical: `and`, `or`, `not`
- Assignment: `=`

**Control Structures:**
- Conditional statements: `if`/`else`
- Iteration: `while` loops
- Block statements with proper scoping

**I/O Operations:**
- Output: `print()` statements

**Additional Features:**
- Single-line comments (`//`)
- Proper operator precedence
- Type coercion (int to float)

### 2.2 Example Program
```minilang
int a = 10;
int b = 5;
bool flag = true;

if (a > b and flag) {
    print(a);
} else {
    print(b);
}

while (a > 0) {
    a = a - 1;
    print(a);
}
```

## 3. Compiler Architecture

### 3.1 Overall Design
The MiniLang compiler follows a traditional multi-pass architecture with three main phases:

```
Source Code → Scanner → Parser → Semantic Analyzer → Success/Error Report
```

### 3.2 Phase 1: Lexical Analysis (Scanner)

**Implementation:** `src/scanner.py`

**Key Features:**
- **Tokenization**: Converts source code into a stream of tokens
- **Keyword Recognition**: Distinguishes keywords from identifiers
- **Number Processing**: Handles both integer and floating-point literals
- **Error Detection**: Identifies invalid characters and malformed tokens
- **Comment Handling**: Skips single-line comments
- **Position Tracking**: Maintains line and column information for error reporting

**Token Categories:**
- Keywords: `int`, `float`, `bool`, `if`, `else`, `while`, `print`, etc.
- Operators: `+`, `-`, `*`, `/`, `>`, `<`, `==`, `!=`, `and`, `or`, `not`
- Delimiters: `;`, `(`, `)`, `{`, `}`
- Literals: Integer, float, and boolean constants
- Identifiers: Variable names

**Technical Implementation:**
- State-machine-based character processing
- Lookahead for two-character operators (`==`, `!=`)
- Comprehensive error recovery mechanisms
- Efficient string processing with position tracking

### 3.3 Phase 2: Syntax Analysis (Parser)

**Implementation:** `src/parser.py`

**Key Features:**
- **Recursive Descent Parsing**: Implements predictive parsing for MiniLang grammar
- **AST Generation**: Builds Abstract Syntax Tree for semantic analysis
- **Error Recovery**: Synchronization points for continued parsing after errors
- **Precedence Handling**: Proper operator precedence and associativity
- **Grammar Support**: Complete implementation of MiniLang grammar rules

**AST Node Types:**
- **Statements**: Variable declarations, assignments, print statements, if/while statements, blocks
- **Expressions**: Binary operations, unary operations, literals, identifiers
- **Structure**: Hierarchical tree representation of program structure

**Grammar Implementation:**
The parser implements a complete recursive descent parser for the MiniLang grammar with the following key productions:
- Expression parsing with proper precedence (logical OR → AND → equality → relational → additive → multiplicative → unary → primary)
- Statement parsing for all MiniLang constructs
- Error recovery at statement boundaries

### 3.4 Phase 3: Semantic Analysis

**Implementation:** `src/semantic_analyzer.py`

**Key Features:**
- **Symbol Table Management**: Hierarchical scoping with proper variable tracking
- **Type Checking**: Static type analysis for all expressions and statements
- **Error Detection**: Comprehensive semantic error identification
- **Scope Management**: Block-level scoping with variable shadowing support

**Type System:**
- **Static Typing**: All variables must be declared with explicit types
- **Type Compatibility**: Rules for arithmetic, logical, and relational operations
- **Implicit Conversions**: int to float conversion in mixed arithmetic
- **Type Safety**: Prevention of invalid type combinations

**Symbol Table Design:**
```
Symbol {
    name: string
    type: string  
    initialized: boolean
    line: integer
    column: integer
}
```

**Semantic Rules:**
1. **Variable Declaration**: Check for duplicate names in current scope
2. **Variable Reference**: Verify declaration and initialization
3. **Assignment**: Type compatibility checking
4. **Operations**: Type-specific operator validation
5. **Control Flow**: Boolean condition requirements

## 4. Implementation Details

### 4.1 Error Handling Strategy

**Lexical Errors:**
- Invalid characters with position information
- Malformed number literals
- Unterminated tokens

**Syntax Errors:**
- Missing delimiters (semicolons, parentheses, braces)
- Invalid statement structures
- Unexpected token sequences
- Recovery at statement boundaries

**Semantic Errors:**
- Undefined variable references
- Type mismatches in assignments and operations
- Variable redeclaration
- Use of uninitialized variables
- Invalid condition types in control structures

### 4.2 Key Algorithms

**Scanner Algorithm:**
```python
def get_next_token():
    skip_whitespace()
    if current_char is digit:
        return read_number()
    elif current_char is letter:
        return read_identifier_or_keyword()
    elif current_char is operator:
        return read_operator()
    else:
        raise lexical_error()
```

**Parser Algorithm:**
```python
def parse_expression():
    # Recursive descent with precedence climbing
    return parse_logical_or()

def parse_statement():
    if current_token is type_keyword:
        return parse_variable_declaration()
    elif current_token is identifier:
        return parse_assignment()
    # ... other statement types
```

**Type Checker Algorithm:**
```python
def check_binary_operation(left_type, operator, right_type):
    if operator in arithmetic_ops:
        return check_arithmetic_compatibility(left_type, right_type)
    elif operator in logical_ops:
        return check_boolean_operands(left_type, right_type)
    # ... other operator types
```

### 4.3 Testing Framework

**Test Categories:**
1. **Valid Programs**: Correct syntax and semantics
2. **Lexical Error Tests**: Invalid tokens and characters
3. **Syntax Error Tests**: Grammar violations
4. **Semantic Error Tests**: Type errors and scope violations

**Test Coverage:**
- All language constructs tested
- Edge cases and error conditions
- Complex nested structures
- Type system boundary cases

## 5. Results and Analysis

### 5.1 Compiler Performance

**Lexical Analysis:**
- Successfully tokenizes all valid MiniLang constructs
- Accurate error detection with precise position reporting
- Efficient processing of large source files

**Syntax Analysis:**
- Complete grammar coverage
- Robust error recovery
- Accurate AST generation for valid programs

**Semantic Analysis:**
- Comprehensive type checking
- Proper scope management
- Detailed error reporting

### 5.2 Test Results

The compiler was tested with multiple test cases:

**Passing Tests:**
- Basic variable operations
- Complex conditional logic
- Nested loop structures
- Mixed-type arithmetic
- Scope and block handling

**Error Detection Tests:**
- All categories of errors properly detected
- Accurate error messages with position information
- Graceful handling of multiple errors

### 5.3 Language Features Validation

✅ **Successfully Implemented:**
- Complete lexical analysis
- Full syntax parsing
- Comprehensive semantic analysis
- Robust error handling
- Detailed reporting

✅ **All Requirements Met:**
- Scanner tokenizes all language constructs
- Parser handles complete MiniLang grammar
- Semantic analyzer validates types and scope rules
- Error recovery allows continued processing

## 6. Challenges and Solutions

### 6.1 Technical Challenges

**Challenge 1: Operator Precedence**
- **Problem**: Implementing correct precedence in recursive descent parser
- **Solution**: Structured precedence levels with dedicated parsing methods

**Challenge 2: Error Recovery**
- **Problem**: Graceful handling of syntax errors
- **Solution**: Synchronization tokens and recovery points

**Challenge 3: Scope Management**
- **Problem**: Proper handling of nested scopes and variable shadowing
- **Solution**: Hierarchical symbol table with parent pointers

**Challenge 4: Type System Design**
- **Problem**: Balancing simplicity with completeness
- **Solution**: Clear rules with implicit conversions where sensible

### 6.2 Design Decisions

**Decision 1: Recursive Descent Parsing**
- **Rationale**: Clear, maintainable, and easy to extend
- **Alternative**: Table-driven parsing
- **Justification**: Better suited for educational purposes

**Decision 2: AST-Based Semantic Analysis**
- **Rationale**: Clean separation of concerns
- **Alternative**: Syntax-directed translation
- **Justification**: More flexible and extensible

**Decision 3: Static Type System**
- **Rationale**: Easier error detection and prevention
- **Alternative**: Dynamic typing
- **Justification**: Better for learning compiler concepts

## 7. Future Enhancements

### 7.1 Language Extensions
- **Functions**: User-defined functions with parameters
- **Arrays**: Basic array support with indexing
- **Strings**: String literals and operations
- **For Loops**: Additional iteration constructs

### 7.2 Compiler Improvements
- **Code Generation**: Intermediate code or assembly generation
- **Optimization**: Basic optimization passes
- **Better Error Messages**: More descriptive error reporting
- **IDE Integration**: Language server protocol support

### 7.3 Advanced Features
- **Type Inference**: Automatic type deduction
- **Generics**: Parameterized types
- **Modules**: Separate compilation units
- **Memory Management**: Automatic memory handling

## 8. Conclusion

The MiniLang compiler project successfully demonstrates the fundamental principles of compiler construction. The implementation covers all essential phases of compilation with robust error handling and comprehensive testing. The project achieves its educational objectives by providing a clear, well-documented example of compiler design and implementation.

### 8.1 Key Achievements
- ✅ Complete three-phase compiler implementation
- ✅ Comprehensive error detection and reporting
- ✅ Robust testing framework with extensive test coverage
- ✅ Clean, maintainable, and well-documented code
- ✅ Educational value for understanding compiler concepts

### 8.2 Learning Outcomes
Through this project, we gained practical experience in:
- Lexical analysis techniques and implementation
- Grammar design and parser construction
- Type system design and semantic analysis
- Error handling and recovery strategies
- Software engineering practices for compiler development

### 8.3 Project Success Metrics
- **Functionality**: All specified features implemented and working
- **Quality**: Comprehensive testing with high code quality
- **Documentation**: Complete documentation with examples
- **Educational Value**: Clear demonstration of compiler concepts

The MiniLang compiler serves as an excellent foundation for understanding compiler construction principles and provides a platform for future enhancements and learning opportunities.

---

**Acknowledgments**

We thank Instructor Syed Zain Ul Hassan for guidance and support throughout this project. This work was completed as part of the CS-4031 Compiler Construction course requirements.

**References**

1. Aho, A. V., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools*
2. Cooper, K. D., & Torczon, L. (2011). *Engineering a Compiler*
3. Appel, A. W. (2002). *Modern Compiler Implementation*
4. Course materials from CS-4031 Compiler Construction