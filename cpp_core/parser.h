/*
 * MiniLang Compiler - Parser (Syntax Analyzer)
 * Authors: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
 * Course: CS-4031 - Compiler Construction
 */

#ifndef PARSER_H
#define PARSER_H

#include "token.h"
#include "ast.h"
#include <vector>
#include <memory>
#include <stdexcept>

class Parser {
private:
    std::vector<Token> tokens;
    size_t position;
    std::vector<std::string> errors;
    
    Token& currentToken() {
        if (position >= tokens.size()) {
            return tokens.back(); // Return EOF
        }
        return tokens[position];
    }
    
    Token& peekToken(int offset = 1) {
        if (position + offset >= tokens.size()) {
            return tokens.back();
        }
        return tokens[position + offset];
    }
    
    void advance() {
        if (position < tokens.size() - 1) {
            position++;
        }
    }
    
    bool match(TokenType type) {
        return currentToken().type == type;
    }
    
    void expect(TokenType type, const std::string& message) {
        if (!match(type)) {
            errors.push_back("Line " + std::to_string(currentToken().line) + ": " + message);
            throw std::runtime_error(message);
        }
        advance();
    }
    
    // Parse program
    std::unique_ptr<Program> parseProgram() {
        auto program = std::make_unique<Program>();
        
        while (!match(TokenType::END_OF_FILE)) {
            try {
                auto stmt = parseStatement();
                if (stmt) {
                    program->statements.push_back(std::move(stmt));
                }
            } catch (const std::exception& e) {
                // Skip to next statement on error
                while (!match(TokenType::SEMICOLON) && !match(TokenType::END_OF_FILE)) {
                    advance();
                }
                if (match(TokenType::SEMICOLON)) advance();
            }
        }
        
        return program;
    }
    
    // Parse statement
    std::unique_ptr<ASTNode> parseStatement() {
        // Function declaration
        if (match(TokenType::FUNCTION)) {
            return parseFunctionDeclaration();
        }
        
        // Variable declaration
        if (match(TokenType::INT) || match(TokenType::FLOAT_TYPE) || match(TokenType::BOOL)) {
            return parseVarDeclaration();
        }
        
        // Return statement
        if (match(TokenType::RETURN)) {
            return parseReturnStatement();
        }
        
        // Print statement
        if (match(TokenType::PRINT)) {
            return parsePrintStatement();
        }
        
        // If statement
        if (match(TokenType::IF)) {
            return parseIfStatement();
        }
        
        // While statement
        if (match(TokenType::WHILE)) {
            return parseWhileStatement();
        }
        
        // For statement
        if (match(TokenType::FOR)) {
            return parseForStatement();
        }
        
        // Do-While statement
        if (match(TokenType::DO)) {
            return parseDoWhileStatement();
        }
        
        // Assignment or function call
        if (match(TokenType::IDENTIFIER)) {
            // Look ahead to determine if it's assignment or function call
            if (peekToken().type == TokenType::LPAREN) {
                return parseFunctionCallStatement();
            }
            return parseAssignment();
        }
        
        errors.push_back("Line " + std::to_string(currentToken().line) + 
                        ": Unexpected token: " + currentToken().value);
        throw std::runtime_error("Unexpected token");
    }
    
    // Parse variable declaration
    std::unique_ptr<ASTNode> parseVarDeclaration() {
        std::string type = currentToken().value;
        advance();
        
        expect(TokenType::IDENTIFIER, "Expected identifier after type");
        std::string name = tokens[position - 1].value;
        
        std::unique_ptr<ASTNode> value = nullptr;
        if (match(TokenType::ASSIGN)) {
            advance();
            value = parseExpression();
        }
        
        expect(TokenType::SEMICOLON, "Expected ';' after variable declaration");
        
        return std::make_unique<VarDeclaration>(type, name, std::move(value));
    }
    
    // Parse assignment
    std::unique_ptr<ASTNode> parseAssignment() {
        std::string name = currentToken().value;
        advance();
        
        expect(TokenType::ASSIGN, "Expected '=' in assignment");
        auto value = parseExpression();
        expect(TokenType::SEMICOLON, "Expected ';' after assignment");
        
        return std::make_unique<Assignment>(name, std::move(value));
    }
    
    // Parse print statement
    std::unique_ptr<ASTNode> parsePrintStatement() {
        advance(); // consume 'print'
        expect(TokenType::LPAREN, "Expected '(' after 'print'");
        auto expr = parseExpression();
        expect(TokenType::RPAREN, "Expected ')' after expression");
        expect(TokenType::SEMICOLON, "Expected ';' after print statement");
        
        return std::make_unique<PrintStatement>(std::move(expr));
    }
    
