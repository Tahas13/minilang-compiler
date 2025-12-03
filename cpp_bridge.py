"""
C++ Compiler Bridge for MiniLang
Authors: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction

This module bridges the Python web interface with the C++ compiler core.
Falls back to Python implementation if C++ executable is not available.
"""

import subprocess
import json
import os
from pathlib import Path
import tempfile

class CPPCompilerBridge:
    """Bridge to use C++ compiler core from Python."""
    
    def __init__(self):
        self.cpp_executable = Path(__file__).parent / "cpp_core" / "minilang_compiler.exe"
        self.cpp_available = self.cpp_executable.exists()
        
        if not self.cpp_available:
            print(f"⚠️  C++ compiler not found at {self.cpp_executable}")
            print("📝 Falling back to Python implementation")
            print("💡 To use C++ core, compile it with: g++ -std=c++17 -O2 -o cpp_core/minilang_compiler.exe cpp_core/main.cpp")
    
    def compile(self, source_code):
        """
        Compile source code using C++ compiler.
        Returns dict with compilation results.
        """
        if not self.cpp_available:
            # Fallback to Python implementation
            from compiler import MiniLangCompiler
            py_compiler = MiniLangCompiler()
            return py_compiler.compile(source_code)
        
        try:
            # Create temporary file for source code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ml', delete=False) as f:
                f.write(source_code)
                temp_file = f.name
            
            # Run C++ compiler
            result = subprocess.run(
                [str(self.cpp_executable), temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Clean up temp file
            os.unlink(temp_file)
            
            # Parse JSON output
            if result.stdout:
                cpp_result = json.loads(result.stdout)
                return self._convert_cpp_result(cpp_result)
            else:
                return {
                    "success": False,
                    "errors": [f"C++ compiler error: {result.stderr}"],
                    "tokens": [],
                    "ast": None,
                    "symbol_table": None
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "errors": ["Compilation timeout"],
                "tokens": [],
                "ast": None,
                "symbol_table": None
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "errors": [f"Failed to parse C++ output: {str(e)}"],
                "tokens": [],
                "ast": None,
                "symbol_table": None
            }
        except Exception as e:
            return {
                "success": False,
                "errors": [f"Unexpected error: {str(e)}"],
                "tokens": [],
                "ast": None,
                "symbol_table": None
            }
    
    def _convert_cpp_result(self, cpp_result):
        """Convert C++ JSON result to Python format."""
        return {
            "success": cpp_result.get("success", False),
            "errors": cpp_result.get("errors", []),
            "tokens": cpp_result.get("tokens", []),
            "ast": cpp_result.get("ast"),
            "symbol_table": cpp_result.get("symbol_table")
        }
    
    def is_cpp_available(self):
        """Check if C++ compiler is available."""
        return self.cpp_available
