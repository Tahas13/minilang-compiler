"""
Syntax Analyzer (Parser) for MiniLang compiler.
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction

Grammar for MiniLang:
program ::= statement_list
statement_list ::= statement*
statement ::= var_declaration | assignment | print_statement | if_statement | while_statement | block
var_declaration ::= type IDENTIFIER ('=' expression)? ';'
assignment ::= IDENTIFIER '=' expression ';'
print_statement ::= 'print' '(' expression ')' ';'
if_statement ::= 'if' '(' expression ')' statement ('else' statement)?
while_statement ::= 'while' '(' expression ')' statement
block ::= '{' statement_list '}'
expression ::= logical_or
logical_or ::= logical_and ('or' logical_and)*
logical_and ::= equality ('and' equality)*
equality ::= relational (('==' | '!=') relational)*
relational ::= additive (('>' | '<') additive)*
additive ::= multiplicative (('+' | '-') multiplicative)*
multiplicative ::= unary (('*' | '/') unary)*
unary ::= ('not' | '-') unary | primary
primary ::= IDENTIFIER | INTEGER_LITERAL | FLOAT_LITERAL | BOOLEAN_LITERAL | '(' expression ')'
type ::= 'int' | 'float' | 'bool'
"""

from typing import List, Optional
from tokens import Token, TokenType
from ast_nodes import *

class ParseError(Exception):
    """Exception raised for parsing errors."""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Parse Error at line {token.line}, column {token.column}: {message}")