    // Parse if statement
    std::unique_ptr<ASTNode> parseIfStatement() {
        advance(); // consume 'if'
        expect(TokenType::LPAREN, "Expected '(' after 'if'");
        auto condition = parseExpression();
        expect(TokenType::RPAREN, "Expected ')' after condition");
        
        auto ifStmt = std::make_unique<IfStatement>(std::move(condition));
        
        // Parse then block
        expect(TokenType::LBRACE, "Expected '{' after if condition");
        while (!match(TokenType::RBRACE) && !match(TokenType::END_OF_FILE)) {
            auto stmt = parseStatement();
            if (stmt) {
                ifStmt->thenStatements.push_back(std::move(stmt));
            }
        }
        expect(TokenType::RBRACE, "Expected '}' after if body");
        
        // Parse else block (optional)
        if (match(TokenType::ELSE)) {
            advance();
            expect(TokenType::LBRACE, "Expected '{' after 'else'");
            while (!match(TokenType::RBRACE) && !match(TokenType::END_OF_FILE)) {
                auto stmt = parseStatement();
                if (stmt) {
                    ifStmt->elseStatements.push_back(std::move(stmt));
                }
            }
            expect(TokenType::RBRACE, "Expected '}' after else body");
        }
        
        return ifStmt;
    }
    
    // Parse while statement
    std::unique_ptr<ASTNode> parseWhileStatement() {
        advance(); // consume 'while'
        expect(TokenType::LPAREN, "Expected '(' after 'while'");
        auto condition = parseExpression();
        expect(TokenType::RPAREN, "Expected ')' after condition");
        
        auto whileStmt = std::make_unique<WhileStatement>(std::move(condition));
        
        expect(TokenType::LBRACE, "Expected '{' after while condition");
        while (!match(TokenType::RBRACE) && !match(TokenType::END_OF_FILE)) {
            auto stmt = parseStatement();
            if (stmt) {
                whileStmt->body.push_back(std::move(stmt));
            }
        }
        expect(TokenType::RBRACE, "Expected '}' after while body");
        
        return whileStmt;
    }
    
    // Parse for statement
    std::unique_ptr<ASTNode> parseForStatement() {
        advance(); // consume 'for'
        expect(TokenType::LPAREN, "Expected '(' after 'for'");
        
        // Parse init (variable declaration or assignment)
        std::unique_ptr<ASTNode> init = nullptr;
        if (match(TokenType::INT) || match(TokenType::FLOAT_TYPE) || match(TokenType::BOOL)) {
            // Parse variable declaration without expecting semicolon
            std::string type = currentToken().value;
            advance();
            
            expect(TokenType::IDENTIFIER, "Expected identifier after type");
            std::string name = tokens[position - 1].value;
            
            std::unique_ptr<ASTNode> value = nullptr;
            if (match(TokenType::ASSIGN)) {
                advance();
                value = parseExpression();
            }
            
            init = std::make_unique<VarDeclaration>(type, name, std::move(value));
        } else if (match(TokenType::IDENTIFIER)) {
            // Parse assignment without expecting semicolon
            std::string name = currentToken().value;
            advance();
            
            expect(TokenType::ASSIGN, "Expected '=' in assignment");
            auto value = parseExpression();
            init = std::make_unique<Assignment>(name, std::move(value));
        }
        
        // Expect semicolon after init
        expect(TokenType::SEMICOLON, "Expected ';' after for loop init");
        
        // Parse condition
        std::unique_ptr<ASTNode> condition = nullptr;
        if (!match(TokenType::SEMICOLON)) {
            condition = parseExpression();
        }
        expect(TokenType::SEMICOLON, "Expected ';' after for loop condition");
        
        // Parse update
        std::unique_ptr<ASTNode> update = nullptr;
        if (!match(TokenType::RPAREN)) {
            if (match(TokenType::IDENTIFIER)) {
                std::string name = currentToken().value;
                advance();
                expect(TokenType::ASSIGN, "Expected '=' in for loop update");
                auto value = parseExpression();
                update = std::make_unique<Assignment>(name, std::move(value));
            }
        }
        expect(TokenType::RPAREN, "Expected ')' after for loop header");
        
        auto forStmt = std::make_unique<ForStatement>(std::move(init), std::move(condition), std::move(update));
        
        expect(TokenType::LBRACE, "Expected '{' after for loop header");
        while (!match(TokenType::RBRACE) && !match(TokenType::END_OF_FILE)) {
            auto stmt = parseStatement();
            if (stmt) {
                forStmt->body.push_back(std::move(stmt));
            }
        }
        expect(TokenType::RBRACE, "Expected '}' after for loop body");
        
        return forStmt;
    }
    
