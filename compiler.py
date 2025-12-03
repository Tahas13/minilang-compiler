"""
Main MiniLang Compiler Driver
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

import sys
import os
from pathlib import Path

# Add src directory to path to import our modules
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from scanner import Scanner, LexicalError
from parser import Parser, ParseError
from semantic_analyzer import TypeChecker, SemanticError
from ast_nodes import ASTPrinter
from ast_visualizer import print_ast_tree
from clean_vertical_ast import print_clean_vertical_ast

class MiniLangCompiler:
    """Main compiler class that coordinates all compilation phases."""
    
    def __init__(self):
        self.source_code = ""
        self.tokens = []
        self.ast = None
        self.symbol_table = None
        self.errors = []
    
    def compile_file(self, filename: str, verbose: bool = False) -> bool:
        """Compile a MiniLang source file."""
        print(f"Compiling {filename}...")
        print("=" * 60)
        
        # Read source file
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.source_code = file.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
        
        if verbose:
            print("Source Code:")
            print("-" * 40)
            print(self.source_code)
            print()
        
        # Phase 1: Lexical Analysis
        print("Phase 1: Lexical Analysis")
        print("-" * 30)
        
        scanner = Scanner(self.source_code)
        self.tokens = scanner.tokenize()
        
        if not self.tokens:
            print("✗ Lexical analysis failed!")
            return False
        
        print("✓ Lexical analysis completed successfully!")
        print(f"Generated {len(self.tokens)} tokens.")
        
        if verbose:
            print("\\nTokens:")
            for i, token in enumerate(self.tokens):
                print(f"{i+1:3d}: {token}")
        
        print()
        
        # Phase 2: Syntax Analysis
        print("Phase 2: Syntax Analysis")
        print("-" * 30)
        
        parser = Parser(self.tokens)
        self.ast = parser.parse()
        
        if self.ast is None:
            print("✗ Syntax analysis failed!")
            return False
        
        print("✓ Syntax analysis completed successfully!")
        print("AST generated.")
        
        if verbose:
            print("\\nAbstract Syntax Tree:")
            print_clean_vertical_ast(self.ast, "simple")
        
        print()
        
        # Phase 3: Semantic Analysis
        print("Phase 3: Semantic Analysis")
        print("-" * 30)
        
        type_checker = TypeChecker()
        success = type_checker.analyze(self.ast)
        
        if not success:
            print(f"✗ Semantic analysis failed!")
            print(f"Found {len(type_checker.errors)} semantic errors.")
            for error in type_checker.errors:
                print(f"  - {error}")
            return False
        
        print("✓ Semantic analysis completed successfully!")
        print("No semantic errors found.")
        self.symbol_table = type_checker.symbol_table
        
        if verbose:
            print(f"\\n{self.symbol_table}")
        
        print()
        print("✓ Compilation completed successfully!")
        print("=" * 60)
        return True
    
    def compile_string(self, source: str, verbose: bool = False) -> bool:
        """Compile MiniLang source code from a string."""
        print("Compiling source code...")
        print("=" * 60)
        
        self.source_code = source
        
        if verbose:
            print("Source Code:")
            print("-" * 40)
            print(self.source_code)
            print()
        
        # Phase 1: Lexical Analysis
        print("Phase 1: Lexical Analysis")
        print("-" * 30)
        
        scanner = Scanner(self.source_code)
        self.tokens = scanner.tokenize()
        
        if not self.tokens:
            print("✗ Lexical analysis failed!")
            return False
        
        print("✓ Lexical analysis completed successfully!")
        print(f"Generated {len(self.tokens)} tokens.")
        print()
        
        # Phase 2: Syntax Analysis
        print("Phase 2: Syntax Analysis")
        print("-" * 30)
        
        parser = Parser(self.tokens)
        self.ast = parser.parse()
        
        if self.ast is None:
            print("✗ Syntax analysis failed!")
            return False
        
        print("✓ Syntax analysis completed successfully!")
        print("AST generated.")
        print()
        
        # Phase 3: Semantic Analysis
        print("Phase 3: Semantic Analysis")
        print("-" * 30)
        
        type_checker = TypeChecker()
        success = type_checker.analyze(self.ast)
        
        if not success:
            print(f"✗ Semantic analysis failed!")
            print(f"Found {len(type_checker.errors)} semantic errors.")
            for error in type_checker.errors:
                print(f"  - {error}")
            return False
        
        print("✓ Semantic analysis completed successfully!")
        print("No semantic errors found.")
        self.symbol_table = type_checker.symbol_table
        
        print()
        print("✓ Compilation completed successfully!")
        print("=" * 60)
        return True

def print_usage():
    """Print usage information."""
    print("MiniLang Compiler")
    print("Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)")
    print("Course: CS-4031 - Compiler Construction")
    print()
    print("Usage:")
    print("  python compiler.py <file.ml> [options]")
    print()
    print("Options:")
    print("  -v, --verbose    Enable verbose output")
    print("  -h, --help       Show this help message")
    print()
    print("Examples:")
    print("  python compiler.py examples/example1_basics.ml")
    print("  python compiler.py examples/example1_basics.ml -v")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print_usage()
        return
    
    if sys.argv[1] in ['-h', '--help']:
        print_usage()
        return
    
    filename = sys.argv[1]
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    
    # Check if file exists and has correct extension
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return
    
    if not filename.endswith('.ml'):
        print("Warning: MiniLang files should have .ml extension.")
    
    # Compile the file
    compiler = MiniLangCompiler()
    success = compiler.compile_file(filename, verbose)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()