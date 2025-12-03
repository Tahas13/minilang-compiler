# MiniLang Compiler - Attributed Grammar and Semantic Rules

**Authors:** Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)  
**Course:** CS-4031 - Compiler Construction  
**Date:** December 3, 2025

---

## 1. Introduction

This document presents the attributed grammar and semantic rules for the MiniLang programming language compiler. The semantic analyzer performs type checking, symbol table management, and ensures program correctness beyond syntactic validity.

---

## 2. MiniLang Grammar Overview

### 2.1 Productions

```
Program     → StmtList
StmtList    → Stmt StmtList | ε
Stmt        → VarDecl | Assignment | PrintStmt | IfStmt | WhileStmt

VarDecl     → Type ID = Expr ;
            | Type ID ;
Assignment  → ID = Expr ;
PrintStmt   → print ( Expr ) ;
IfStmt      → if ( Expr ) { StmtList } ElsePart
ElsePart    → else { StmtList } | ε
WhileStmt   → while ( Expr ) { StmtList }

Expr        → OrExpr
OrExpr      → AndExpr or OrExpr | AndExpr
AndExpr     → EqExpr and AndExpr | EqExpr
EqExpr      → RelExpr EqOp EqExpr | RelExpr
RelExpr     → AddExpr RelOp RelExpr | AddExpr
AddExpr     → MultExpr AddOp AddExpr | MultExpr
MultExpr    → UnaryExpr MultOp MultExpr | UnaryExpr
UnaryExpr   → UnaryOp UnaryExpr | Primary
Primary     → ID | INTEGER | FLOAT | BOOLEAN | ( Expr )

Type        → int | float | bool
EqOp        → == | !=
RelOp       → < | > | <= | >=
AddOp       → + | -
MultOp      → * | /
UnaryOp     → - | not
BOOLEAN     → true | false
```

---

## 3. Attributed Grammar with Semantic Rules

### 3.1 Attributes

**Synthesized Attributes:**
- `type`: The data type of an expression (int, float, bool)
- `value`: The value of a literal
- `name`: The identifier name

**Inherited Attributes:**
- `env`: Symbol table environment

### 3.2 Symbol Table

```
SymbolTable = Map<string, Symbol>

Symbol {
    type: string          // "int", "float", or "bool"
    initialized: boolean  // true if variable has been assigned
}
```

---

## 4. Semantic Rules by Production

### 4.1 Variable Declaration

#### **Production:**
```
VarDecl → Type ID = Expr ;
```

#### **Semantic Rules:**
1. **Check if variable already declared:**
   - If `ID.name ∈ SymbolTable` → ERROR: "Variable already declared: ID.name"

2. **Type compatibility:**
   - `Type(Expr) = Type.value`
   - If `Type(Expr) ≠ Type.value` → ERROR: "Type mismatch in declaration"

3. **Symbol table update:**
   ```
   SymbolTable[ID.name] = Symbol {
       type: Type.value,
       initialized: true
   }
   ```

#### **Production (without initialization):**
```
VarDecl → Type ID ;
```

#### **Semantic Rules:**
1. **Check if variable already declared:**
   - If `ID.name ∈ SymbolTable` → ERROR: "Variable already declared: ID.name"

2. **Symbol table update:**
   ```
   SymbolTable[ID.name] = Symbol {
       type: Type.value,
       initialized: false
   }
   ```

---

### 4.2 Assignment Statement

#### **Production:**
```
Assignment → ID = Expr ;
```

#### **Semantic Rules:**
1. **Check variable declaration:**
   - If `ID.name ∉ SymbolTable` → ERROR: "Undefined variable: ID.name"

2. **Type compatibility:**
   - `Type(ID) = SymbolTable[ID.name].type`
   - `Type(Expr)` must match `Type(ID)`
   - If `Type(Expr) ≠ Type(ID)` → ERROR: "Type mismatch in assignment"

3. **Update initialization status:**
   ```
   SymbolTable[ID.name].initialized = true
   ```

---

### 4.3 Print Statement

