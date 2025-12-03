# MiniLang Compiler

**Course:** CS-4031 – Compiler Construction  
**Instructor:** Syed Zain Ul Hassan  
**Semester:** Fall 2025  
**Group Members:** Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)

## 🌟 **NEW: Web Application Interface!**

We've created a professional web application using **Streamlit** that provides:
- 🎯 **Interactive Code Editor** with syntax highlighting
- 🔍 **Real-time Compilation** through all three phases
- 📊 **Visual AST Tree Display** with beautiful formatting
- 🌐 **Cloud Deployment Ready** for easy sharing and demonstration
- 📱 **Mobile Responsive** design that works on all devices

### 🚀 **Quick Start - Web App**

```bash
# Install dependencies
pip install -r requirements.txt

# Run web application
streamlit run streamlit_app.py

# Or use the deployment script
python run_webapp.py
```

**Access the app at:** `http://localhost:8501`

### 🌐 **Deploy to Cloud (FREE)**

Deploy your compiler web app to the cloud in minutes:

1. **Streamlit Cloud** (Recommended):
   - Push to GitHub
   - Connect at https://share.streamlit.io/
   - Deploy with one click!

2. **Heroku/Railway**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions

## Overview

MiniLang is a simple, structured, and beginner-friendly programming language designed to demonstrate the fundamental concepts of programming such as variables, conditionals, and loops. This project implements a complete compiler for MiniLang that performs lexical analysis, syntax parsing, and semantic validation.

## Language Features

MiniLang supports the following features:

### Data Types
- `int`: Integer values
- `float`: Floating-point values  
- `bool`: Boolean values (true/false)

### Operators
- **Arithmetic:** `+`, `-`, `*`, `/`
- **Relational:** `>`, `<`, `==`, `!=`
- **Logical:** `and`, `or`, `not`
- **Assignment:** `=`

### Control Flow
- `if`/`else` statements
- `while` loops
- Block statements with `{` `}`

### Input/Output
- `print()` statement for output

### Comments
- Single-line comments with `//`

## Example MiniLang Program

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

## Project Structure

```
cc_project/
├── src/                    # Source code
│   ├── token.py           # Token definitions
│   ├── scanner.py         # Lexical analyzer
│   ├── ast_nodes.py       # AST node definitions
│   ├── parser.py          # Syntax analyzer
│   ├── symbol_table.py    # Symbol table management
│   └── semantic_analyzer.py # Semantic analyzer
├── examples/              # Example MiniLang programs
│   ├── example1_basics.ml
│   ├── example2_conditionals.ml
│   ├── example3_loops.ml
│   ├── example4_complex.ml
│   ├── example5_types.ml
│   └── error_cases.ml
├── docs/                  # Documentation
├── tests/                 # Test files
├── compiler.py           # Main compiler driver
├── test_runner.py        # Test runner script
└── README.md             # This file
```

## Installation & Usage

### 🌐 **Web Application (Recommended)**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch web app:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open in browser:**
   - Automatically opens at `http://localhost:8501`
   - Interactive interface with real-time compilation
   - Multiple example programs included
   - Visual AST tree display

### 💻 **Command Line Interface**

### Prerequisites
- Python 3.7 or higher

### Running the Compiler

1. **Compile a MiniLang file:**
   ```bash
   python compiler.py examples/example1_basics.ml
   ```

2. **Compile with verbose output:**
   ```bash
   python compiler.py examples/example1_basics.ml -v
   ```

3. **Show help:**
   ```bash
   python compiler.py --help
   ```

### Running Tests

1. **Run all test cases:**
   ```bash
   python test_runner.py
   ```

2. **Run demo with the proposal example:**
   ```bash
   python test_runner.py --demo
   ```

## Compiler Architecture

The MiniLang compiler is implemented in three main phases:

### 1. Lexical Analysis (Scanner)
- **File:** `src/scanner.py`
- **Purpose:** Tokenizes MiniLang source code into tokens
- **Features:**
  - Recognizes keywords, identifiers, literals, operators, and delimiters
  - Handles single-line comments
  - Provides detailed error reporting with line/column information
  - Supports integer and floating-point number recognition

### 2. Syntax Analysis (Parser)
- **File:** `src/parser.py`
- **Purpose:** Parses tokens according to MiniLang grammar rules
- **Features:**
  - Recursive descent parser implementation
  - Generates Abstract Syntax Tree (AST)
  - Comprehensive error recovery
  - Supports all MiniLang language constructs

### 3. Semantic Analysis
- **File:** `src/semantic_analyzer.py`
- **Purpose:** Validates variable declarations, type consistency, and detects semantic errors
- **Features:**
  - Symbol table management with scope handling
  - Type checking for all operations
  - Detection of undeclared variables
  - Type compatibility validation
  - Proper error reporting

## Grammar Specification

```
program ::= statement_list
statement_list ::= statement*
statement ::= var_declaration | assignment | print_statement 
            | if_statement | while_statement | block

var_declaration ::= type IDENTIFIER ('=' expression)? ';'
assignment ::= IDENTIFIER '=' expression ';'
print_statement ::= 'print' '(' expression ')' ';'
if_statement ::= 'if' '(' expression ')' statement ('else' statement)?
while_statement ::= 'while' '(' expression ')' statement
block ::= '{' statement_list '}'

expression ::= logical_or
logical_or ::= logical_and ('or' logical_and)*
logical_and ::= equality ('and' equality)*
equality ::= relational (('==' | '!=') relational)*
relational ::= additive (('>' | '<') additive)*
additive ::= multiplicative (('+' | '-') multiplicative)*
multiplicative ::= unary (('*' | '/') unary)*
unary ::= ('not' | '-') unary | primary
primary ::= IDENTIFIER | INTEGER_LITERAL | FLOAT_LITERAL 
          | BOOLEAN_LITERAL | '(' expression ')'

type ::= 'int' | 'float' | 'bool'
```

## Type System

MiniLang implements a static type system with the following rules:

### Type Compatibility
- **Assignment:** Target type must be compatible with source type
- **Arithmetic operations:** 
  - `int` + `int` → `int`
  - `int` + `float` → `float`
  - `float` + `float` → `float`
- **Logical operations:** Both operands must be `bool`
- **Relational operations:** Operands must be numeric; result is `bool`

### Implicit Conversions
- `int` can be implicitly converted to `float`
- No other implicit conversions are allowed

## Error Handling

The compiler provides comprehensive error detection and reporting:

### Lexical Errors
- Invalid characters
- Malformed numbers
- Unterminated tokens

### Syntax Errors
- Missing semicolons
- Unmatched parentheses/braces
- Invalid statement structures

### Semantic Errors
- Undeclared variables
- Type mismatches
- Variable redeclaration
- Use of uninitialized variables
- Invalid operand types

## Example Test Cases

### Valid Programs
- **Basic operations:** Variable declarations, arithmetic, print statements
- **Conditionals:** If-else statements with boolean expressions
- **Loops:** While loops with proper conditions
- **Complex expressions:** Nested operations and logical combinations

### Error Cases
- Type mismatches in assignments
- Undeclared variable usage
- Invalid operator usage
- Non-boolean conditions in control structures

## Future Enhancements

Potential improvements for the MiniLang compiler:
- Add function declarations and calls
- Implement arrays and string support
- Add more data types (char, string)
- Include for-loops and switch statements
- Generate executable code or intermediate representation
- Add optimization passes

## Contributing

This project is part of an academic assignment for CS-4031. For questions or issues, please contact:
- Shozab Mehdi: [22k-4522]
- Taha Sharif: [22k-4145]

## License

This project is created for educational purposes as part of the Compiler Construction course.