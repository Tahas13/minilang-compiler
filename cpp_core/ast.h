/*
 * MiniLang Compiler - AST Node Definitions
 * Authors: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
 * Course: CS-4031 - Compiler Construction
 */

#ifndef AST_H
#define AST_H

#include <string>
#include <vector>
#include <memory>
#include "json.hpp"

using json = nlohmann::json;

// Base AST Node
class ASTNode {
public:
    virtual ~ASTNode() = default;
    virtual json toJSON() const = 0;
    virtual std::string getType() const = 0;
};

// Program Node
class Program : public ASTNode {
public:
    std::vector<std::unique_ptr<ASTNode>> statements;
    
    json toJSON() const override {
        json j;
        j["type"] = "Program";
        j["statements"] = json::array();
        for (const auto& stmt : statements) {
            j["statements"].push_back(stmt->toJSON());
        }
        return j;
    }
    
    std::string getType() const override { return "Program"; }
};

// Variable Declaration
class VarDeclaration : public ASTNode {
public:
    std::string varType;
    std::string name;
    std::unique_ptr<ASTNode> value;
    
    VarDeclaration(const std::string& type, const std::string& n, std::unique_ptr<ASTNode> val = nullptr)
        : varType(type), name(n), value(std::move(val)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "VarDeclaration";
        j["varType"] = varType;
        j["name"] = name;
        if (value) {
            j["value"] = value->toJSON();
        }
        return j;
    }
    
    std::string getType() const override { return "VarDeclaration"; }
};

// Assignment
class Assignment : public ASTNode {
public:
    std::string name;
    std::unique_ptr<ASTNode> value;
    
    Assignment(const std::string& n, std::unique_ptr<ASTNode> val)
        : name(n), value(std::move(val)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "Assignment";
        j["name"] = name;
        j["value"] = value->toJSON();
        return j;
    }
    
    std::string getType() const override { return "Assignment"; }
};

// Binary Operation
class BinaryOp : public ASTNode {
public:
    std::unique_ptr<ASTNode> left;
    std::string op;
    std::unique_ptr<ASTNode> right;
    
    BinaryOp(std::unique_ptr<ASTNode> l, const std::string& o, std::unique_ptr<ASTNode> r)
        : left(std::move(l)), op(o), right(std::move(r)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "BinaryOp";
        j["operator"] = op;
        j["left"] = left->toJSON();
        j["right"] = right->toJSON();
        return j;
    }
    
    std::string getType() const override { return "BinaryOp"; }
};

// Unary Operation
class UnaryOp : public ASTNode {
public:
    std::string op;
    std::unique_ptr<ASTNode> operand;
    
    UnaryOp(const std::string& o, std::unique_ptr<ASTNode> operand)
        : op(o), operand(std::move(operand)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "UnaryOp";
        j["operator"] = op;
        j["operand"] = operand->toJSON();
        return j;
    }
    
    std::string getType() const override { return "UnaryOp"; }
};

// Literals
class IntegerLiteral : public ASTNode {
public:
    int value;
    
    IntegerLiteral(int v) : value(v) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "IntegerLiteral";
        j["value"] = value;
        return j;
    }
    
    std::string getType() const override { return "IntegerLiteral"; }
};

class FloatLiteral : public ASTNode {
public:
    double value;
    
    FloatLiteral(double v) : value(v) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "FloatLiteral";
        j["value"] = value;
        return j;
    }
    
    std::string getType() const override { return "FloatLiteral"; }
};

class BooleanLiteral : public ASTNode {
public:
    bool value;
    
    BooleanLiteral(bool v) : value(v) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "BooleanLiteral";
        j["value"] = value;
        return j;
    }
    
    std::string getType() const override { return "BooleanLiteral"; }
};

class Identifier : public ASTNode {
public:
    std::string name;
    
    Identifier(const std::string& n) : name(n) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "Identifier";
        j["name"] = name;
        return j;
    }
    
    std::string getType() const override { return "Identifier"; }
};

// Print Statement
class PrintStatement : public ASTNode {
public:
    std::unique_ptr<ASTNode> expression;
    
    PrintStatement(std::unique_ptr<ASTNode> expr)
        : expression(std::move(expr)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "PrintStatement";
        j["expression"] = expression->toJSON();
        return j;
    }
    
    std::string getType() const override { return "PrintStatement"; }
};

// If Statement
class IfStatement : public ASTNode {
public:
    std::unique_ptr<ASTNode> condition;
    std::vector<std::unique_ptr<ASTNode>> thenStatements;
    std::vector<std::unique_ptr<ASTNode>> elseStatements;
    
