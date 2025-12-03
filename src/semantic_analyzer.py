"""
Semantic Analyzer for MiniLang compiler.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

from typing import List, Optional, Any
from ast_nodes import *
from symbol_table import SymbolTable, Symbol

class SemanticError(Exception):
    """Exception raised for semantic analysis errors."""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Semantic Error at line {line}, column {column}: {message}")

class TypeChecker(ASTVisitor):
    """Semantic analyzer that performs type checking and symbol table management."""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        self.current_scope = self.symbol_table
    
    def add_error(self, message: str, line: int = 0, column: int = 0):
        """Add a semantic error to the list."""
        error = SemanticError(message, line, column)
        self.errors.append(error)
        print(f"Semantic Error: {error}")
    
    def analyze(self, ast: Program) -> bool:
        """Analyze the AST for semantic errors. Returns True if no errors."""
        self.errors = []
        try:
            self.visit(ast)
            return len(self.errors) == 0
        except Exception as e:
            self.add_error(f"Internal error during semantic analysis: {e}")
            return False
    
    def get_expression_type(self, expr: Expression) -> Optional[str]:
        """Get the type of an expression."""
        if isinstance(expr, IntegerLiteral):
            return 'int'
        elif isinstance(expr, FloatLiteral):
            return 'float'
        elif isinstance(expr, BooleanLiteral):
            return 'bool'
        elif isinstance(expr, Identifier):
            symbol = self.current_scope.lookup(expr.name)
            if symbol:
                return symbol.type
            else:
                self.add_error(f"Undefined variable: {expr.name}")
                return None
        elif isinstance(expr, BinaryOp):
            return self.get_binary_op_type(expr)
        elif isinstance(expr, UnaryOp):
            return self.get_unary_op_type(expr)
        else:
            self.add_error(f"Unknown expression type: {type(expr).__name__}")
            return None
    
    def get_binary_op_type(self, expr: BinaryOp) -> Optional[str]:
        """Get the result type of a binary operation."""
        left_type = self.get_expression_type(expr.left)
        right_type = self.get_expression_type(expr.right)
        
        if left_type is None or right_type is None:
            return None
        
        # Arithmetic operators (+, -, *, /)
        if expr.operator in ['+', '-', '*', '/']:
            if left_type == 'int' and right_type == 'int':
                return 'int'
            elif (left_type in ['int', 'float']) and (right_type in ['int', 'float']):
                return 'float'
            else:
                self.add_error(f"Invalid operand types for {expr.operator}: {left_type} and {right_type}")
                return None
        
        # Relational operators (>, <, >=, <=)
        elif expr.operator in ['>', '<', '>=', '<=']:
            if (left_type in ['int', 'float']) and (right_type in ['int', 'float']):
                return 'bool'
            else:
                self.add_error(f"Invalid operand types for {expr.operator}: {left_type} and {right_type}")
                return None
        
        # Equality operators (==, !=)
        elif expr.operator in ['==', '!=']:
            if left_type == right_type:
                return 'bool'
            elif (left_type in ['int', 'float']) and (right_type in ['int', 'float']):
                return 'bool'
            else:
                self.add_error(f"Cannot compare {left_type} with {right_type}")
                return None
        
        # Logical operators (and, or)
        elif expr.operator in ['and', 'or']:
            if left_type == 'bool' and right_type == 'bool':
                return 'bool'
            else:
                self.add_error(f"Logical operator {expr.operator} requires boolean operands, got {left_type} and {right_type}")
                return None
        
        else:
            self.add_error(f"Unknown binary operator: {expr.operator}")
            return None
    
    def get_unary_op_type(self, expr: UnaryOp) -> Optional[str]:
        """Get the result type of a unary operation."""
        operand_type = self.get_expression_type(expr.operand)
        
        if operand_type is None:
            return None
        
        if expr.operator == 'not':
            if operand_type == 'bool':
                return 'bool'
            else:
                self.add_error(f"Logical NOT operator requires boolean operand, got {operand_type}")
                return None
        
        elif expr.operator == '-':
            if operand_type in ['int', 'float']:
                return operand_type
            else:
                self.add_error(f"Unary minus operator requires numeric operand, got {operand_type}")
                return None
        
        else:
            self.add_error(f"Unknown unary operator: {expr.operator}")
            return None
    
    def can_assign(self, target_type: str, source_type: str) -> bool:
        """Check if source type can be assigned to target type."""
        if target_type == source_type:
            return True
        
        # Allow int to float conversion
        if target_type == 'float' and source_type == 'int':
            return True
        
        return False
    
    def visit_program(self, node: Program):
        """Visit the program node."""
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_var_declaration(self, node: VarDeclaration):
        """Visit variable declaration node."""
        # Check if variable is already declared in current scope
        if node.name in self.current_scope.symbols:
            self.add_error(f"Variable '{node.name}' already declared in this scope")
            return
        
        # If there's an initial value, check type compatibility
        if node.value:
            value_type = self.get_expression_type(node.value)
            if value_type and not self.can_assign(node.var_type, value_type):
                self.add_error(f"Cannot assign {value_type} to {node.var_type} variable '{node.name}'")
                return
        
        # Add variable to symbol table
        self.current_scope.define(
            node.name, 
            node.var_type, 
            value=(node.value is not None)
        )
    
    def visit_assignment(self, node: Assignment):
        """Visit assignment node."""
        # Check if variable is declared
        symbol = self.current_scope.lookup(node.name)
        if symbol is None:
            self.add_error(f"Undefined variable: {node.name}")
            return
        
        # Check type compatibility
        value_type = self.get_expression_type(node.value)
        if value_type and not self.can_assign(symbol.type, value_type):
            self.add_error(f"Cannot assign {value_type} to {symbol.type} variable '{node.name}'")
            return
        
        # Mark variable as initialized
        self.current_scope.assign(node.name, True)
    
    def visit_print_statement(self, node: PrintStatement):
        """Visit print statement node."""
        # Just check that the expression is valid
        self.get_expression_type(node.expression)
    
    def visit_if_statement(self, node: IfStatement):
        """Visit if statement node."""
        # Check condition type
        condition_type = self.get_expression_type(node.condition)
        if condition_type and condition_type != 'bool':
            self.add_error(f"If condition must be boolean, got {condition_type}")
        
        # Visit then statements
        for stmt in node.then_statements:
            self.visit(stmt)
        
        # Visit else statements if present
        if node.else_statements:
            for stmt in node.else_statements:
                self.visit(stmt)
    
    def visit_while_statement(self, node: WhileStatement):
        """Visit while statement node."""
        # Check condition type
        condition_type = self.get_expression_type(node.condition)
        if condition_type and condition_type != 'bool':
            self.add_error(f"While condition must be boolean, got {condition_type}")
        
        # Visit body statements
        for stmt in node.body:
            self.visit(stmt)
    
    def visit_block(self, node: Block):
        """Visit block node (creates new scope)."""
        # Create new scope for the block
        old_scope = self.current_scope
        self.current_scope = self.current_scope.create_child_scope()
        
        try:
            # Visit all statements in the block
            for stmt in node.statements:
                self.visit(stmt)
        finally:
            # Restore previous scope
            self.current_scope = old_scope
    
    def visit_binary_op(self, node: BinaryOp):
        """Visit binary operation node."""
        # Type checking is done in get_binary_op_type
        self.get_binary_op_type(node)
    
    def visit_unary_op(self, node: UnaryOp):
        """Visit unary operation node."""
        # Type checking is done in get_unary_op_type
        self.get_unary_op_type(node)
    
    def visit_identifier(self, node: Identifier):
        """Visit identifier node."""
        # Check if variable is declared
        symbol = self.current_scope.lookup(node.name)
        if symbol is None:
            self.add_error(f"Undefined variable: {node.name}")
        elif not symbol.initialized:
            self.add_error(f"Variable '{node.name}' used before initialization")
    
    def visit_integer_literal(self, node: IntegerLiteral):
        """Visit integer literal node."""
        pass  # No semantic checking needed for literals
    
    def visit_float_literal(self, node: FloatLiteral):
        """Visit float literal node."""
        pass  # No semantic checking needed for literals
    
    def visit_boolean_literal(self, node: BooleanLiteral):
        """Visit boolean literal node."""
        pass  # No semantic checking needed for literals
    
    def visit(self, node: ASTNode):
        """Generic visit method that dispatches to specific visit methods."""
        method_name = f"visit_{node.__class__.__name__.lower()}"
        method_name = method_name.replace('literal', '_literal')
        method_name = method_name.replace('statement', '_statement')
        method_name = method_name.replace('declaration', '_declaration')
        method_name = method_name.replace('binaryop', 'binary_op')
        method_name = method_name.replace('unaryop', 'unary_op')
        
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            raise Exception(f"No visit method for {node.__class__.__name__}")

# Test the semantic analyzer
if __name__ == "__main__":
    from scanner import Scanner
    from parser import Parser
    
    # Test with correct code
    test_code1 = '''
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
    '''
    
    print("Testing correct code:")
    print("=" * 50)
    
    scanner = Scanner(test_code1)
    tokens = scanner.tokenize()
    
    if tokens:
        parser = Parser(tokens)
        ast = parser.parse()
        
        if ast:
            analyzer = TypeChecker()
            success = analyzer.analyze(ast)
            
            if success:
                print("✓ Semantic analysis passed!")
                print("\nSymbol Table:")
                print(analyzer.symbol_table)
            else:
                print("✗ Semantic analysis failed!")
    
    # Test with errors
    test_code2 = '''
    int a = 10;
    bool b = a + 5;  // Type error: assigning int to bool
    
    if (a) {  // Type error: condition should be boolean
        print(c);  // Error: undefined variable
    }
    
    a = true;  // Type error: assigning bool to int
    '''
    
    print("\n\nTesting code with errors:")
    print("=" * 50)
    
    scanner2 = Scanner(test_code2)
    tokens2 = scanner2.tokenize()
    
    if tokens2:
        parser2 = Parser(tokens2)
        ast2 = parser2.parse()
        
        if ast2:
            analyzer2 = TypeChecker()
            success2 = analyzer2.analyze(ast2)
            
            if not success2:
                print(f"✓ Found {len(analyzer2.errors)} semantic errors as expected!")
            else:
                print("✗ Should have found semantic errors!")