    // Parse do-while statement
    std::unique_ptr<ASTNode> parseDoWhileStatement() {
        advance(); // consume 'do'
        
        auto doWhileStmt = std::make_unique<DoWhileStatement>(nullptr);
        
        expect(TokenType::LBRACE, "Expected '{' after 'do'");
        while (!match(TokenType::RBRACE) && !match(TokenType::END_OF_FILE)) {
            auto stmt = parseStatement();
            if (stmt) {
                doWhileStmt->body.push_back(std::move(stmt));
            }
        }
        expect(TokenType::RBRACE, "Expected '}' after do body");
        
        expect(TokenType::WHILE, "Expected 'while' after do body");
        expect(TokenType::LPAREN, "Expected '(' after 'while'");
        doWhileStmt->condition = parseExpression();
        expect(TokenType::RPAREN, "Expected ')' after condition");
        expect(TokenType::SEMICOLON, "Expected ';' after do-while statement");
        
        return doWhileStmt;
    }
    
    // Parse function declaration
    std::unique_ptr<ASTNode> parseFunctionDeclaration() {
        advance(); // consume 'function'
        
        // Parse return type
        if (!match(TokenType::INT) && !match(TokenType::FLOAT_TYPE) && !match(TokenType::BOOL)) {
            errors.push_back("Expected return type after 'function'");
            throw std::runtime_error("Expected return type");
        }
        std::string returnType = currentToken().value;
        advance();
        
        // Parse function name
        expect(TokenType::IDENTIFIER, "Expected function name");
        std::string name = tokens[position - 1].value;
        
        auto funcDecl = std::make_unique<FunctionDeclaration>(returnType, name);
        
        // Parse parameters
        expect(TokenType::LPAREN, "Expected '(' after function name");
        while (!match(TokenType::RPAREN) && !match(TokenType::END_OF_FILE)) {
            if (!match(TokenType::INT) && !match(TokenType::FLOAT_TYPE) && !match(TokenType::BOOL)) {
                errors.push_back("Expected parameter type");
                throw std::runtime_error("Expected parameter type");
            }
            std::string paramType = currentToken().value;
            advance();
            
            expect(TokenType::IDENTIFIER, "Expected parameter name");
            std::string paramName = tokens[position - 1].value;
            
            funcDecl->parameters.push_back({paramType, paramName});
            
            if (match(TokenType::COMMA)) {
                advance();
            } else {
                break;
            }
        }
        expect(TokenType::RPAREN, "Expected ')' after parameters");
        
        // Parse function body
        expect(TokenType::LBRACE, "Expected '{' after function header");
        while (!match(TokenType::RBRACE) && !match(TokenType::END_OF_FILE)) {
            auto stmt = parseStatement();
            if (stmt) {
                funcDecl->body.push_back(std::move(stmt));
            }
        }
        expect(TokenType::RBRACE, "Expected '}' after function body");
        
        return funcDecl;
    }
    
    // Parse return statement
    std::unique_ptr<ASTNode> parseReturnStatement() {
        advance(); // consume 'return'
        
        std::unique_ptr<ASTNode> value = nullptr;
        if (!match(TokenType::SEMICOLON)) {
            value = parseExpression();
        }
        
        expect(TokenType::SEMICOLON, "Expected ';' after return statement");
        return std::make_unique<ReturnStatement>(std::move(value));
    }
    
    // Parse function call as statement
    std::unique_ptr<ASTNode> parseFunctionCallStatement() {
        std::string name = currentToken().value;
        advance();
        
        auto funcCall = std::make_unique<FunctionCall>(name);
        
        expect(TokenType::LPAREN, "Expected '(' after function name");
        while (!match(TokenType::RPAREN) && !match(TokenType::END_OF_FILE)) {
            funcCall->arguments.push_back(parseExpression());
            if (match(TokenType::COMMA)) {
                advance();
            } else {
                break;
            }
        }
        expect(TokenType::RPAREN, "Expected ')' after arguments");
        expect(TokenType::SEMICOLON, "Expected ';' after function call");
        
        return funcCall;
    }
    
    // Parse expression (lowest precedence: or)
    std::unique_ptr<ASTNode> parseExpression() {
        return parseOrExpression();
    }
    
    std::unique_ptr<ASTNode> parseOrExpression() {
        auto left = parseAndExpression();
        
        while (match(TokenType::OR)) {
            std::string op = currentToken().value;
            advance();
            auto right = parseAndExpression();
            left = std::make_unique<BinaryOp>(std::move(left), op, std::move(right));
        }
        
        return left;
    }
    