    IfStatement(std::unique_ptr<ASTNode> cond)
        : condition(std::move(cond)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "IfStatement";
        j["condition"] = condition->toJSON();
        j["thenStatements"] = json::array();
        for (const auto& stmt : thenStatements) {
            j["thenStatements"].push_back(stmt->toJSON());
        }
        j["elseStatements"] = json::array();
        for (const auto& stmt : elseStatements) {
            j["elseStatements"].push_back(stmt->toJSON());
        }
        return j;
    }
    
    std::string getType() const override { return "IfStatement"; }
};

// While Statement
class WhileStatement : public ASTNode {
public:
    std::unique_ptr<ASTNode> condition;
    std::vector<std::unique_ptr<ASTNode>> body;
    
    WhileStatement(std::unique_ptr<ASTNode> cond)
        : condition(std::move(cond)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "WhileStatement";
        j["condition"] = condition->toJSON();
        j["body"] = json::array();
        for (const auto& stmt : body) {
            j["body"].push_back(stmt->toJSON());
        }
        return j;
    }
    
    std::string getType() const override { return "WhileStatement"; }
};

// For Statement
class ForStatement : public ASTNode {
public:
    std::unique_ptr<ASTNode> init;
    std::unique_ptr<ASTNode> condition;
    std::unique_ptr<ASTNode> update;
    std::vector<std::unique_ptr<ASTNode>> body;
    
    ForStatement(std::unique_ptr<ASTNode> i, std::unique_ptr<ASTNode> c, std::unique_ptr<ASTNode> u)
        : init(std::move(i)), condition(std::move(c)), update(std::move(u)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "ForStatement";
        j["init"] = init ? init->toJSON() : nullptr;
        j["condition"] = condition ? condition->toJSON() : nullptr;
        j["update"] = update ? update->toJSON() : nullptr;
        j["body"] = json::array();
        for (const auto& stmt : body) {
            j["body"].push_back(stmt->toJSON());
        }
        return j;
    }
    
    std::string getType() const override { return "ForStatement"; }
};

// Do-While Statement
class DoWhileStatement : public ASTNode {
public:
    std::unique_ptr<ASTNode> condition;
    std::vector<std::unique_ptr<ASTNode>> body;
    
    DoWhileStatement(std::unique_ptr<ASTNode> cond)
        : condition(std::move(cond)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "DoWhileStatement";
        j["condition"] = condition->toJSON();
        j["body"] = json::array();
        for (const auto& stmt : body) {
            j["body"].push_back(stmt->toJSON());
        }
        return j;
    }
    
    std::string getType() const override { return "DoWhileStatement"; }
};

// Function Declaration
class FunctionDeclaration : public ASTNode {
public:
    std::string returnType;
    std::string name;
    std::vector<std::pair<std::string, std::string>> parameters; // (type, name)
    std::vector<std::unique_ptr<ASTNode>> body;
    
    FunctionDeclaration(const std::string& retType, const std::string& funcName)
        : returnType(retType), name(funcName) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "FunctionDeclaration";
        j["returnType"] = returnType;
        j["name"] = name;
        j["parameters"] = json::array();
        for (const auto& param : parameters) {
            json p;
            p["type"] = param.first;
            p["name"] = param.second;
            j["parameters"].push_back(p);
        }
        j["body"] = json::array();
        for (const auto& stmt : body) {
            j["body"].push_back(stmt->toJSON());
        }
        return j;
    }
    
    std::string getType() const override { return "FunctionDeclaration"; }
};

// Function Call
class FunctionCall : public ASTNode {
public:
    std::string name;
    std::vector<std::unique_ptr<ASTNode>> arguments;
    
    FunctionCall(const std::string& funcName) : name(funcName) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "FunctionCall";
        j["name"] = name;
        j["arguments"] = json::array();
        for (const auto& arg : arguments) {
            j["arguments"].push_back(arg->toJSON());
        }
        return j;
    }
    
    std::string getType() const override { return "FunctionCall"; }
};

// Return Statement
class ReturnStatement : public ASTNode {
public:
    std::unique_ptr<ASTNode> value;
    
    ReturnStatement(std::unique_ptr<ASTNode> val) : value(std::move(val)) {}
    
    json toJSON() const override {
        json j;
        j["type"] = "ReturnStatement";
        j["value"] = value ? value->toJSON() : nullptr;
        return j;
    }
    
    std::string getType() const override { return "ReturnStatement"; }
};

#endif // AST_H
