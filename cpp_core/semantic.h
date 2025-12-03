/*
 * MiniLang Compiler - Semantic Analyzer (Type Checker)
 * Authors: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
 * Course: CS-4031 - Compiler Construction
 */

#ifndef SEMANTIC_H
#define SEMANTIC_H

#include "ast.h"
#include <map>
#include <string>
#include <vector>

struct Symbol {
    std::string type;
    bool initialized;
    bool isFunction;
    std::vector<std::string> paramTypes;
    
    Symbol() : type(""), initialized(false), isFunction(false) {}
    Symbol(const std::string& t, bool init = false) : type(t), initialized(init), isFunction(false) {}
    Symbol(const std::string& t, const std::vector<std::string>& params) 
        : type(t), initialized(true), isFunction(true), paramTypes(params) {}
};

class SemanticAnalyzer {
private:
    std::map<std::string, Symbol> symbolTable;
    std::vector<std::string> errors;
    std::string currentFunction;
    std::string currentFunctionReturnType;
    
    void addError(const std::string& message) {
        errors.push_back(message);
    }
    
    std::string analyzeExpression(const ASTNode* node) {
        if (!node) return "";
        
        std::string type = node->getType();
        
        if (type == "IntegerLiteral") {
            return "int";
        } else if (type == "FloatLiteral") {
            return "float";
        } else if (type == "BooleanLiteral") {
            return "bool";
        } else if (type == "Identifier") {
            auto idNode = dynamic_cast<const Identifier*>(node);
            if (idNode) {
                auto it = symbolTable.find(idNode->name);
                if (it == symbolTable.end()) {
                    addError("Undefined variable: " + idNode->name);
                    return "";
                }
                if (it->second.isFunction) {
                    addError("Cannot use function as variable: " + idNode->name);
                    return "";
                }
                if (!it->second.initialized) {
                    addError("Variable used before initialization: " + idNode->name);
                }
                return it->second.type;
            }
        } else if (type == "FunctionCall") {
            auto funcCall = dynamic_cast<const FunctionCall*>(node);
            if (funcCall) {
                auto it = symbolTable.find(funcCall->name);
                if (it == symbolTable.end()) {
                    addError("Undefined function: " + funcCall->name);
                    return "";
                }
                if (!it->second.isFunction) {
                    addError("Not a function: " + funcCall->name);
                    return "";
                }
                
                // Check argument count
                if (funcCall->arguments.size() != it->second.paramTypes.size()) {
                    addError("Function " + funcCall->name + " expects " + 
                            std::to_string(it->second.paramTypes.size()) + " arguments, got " +
                            std::to_string(funcCall->arguments.size()));
                    return "";
                }
                
                // Check argument types
                for (size_t i = 0; i < funcCall->arguments.size(); i++) {
                    std::string argType = analyzeExpression(funcCall->arguments[i].get());
                    if (!argType.empty() && argType != it->second.paramTypes[i]) {
                        addError("Argument " + std::to_string(i + 1) + " type mismatch: expected " +
                                it->second.paramTypes[i] + ", got " + argType);
                    }
                }
                
                return it->second.type;
            }
        } else if (type == "BinaryOp") {
            auto binOp = dynamic_cast<const BinaryOp*>(node);
            if (binOp) {
                std::string leftType = analyzeExpression(binOp->left.get());
                std::string rightType = analyzeExpression(binOp->right.get());
                
                // Arithmetic operators
                if (binOp->op == "+" || binOp->op == "-" || binOp->op == "*" || binOp->op == "/") {
                    if (leftType != "int" && leftType != "float") {
                        addError("Invalid operand type for " + binOp->op + ": " + leftType);
                        return "";
                    }
                    if (rightType != "int" && rightType != "float") {
                        addError("Invalid operand type for " + binOp->op + ": " + rightType);
                        return "";
                    }
                    // Result is float if either operand is float
                    return (leftType == "float" || rightType == "float") ? "float" : "int";
                }
                
                // Comparison operators
                if (binOp->op == ">" || binOp->op == "<" || binOp->op == ">=" || 
                    binOp->op == "<=" || binOp->op == "==" || binOp->op == "!=") {
                    if (leftType != rightType) {
                        addError("Type mismatch in comparison: " + leftType + " and " + rightType);
                    }
                    return "bool";
                }
                
                // Logical operators
                if (binOp->op == "and" || binOp->op == "or") {
                    if (leftType != "bool") {
                        addError("Invalid operand type for " + binOp->op + ": " + leftType);
                    }
                    if (rightType != "bool") {
                        addError("Invalid operand type for " + binOp->op + ": " + rightType);
                    }
                    return "bool";
                }
            }
        } else if (type == "UnaryOp") {
            auto unOp = dynamic_cast<const UnaryOp*>(node);
            if (unOp) {
                std::string operandType = analyzeExpression(unOp->operand.get());
                
                if (unOp->op == "not") {
                    if (operandType != "bool") {
                        addError("Invalid operand type for not: " + operandType);
                    }
                    return "bool";
                } else if (unOp->op == "-") {
                    if (operandType != "int" && operandType != "float") {
                        addError("Invalid operand type for unary -: " + operandType);
                    }
                    return operandType;
                }
            }
        }
        
        return "";
    }
    
