# MiniLang Compiler - Viva Preparation Guide

**Course:** CS-4031 – Compiler Construction  
**Instructor:** Syed Zain Ul Hassan  
**Semester:** Fall 2025  
**Group Members:** Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)

---

## 📋 Table of Contents
1. [Project Proposal](#1-project-proposal)
2. [Grammar Explanation](#2-grammar-explanation)
3. [Grammar Specification](#3-grammar-specification)
4. [Semantic Rules](#4-semantic-rules)
5. [Code Overview](#5-code-overview)
6. [Sample Programs](#6-sample-programs)
7. [Program Variations & Testing](#7-program-variations--testing)

---

## 1. Project Proposal

### 1.1 Project Title
**MiniLang: A Complete Educational Compiler Implementation**

### 1.2 Project Objectives
The primary goal is to design and implement a complete three-phase compiler for MiniLang, demonstrating:

1. **Lexical Analysis (Scanning)**
   - Tokenization of source code
   - Keyword and identifier recognition
   - Error detection and reporting

2. **Syntax Analysis (Parsing)**
   - Recursive descent parsing
   - Abstract Syntax Tree (AST) generation
   - Grammar validation

3. **Semantic Analysis**
   - Type checking and validation
   - Symbol table management
   - Scope handling

### 1.3 Language Design Motivation
MiniLang was designed to:
- Demonstrate fundamental compiler construction principles
- Provide clear examples of lexical, syntax, and semantic analysis
- Support essential programming constructs (variables, control flow, expressions)
- Maintain simplicity while being feature-complete for educational purposes

### 1.4 Target Features
- **Data Types:** int, float, bool
- **Operators:** Arithmetic (+, -, *, /), Relational (>, <, ==, !=), Logical (and, or, not)
- **Control Flow:** if/else, while loops, for loops, do-while loops
- **Functions:** User-defined functions with parameters and return values
- **Scoping:** Block-level scoping with proper variable shadowing
- **I/O:** print() statements for output

### 1.5 Implementation Strategy
- **Language:** Python 3.x for rapid development and clarity
- **Architecture:** Multi-pass compiler with distinct phases
- **Error Handling:** Comprehensive error detection and recovery
- **Testing:** Extensive test suite with valid and invalid programs
- **Interface:** Web-based interface using Streamlit for interactive compilation

### 1.6 Deliverables
- ✅ Complete compiler implementation (Scanner, Parser, Semantic Analyzer)
- ✅ Comprehensive documentation (Grammar, Semantic Rules, Reports)
- ✅ Test suite with 15+ example programs
- ✅ Web interface for interactive compilation
- ✅ GitHub repository with version control

---

## 2. Grammar Explanation

### 2.1 Grammar Design Philosophy

**Top-Down Approach:**
Our grammar follows a hierarchical structure starting from a Program and breaking down into smaller components:
- **Program** → Collection of statements
- **Statements** → Individual instructions (declarations, assignments, control flow)
- **Expressions** → Values and computations with proper precedence

**Key Design Principles:**

1. **Operator Precedence (Lowest to Highest):**
   - Logical OR (`or`)
   - Logical AND (`and`)
   - Equality (`==`, `!=`)
   - Relational (`>`, `<`, `>=`, `<=`)
   - Additive (`+`, `-`)
   - Multiplicative (`*`, `/`)
   - Unary (`not`, `-`)
   - Primary (literals, identifiers, parentheses)

2. **Left-Associativity:**
   All binary operators are left-associative: `a + b + c = (a + b) + c`

3. **Unambiguous Grammar:**
   No ambiguity in parsing - each construct has exactly one derivation

### 2.2 Grammar Categories

**1. Program Structure:**
```
Program → StatementList
StatementList → Statement StatementList | ε
```
A program is a sequence of zero or more statements.

**2. Statement Types:**
- **VarDecl:** Variable declarations with optional initialization
- **Assignment:** Assigning values to existing variables
- **PrintStmt:** Output statements
- **IfStmt:** Conditional branching
- **WhileStmt:** While loops
- **ForStmt:** For loops with init, condition, and update
- **DoWhileStmt:** Do-while loops (execute at least once)
- **FunctionDecl:** Function definitions
- **ReturnStmt:** Function return statements
- **Block:** Grouped statements with `{}`

**3. Expression Hierarchy:**
The expression grammar implements operator precedence through nested productions:
```
Expression → LogicalOr
LogicalOr → LogicalAnd ('or' LogicalAnd)*
LogicalAnd → Equality ('and' Equality)*
Equality → Relational (('==' | '!=') Relational)*
Relational → Additive (('>' | '<' | '>=' | '<=') Additive)*
Additive → Multiplicative (('+' | '-') Multiplicative)*
Multiplicative → Unary (('*' | '/') Unary)*
Unary → ('not' | '-') Unary | Primary
Primary → IDENTIFIER | Literal | '(' Expression ')' | FunctionCall
```

### 2.3 Why This Grammar?

**Advantages:**
- ✅ **Predictive Parsing:** Can be parsed with 1-token lookahead
- ✅ **No Left Recursion:** Suitable for recursive descent parsing
- ✅ **Clear Precedence:** Natural operator precedence without conflicts
- ✅ **Extensible:** Easy to add new constructs
- ✅ **Readable:** Matches programmer intuition

**Grammar Properties:**
- **LL(1) Compatible:** Can be parsed top-down with one lookahead
- **Deterministic:** Each production has distinct first sets
- **Complete:** Covers all MiniLang language features

---

## 3. Grammar Specification

### 3.1 Complete Context-Free Grammar

```
1.  Program          → StatementList
2.  StatementList    → Statement StatementList | ε
3.  Statement        → VarDecl | Assignment | PrintStmt | IfStmt 
                      | WhileStmt | ForStmt | DoWhileStmt 
                      | FunctionDecl | ReturnStmt | Block | FunctionCallStmt
4.  VarDecl          → Type IDENTIFIER ('=' Expression)? ';'
5.  Assignment       → IDENTIFIER '=' Expression ';'
6.  PrintStmt        → 'print' '(' Expression ')' ';'
7.  IfStmt           → 'if' '(' Expression ')' Statement ('else' Statement)?
8.  WhileStmt        → 'while' '(' Expression ')' Statement
9.  ForStmt          → 'for' '(' (VarDecl | Assignment)? ';' Expression? ';' Assignment? ')' Statement
10. DoWhileStmt      → 'do' Statement 'while' '(' Expression ')' ';'
11. FunctionDecl     → 'function' Type IDENTIFIER '(' ParamList? ')' Block
12. ParamList        → Type IDENTIFIER (',' Type IDENTIFIER)*
13. ReturnStmt       → 'return' Expression? ';'
14. FunctionCallStmt → IDENTIFIER '(' ArgList? ')' ';'
15. Block            → '{' StatementList '}'

16. Expression       → LogicalOr
17. LogicalOr        → LogicalAnd ('or' LogicalAnd)*
18. LogicalAnd       → Equality ('and' Equality)*
19. Equality         → Relational (('==' | '!=') Relational)*
20. Relational       → Additive (('>' | '<' | '>=' | '<=') Additive)*
21. Additive         → Multiplicative (('+' | '-') Multiplicative)*
22. Multiplicative   → Unary (('*' | '/') Unary)*
23. Unary            → ('not' | '-') Unary | Primary
24. Primary          → IDENTIFIER | INTEGER | FLOAT | BOOLEAN 
                      | '(' Expression ')' | FunctionCall
25. FunctionCall     → IDENTIFIER '(' ArgList? ')'
26. ArgList          → Expression (',' Expression)*

27. Type             → 'int' | 'float' | 'bool'
```

### 3.2 Terminal Symbols

**Keywords:**
```
int, float, bool, true, false, if, else, while, for, do, 
function, return, print, and, or, not
```

**Operators:**
```
Arithmetic:  +  -  *  /
Relational:  >  <  >=  <=  ==  !=
Logical:     and  or  not
Assignment:  =
```

**Delimiters:**
```
;  ,  (  )  {  }
```

**Literals:**
```
INTEGER_LITERAL:  [0-9]+
FLOAT_LITERAL:    [0-9]+\.[0-9]+
BOOLEAN_LITERAL:  true | false
IDENTIFIER:       [a-zA-Z_][a-zA-Z0-9_]*
```

### 3.3 Non-Terminal Symbols
```
Program, StatementList, Statement, VarDecl, Assignment, PrintStmt,
IfStmt, WhileStmt, ForStmt, DoWhileStmt, FunctionDecl, ParamList,
ReturnStmt, FunctionCallStmt, Block, Expression, LogicalOr, 
LogicalAnd, Equality, Relational, Additive, Multiplicative, 
Unary, Primary, FunctionCall, ArgList, Type
```

### 3.4 Operator Precedence & Associativity

| Level | Operators | Associativity | Description |
|-------|-----------|---------------|-------------|
| 1 (Lowest) | `or` | Left | Logical OR |
| 2 | `and` | Left | Logical AND |
| 3 | `==`, `!=` | Left | Equality |
| 4 | `>`, `<`, `>=`, `<=` | Left | Relational |
| 5 | `+`, `-` | Left | Additive |
| 6 | `*`, `/` | Left | Multiplicative |
| 7 | `not`, `-` (unary) | Right | Unary |
| 8 (Highest) | `()`, literals | - | Primary |

---

## 4. Semantic Rules

### 4.1 Type System Rules

#### Rule 1: Variable Declaration
```
VarDecl → Type IDENTIFIER ('=' Expression)? ';'

Semantic Actions:
1. Check if IDENTIFIER already exists in current scope
   - If exists → Error: "Variable 'x' already declared"
2. If initialization expression exists:
   - Get type of Expression
   - Check if Expression.type can be assigned to declared Type
   - If incompatible → Error: "Cannot assign X to Y"
3. Add symbol to symbol table:
   - Name: IDENTIFIER.lexeme
   - Type: declared Type
   - Initialized: true if '=' present, false otherwise
```

**Example:**
```minilang
int x = 10;        // ✓ Valid: x is int, 10 is int
float y = 5;       // ✓ Valid: int→float conversion allowed
bool z = 3 + 5;    // ✗ Error: Cannot assign int to bool
int x = 20;        // ✗ Error: Variable 'x' already declared
```

#### Rule 2: Assignment Statement
```
Assignment → IDENTIFIER '=' Expression ';'

Semantic Actions:
1. Lookup IDENTIFIER in symbol table
   - If not found → Error: "Undefined variable 'x'"
2. Get type of Expression
3. Check if Expression.type can be assigned to variable type
   - If incompatible → Error: "Type mismatch"
4. Mark variable as initialized
```

**Example:**
```minilang
int a = 5;
a = 10;            // ✓ Valid: int = int
a = 3.14;          // ✗ Error: Cannot assign float to int
b = 20;            // ✗ Error: Undefined variable 'b'
```

#### Rule 3: Arithmetic Operations
```
BinaryOp → Expression ('+' | '-' | '*' | '/') Expression

Semantic Actions:
1. Get left_type = type of left Expression
2. Get right_type = type of right Expression
3. Check compatibility:
   - int OP int → result: int
   - int OP float → result: float
   - float OP int → result: float
   - float OP float → result: float
   - bool OP any → Error
```

**Type Compatibility Matrix:**

| Left | Operator | Right | Result | Valid? |
|------|----------|-------|--------|--------|
| int | +, -, *, / | int | int | ✓ |
| int | +, -, *, / | float | float | ✓ |
| float | +, -, *, / | int | float | ✓ |
| float | +, -, *, / | float | float | ✓ |
| bool | +, -, *, / | any | - | ✗ |

**Example:**
```minilang
int a = 5 + 3;         // ✓ Result: int
float b = 5 + 3.14;    // ✓ Result: float (5 promoted to 5.0)
float c = 2.5 * 4;     // ✓ Result: float
bool d = true + 1;     // ✗ Error: Invalid operands
```

#### Rule 4: Relational Operations
```
BinaryOp → Expression ('>' | '<' | '>=' | '<=') Expression

Semantic Actions:
1. Get left_type and right_type
2. Check both are numeric (int or float)
   - If not → Error: "Relational operators require numeric operands"
3. Result type = bool
```

**Example:**
```minilang
bool result1 = 5 > 3;           // ✓ Result: bool (true)
bool result2 = 3.14 < 5;        // ✓ Result: bool (true)
bool result3 = true > false;    // ✗ Error: bool not numeric
```

#### Rule 5: Equality Operations
```
BinaryOp → Expression ('==' | '!=') Expression

Semantic Actions:
1. Get left_type and right_type
2. Check types are comparable:
   - int == int → valid
   - float == float → valid
   - bool == bool → valid
   - int == float → valid (with implicit conversion)
   - Different base types → Error
3. Result type = bool
```

**Example:**
```minilang
bool eq1 = (5 == 5);           // ✓ true
bool eq2 = (3.14 == 3);        // ✓ false (3 promoted to 3.0)
bool eq3 = (true == false);    // ✓ false
bool eq4 = (5 == true);        // ✗ Error: Cannot compare int with bool
```

#### Rule 6: Logical Operations
```
BinaryOp → Expression ('and' | 'or') Expression

Semantic Actions:
1. Check left_type == bool
   - If not → Error: "Left operand must be boolean"
2. Check right_type == bool
   - If not → Error: "Right operand must be boolean"
3. Result type = bool
```

**Example:**
```minilang
bool result1 = true and false;     // ✓ Result: false
bool result2 = (5 > 3) or false;   // ✓ Result: true
bool result3 = 5 and 3;            // ✗ Error: Operands must be bool
```

#### Rule 7: Unary Operations
```
UnaryOp → ('not' | '-') Expression

Semantic Actions:
For 'not':
  - Check Expression.type == bool
  - Result type = bool

For '-' (negation):
  - Check Expression.type in {int, float}
  - Result type = Expression.type
```

**Example:**
```minilang
bool b = not true;         // ✓ Result: false
int neg = -5;              // ✓ Result: -5
float negf = -3.14;        // ✓ Result: -3.14
bool wrong = not 5;        // ✗ Error: 'not' requires bool
```

### 4.2 Control Flow Rules

#### Rule 8: If Statement
```
IfStmt → 'if' '(' Expression ')' Statement ('else' Statement)?

Semantic Actions:
1. Check Expression.type == bool
   - If not → Error: "If condition must be boolean"
2. Process then-statement in new scope
3. If else-clause exists, process else-statement in new scope
```

**Example:**
```minilang
if (5 > 3) {           // ✓ Valid: condition is bool
    print(1);
}

if (5) {               // ✗ Error: condition must be bool
    print(1);
}
```

#### Rule 9: While Loop
```
WhileStmt → 'while' '(' Expression ')' Statement

Semantic Actions:
1. Check Expression.type == bool
   - If not → Error: "While condition must be boolean"
2. Process body in new scope (allows redeclaration in loop body)
```

**Example:**
```minilang
while (x > 0) {        // ✓ Valid: condition is bool
    x = x - 1;
}

while (x) {            // ✗ Error: condition must be bool
    x = x - 1;
}
```

#### Rule 10: For Loop
```
ForStmt → 'for' '(' Init? ';' Condition? ';' Update? ')' Statement

Semantic Actions:
1. Create new scope for entire loop
2. Process Init (variable declaration or assignment)
3. If Condition exists:
   - Check Condition.type == bool
4. Process Update (assignment)
5. Process body statements
6. Exit scope (loop variables discarded)
```

**Example:**
```minilang
for (int i = 0; i < 10; i = i + 1) {    // ✓ Valid
    print(i);
}

for (int i = 0; i; i = i + 1) {         // ✗ Error: condition not bool
    print(i);
}
```

#### Rule 11: Do-While Loop
```
DoWhileStmt → 'do' Statement 'while' '(' Expression ')' ';'

Semantic Actions:
1. Process body statement first (executes at least once)
2. Check Expression.type == bool
   - If not → Error: "Do-while condition must be boolean"
```

**Example:**
```minilang
do {
    print(x);
    x = x - 1;
} while (x > 0);       // ✓ Valid

do {
    print(x);
} while (x);           // ✗ Error: condition must be bool
```

### 4.3 Function Rules

#### Rule 12: Function Declaration
```
FunctionDecl → 'function' Type IDENTIFIER '(' ParamList? ')' Block

Semantic Actions:
1. Check if function name already exists in current scope
   - If exists → Error: "Function already declared"
2. Add function to symbol table:
   - Name: IDENTIFIER
   - Type: return type
   - IsFunction: true
   - ParamTypes: list of parameter types
3. Create new scope for function body
4. Add each parameter to function scope
5. Process function body statements
6. Exit function scope
```

**Example:**
```minilang
function int add(int a, int b) {
    return a + b;
}

function int add(float x) {    // ✗ Error: Function 'add' already declared
    return x;
}
```

#### Rule 13: Function Call
```
FunctionCall → IDENTIFIER '(' ArgList? ')'

Semantic Actions:
1. Lookup function in symbol table
   - If not found → Error: "Undefined function"
2. Check it's actually a function
   - If not → Error: "'x' is not a function"
3. Check argument count matches parameter count
   - If not → Error: "Expected N arguments, got M"
4. Check each argument type matches parameter type
   - If not compatible → Error: "Argument type mismatch"
5. Result type = function's return type
```

**Example:**
```minilang
function int add(int a, int b) {
    return a + b;
}

int result = add(5, 3);         // ✓ Valid
int wrong1 = add(5);            // ✗ Error: Expected 2 arguments, got 1
float wrong2 = add(5, true);    // ✗ Error: Argument 2 type mismatch
```

#### Rule 14: Return Statement
```
ReturnStmt → 'return' Expression? ';'

Semantic Actions:
1. Must be inside a function
   - If not → Error: "Return outside function"
2. If Expression exists:
   - Check Expression.type matches function return type
   - If not → Error: "Return type mismatch"
3. If no Expression (empty return):
   - Function return type should be void (if supported)
```

**Example:**
```minilang
function int getValue() {
    return 42;              // ✓ Valid: int matches return type
}

function bool getFlag() {
    return 5;               // ✗ Error: Cannot return int from bool function
}
```

### 4.4 Scope Rules

#### Rule 15: Block Scope
```
Block → '{' StatementList '}'

Semantic Actions:
1. Create new child scope (child of current scope)
2. Set current_scope = new_scope
3. Process all statements in StatementList
4. Restore current_scope = parent scope
5. All variables declared in block are discarded
```

**Variable Shadowing:**
```minilang
int x = 10;           // Outer scope x
{
    int x = 20;       // ✓ Valid: Inner scope x (shadows outer)
    print(x);         // Prints 20
}
print(x);             // Prints 10 (outer x)
```

#### Rule 16: Variable Lookup
```
When accessing a variable:
1. Search current scope first
2. If not found, search parent scope
3. Continue up the scope chain
4. If not found in any scope → Error: "Undefined variable"
```

**Example:**
```minilang
int global = 1;
{
    int local = 2;
    print(global);    // ✓ Found in parent scope
    print(local);     // ✓ Found in current scope
}
print(local);         // ✗ Error: 'local' not in scope
```

### 4.5 Initialization Rules

#### Rule 17: Use Before Initialization
```
When referencing a variable:
1. Check if variable is declared
2. Check if variable has been initialized
   - If not initialized → Error: "Variable used before initialization"
```

**Example:**
```minilang
int x;
print(x);             // ✗ Error: 'x' used before initialization

int y = 5;
print(y);             // ✓ Valid: 'y' is initialized

int z;
z = 10;
print(z);             // ✓ Valid: 'z' initialized by assignment
```

---

## 5. Code Overview

### 5.1 Architecture Overview

```
┌─────────────────┐
│  Source Code    │
│   (.ml file)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Scanner      │  Phase 1: Lexical Analysis
│  (scanner.py)   │  • Tokenization
└────────┬────────┘  • Keyword recognition
         │           • Error detection
         ▼
┌─────────────────┐
│  Token Stream   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Parser       │  Phase 2: Syntax Analysis
│  (parser.py)    │  • Grammar validation
└────────┬────────┘  • AST construction
         │           • Syntax error detection
         ▼
┌─────────────────┐
│   AST Nodes     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Semantic     │  Phase 3: Semantic Analysis
│   Analyzer      │  • Type checking
│(semantic_       │  • Scope management
│ analyzer.py)    │  • Symbol table
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Success/Errors  │
└─────────────────┘
```

### 5.2 File Structure

```
cc_project/
├── src/
│   ├── tokens.py              # Token type definitions
│   ├── scanner.py             # Lexical analyzer (Phase 1)
│   ├── ast_nodes.py           # AST node classes
│   ├── parser.py              # Syntax analyzer (Phase 2)
│   ├── symbol_table.py        # Symbol table implementation
│   ├── semantic_analyzer.py   # Type checker (Phase 3)
│   └── compiler.py            # Main compiler driver
│
├── cpp_core/                  # C++ implementation (bonus)
│   ├── token.h
│   ├── scanner.h
│   ├── ast.h
│   ├── parser.h
│   └── semantic.h
│
├── examples/                  # Sample programs
│   ├── for_loop_example.ml
│   ├── function_example.ml
│   ├── all_features.ml
│   └── ... (15+ examples)
│
├── docs/                      # Documentation
│   ├── grammar_specification.md
│   └── project_report.md
│
├── streamlit_app.py           # Web interface
├── requirements.txt
└── README.md
```

### 5.3 Key Components

#### 5.3.1 Scanner (Lexical Analyzer)
**File:** `src/scanner.py`

**Purpose:** Convert source code into tokens

**Key Methods:**
```python
class Scanner:
    def tokenize(self) -> List[Token]:
        # Main tokenization loop
        
    def skip_whitespace(self):
        # Skip spaces, tabs, newlines
        
    def skip_comment(self):
        # Handle // comments
        
    def read_number(self) -> Token:
        # Handle integers and floats
        
    def read_identifier(self) -> Token:
        # Handle identifiers and keywords
```

**Key Features:**
- Position tracking (line, column) for error reporting
- Keyword recognition vs identifiers
- Multi-character operator handling (`==`, `!=`, `>=`, `<=`)
- Comprehensive error messages

#### 5.3.2 Parser (Syntax Analyzer)
**File:** `src/parser.py`

**Purpose:** Validate grammar and build AST

**Key Methods:**
```python
class Parser:
    def parse(self) -> Program:
        # Entry point - returns root AST node
        
    def parse_statement(self) -> Statement:
        # Dispatch to appropriate statement parser
        
    def parse_expression(self) -> Expression:
        # Parse expressions with precedence
        
    def parse_for_statement(self) -> ForStatement:
        # Parse for loops
        
    def parse_function_declaration(self) -> FunctionDeclaration:
        # Parse function definitions
```

**Parsing Strategy:**
- **Recursive Descent:** Each grammar rule = one method
- **Operator Precedence:** Handled by method nesting depth
- **Error Recovery:** Synchronization at statement boundaries

#### 5.3.3 AST Nodes
**File:** `src/ast_nodes.py`

**Purpose:** Represent program structure

**Node Categories:**
```python
# Base classes
class ASTNode: pass
class Statement(ASTNode): pass
class Expression(ASTNode): pass

# Statement nodes
@dataclass
class VarDeclaration(Statement):
    var_type: str
    name: str
    value: Optional[Expression]

@dataclass
class Assignment(Statement):
    name: str
    value: Expression

@dataclass
class ForStatement(Statement):
    init: Optional[Statement]
    condition: Optional[Expression]
    update: Optional[Statement]
    body: List[Statement]

@dataclass
class FunctionDeclaration(Statement):
    return_type: str
    name: str
    parameters: List[tuple]  # [(type, name), ...]
    body: List[Statement]

# Expression nodes
@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class FunctionCall(Expression):
    name: str
    arguments: List[Expression]
```

#### 5.3.4 Symbol Table
**File:** `src/symbol_table.py`

**Purpose:** Track variables and their types

**Structure:**
```python
@dataclass
class Symbol:
    name: str
    type: str
    initialized: bool
    is_function: bool = False
    param_types: Optional[list] = None

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.parent: Optional[SymbolTable] = None
    
    def define(self, name, symbol_type, ...):
        # Add new symbol
    
    def lookup(self, name) -> Optional[Symbol]:
        # Search this scope and parents
    
    def create_child_scope(self) -> SymbolTable:
        # For nested blocks/functions
```

**Features:**
- Hierarchical scoping with parent pointers
- Variable shadowing support
- Function symbol tracking with parameter types

#### 5.3.5 Semantic Analyzer
**File:** `src/semantic_analyzer.py`

**Purpose:** Type checking and validation

**Key Methods:**
```python
class TypeChecker(ASTVisitor):
    def visit_var_declaration(self, node):
        # Check redeclaration, type compatibility
        
    def visit_assignment(self, node):
        # Check variable exists, type matches
        
    def visit_for_statement(self, node):
        # Create scope, check condition is bool
        
    def visit_function_declaration(self, node):
        # Add to symbol table, check body
        
    def visit_function_call(self, node):
        # Verify arguments match parameters
        
    def get_expression_type(self, expr) -> str:
        # Return type of any expression
```

**Visitor Pattern:**
- Each AST node type has a `visit_*` method
- Recursive traversal of AST tree
- Maintains current scope during traversal

### 5.4 Compilation Flow

**Step-by-Step Process:**

```python
# 1. Read source code
source_code = read_file("program.ml")

# 2. Lexical Analysis
scanner = Scanner(source_code)
tokens = scanner.tokenize()
if scanner.errors:
    report_errors(scanner.errors)
    exit()

# 3. Syntax Analysis
parser = Parser(tokens)
ast = parser.parse()
if parser.errors:
    report_errors(parser.errors)
    exit()

# 4. Semantic Analysis
analyzer = TypeChecker()
success = analyzer.analyze(ast)
if not success:
    report_errors(analyzer.errors)
    exit()

# 5. Success!
print("Compilation successful!")
```

### 5.5 Web Interface
**File:** `streamlit_app.py`

**Features:**
- Interactive code editor with syntax highlighting
- Real-time compilation through all three phases
- Visual AST tree display
- Error highlighting
- Pre-loaded examples (15+ programs)
- Phase-by-phase results display

**Usage:**
```bash
streamlit run streamlit_app.py
```

---

## 6. Sample Programs

### 6.1 Basic Variables and Arithmetic

**File:** `examples/example1_basics.ml`

```minilang
// Basic variable declarations and arithmetic
int a = 10;
int b = 20;
int sum = a + b;
int diff = b - a;
int prod = a * b;

float x = 3.14;
float y = 2.5;
float result = x * y;

print(sum);
print(result);
```

**What it demonstrates:**
- Variable declarations with initialization
- Integer and float types
- Arithmetic operations
- Print statements

### 6.2 Conditional Statements

**File:** `examples/example2_conditionals.ml`

```minilang
// If-else statements
int age = 20;
bool isStudent = true;

if (age >= 18 and isStudent) {
    print(1);  // Eligible for student discount
} else {
    print(0);
}

// Nested conditions
int score = 85;

if (score >= 90) {
    print(90);  // Grade A
} else {
    if (score >= 80) {
        print(80);  // Grade B
    } else {
        print(70);  // Grade C or below
    }
}
```

**What it demonstrates:**
- Boolean variables
- Relational operators (`>=`)
- Logical operators (`and`)
- If-else statements
- Nested conditionals

### 6.3 While Loops

**File:** `examples/example3_loops.ml`

```minilang
// While loop example
int counter = 1;
int sum = 0;

while (counter <= 5) {
    sum = sum + counter;
    print(sum);
    counter = counter + 1;
}

print(sum);  // Final sum: 15
```

**What it demonstrates:**
- While loop syntax
- Loop control with condition
- Variable updates inside loop
- Accumulator pattern

### 6.4 For Loops

**File:** `examples/for_loop_example.ml`

```minilang
// For loop example
for (int i = 0; i < 5; i = i + 1) {
    print(i);
}

// For loop with accumulator
int total = 0;
for (int j = 1; j <= 10; j = j + 1) {
    total = total + j;
}
print(total);  // Prints 55
```

**What it demonstrates:**
- For loop syntax
- Loop variable initialization
- Loop condition
- Loop update expression
- Variable scope (i and j only exist in their loops)

### 6.5 Do-While Loops

**File:** `examples/do_while_example.ml`

```minilang
// Do-while loop (executes at least once)
int x = 5;

do {
    print(x);
    x = x - 1;
} while (x > 0);

// Do-while with false condition (still runs once)
int y = 0;
do {
    print(y);  // Prints 0
} while (y > 10);  // False, but body already executed
```

**What it demonstrates:**
- Do-while syntax
- Guaranteed first execution
- Post-condition checking
- Difference from while loops

### 6.6 Functions - Simple

**File:** `examples/function_example.ml`

```minilang
// Function to calculate square
function int square(int n) {
    return n * n;
}

// Function to check if positive
function bool isPositive(int x) {
    return x > 0;
}

int num = 5;
int result = square(num);
print(result);  // Prints 25

bool check = isPositive(-3);
print(check);   // Prints false
```

**What it demonstrates:**
- Function declaration syntax
- Parameters
- Return statements
- Function calls
- Different return types (int, bool)

### 6.7 Functions - Addition

**File:** `examples/function_add_example.ml`

```minilang
// Function with multiple parameters
function int add(int a, int b) {
    return a + b;
}

function float addFloat(float x, float y) {
    return x + y;
}

int sum1 = add(10, 20);
print(sum1);  // Prints 30

float sum2 = addFloat(3.14, 2.86);
print(sum2);  // Prints 6.0
```

**What it demonstrates:**
- Multiple parameters
- Same function name with different types
- Type-specific functions
- Float arithmetic

### 6.8 Nested Loops

**File:** `examples/nested_loops.ml`

```minilang
// Nested for loops
for (int i = 1; i <= 3; i = i + 1) {
    for (int j = 1; j <= 3; j = j + 1) {
        int product = i * j;
        print(product);
    }
}

// Nested while loops
int outer = 0;
while (outer < 2) {
    int inner = 0;
    while (inner < 2) {
        print(outer);
        print(inner);
        inner = inner + 1;
    }
    outer = outer + 1;
}
```

**What it demonstrates:**
- Nested loops
- Loop variable scoping
- Multiplication tables pattern
- Independent loop counters

### 6.9 Complex Expression

**File:** `examples/example4_complex.ml`

```minilang
// Complex expressions and operator precedence
int a = 5;
int b = 10;
int c = 3;

// Arithmetic precedence: * before +
int result1 = a + b * c;  // 5 + (10 * 3) = 35
print(result1);

// Relational and logical operators
bool complex = (a < b) and ((b > c) or (a == c));
print(complex);  // true and (true or false) = true

// Mixed types with implicit conversion
float mixed = a + 2.5;  // int + float = float
print(mixed);  // 7.5
```

**What it demonstrates:**
- Operator precedence
- Complex boolean expressions
- Parentheses for grouping
- Type coercion (int to float)

### 6.10 All Features Combined

**File:** `examples/all_features.ml`

```minilang
// Complete program showcasing all MiniLang features

// Functions
function int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        int prev = factorial(n - 1);
        return n * prev;
    }
}

function bool isPrime(int num) {
    if (num <= 1) {
        return false;
    }
    for (int i = 2; i < num; i = i + 1) {
        int remainder = num - ((num / i) * i);  // Modulo simulation
        if (remainder == 0) {
            return false;
        }
    }
    return true;
}

// Main program
int n = 5;
int fact = factorial(n);
print(fact);  // 120

// Check primes
for (int num = 2; num <= 10; num = num + 1) {
    bool prime = isPrime(num);
    if (prime) {
        print(num);  // Prints 2, 3, 5, 7
    }
}

// Complex calculations
int sum = 0;
int count = 0;

while (count < 10) {
    count = count + 1;
    
    if (count < 5) {
        sum = sum + count;
    } else {
        sum = sum + (count * 2);
    }
}

print(sum);

// Float operations
float pi = 3.14159;
float radius = 5.0;
float area = pi * (radius * radius);
print(area);
```

**What it demonstrates:**
- Recursive functions
- Complex algorithms (factorial, prime checking)
- Multiple function definitions
- For, while loops
- If-else conditionals
- Integer and float operations
- All operator types
- Variable scoping

---

## 7. Program Variations & Testing

### 7.1 How to Modify Sample Programs

#### Variation 1: Change Data Types
```minilang
// Original
int x = 10;

// Variation: Use float
float x = 10.5;
```

#### Variation 2: Modify Loop Bounds
```minilang
// Original
for (int i = 0; i < 5; i = i + 1) {
    print(i);
}

// Variation: Different range
for (int i = 10; i < 20; i = i + 2) {  // Count by 2s
    print(i);
}
```

#### Variation 3: Add More Operations
```minilang
// Original
int sum = a + b;

// Variation: Multiple operations
int sum = a + b;
int diff = a - b;
int prod = a * b;
float avg = (a + b) / 2.0;
```

#### Variation 4: Nest Control Structures
```minilang
// Original
if (x > 0) {
    print(x);
}

// Variation: Nested
if (x > 0) {
    if (x > 10) {
        print(10);
    } else {
        print(x);
    }
}
```

### 7.2 Common Test Cases

#### Test Case 1: Type Checking
```minilang
// Should PASS
int a = 5;
float b = 3.14;
float c = a + b;  // int + float = float ✓

// Should FAIL
bool d = a + b;  // Cannot assign float to bool ✗
```

#### Test Case 2: Scope Testing
```minilang
// Should PASS
int x = 10;
{
    int x = 20;  // Shadow outer x ✓
    print(x);    // Prints 20
}
print(x);        // Prints 10

// Should FAIL
{
    int y = 5;
}
print(y);        // Error: y not in scope ✗
```

#### Test Case 3: Initialization
```minilang
// Should FAIL
int x;
print(x);  // Error: used before initialization ✗

// Should PASS
int x;
x = 5;
print(x);  // ✓ Initialized by assignment
```

#### Test Case 4: Function Arguments
```minilang
function int add(int a, int b) {
    return a + b;
}

// Should PASS
int result = add(5, 3);  // ✓ Correct args

// Should FAIL
int wrong1 = add(5);           // ✗ Wrong arg count
int wrong2 = add(5, true);     // ✗ Wrong arg type
int wrong3 = add(5, 3, 7);     // ✗ Too many args
```

### 7.3 Error Testing Examples

#### Lexical Errors
```minilang
int x = 10@;     // ✗ Invalid character '@'
float y = 3.14.15;  // ✗ Malformed number
```

#### Syntax Errors
```minilang
int x = 10       // ✗ Missing semicolon
if (x > 5 {      // ✗ Missing closing parenthesis
    print(x)     // ✗ Missing semicolon
                 // ✗ Missing closing brace
```

#### Semantic Errors
```minilang
int x = 10;
int x = 20;      // ✗ Variable already declared

y = 5;           // ✗ Undefined variable

int a = true;    // ✗ Type mismatch

if (5) {         // ✗ Condition must be bool
    print(1);
}
```

### 7.4 Testing Workflow

1. **Test Valid Programs:**
   ```bash
   # Run web interface
   streamlit run streamlit_app.py
   
   # Select example: "All Features"
   # Click "Compile"
   # Should see: ✓ All phases pass
   ```

2. **Test Invalid Programs:**
   ```bash
   # Modify an example to introduce error
   # Click "Compile"
   # Should see: ✗ Error with description
   ```

3. **Test Each Phase Independently:**
   - Scanner: Test with invalid characters
   - Parser: Test with syntax errors
   - Semantic: Test with type errors

### 7.5 Quick Demo Script

**For Viva Demonstration:**

1. **Show Basic Program:**
   - Open `example1_basics.ml`
   - Compile successfully
   - Show token list, AST, symbol table

2. **Demonstrate For Loop:**
   - Open `for_loop_example.ml`
   - Compile
   - Explain loop phases (init, condition, update)

3. **Show Function Example:**
   - Open `function_add_example.ml`
   - Explain parameters, return type
   - Show function call type checking

4. **Introduce Error:**
   - Modify: Change `int x = 10;` to `int x = true;`
   - Compile
   - Show semantic error: "Cannot assign bool to int"

5. **Show Complex Program:**
   - Open `all_features.ml`
   - Highlight different features used
   - Compile successfully

---

## 8. Quick Reference

### 8.1 MiniLang Syntax Cheat Sheet

```minilang
// Variables
int x = 10;
float y = 3.14;
bool flag = true;

// Arithmetic
int sum = a + b;
int diff = a - b;
int prod = a * b;
int quot = a / b;

// Comparison
bool greater = a > b;
bool less = a < b;
bool equal = a == b;
bool notEqual = a != b;

// Logic
bool and_result = true and false;
bool or_result = true or false;
bool not_result = not true;

// If-Else
if (condition) {
    // statements
} else {
    // statements
}

// While
while (condition) {
    // statements
}

// For
for (int i = 0; i < 10; i = i + 1) {
    // statements
}

// Do-While
do {
    // statements
} while (condition);

// Function
function int funcName(int param1, float param2) {
    // statements
    return value;
}

// Function Call
int result = funcName(5, 3.14);

// Print
print(expression);
```

### 8.2 Common Viva Questions & Answers

**Q: Why did you choose this grammar?**
A: Our grammar is LL(1) compatible, which allows predictive parsing with one-token lookahead. It's unambiguous, supports operator precedence naturally through production nesting, and is extensible for future features.

**Q: How do you handle operator precedence?**
A: Through the structure of expression productions. Lower precedence operators (like OR) appear at higher levels of the grammar, while higher precedence operators (like multiplication) appear at lower levels. This ensures correct parsing order.

**Q: Explain your symbol table design.**
A: We use a hierarchical symbol table with parent pointers for scope management. Each scope can look up variables in its own symbols or delegate to parent scopes. This supports block-level scoping and variable shadowing naturally.

**Q: How do you check function argument types?**
A: When visiting a FunctionCall node, we: (1) Lookup the function in the symbol table, (2) Retrieve its parameter type list, (3) Compare argument count, (4) Check each argument's type against corresponding parameter type using our type compatibility rules.

**Q: What's the difference between int and float in your compiler?**
A: They're distinct types with automatic promotion: int+int=int, but int+float=float. We allow implicit int→float conversion in assignments and operations but not float→int (would lose precision).

**Q: How do you handle nested scopes?**
A: Each block creates a new SymbolTable with a parent pointer to the enclosing scope. Variable lookup searches current scope first, then recursively searches parent scopes. When exiting a block, we restore the parent scope, discarding the block's symbols.

**Q: What errors can your compiler detect?**
A: Lexical (invalid characters), Syntactic (grammar violations, missing semicolons), and Semantic (type mismatches, undefined variables, redeclarations, uninitialized usage, wrong function arguments).

### 8.3 Key Points to Remember

✅ **Three Phases:** Scanner → Parser → Semantic Analyzer
✅ **Grammar Type:** LL(1), predictive, no left recursion
✅ **Parsing Method:** Recursive descent
✅ **Type System:** Static typing with int→float coercion
✅ **Scope:** Block-level with hierarchical symbol table
✅ **Error Handling:** Comprehensive detection at all phases
✅ **New Features:** For loops, do-while loops, functions with parameters
✅ **Testing:** 15+ example programs covering all features

---

**End of Viva Preparation Guide**

*For more details, refer to:*
- `docs/grammar_specification.md` - Complete grammar
- `docs/project_report.md` - Full project report
- `SEMANTIC_RULES.md` - Detailed semantic rules
- `examples/*.ml` - All sample programs