class Parser:
    """Recursive descent parser for MiniLang."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    def current_token(self) -> Token:
        """Get the current token."""
        if self.current >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[self.current]
    
    def peek_token(self, offset: int = 1) -> Token:
        """Peek at a future token."""
        peek_pos = self.current + offset
        if peek_pos >= len(self.tokens):
            return self.tokens[-1]  # EOF token
        return self.tokens[peek_pos]
    
    def advance(self) -> Token:
        """Move to the next token and return the previous one."""
        if self.current < len(self.tokens) - 1:
            self.current += 1
        return self.tokens[self.current - 1]
    
    def check(self, token_type: TokenType) -> bool:
        """Check if current token is of the given type."""
        return self.current_token().type == token_type
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        """Consume a token of the expected type or raise an error."""
        if self.check(token_type):
            return self.advance()
        raise ParseError(message, self.current_token())
    
    def synchronize(self):
        """Recover from parser error by finding the next statement."""
        self.advance()
        while not self.check(TokenType.EOF):
            if self.tokens[self.current - 1].type == TokenType.SEMICOLON:
                return
            if self.current_token().type in [TokenType.IF, TokenType.WHILE, 
                                           TokenType.INT, TokenType.FLOAT, TokenType.BOOL,
                                           TokenType.PRINT]:
                return
            self.advance()
    
    def parse(self) -> Program:
        """Parse the tokens into an AST."""
        try:
            statements = self.parse_program()
            return Program(statements)
        except ParseError as e:
            print(f"Parser Error: {e}")
            return None
    
    def parse_program(self) -> List[Statement]:
        """Parse the entire program."""
        statements = []
        
        while not self.check(TokenType.EOF):
            # Skip newlines
            if self.match(TokenType.NEWLINE):
                continue
            
            try:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            except ParseError as e:
                print(f"Parser Error: {e}")
                self.synchronize()
        
        return statements
    
    def parse_statement(self) -> Statement:
        """Parse a statement."""
        # Variable declaration
        if self.check(TokenType.INT) or self.check(TokenType.FLOAT) or self.check(TokenType.BOOL):
            return self.parse_var_declaration()
        
        # Print statement
        if self.check(TokenType.PRINT):
            return self.parse_print_statement()
        
        # If statement
        if self.check(TokenType.IF):
            return self.parse_if_statement()
        
        # While statement
        if self.check(TokenType.WHILE):
            return self.parse_while_statement()
        
        # Block statement
        if self.check(TokenType.LEFT_BRACE):
            return self.parse_block()
        
        # Assignment statement (must check this after other statements)
        if self.check(TokenType.IDENTIFIER):
            return self.parse_assignment()
        
        raise ParseError(f"Unexpected token: {self.current_token().value}", self.current_token())
    
    def parse_var_declaration(self) -> VarDeclaration:
        """Parse variable declaration: type IDENTIFIER ('=' expression)? ';'"""
        var_type_token = self.advance()  # int, float, or bool
        var_type = var_type_token.value
        
        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        value = None
        if self.match(TokenType.ASSIGN):
            value = self.parse_expression()
        
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        
        return VarDeclaration(var_type, name, value)
    
    def parse_assignment(self) -> Assignment:
        """Parse assignment: IDENTIFIER '=' expression ';'"""
        name_token = self.advance()  # IDENTIFIER
        name = name_token.value
        
        self.consume(TokenType.ASSIGN, "Expected '=' in assignment")
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after assignment")
        
        return Assignment(name, value)
    
    def parse_print_statement(self) -> PrintStatement:
        """Parse print statement: 'print' '(' expression ')' ';'"""
        self.advance()  # consume 'print'
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'print'")
        expression = self.parse_expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
        self.consume(TokenType.SEMICOLON, "Expected ';' after print statement")
        
        return PrintStatement(expression)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse if statement: 'if' '(' expression ')' statement ('else' statement)?"""
        self.advance()  # consume 'if'
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'if'")
        condition = self.parse_expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after if condition")
        
        then_stmt = self.parse_statement()
        then_statements = [then_stmt] if not isinstance(then_stmt, Block) else then_stmt.statements
        
        else_statements = None
        if self.match(TokenType.ELSE):
            else_stmt = self.parse_statement()
            else_statements = [else_stmt] if not isinstance(else_stmt, Block) else else_stmt.statements
        
        return IfStatement(condition, then_statements, else_statements)
    
    def parse_while_statement(self) -> WhileStatement:
        """Parse while statement: 'while' '(' expression ')' statement"""
        self.advance()  # consume 'while'
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'")
        condition = self.parse_expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after while condition")
        
        body_stmt = self.parse_statement()
        body = [body_stmt] if not isinstance(body_stmt, Block) else body_stmt.statements
        
        return WhileStatement(condition, body)
    
    def parse_block(self) -> Block:
        """Parse block: '{' statement_list '}'"""
        self.advance()  # consume '{'
        
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.check(TokenType.EOF):
            if self.match(TokenType.NEWLINE):
                continue
            statements.append(self.parse_statement())
        
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after block")
        return Block(statements)
    
    def parse_expression(self) -> Expression:
        """Parse expression (start with lowest precedence)."""
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> Expression:
        """Parse logical OR: logical_and ('or' logical_and)*"""
        expr = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            operator = 'or'
            right = self.parse_logical_and()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_logical_and(self) -> Expression:
        """Parse logical AND: equality ('and' equality)*"""
        expr = self.parse_equality()
        
        while self.match(TokenType.AND):
            operator = 'and'
            right = self.parse_equality()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_equality(self) -> Expression:
        """Parse equality: relational (('==' | '!=') relational)*"""
        expr = self.parse_relational()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = '==' if self.tokens[self.current - 1].type == TokenType.EQUAL else '!='
            right = self.parse_relational()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_relational(self) -> Expression:
        """Parse relational: additive (('>' | '<' | '>=' | '<=') additive)*"""
        expr = self.parse_additive()
        
        while self.match(TokenType.GREATER_THAN, TokenType.LESS_THAN, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            token_type = self.tokens[self.current - 1].type
            if token_type == TokenType.GREATER_THAN:
                operator = '>'
            elif token_type == TokenType.LESS_THAN:
                operator = '<'
            elif token_type == TokenType.GREATER_EQUAL:
                operator = '>='
            else:  # LESS_EQUAL
                operator = '<='
            right = self.parse_additive()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_additive(self) -> Expression:
        """Parse additive: multiplicative (('+' | '-') multiplicative)*"""
        expr = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = '+' if self.tokens[self.current - 1].type == TokenType.PLUS else '-'
            right = self.parse_multiplicative()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_multiplicative(self) -> Expression:
        """Parse multiplicative: unary (('*' | '/') unary)*"""
        expr = self.parse_unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = '*' if self.tokens[self.current - 1].type == TokenType.MULTIPLY else '/'
            right = self.parse_unary()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def parse_unary(self) -> Expression:
        """Parse unary: ('not' | '-') unary | primary"""
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = 'not' if self.tokens[self.current - 1].type == TokenType.NOT else '-'
            expr = self.parse_unary()
            return UnaryOp(operator, expr)
        
        return self.parse_primary()
    
    def parse_primary(self) -> Expression:
        """Parse primary: IDENTIFIER | INTEGER_LITERAL | FLOAT_LITERAL | BOOLEAN_LITERAL | '(' expression ')'"""
        
        # Boolean literal
        if self.check(TokenType.BOOLEAN_LITERAL):
            value = self.advance().value
            return BooleanLiteral(value)
        
        # Integer literal
        if self.check(TokenType.INTEGER_LITERAL):
            value = self.advance().value
            return IntegerLiteral(value)
        
        # Float literal
        if self.check(TokenType.FLOAT_LITERAL):
            value = self.advance().value
            return FloatLiteral(value)
        
        # Identifier
        if self.check(TokenType.IDENTIFIER):
            name = self.advance().value
            return Identifier(name)
        
        # Parenthesized expression
        if self.match(TokenType.LEFT_PAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return expr
        
        raise ParseError(f"Unexpected token in expression: {self.current_token().value}", 
                        self.current_token())

# Test the parser
if __name__ == "__main__":
    from scanner import Scanner
    
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
    '''
    
    # Tokenize
    scanner = Scanner(test_code)
    tokens = scanner.tokenize()
    
    if tokens:
        # Parse
        parser = Parser(tokens)
        ast = parser.parse()
        
        if ast:
            print("AST Structure:")
            print("=" * 50)
            printer = ASTPrinter()
            printer.visit(ast)