    void analyzeStatement(const ASTNode* node) {
        if (!node) return;
        
        std::string type = node->getType();
        
        if (type == "VarDeclaration") {
            auto varDecl = dynamic_cast<const VarDeclaration*>(node);
            if (varDecl) {
                // Check if variable already declared
                if (symbolTable.find(varDecl->name) != symbolTable.end()) {
                    addError("Variable already declared: " + varDecl->name);
                    return;
                }
                
                // Check initializer type
                if (varDecl->value) {
                    std::string valueType = analyzeExpression(varDecl->value.get());
                    if (!valueType.empty() && valueType != varDecl->varType) {
                        addError("Type mismatch in declaration: expected " + 
                                varDecl->varType + ", got " + valueType);
                    }
                    symbolTable[varDecl->name] = Symbol(varDecl->varType, true);
                } else {
                    symbolTable[varDecl->name] = Symbol(varDecl->varType, false);
                }
            }
        } else if (type == "Assignment") {
            auto assign = dynamic_cast<const Assignment*>(node);
            if (assign) {
                // Check if variable is declared
                auto it = symbolTable.find(assign->name);
                if (it == symbolTable.end()) {
                    addError("Undefined variable: " + assign->name);
                    return;
                }
                
                // Check value type
                std::string valueType = analyzeExpression(assign->value.get());
                if (!valueType.empty() && valueType != it->second.type) {
                    addError("Type mismatch in assignment: expected " + 
                            it->second.type + ", got " + valueType);
                }
                
                // Mark as initialized
                it->second.initialized = true;
            }
        } else if (type == "PrintStatement") {
            auto print = dynamic_cast<const PrintStatement*>(node);
            if (print) {
                analyzeExpression(print->expression.get());
            }
        } else if (type == "IfStatement") {
            auto ifStmt = dynamic_cast<const IfStatement*>(node);
            if (ifStmt) {
                std::string condType = analyzeExpression(ifStmt->condition.get());
                if (!condType.empty() && condType != "bool") {
                    addError("If condition must be boolean, got " + condType);
                }
                
                for (const auto& stmt : ifStmt->thenStatements) {
                    analyzeStatement(stmt.get());
                }
                
                for (const auto& stmt : ifStmt->elseStatements) {
                    analyzeStatement(stmt.get());
                }
            }
        } else if (type == "WhileStatement") {
            auto whileStmt = dynamic_cast<const WhileStatement*>(node);
            if (whileStmt) {
                std::string condType = analyzeExpression(whileStmt->condition.get());
                if (!condType.empty() && condType != "bool") {
                    addError("While condition must be boolean, got " + condType);
                }
                
                for (const auto& stmt : whileStmt->body) {
                    analyzeStatement(stmt.get());
                }
            }
        } else if (type == "ForStatement") {
            auto forStmt = dynamic_cast<const ForStatement*>(node);
            if (forStmt) {
                if (forStmt->init) {
                    analyzeStatement(forStmt->init.get());
                }
                
                if (forStmt->condition) {
                    std::string condType = analyzeExpression(forStmt->condition.get());
                    if (!condType.empty() && condType != "bool") {
                        addError("For condition must be boolean, got " + condType);
                    }
                }
                
                if (forStmt->update) {
                    analyzeStatement(forStmt->update.get());
                }
                
                for (const auto& stmt : forStmt->body) {
                    analyzeStatement(stmt.get());
                }
            }
        } else if (type == "DoWhileStatement") {
            auto doWhileStmt = dynamic_cast<const DoWhileStatement*>(node);
            if (doWhileStmt) {
                for (const auto& stmt : doWhileStmt->body) {
                    analyzeStatement(stmt.get());
                }
                
                std::string condType = analyzeExpression(doWhileStmt->condition.get());
                if (!condType.empty() && condType != "bool") {
                    addError("Do-while condition must be boolean, got " + condType);
                }
            }
        } else if (type == "FunctionDeclaration") {
            auto funcDecl = dynamic_cast<const FunctionDeclaration*>(node);
            if (funcDecl) {
                // Check if function already declared
                if (symbolTable.find(funcDecl->name) != symbolTable.end()) {
                    addError("Function already declared: " + funcDecl->name);
                    return;
                }
                
                // Add function to symbol table
                std::vector<std::string> paramTypes;
                for (const auto& param : funcDecl->parameters) {
                    paramTypes.push_back(param.first);
                }
                symbolTable[funcDecl->name] = Symbol(funcDecl->returnType, paramTypes);
                
                // Save previous function context
                std::string prevFunction = currentFunction;
                std::string prevReturnType = currentFunctionReturnType;
                
                currentFunction = funcDecl->name;
                currentFunctionReturnType = funcDecl->returnType;
                
                // Add parameters to symbol table
                std::map<std::string, Symbol> prevSymbolTable = symbolTable;
                for (const auto& param : funcDecl->parameters) {
                    symbolTable[param.second] = Symbol(param.first, true);
                }
                
                // Analyze function body
                for (const auto& stmt : funcDecl->body) {
                    analyzeStatement(stmt.get());
                }
                
                // Restore symbol table (remove local variables)
                symbolTable = prevSymbolTable;
                
                // Restore previous function context
                currentFunction = prevFunction;
                currentFunctionReturnType = prevReturnType;
            }
        } else if (type == "ReturnStatement") {
            auto returnStmt = dynamic_cast<const ReturnStatement*>(node);
            if (returnStmt) {
                if (currentFunction.empty()) {
                    addError("Return statement outside function");
                    return;
                }
                
                if (returnStmt->value) {
                    std::string returnType = analyzeExpression(returnStmt->value.get());
                    if (!returnType.empty() && returnType != currentFunctionReturnType) {
                        addError("Return type mismatch: expected " + currentFunctionReturnType + 
                                ", got " + returnType);
                    }
                }
            }
        } else if (type == "FunctionCall") {
            auto funcCall = dynamic_cast<const FunctionCall*>(node);
            if (funcCall) {
                analyzeExpression(funcCall);
            }
        }
    }
    
public:
    bool analyze(const Program* program) {
        if (!program) return false;
        
        symbolTable.clear();
        errors.clear();
        
        for (const auto& stmt : program->statements) {
            analyzeStatement(stmt.get());
        }
        
        return errors.empty();
    }
    
    std::vector<std::string> getErrors() const {
        return errors;
    }
    
    std::map<std::string, Symbol> getSymbolTable() const {
        return symbolTable;
    }
};

#endif // SEMANTIC_H
