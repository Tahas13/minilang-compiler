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
        // Variable declaration
        if (match(TokenType::INT) || match(TokenType::FLOAT_TYPE) || match(TokenType::BOOL)) {
            return parseVarDeclaration();
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
        
        // Assignment
        if (match(TokenType::IDENTIFIER)) {
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
        
        // Identifier
        if (match(TokenType::IDENTIFIER)) {
            std::string name = currentToken().value;
            advance();
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
            return parseProgram();
        } catch (const std::exception& e) {
            return nullptr;
        }
    }
    
    std::vector<std::string> getErrors() const {
        return errors;
    }
};

#endif // PARSER_H
