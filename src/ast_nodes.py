"""
Abstract Syntax Tree (AST) node definitions for MiniLang compiler.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional
from dataclasses import dataclass

class ASTNode(ABC):
    """Base class for all AST nodes."""
    pass

class Statement(ASTNode):
    """Base class for all statement nodes."""
    pass

class Expression(ASTNode):
    """Base class for all expression nodes."""
    pass

@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    statements: List[Statement]

@dataclass
class VarDeclaration(Statement):
    """Variable declaration statement."""
    var_type: str  # 'int', 'float', 'bool'
    name: str
    value: Optional[Expression] = None

@dataclass
class Assignment(Statement):
    """Assignment statement."""
    name: str
    value: Expression

@dataclass
class PrintStatement(Statement):
    """Print statement."""
    expression: Expression

@dataclass
class IfStatement(Statement):
    """If statement with optional else clause."""
    condition: Expression
    then_statements: List[Statement]
    else_statements: Optional[List[Statement]] = None

@dataclass
class WhileStatement(Statement):
    """While loop statement."""
    condition: Expression
    body: List[Statement]

@dataclass
class Block(Statement):
    """Block statement (group of statements in braces)."""
    statements: List[Statement]

# Expression nodes

@dataclass
class BinaryOp(Expression):
    """Binary operation expression."""
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryOp(Expression):
    """Unary operation expression."""
    operator: str
    operand: Expression

@dataclass
class Identifier(Expression):
    """Identifier (variable reference)."""
    name: str

@dataclass
class IntegerLiteral(Expression):
    """Integer literal."""
    value: int

@dataclass
class FloatLiteral(Expression):
    """Float literal."""
    value: float

@dataclass
class BooleanLiteral(Expression):
    """Boolean literal."""
    value: bool

# Visitor pattern for AST traversal
class ASTVisitor(ABC):
    """Base class for AST visitors."""
    
    @abstractmethod
    def visit_program(self, node: Program):
        pass
    
    @abstractmethod
    def visit_var_declaration(self, node: VarDeclaration):
        pass
    
    @abstractmethod
    def visit_assignment(self, node: Assignment):
        pass
    
    @abstractmethod
    def visit_print_statement(self, node: PrintStatement):
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: IfStatement):
        pass
    
    @abstractmethod
    def visit_while_statement(self, node: WhileStatement):
        pass
    
    @abstractmethod
    def visit_block(self, node: Block):
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: BinaryOp):
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: UnaryOp):
        pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier):
        pass
    
    @abstractmethod
    def visit_integer_literal(self, node: IntegerLiteral):
        pass
    
    @abstractmethod
    def visit_float_literal(self, node: FloatLiteral):
        pass
    
    @abstractmethod
    def visit_boolean_literal(self, node: BooleanLiteral):
        pass

class ASTPrinter(ASTVisitor):
    """Visitor that prints the AST structure."""
    
    def __init__(self):
        self.indent_level = 0
    
    def _indent(self):
        return "  " * self.indent_level
    
    def visit_program(self, node: Program):
        print(f"{self._indent()}Program:")
        self.indent_level += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent_level -= 1
    
    def visit_var_declaration(self, node: VarDeclaration):
        print(f"{self._indent()}VarDeclaration: {node.var_type} {node.name}")
        if node.value:
            self.indent_level += 1
            print(f"{self._indent()}Value:")
            self.indent_level += 1
            self.visit(node.value)
            self.indent_level -= 2
    
    def visit_assignment(self, node: Assignment):
        print(f"{self._indent()}Assignment: {node.name}")
        self.indent_level += 1
        print(f"{self._indent()}Value:")
        self.indent_level += 1
        self.visit(node.value)
        self.indent_level -= 2
    
    def visit_print_statement(self, node: PrintStatement):
        print(f"{self._indent()}PrintStatement:")
        self.indent_level += 1
        self.visit(node.expression)
        self.indent_level -= 1
    
    def visit_if_statement(self, node: IfStatement):
        print(f"{self._indent()}IfStatement:")
        self.indent_level += 1
        print(f"{self._indent()}Condition:")
        self.indent_level += 1
        self.visit(node.condition)
        self.indent_level -= 1
        print(f"{self._indent()}Then:")
        self.indent_level += 1
        for stmt in node.then_statements:
            self.visit(stmt)
        self.indent_level -= 1
        if node.else_statements:
            print(f"{self._indent()}Else:")
            self.indent_level += 1
            for stmt in node.else_statements:
                self.visit(stmt)
            self.indent_level -= 1
        self.indent_level -= 1
    
    def visit_while_statement(self, node: WhileStatement):
        print(f"{self._indent()}WhileStatement:")
        self.indent_level += 1
        print(f"{self._indent()}Condition:")
        self.indent_level += 1
        self.visit(node.condition)
        self.indent_level -= 1
        print(f"{self._indent()}Body:")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 2
    
    def visit_block(self, node: Block):
        print(f"{self._indent()}Block:")
        self.indent_level += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent_level -= 1
    
    def visit_binary_op(self, node: BinaryOp):
        print(f"{self._indent()}BinaryOp: {node.operator}")
        self.indent_level += 1
        print(f"{self._indent()}Left:")
        self.indent_level += 1
        self.visit(node.left)
        self.indent_level -= 1
        print(f"{self._indent()}Right:")
        self.indent_level += 1
        self.visit(node.right)
        self.indent_level -= 2
    
    def visit_unary_op(self, node: UnaryOp):
        print(f"{self._indent()}UnaryOp: {node.operator}")
        self.indent_level += 1
        self.visit(node.operand)
        self.indent_level -= 1
    
    def visit_identifier(self, node: Identifier):
        print(f"{self._indent()}Identifier: {node.name}")
    
    def visit_integer_literal(self, node: IntegerLiteral):
        print(f"{self._indent()}IntegerLiteral: {node.value}")
    
    def visit_float_literal(self, node: FloatLiteral):
        print(f"{self._indent()}FloatLiteral: {node.value}")
    
    def visit_boolean_literal(self, node: BooleanLiteral):
        print(f"{self._indent()}BooleanLiteral: {node.value}")
    
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