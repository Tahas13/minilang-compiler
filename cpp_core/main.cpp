/*
 * MiniLang Compiler - Main Driver
 * Authors: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
 * Course: CS-4031 - Compiler Construction
 * 
 * This C++ core implements all three compiler phases and outputs JSON
 * for integration with the Python web interface.
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "scanner.h"
#include "parser.h"
#include "semantic.h"
#include "json.hpp"

using json = nlohmann::json;

std::string readFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        return "";
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

json tokensToJSON(const std::vector<Token>& tokens) {
    json tokensArray = json::array();
    
    for (const auto& token : tokens) {
        if (token.type != TokenType::END_OF_FILE) {
            json tokenObj;
            tokenObj["type"] = TokenHelper::tokenTypeToString(token.type);
            tokenObj["value"] = token.value;
            tokenObj["line"] = token.line;
            tokenObj["column"] = token.column;
            tokensArray.push_back(tokenObj);
        }
    }
    
    return tokensArray;
}

json symbolTableToJSON(const std::map<std::string, Symbol>& table) {
    json symbolsObj;
    
    for (const auto& [name, symbol] : table) {
        json symObj;
        symObj["type"] = symbol.type;
        symObj["initialized"] = symbol.initialized;
        symbolsObj[name] = symObj;
    }
    
    return symbolsObj;
}

int main(int argc, char* argv[]) {
    json result;
    
    try {
        // Check arguments
        if (argc < 2) {
            std::cerr << "Usage: " << argv[0] << " <source_file>" << std::endl;
            return 1;
        }
        
        std::string sourceCode;
        
        // Read from file or stdin
        if (std::string(argv[1]) == "-") {
            // Read from stdin
            std::stringstream buffer;
            buffer << std::cin.rdbuf();
            sourceCode = buffer.str();
        } else {
            // Read from file
            sourceCode = readFile(argv[1]);
            if (sourceCode.empty()) {
                result["success"] = false;
                result["phase"] = "file";
                result["errors"] = json::array({"Failed to read source file"});
                std::cout << result.dump(2) << std::endl;
                return 1;
            }
        }
        
        // Phase 1: Lexical Analysis
        Scanner scanner(sourceCode);
        std::vector<Token> tokens = scanner.tokenize();
        
        result["tokens"] = tokensToJSON(tokens);
        
        // Phase 2: Syntax Analysis
        Parser parser(tokens);
        auto ast = parser.parse();
        
        if (!ast || !parser.getErrors().empty()) {
            result["success"] = false;
            result["phase"] = "syntax";
            result["errors"] = parser.getErrors();
            std::cout << result.dump(2) << std::endl;
            return 1;
        }
        
        result["ast"] = ast->toJSON();
        
        // Phase 3: Semantic Analysis
        SemanticAnalyzer analyzer;
        bool semanticSuccess = analyzer.analyze(ast.get());
        
        result["symbol_table"] = symbolTableToJSON(analyzer.getSymbolTable());
        
        if (!semanticSuccess) {
            result["success"] = false;
            result["phase"] = "semantic";
            result["errors"] = analyzer.getErrors();
        } else {
            result["success"] = true;
            result["errors"] = json::array();
        }
        
    } catch (const std::exception& e) {
        result["success"] = false;
        result["phase"] = "unknown";
        result["errors"] = json::array({e.what()});
    }
    
    // Output JSON result
    std::cout << result.dump(2) << std::endl;
    
    return result["success"].get<bool>() ? 0 : 1;
}
