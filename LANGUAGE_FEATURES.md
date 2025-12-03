# MiniLang Language Features & Examples

**Authors:** Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)  
**Course:** CS-4031 - Compiler Construction  
**Date:** December 3, 2025

---

## Overview

MiniLang is a statically-typed imperative programming language with support for:
- Variables and basic data types (int, float, bool)
- Arithmetic, logical, and comparison operators
- Control flow (if-else, while, for, do-while)
- Functions with parameters and return values
- Recursion

---

## 1. Data Types

### Supported Types
- `int` - Integer numbers (e.g., 42, -10, 0)
- `float` - Floating-point numbers (e.g., 3.14, -2.5, 0.0)
- `bool` - Boolean values (`true` or `false`)

---

## 2. Variable Declarations

### Syntax
```
Type identifier = expression;
Type identifier;  // Uninitialized
```

### Examples
```c
int x = 10;
float pi = 3.14159;
bool flag = true;
int y;  // Uninitialized variable
```

---

## 3. Operators

### Arithmetic Operators
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division
- `-` Unary negation

**Example:**
```c
int a = 10 + 5;
int b = a * 2;
int c = -b;
```

### Comparison Operators
- `==` Equal to
- `!=` Not equal to
- `<` Less than
- `>` Greater than
- `<=` Less than or equal to
- `>=` Greater than or equal to

**Example:**
```c
bool result = x > y;
bool equal = a == b;
```

### Logical Operators
- `and` Logical AND
- `or` Logical OR
- `not` Logical NOT

**Example:**
```c
bool condition = (x > 5) and (y < 10);
bool flag = not condition;
```

---

## 4. Control Flow

### If-Else Statement

**Syntax:**
```
if (condition) {
    statements
} else {
    statements
}
```

**Example:**
```c
int x = 10;
if (x > 5) {
    print(1);
} else {
    print(0);
}
```

---

### While Loop

**Syntax:**
```
while (condition) {
    statements
}
```

**Example:**
```c
int counter = 5;
while (counter > 0) {
    print(counter);
    counter = counter - 1;
}
```

---

### For Loop

**Syntax:**
```
for (init; condition; update) {
    statements
}
```

**Example:**
```c
int sum = 0;
for (int i = 1; i <= 10; i = i + 1) {
    sum = sum + i;
}
print(sum);  // Outputs: 55
```

**Features:**
- Init can be variable declaration or assignment
- Condition must be boolean expression
- Update is typically an assignment
- Loop variable scoped to loop body

---

### Do-While Loop

**Syntax:**
```
do {
    statements
} while (condition);
```

**Example:**
```c
int count = 5;
do {
    print(count);
    count = count - 1;
} while (count > 0);
```

**Note:** Body executes at least once before condition check.

---

## 5. Functions

### Function Declaration

**Syntax:**
```
function returnType functionName(parameters) {
    statements
    return expression;
}
```

**Example:**
```c
function int add(int a, int b) {
    int result = a + b;
    return result;
}
```

### Function Call

**Example:**
```c
int sum = add(10, 20);
print(sum);  // Outputs: 30
```

### Recursive Functions

**Example - Factorial:**
```c
function int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int result = factorial(5);
print(result);  // Outputs: 120
```

---

## 6. Print Statement

**Syntax:**
```
print(expression);
```

**Example:**
```c
int x = 42;
print(x);
print(x + 10);
print(x > 40);
```

---

## 7. Complete Examples

### Example 1: Even/Odd Checker

```c
function bool isEven(int n) {
    int remainder = n - (n / 2 * 2);
    bool result = remainder == 0;
    return result;
}

int num = 8;
bool even = isEven(num);
if (even) {
    print(1);  // 1 = true
} else {
    print(0);  // 0 = false
}
```

---

### Example 2: Power Function

```c
function int power(int base, int exp) {
    int result = 1;
    for (int i = 0; i < exp; i = i + 1) {
        result = result * base;
    }
    return result;
}

int x = 2;
int y = 8;
int z = power(x, y);
print(z);  // Outputs: 256
```

---

### Example 3: Sum with Do-While

