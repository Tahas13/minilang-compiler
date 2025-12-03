# MiniLang Grammar Specification and Semantic Rules

**Course:** CS-4031 – Compiler Construction  
**Instructor:** Syed Zain Ul Hassan  
**Authors:** Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)

## Formal Grammar

### Context-Free Grammar for MiniLang

```
1.  Program       → StatementList
2.  StatementList → Statement StatementList | ε
3.  Statement     → VarDecl | Assignment | PrintStmt | IfStmt | WhileStmt | Block
4.  VarDecl       → Type IDENTIFIER InitOpt ';'
5.  InitOpt       → '=' Expression | ε
6.  Assignment    → IDENTIFIER '=' Expression ';'
7.  PrintStmt     → 'print' '(' Expression ')' ';'
8.  IfStmt        → 'if' '(' Expression ')' Statement ElseOpt
9.  ElseOpt       → 'else' Statement | ε
10. WhileStmt     → 'while' '(' Expression ')' Statement
11. Block         → '{' StatementList '}'
12. Expression    → LogicalOr
13. LogicalOr     → LogicalAnd LogicalOrRest
14. LogicalOrRest → 'or' LogicalAnd LogicalOrRest | ε
15. LogicalAnd    → Equality LogicalAndRest
16. LogicalAndRest → 'and' Equality LogicalAndRest | ε
17. Equality      → Relational EqualityRest
18. EqualityRest  → ('==' | '!=') Relational EqualityRest | ε
19. Relational    → Additive RelationalRest
20. RelationalRest → ('>' | '<') Additive RelationalRest | ε
21. Additive      → Multiplicative AdditiveRest
22. AdditiveRest  → ('+' | '-') Multiplicative AdditiveRest | ε
23. Multiplicative → Unary MultiplicativeRest
24. MultiplicativeRest → ('*' | '/') Unary MultiplicativeRest | ε
25. Unary         → UnaryOp Unary | Primary
26. UnaryOp       → 'not' | '-'
27. Primary       → IDENTIFIER | INTEGER_LITERAL | FLOAT_LITERAL 
                  | BOOLEAN_LITERAL | '(' Expression ')'
28. Type          → 'int' | 'float' | 'bool'
```

### Terminal Symbols

```
Keywords:     int, float, bool, true, false, if, else, while, print, and, or, not
Operators:    +, -, *, /, >, <, ==, !=, =
Delimiters:   ;, (, ), {, }
Literals:     INTEGER_LITERAL, FLOAT_LITERAL, BOOLEAN_LITERAL
Identifiers:  IDENTIFIER
Comments:     // (single-line comments)
```

### Non-Terminal Symbols

```
Program, StatementList, Statement, VarDecl, InitOpt, Assignment, PrintStmt,
IfStmt, ElseOpt, WhileStmt, Block, Expression, LogicalOr, LogicalOrRest,
LogicalAnd, LogicalAndRest, Equality, EqualityRest, Relational, RelationalRest,
Additive, AdditiveRest, Multiplicative, MultiplicativeRest, Unary, UnaryOp,
Primary, Type
```

## Attributed Grammar with Semantic Rules

### Semantic Attributes

- **type**: Data type of expressions and variables
- **value**: Compile-time value (for literals)
- **symbol_table**: Current symbol table scope
- **initialized**: Whether a variable has been initialized

### Production Rules with Semantic Actions

#### 1. Variable Declaration
```
VarDecl → Type IDENTIFIER InitOpt ';'
{
    // Semantic Rule 1: Variable Declaration
    if (lookup(IDENTIFIER.lexeme) in current_scope) {
        error("Variable already declared in current scope");
    } else {
        if (InitOpt.has_value) {
            if (can_assign(Type.type, InitOpt.type)) {
                define_symbol(IDENTIFIER.lexeme, Type.type, true);
            } else {
                error("Type mismatch in variable initialization");
            }
        } else {
            define_symbol(IDENTIFIER.lexeme, Type.type, false);
        }
    }
}
```

#### 2. Assignment Statement
```
Assignment → IDENTIFIER '=' Expression ';'
{
    // Semantic Rule 2: Assignment
    symbol = lookup(IDENTIFIER.lexeme);
    if (symbol == null) {
        error("Undefined variable: " + IDENTIFIER.lexeme);
    } else {
        if (can_assign(symbol.type, Expression.type)) {
            symbol.initialized = true;
        } else {
            error("Type mismatch in assignment");
        }
    }
}
```

#### 3. Binary Operations
```
Additive → Multiplicative '+' Additive
{
    // Semantic Rule 3: Arithmetic Operations
    left_type = Multiplicative.type;
    right_type = Additive.type;
    
    if (left_type == "int" && right_type == "int") {
        Additive.type = "int";
    } else if ((left_type == "int" || left_type == "float") && 
               (right_type == "int" || right_type == "float")) {
        Additive.type = "float";
    } else {
        error("Invalid operand types for arithmetic operation");
    }
}
```

#### 4. Logical Operations
```
LogicalAnd → Equality 'and' LogicalAnd
{
    // Semantic Rule 4: Logical Operations
    if (Equality.type == "bool" && LogicalAnd.type == "bool") {
        LogicalAnd.type = "bool";
    } else {
        error("Logical operators require boolean operands");
    }
}
```

