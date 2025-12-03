"""
Symbol Table for MiniLang compiler.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class Symbol:
    """Represents a symbol in the symbol table."""
    name: str
    type: str  # 'int', 'float', 'bool'
    value: Optional[Any] = None
    line: int = 0
    column: int = 0
    initialized: bool = False

class SymbolTable:
    """Symbol table for tracking variable declarations and their types."""
    
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.parent: Optional['SymbolTable'] = None
    
    def define(self, name: str, symbol_type: str, line: int = 0, column: int = 0, value: Any = None) -> bool:
        """Define a new symbol. Returns False if already defined in this scope."""
        if name in self.symbols:
            return False
        
        self.symbols[name] = Symbol(
            name=name,
            type=symbol_type,
            value=value,
            line=line,
            column=column,
            initialized=(value is not None)
        )
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in this scope or parent scopes."""
        if name in self.symbols:
            return self.symbols[name]
        
        if self.parent is not None:
            return self.parent.lookup(name)
        
        return None
    
    def assign(self, name: str, value: Any) -> bool:
        """Assign a value to an existing symbol. Returns False if not found."""
        symbol = self.lookup(name)
        if symbol is None:
            return False
        
        symbol.value = value
        symbol.initialized = True
        return True
    
    def is_defined(self, name: str) -> bool:
        """Check if a symbol is defined in this scope or parent scopes."""
        return self.lookup(name) is not None
    
    def is_initialized(self, name: str) -> bool:
        """Check if a symbol is initialized."""
        symbol = self.lookup(name)
        return symbol is not None and symbol.initialized
    
    def get_type(self, name: str) -> Optional[str]:
        """Get the type of a symbol."""
        symbol = self.lookup(name)
        return symbol.type if symbol else None
    
    def create_child_scope(self) -> 'SymbolTable':
        """Create a child scope (for blocks, functions, etc.)."""
        child = SymbolTable()
        child.parent = self
        return child
    
    def __str__(self) -> str:
        """String representation of the symbol table."""
        result = "Symbol Table:\n"
        result += "-" * 40 + "\n"
        for name, symbol in self.symbols.items():
            result += f"{name}: {symbol.type}"
            if symbol.initialized:
                result += f" = {symbol.value}"
            result += f" (line {symbol.line})\n"
        return result