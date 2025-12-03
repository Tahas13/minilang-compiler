/*
 * MiniLang Compiler - Token Definitions
 * Authors: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
 * Course: CS-4031 - Compiler Construction
 */

#ifndef TOKEN_H
#define TOKEN_H

#include <string>
#include <map>

enum class TokenType {
    // Literals
    INTEGER,
    FLOAT,
    BOOLEAN,
    IDENTIFIER,
    
    // Keywords
    INT,
    FLOAT_TYPE,
    BOOL,
    IF,
    ELSE,
    WHILE,
    PRINT,
    TRUE,
    FALSE,
    
    // Operators
    PLUS,
    MINUS,
    MULTIPLY,
    DIVIDE,
    ASSIGN,
    EQUAL,
    NOT_EQUAL,
    LESS_THAN,
    GREATER_THAN,
    LESS_EQUAL,
    GREATER_EQUAL,
    AND,
    OR,
    NOT,
    
    // Delimiters
    LPAREN,
    RPAREN,
    LBRACE,
    RBRACE,
    SEMICOLON,
    COMMA,
    
    // Special
    END_OF_FILE,
    INVALID
};

struct Token {
    TokenType type;
    std::string value;
    int line;
    int column;
    
    Token(TokenType t, const std::string& v, int l, int c)
        : type(t), value(v), line(l), column(c) {}
};

class TokenHelper {
public:
    static std::string tokenTypeToString(TokenType type) {
        static const std::map<TokenType, std::string> typeNames = {
            {TokenType::INTEGER, "INTEGER"},
            {TokenType::FLOAT, "FLOAT"},
            {TokenType::BOOLEAN, "BOOLEAN"},
            {TokenType::IDENTIFIER, "IDENTIFIER"},
            {TokenType::INT, "INT"},
            {TokenType::FLOAT_TYPE, "FLOAT_TYPE"},
            {TokenType::BOOL, "BOOL"},
            {TokenType::IF, "IF"},
            {TokenType::ELSE, "ELSE"},
            {TokenType::WHILE, "WHILE"},
            {TokenType::PRINT, "PRINT"},
            {TokenType::TRUE, "TRUE"},
            {TokenType::FALSE, "FALSE"},
            {TokenType::PLUS, "PLUS"},
            {TokenType::MINUS, "MINUS"},
            {TokenType::MULTIPLY, "MULTIPLY"},
            {TokenType::DIVIDE, "DIVIDE"},
            {TokenType::ASSIGN, "ASSIGN"},
            {TokenType::EQUAL, "EQUAL"},
            {TokenType::NOT_EQUAL, "NOT_EQUAL"},
            {TokenType::LESS_THAN, "LESS_THAN"},
            {TokenType::GREATER_THAN, "GREATER_THAN"},
            {TokenType::LESS_EQUAL, "LESS_EQUAL"},
            {TokenType::GREATER_EQUAL, "GREATER_EQUAL"},
            {TokenType::AND, "AND"},
            {TokenType::OR, "OR"},
            {TokenType::NOT, "NOT"},
            {TokenType::LPAREN, "LPAREN"},
            {TokenType::RPAREN, "RPAREN"},
            {TokenType::LBRACE, "LBRACE"},
            {TokenType::RBRACE, "RBRACE"},
            {TokenType::SEMICOLON, "SEMICOLON"},
            {TokenType::COMMA, "COMMA"},
            {TokenType::END_OF_FILE, "EOF"},
            {TokenType::INVALID, "INVALID"}
        };
        
        auto it = typeNames.find(type);
        return (it != typeNames.end()) ? it->second : "UNKNOWN";
    }
    
    static std::map<std::string, TokenType> getKeywords() {
        static std::map<std::string, TokenType> keywords = {
            {"int", TokenType::INT},
            {"float", TokenType::FLOAT_TYPE},
            {"bool", TokenType::BOOL},
            {"if", TokenType::IF},
            {"else", TokenType::ELSE},
            {"while", TokenType::WHILE},
            {"print", TokenType::PRINT},
            {"true", TokenType::TRUE},
            {"false", TokenType::FALSE},
            {"and", TokenType::AND},
            {"or", TokenType::OR},
            {"not", TokenType::NOT}
        };
        return keywords;
    }
};

#endif // TOKEN_H
