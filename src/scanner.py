"""
Lexical Analyzer (Scanner) for MiniLang compiler.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction
"""

import re
from typing import List, Optional
from tokens import Token, TokenType, KEYWORDS, TWO_CHAR_OPERATORS, SINGLE_CHAR_TOKENS

class LexicalError(Exception):
    """Exception raised for lexical analysis errors."""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexical Error at line {line}, column {column}: {message}")

class Scanner:
    """Lexical analyzer for MiniLang."""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.errors = []  # Track lexical errors
        
    def current_char(self) -> Optional[str]:
        """Returns the current character or None if at end of input."""
        if self.position >= len(self.source_code):
            return None
        return self.source_code[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at the character at current position + offset."""
        peek_pos = self.position + offset
        if peek_pos >= len(self.source_code):
            return None
        return self.source_code[peek_pos]
    
    def advance(self) -> None:
        """Move to the next character."""
        if self.position < len(self.source_code):
            if self.source_code[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters except newlines."""
        while self.current_char() is not None and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self) -> None:
        """Skip single-line comments starting with //."""
        if self.current_char() == '/' and self.peek_char() == '/':
            # Skip until end of line
            while self.current_char() is not None and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """Read numeric literals (integers and floats)."""
        start_line = self.line
        start_column = self.column
        number_str = ""
        is_float = False
        
        while (self.current_char() is not None and 
               (self.current_char().isdigit() or self.current_char() == '.')):
            if self.current_char() == '.':
                if is_float:
                    # Second decimal point - error
                    raise LexicalError("Invalid number format: multiple decimal points", 
                                     start_line, start_column)
                is_float = True
            number_str += self.current_char()
            self.advance()
        
        if number_str.endswith('.'):
            raise LexicalError("Invalid number format: number cannot end with decimal point", 
                             start_line, start_column)
        
        try:
            if is_float:
                value = float(number_str)
                return Token(TokenType.FLOAT_LITERAL, value, start_line, start_column)
            else:
                value = int(number_str)
                return Token(TokenType.INTEGER_LITERAL, value, start_line, start_column)
        except ValueError:
            raise LexicalError(f"Invalid number format: {number_str}", start_line, start_column)
    
    def read_identifier(self) -> Token:
        """Read identifiers and keywords."""
        start_line = self.line
        start_column = self.column
        identifier = ""
        
        # First character must be letter or underscore
        if not (self.current_char().isalpha() or self.current_char() == '_'):
            raise LexicalError("Invalid identifier: must start with letter or underscore", 
                             start_line, start_column)
        
        while (self.current_char() is not None and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            identifier += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        
        # Special handling for boolean literals
        if identifier in ['true', 'false']:
            value = identifier == 'true'
            return Token(TokenType.BOOLEAN_LITERAL, value, start_line, start_column)
        else:
            return Token(token_type, identifier, start_line, start_column)
    
    def read_operator(self) -> Token:
        """Read operators (single and double character)."""
        start_line = self.line
        start_column = self.column
        
        current = self.current_char()
        next_char = self.peek_char()
        
        # Check for two-character operators
        two_char = current + (next_char or '')
        if two_char in TWO_CHAR_OPERATORS:
            self.advance()  # First character
            self.advance()  # Second character
            return Token(TWO_CHAR_OPERATORS[two_char], two_char, start_line, start_column)
        
        # Single character operators
        if current in SINGLE_CHAR_TOKENS:
            self.advance()
            return Token(SINGLE_CHAR_TOKENS[current], current, start_line, start_column)
        
        raise LexicalError(f"Unknown operator: {current}", start_line, start_column)
    
    def get_next_token(self) -> Token:
        """Get the next token from the input."""
        while self.current_char() is not None:
            # Skip whitespace
            if self.current_char() in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Handle newlines
            if self.current_char() == '\n':
                token = Token(TokenType.NEWLINE, '\\n', self.line, self.column)
                self.advance()
                return token
            
            # Handle comments
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            # Handle numbers
            if self.current_char().isdigit():
                return self.read_number()
            
            # Handle identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                return self.read_identifier()
            
            # Handle operators and delimiters
            if (self.current_char() in SINGLE_CHAR_TOKENS or 
                (self.current_char() + (self.peek_char() or '')) in TWO_CHAR_OPERATORS):
                return self.read_operator()
            
            # Unknown character
            raise LexicalError(f"Unexpected character: '{self.current_char()}'", 
                             self.line, self.column)
        
        # End of file
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code."""
        self.tokens = []
        self.errors = []  # Reset errors
        
        try:
            while True:
                token = self.get_next_token()
                self.tokens.append(token)
                if token.type == TokenType.EOF:
                    break
            
            return self.tokens
        
        except LexicalError as e:
            self.errors.append(str(e))
            print(f"Lexical Analysis Error: {e}")
            return []
    
    def print_tokens(self) -> None:
        """Print all tokens for debugging."""
        for token in self.tokens:
            print(token)

# Example usage and test
if __name__ == "__main__":
    # Test with the example MiniLang code from the proposal
    test_code = '''
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
    
    // This is a comment
    float pi = 3.14;
    '''
    
    scanner = Scanner(test_code)
    tokens = scanner.tokenize()
    
    print("Tokens generated:")
    print("=" * 50)
    scanner.print_tokens()