#### 5. Relational Operations
```
Relational → Additive '>' Relational
{
    // Semantic Rule 5: Relational Operations
    left_type = Additive.type;
    right_type = Relational.type;
    
    if ((left_type == "int" || left_type == "float") && 
        (right_type == "int" || right_type == "float")) {
        Relational.type = "bool";
    } else {
        error("Relational operators require numeric operands");
    }
}
```

#### 6. Identifier Reference
```
Primary → IDENTIFIER
{
    // Semantic Rule 6: Variable Reference
    symbol = lookup(IDENTIFIER.lexeme);
    if (symbol == null) {
        error("Undefined variable: " + IDENTIFIER.lexeme);
    } else {
        if (!symbol.initialized) {
            error("Variable used before initialization: " + IDENTIFIER.lexeme);
        }
        Primary.type = symbol.type;
    }
}
```

#### 7. Control Flow Conditions
```
IfStmt → 'if' '(' Expression ')' Statement ElseOpt
{
    // Semantic Rule 7: If Statement
    if (Expression.type != "bool") {
        error("If condition must be boolean");
    }
    // Process statements in new scope
    enter_scope();
    process(Statement);
    if (ElseOpt.present) {
        process(ElseOpt.statement);
    }
    exit_scope();
}

WhileStmt → 'while' '(' Expression ')' Statement
{
    // Semantic Rule 8: While Statement
    if (Expression.type != "bool") {
        error("While condition must be boolean");
    }
    // Process body in new scope
    enter_scope();
    process(Statement);
    exit_scope();
}
```

## Type System Rules

### Type Compatibility Matrix

| Operation | Left Type | Right Type | Result Type | Valid? |
|-----------|-----------|------------|-------------|---------|
| +, -, *, / | int | int | int | ✓ |
| +, -, *, / | int | float | float | ✓ |
| +, -, *, / | float | int | float | ✓ |
| +, -, *, / | float | float | float | ✓ |
| +, -, *, / | bool | any | - | ✗ |
| >, < | int | int | bool | ✓ |
| >, < | int | float | bool | ✓ |
| >, < | float | int | bool | ✓ |
| >, < | float | float | bool | ✓ |
| >, < | bool | any | - | ✗ |
| ==, != | int | int | bool | ✓ |
| ==, != | float | float | bool | ✓ |
| ==, != | bool | bool | bool | ✓ |
| ==, != | int | float | bool | ✓ |
| and, or | bool | bool | bool | ✓ |
| and, or | non-bool | any | - | ✗ |

### Assignment Compatibility

```
Assignment_Compatible(target_type, source_type):
    if target_type == source_type:
        return true
    if target_type == "float" and source_type == "int":
        return true  // Implicit int to float conversion
    return false
```

## Scope Rules

### Scope Management
1. **Global Scope**: Contains all top-level variable declarations
2. **Block Scope**: Each `{}` block creates a new scope
3. **Variable Lookup**: Search current scope first, then parent scopes
4. **Variable Shadowing**: Inner scope variables can shadow outer scope variables

### Scope Semantic Rules
```
Block → '{' StatementList '}'
{
    // Semantic Rule 9: Block Scope
    enter_scope();
    process(StatementList);
    exit_scope();
}
```

## Error Detection Rules

### Lexical Errors
- Invalid characters in input
- Malformed number literals
- Unterminated comments

### Syntax Errors
- Missing semicolons
- Unmatched parentheses or braces
- Invalid statement structures
- Unexpected tokens

### Semantic Errors
- **Type Errors**: Incompatible types in operations or assignments
- **Declaration Errors**: Variable redeclaration in same scope
- **Reference Errors**: Use of undeclared variables
- **Initialization Errors**: Use of uninitialized variables
- **Control Flow Errors**: Non-boolean conditions in if/while statements

## Symbol Table Structure

```
Symbol {
    name: string
    type: string  // "int", "float", "bool"
    initialized: boolean
    scope_level: integer
    line: integer
    column: integer
}

SymbolTable {
    symbols: Map<string, Symbol>
    parent: SymbolTable
    
    methods:
        lookup(name): Symbol
        define(name, type, initialized): boolean
        is_defined(name): boolean
        create_child_scope(): SymbolTable
}
```

## Example Semantic Analysis

### Input Program
```minilang
int x = 10;
float y;
bool flag = true;

if (x > 5 and flag) {
    y = x + 3.14;
    print(y);
}
```

### Semantic Analysis Steps
1. **x = 10**: Define `x` as `int`, initialized = true
2. **float y**: Define `y` as `float`, initialized = false  
3. **flag = true**: Define `flag` as `bool`, initialized = true
4. **x > 5**: Check `x` is defined and initialized, result type = `bool`
5. **and flag**: Check `flag` is defined and initialized, result type = `bool`
6. **y = x + 3.14**: 
   - Check `x` and `y` are defined
   - `x` (int) + `3.14` (float) → `float`
   - Assignment `float = float` ✓
   - Mark `y` as initialized
7. **print(y)**: Check `y` is defined and initialized ✓

This comprehensive grammar specification and semantic rule set ensures that MiniLang programs are syntactically correct and semantically valid before execution.