    std::unique_ptr<ASTNode> parseAndExpression() {
        auto left = parseEqualityExpression();
        
        while (match(TokenType::AND)) {
            std::string op = currentToken().value;
            advance();
            auto right = parseEqualityExpression();
            left = std::make_unique<BinaryOp>(std::move(left), op, std::move(right));
        }
        
        return left;
    }
    
    std::unique_ptr<ASTNode> parseEqualityExpression() {
        auto left = parseRelationalExpression();
        
        while (match(TokenType::EQUAL) || match(TokenType::NOT_EQUAL)) {
            std::string op = currentToken().value;
            advance();
            auto right = parseRelationalExpression();
            left = std::make_unique<BinaryOp>(std::move(left), op, std::move(right));
        }
        
        return left;
    }
    
    std::unique_ptr<ASTNode> parseRelationalExpression() {
        auto left = parseAdditiveExpression();
        
        while (match(TokenType::LESS_THAN) || match(TokenType::GREATER_THAN) ||
               match(TokenType::LESS_EQUAL) || match(TokenType::GREATER_EQUAL)) {
            std::string op = currentToken().value;
            advance();
            auto right = parseAdditiveExpression();
            left = std::make_unique<BinaryOp>(std::move(left), op, std::move(right));
        }
        
        return left;
    }
    
    std::unique_ptr<ASTNode> parseAdditiveExpression() {
        auto left = parseMultiplicativeExpression();
        
        while (match(TokenType::PLUS) || match(TokenType::MINUS)) {
            std::string op = currentToken().value;
            advance();
            auto right = parseMultiplicativeExpression();
            left = std::make_unique<BinaryOp>(std::move(left), op, std::move(right));
        }
        
        return left;
    }
    
    std::unique_ptr<ASTNode> parseMultiplicativeExpression() {
        auto left = parseUnaryExpression();
        
        while (match(TokenType::MULTIPLY) || match(TokenType::DIVIDE)) {
            std::string op = currentToken().value;
            advance();
            auto right = parseUnaryExpression();
            left = std::make_unique<BinaryOp>(std::move(left), op, std::move(right));
        }
        
        return left;
    }
    
    std::unique_ptr<ASTNode> parseUnaryExpression() {
        if (match(TokenType::NOT) || match(TokenType::MINUS)) {
            std::string op = currentToken().value;
            advance();
            auto operand = parseUnaryExpression();
            return std::make_unique<UnaryOp>(op, std::move(operand));
        }
        
        return parsePrimaryExpression();
    }
    
    std::unique_ptr<ASTNode> parsePrimaryExpression() {
        // Integer literal
        if (match(TokenType::INTEGER)) {
            int value = std::stoi(currentToken().value);
            advance();
            return std::make_unique<IntegerLiteral>(value);
        }
        
        // Float literal
        if (match(TokenType::FLOAT)) {
            double value = std::stod(currentToken().value);
            advance();
            return std::make_unique<FloatLiteral>(value);
        }
        
        // Boolean literals
        if (match(TokenType::TRUE)) {
            advance();
            return std::make_unique<BooleanLiteral>(true);
        }
        
        if (match(TokenType::FALSE)) {
            advance();
            return std::make_unique<BooleanLiteral>(false);
        }
        
        // Identifier or function call
        if (match(TokenType::IDENTIFIER)) {
            std::string name = currentToken().value;
            advance();
            
            // Check if it's a function call
            if (match(TokenType::LPAREN)) {
                advance();
                auto funcCall = std::make_unique<FunctionCall>(name);
                
                while (!match(TokenType::RPAREN) && !match(TokenType::END_OF_FILE)) {
                    funcCall->arguments.push_back(parseExpression());
                    if (match(TokenType::COMMA)) {
                        advance();
                    } else {
                        break;
                    }
                }
                expect(TokenType::RPAREN, "Expected ')' after arguments");
                return funcCall;
            }
            
            return std::make_unique<Identifier>(name);
        }
        
        // Parenthesized expression
        if (match(TokenType::LPAREN)) {
            advance();
            auto expr = parseExpression();
            expect(TokenType::RPAREN, "Expected ')' after expression");
            return expr;
        }
        
        errors.push_back("Line " + std::to_string(currentToken().line) + 
                        ": Unexpected token in expression: " + currentToken().value);
        throw std::runtime_error("Unexpected token in expression");
    }
    
public:
    Parser(const std::vector<Token>& toks) : tokens(toks), position(0) {}
    
    std::unique_ptr<Program> parse() {
        try {
            auto program = parseProgram();
            // If there were any errors during parsing, return nullptr
            if (!errors.empty()) {
                return nullptr;
            }
            return program;
        } catch (const std::exception& e) {
            return nullptr;
        }
    }
    
    std::vector<std::string> getErrors() const {
        return errors;
    }
};

#endif // PARSER_H
