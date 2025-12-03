"""
Token definitions for MiniLang compiler.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional

class TokenType(Enum):
    # Data Types
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    
    # Literals
    INTEGER_LITERAL = auto()
    FLOAT_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Arithmetic Operators
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    
    # Relational Operators
    GREATER_THAN = auto()      # >
    LESS_THAN = auto()         # <
    GREATER_EQUAL = auto()     # >=
    LESS_EQUAL = auto()        # <=
    EQUAL = auto()             # ==
    NOT_EQUAL = auto()         # !=
    
    # Logical Operators
    AND = auto()           # and
    OR = auto()            # or
    NOT = auto()           # not
    
    # Assignment
    ASSIGN = auto()        # =
    
    # Control Flow
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    DO = auto()
    
    # Functions
    FUNCTION = auto()
    RETURN = auto()
    
    # I/O
    PRINT = auto()
    
    # Delimiters
    SEMICOLON = auto()     # ;
    COMMA = auto()         # ,
    LEFT_PAREN = auto()    # (
    RIGHT_PAREN = auto()   # )
    LEFT_BRACE = auto()    # {
    RIGHT_BRACE = auto()   # }
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    COMMENT = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __str__(self):
        return f"Token({self.type.name}, {self.value}, {self.line}:{self.column})"
    
    def __repr__(self):
        return self.__str__()

# Keywords mapping
KEYWORDS = {
    'int': TokenType.INT,
    'float': TokenType.FLOAT,
    'bool': TokenType.BOOL,
    'true': TokenType.BOOLEAN_LITERAL,
    'false': TokenType.BOOLEAN_LITERAL,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'do': TokenType.DO,
    'function': TokenType.FUNCTION,
    'return': TokenType.RETURN,
    'print': TokenType.PRINT,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
}

# Two-character operators
TWO_CHAR_OPERATORS = {
    '==': TokenType.EQUAL,
    '!=': TokenType.NOT_EQUAL,
    '>=': TokenType.GREATER_EQUAL,
    '<=': TokenType.LESS_EQUAL,
}

# Single-character operators and delimiters
SINGLE_CHAR_TOKENS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '>': TokenType.GREATER_THAN,
    '<': TokenType.LESS_THAN,
    '=': TokenType.ASSIGN,
    ';': TokenType.SEMICOLON,
    ',': TokenType.COMMA,
    '(': TokenType.LEFT_PAREN,
    ')': TokenType.RIGHT_PAREN,
    '{': TokenType.LEFT_BRACE,
    '}': TokenType.RIGHT_BRACE,
}