#### **Production:**
```
PrintStmt → print ( Expr ) ;
```

#### **Semantic Rules:**
1. **Type checking:**
   - `Type(Expr)` must be valid (int, float, or bool)
   - Evaluate `Expr` to ensure all variables are declared and types are correct

2. **No specific type required:**
   - Print accepts any valid expression type

---

### 4.4 Arithmetic Expressions

#### **Production:**
```
Expr → Expr₁ + Expr₂
Expr → Expr₁ - Expr₂
Expr → Expr₁ * Expr₂
Expr → Expr₁ / Expr₂
```

#### **Semantic Rules:**
1. **Operand type checking:**
   - `Type(Expr₁) ∈ {int, float}`
   - `Type(Expr₂) ∈ {int, float}`
   - If operand type is invalid → ERROR: "Invalid operand type for arithmetic operator"

2. **Result type:**
   ```
   Type(Expr) = {
       float  if Type(Expr₁) = float OR Type(Expr₂) = float
       int    otherwise
   }
   ```

---

### 4.5 Comparison Expressions

#### **Production:**
```
Expr → Expr₁ > Expr₂
Expr → Expr₁ < Expr₂
Expr → Expr₁ >= Expr₂
Expr → Expr₁ <= Expr₂
Expr → Expr₁ == Expr₂
Expr → Expr₁ != Expr₂
```

#### **Semantic Rules:**
1. **Type compatibility:**
   - `Type(Expr₁) = Type(Expr₂)`
   - If types don't match → ERROR: "Type mismatch in comparison"

2. **Result type:**
   ```
   Type(Expr) = bool
   ```

---

### 4.6 Logical Expressions

#### **Production:**
```
Expr → Expr₁ and Expr₂
Expr → Expr₁ or Expr₂
```

#### **Semantic Rules:**
1. **Operand type checking:**
   - `Type(Expr₁) = bool`
   - `Type(Expr₂) = bool`
   - If operand type is not bool → ERROR: "Invalid operand type for logical operator"

2. **Result type:**
   ```
   Type(Expr) = bool
   ```

---

### 4.7 Unary Expressions

#### **Production (Negation):**
```
Expr → - Expr₁
```

#### **Semantic Rules:**
1. **Operand type checking:**
   - `Type(Expr₁) ∈ {int, float}`
   - If invalid type → ERROR: "Invalid operand type for unary minus"

2. **Result type:**
   ```
   Type(Expr) = Type(Expr₁)
   ```

#### **Production (Logical NOT):**
```
Expr → not Expr₁
```

#### **Semantic Rules:**
1. **Operand type checking:**
   - `Type(Expr₁) = bool`
   - If `Type(Expr₁) ≠ bool` → ERROR: "Invalid operand type for NOT operator"

2. **Result type:**
   ```
   Type(Expr) = bool
   ```

---

### 4.8 If Statement

#### **Production:**
```
IfStmt → if ( Expr ) { StmtList₁ } else { StmtList₂ }
```

#### **Semantic Rules:**
1. **Condition type checking:**
   - `Type(Expr) = bool`
   - If `Type(Expr) ≠ bool` → ERROR: "If condition must be boolean"

2. **Statement analysis:**
   - Analyze all statements in `StmtList₁` with current environment
   - Analyze all statements in `StmtList₂` with current environment

---

### 4.9 While Statement

#### **Production:**
```
WhileStmt → while ( Expr ) { StmtList }
```

#### **Semantic Rules:**
1. **Condition type checking:**
   - `Type(Expr) = bool`
   - If `Type(Expr) ≠ bool` → ERROR: "While condition must be boolean"

2. **Body analysis:**
   - Analyze all statements in `StmtList` with current environment

---

### 4.10 Identifier Expression

#### **Production:**
```
Primary → ID
```

#### **Semantic Rules:**
1. **Variable declaration check:**
   - If `ID.name ∉ SymbolTable` → ERROR: "Undefined variable: ID.name"

2. **Initialization check:**
   - If `SymbolTable[ID.name].initialized = false` → WARNING: "Variable used before initialization"

