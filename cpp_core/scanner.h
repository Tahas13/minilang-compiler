/*
 * MiniLang Compiler - Scanner (Lexical Analyzer)
 * Authors: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
 * Course: CS-4031 - Compiler Construction
 */

#ifndef SCANNER_H
#define SCANNER_H

#include "token.h"
#include <vector>
#include <string>
#include <cctype>

class Scanner {
private:
    std::string source;
    size_t position;
    int line;
    int column;
    std::vector<Token> tokens;
    std::map<std::string, TokenType> keywords;
    
    char currentChar() {
        if (position >= source.length()) return '\0';
        return source[position];
    }
    
    char peekChar(int offset = 1) {
        if (position + offset >= source.length()) return '\0';
        return source[position + offset];
    }
    
    void advance() {
        if (position < source.length()) {
            if (source[position] == '\n') {
                line++;
                column = 1;
            } else {
                column++;
            }
            position++;
        }
    }
    
    void skipWhitespace() {
        while (std::isspace(currentChar())) {
            advance();
        }
    }
    
    void skipComment() {
        if (currentChar() == '/' && peekChar() == '/') {
            while (currentChar() != '\n' && currentChar() != '\0') {
                advance();
            }
        }
    }
    
    Token scanNumber() {
        int startLine = line;
        int startColumn = column;
        std::string number;
        bool isFloat = false;
        
        while (std::isdigit(currentChar())) {
            number += currentChar();
            advance();
        }
        
        if (currentChar() == '.' && std::isdigit(peekChar())) {
            isFloat = true;
            number += currentChar();
            advance();
            
            while (std::isdigit(currentChar())) {
                number += currentChar();
                advance();
            }
        }
        
        return Token(isFloat ? TokenType::FLOAT : TokenType::INTEGER, 
                     number, startLine, startColumn);
    }
    
    Token scanIdentifier() {
        int startLine = line;
        int startColumn = column;
        std::string identifier;
        
        while (std::isalnum(currentChar()) || currentChar() == '_') {
            identifier += currentChar();
            advance();
        }
        
        // Check if it's a keyword
        auto it = keywords.find(identifier);
        if (it != keywords.end()) {
            return Token(it->second, identifier, startLine, startColumn);
        }
        
        return Token(TokenType::IDENTIFIER, identifier, startLine, startColumn);
    }
    
public:
    Scanner(const std::string& src) 
        : source(src), position(0), line(1), column(1) {
        keywords = TokenHelper::getKeywords();
    }
    
    std::vector<Token> tokenize() {
        tokens.clear();
        
        while (position < source.length()) {
            skipWhitespace();
            
            if (position >= source.length()) break;
            
            // Skip comments
            if (currentChar() == '/' && peekChar() == '/') {
                skipComment();
                continue;
            }
            
            char ch = currentChar();
            int startLine = line;
            int startColumn = column;
            
            // Numbers
            if (std::isdigit(ch)) {
                tokens.push_back(scanNumber());
                continue;
            }
            
            // Identifiers and keywords
            if (std::isalpha(ch) || ch == '_') {
                tokens.push_back(scanIdentifier());
                continue;
            }
            
            // Operators and delimiters
            switch (ch) {
                case '+':
                    tokens.push_back(Token(TokenType::PLUS, "+", startLine, startColumn));
                    advance();
                    break;
                case '-':
                    tokens.push_back(Token(TokenType::MINUS, "-", startLine, startColumn));
                    advance();
                    break;
                case '*':
                    tokens.push_back(Token(TokenType::MULTIPLY, "*", startLine, startColumn));
                    advance();
                    break;
                case '/':
                    tokens.push_back(Token(TokenType::DIVIDE, "/", startLine, startColumn));
                    advance();
                    break;
                case '(':
                    tokens.push_back(Token(TokenType::LPAREN, "(", startLine, startColumn));
                    advance();
                    break;
                case ')':
                    tokens.push_back(Token(TokenType::RPAREN, ")", startLine, startColumn));
                    advance();
                    break;
                case '{':
                    tokens.push_back(Token(TokenType::LBRACE, "{", startLine, startColumn));
                    advance();
                    break;
                case '}':
                    tokens.push_back(Token(TokenType::RBRACE, "}", startLine, startColumn));
                    advance();
                    break;
                case ';':
                    tokens.push_back(Token(TokenType::SEMICOLON, ";", startLine, startColumn));
                    advance();
                    break;
                case ',':
                    tokens.push_back(Token(TokenType::COMMA, ",", startLine, startColumn));
                    advance();
                    break;
                case '=':
                    if (peekChar() == '=') {
                        tokens.push_back(Token(TokenType::EQUAL, "==", startLine, startColumn));
                        advance();
                        advance();
                    } else {
                        tokens.push_back(Token(TokenType::ASSIGN, "=", startLine, startColumn));
                        advance();
                    }
                    break;
                case '!':
                    if (peekChar() == '=') {
                        tokens.push_back(Token(TokenType::NOT_EQUAL, "!=", startLine, startColumn));
                        advance();
                        advance();
                    } else {
                        tokens.push_back(Token(TokenType::INVALID, "!", startLine, startColumn));
                        advance();
                    }
                    break;
                case '<':
                    if (peekChar() == '=') {
                        tokens.push_back(Token(TokenType::LESS_EQUAL, "<=", startLine, startColumn));
                        advance();
                        advance();
                    } else {
                        tokens.push_back(Token(TokenType::LESS_THAN, "<", startLine, startColumn));
                        advance();
                    }
                    break;
                case '>':
                    if (peekChar() == '=') {
                        tokens.push_back(Token(TokenType::GREATER_EQUAL, ">=", startLine, startColumn));
                        advance();
                        advance();
                    } else {
                        tokens.push_back(Token(TokenType::GREATER_THAN, ">", startLine, startColumn));
                        advance();
                    }
                    break;
                default:
                    tokens.push_back(Token(TokenType::INVALID, std::string(1, ch), startLine, startColumn));
                    advance();
                    break;
            }
        }
        
        tokens.push_back(Token(TokenType::END_OF_FILE, "", line, column));
        return tokens;
    }
};

#endif // SCANNER_H