```c
function int sumUpTo(int n) {
    int sum = 0;
    int i = 1;
    do {
        sum = sum + i;
        i = i + 1;
    } while (i <= n);
    return sum;
}

int result = sumUpTo(10);
print(result);  // Outputs: 55
```

---

### Example 4: Greatest Common Divisor (GCD)

```c
function int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a - (a / b * b);  // a % b
        a = temp;
    }
    return a;
}

int x = 48;
int y = 18;
int result = gcd(x, y);
print(result);  // Outputs: 6
```

---

### Example 5: Fibonacci Sequence

```c
function int fibonacci(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

for (int i = 0; i < 10; i = i + 1) {
    int fib = fibonacci(i);
    print(fib);
}
// Outputs: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

---

### Example 6: All Features Combined

```c
// Function to check prime number
function bool isPrime(int n) {
    if (n <= 1) {
        return false;
    }
    
    int i = 2;
    while (i * i <= n) {
        int quotient = n / i;
        if (quotient * i == n) {
            return false;
        }
        i = i + 1;
    }
    return true;
}

// Print prime numbers from 2 to 20
for (int num = 2; num <= 20; num = num + 1) {
    bool prime = isPrime(num);
    if (prime) {
        print(num);
    }
}
// Outputs: 2, 3, 5, 7, 11, 13, 17, 19
```

---

## 8. Language Rules

### Type System
1. **Static Typing:** All variables must be declared with a type
2. **Type Safety:** Operations must be type-compatible
3. **No Implicit Conversions:** Except `int` → `float` in arithmetic
4. **Boolean Conditions:** Control flow conditions must be boolean

### Scoping Rules
1. **Global Scope:** Variables declared outside functions
2. **Function Scope:** Parameters and local variables
3. **Block Scope:** For-loop init variables scoped to loop
4. **Shadowing:** Not allowed - redeclaration is an error

### Function Rules
1. **Forward Declaration:** Not required - functions can call each other
2. **Recursion:** Fully supported
3. **Return Required:** Functions must return a value of declared type
4. **Parameter Passing:** Pass by value only

---

## 9. Limitations

Current MiniLang does **NOT** support:
- Arrays or strings
- Pointers or references
- Structs or classes
- Void functions (all functions must return a value)
- Multiple return statements (only one per function)
- Break/continue statements
- Switch/case statements
- Global constants
- File I/O
- Standard library

---

## 10. Running Examples

All example files are in the `examples/` directory:
- `for_loop_example.ml` - For loop demonstration
- `do_while_example.ml` - Do-while loop demonstration
- `function_example.ml` - Recursive factorial
- `function_add_example.ml` - Simple function call
- `nested_loops.ml` - Nested loop example
- `all_features.ml` - Comprehensive feature showcase

To compile an example:
```bash
Get-Content examples/for_loop_example.ml | cpp_core/minilang_compiler.exe
```

---

## 11. Error Messages

### Common Compile-Time Errors

**Type Mismatch:**
```c
int x = true;  // Error: Type mismatch in declaration: expected int, got bool
```

**Undefined Variable:**
```c
print(undefined);  // Error: Undefined variable: undefined
```

**Function Errors:**
```c
function int test() {
    return true;  // Error: Return type mismatch: expected int, got bool
}

test(5);  // Error: Function test expects 0 arguments, got 1
```

**Condition Errors:**
```c
int x = 5;
if (x) { }  // Error: If condition must be boolean, got int
```

---

## 12. Best Practices

1. **Initialize Variables:** Always initialize before use
2. **Type Consistency:** Match types in assignments and comparisons
3. **Function Return:** Ensure all code paths return correct type
4. **Boolean Conditions:** Use comparison operators for conditions
5. **Loop Variables:** Use meaningful names and appropriate types

---

## Conclusion

MiniLang provides essential programming constructs for learning compiler design while maintaining simplicity. The language supports structured programming with functions, loops, and conditionals, making it suitable for educational purposes and demonstrating compilation phases.

For technical details on grammar and semantic rules, see `SEMANTIC_RULES.md`.