3. **Type synthesis:**
   ```
   Type(Primary) = SymbolTable[ID.name].type
   ```

---

### 4.11 Literal Expressions

#### **Production (Integer):**
```
Primary → INTEGER
```

#### **Semantic Rules:**
```
Type(Primary) = int
Primary.value = INTEGER.value
```

#### **Production (Float):**
```
Primary → FLOAT
```

#### **Semantic Rules:**
```
Type(Primary) = float
Primary.value = FLOAT.value
```

#### **Production (Boolean):**
```
Primary → true | false
```

#### **Semantic Rules:**
```
Type(Primary) = bool
Primary.value = true | false
```

---

## 5. Type Compatibility Rules

### 5.1 Numeric Type Coercion
- When mixing `int` and `float` in arithmetic operations, the result is `float`
- No automatic conversion between numeric types and `bool`

### 5.2 Type Hierarchy
```
float  (wider)
  ↑
int
```

### 5.3 Implicit Conversions
- `int → float` (allowed in mixed arithmetic)
- No other implicit conversions

---

## 6. Error Categories

### 6.1 Type Errors
- Type mismatch in variable declaration
- Type mismatch in assignment
- Invalid operand types for operators
- Type mismatch in comparisons

### 6.2 Declaration Errors
- Variable already declared
- Undefined variable
- Variable used before initialization

### 6.3 Semantic Errors
- Non-boolean condition in if/while statements
- Invalid operations (e.g., bool + int)

---

## 7. Example Semantic Analysis

### 7.1 Valid Program

```c
int x = 10;
int y = 20;
bool result = x > y;

if (result) {
    print(x);
} else {
    print(y);
}
```

**Semantic Analysis:**
1. Line 1: Declare `x` as `int`, initialize to 10 ✓
2. Line 2: Declare `y` as `int`, initialize to 20 ✓
3. Line 3: `x > y` returns `bool`, matches `result` type ✓
4. Line 5: `result` is `bool`, valid condition ✓
5. All variables declared and properly typed ✓

### 7.2 Invalid Program (Type Error)

```c
int x = true;  // ERROR: Type mismatch
```

**Error:** "Type mismatch in declaration: expected int, got bool"

### 7.3 Invalid Program (Undefined Variable)

```c
print(undeclared);  // ERROR: Undefined variable
```

**Error:** "Undefined variable: undeclared"

### 7.4 Invalid Program (Condition Type)

```c
int x = 10;
if (x) {  // ERROR: Non-boolean condition
    print(x);
}
```

**Error:** "If condition must be boolean, got int"

---

## 8. Implementation Notes

### 8.1 Semantic Analyzer Structure

The semantic analyzer is implemented in `cpp_core/semantic.h` with:
- `SemanticAnalyzer` class
- Symbol table (map of variable names to symbols)
- Recursive AST traversal
- Error collection and reporting

### 8.2 Key Functions

```cpp
class SemanticAnalyzer {
    std::string analyzeExpression(const ASTNode* node);
    void analyzeStatement(const ASTNode* node);
    bool analyze(const Program* program);
}
```

### 8.3 Symbol Table Operations

```cpp
// Add variable to symbol table
symbolTable[name] = Symbol(type, initialized);

// Check if variable exists
if (symbolTable.find(name) == symbolTable.end())
    addError("Undefined variable");

// Get variable type
std::string varType = symbolTable[name].type;
```

---

## 9. Conclusion

The attributed grammar and semantic rules presented in this document ensure that MiniLang programs are:
- **Type-safe:** All operations respect type constraints
- **Well-defined:** All variables are declared before use
- **Correct:** Control flow conditions are boolean
- **Consistent:** Type rules are uniformly applied

The semantic analyzer catches errors at compile-time, preventing runtime type errors and undefined behavior.

---

## References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.).
2. Appel, A. W. (2002). *Modern Compiler Implementation in C*.
3. Cooper, K., & Torczon, L. (2011). *Engineering a Compiler* (2nd ed.).
