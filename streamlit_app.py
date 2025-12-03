"""
MiniLang Compiler Web Interface using Streamlit
Author: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)
Course: CS-4031 - Compiler Construction

A web-based interface for the MiniLang compiler with real-time compilation,
syntax highlighting, and interactive AST visualization.
"""

import streamlit as st
import sys
from pathlib import Path
import io
import base64
from typing import Dict, List

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import compiler components
from scanner import Scanner
from parser import Parser
from semantic_analyzer import TypeChecker
from clean_vertical_ast import print_clean_vertical_ast
from web_ast import get_web_ast_string
from compiler import MiniLangCompiler

# Page configuration
st.set_page_config(
    page_title="MiniLang Compiler",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS styling with glassmorphism and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(45deg, #fff, #ffd89b, #19547b);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -2px;
        animation: slideIn 0.8s ease-out, float 3s ease-in-out infinite;
        text-shadow: 0 0 40px rgba(255,255,255,0.5);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 2rem;
        animation: slideIn 1s ease-out;
    }
    
    .phase-header {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(20px);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 20px;
        margin: 2rem 0 1rem 0;
        font-weight: 700;
        font-size: 1.3rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 2px solid rgba(255, 255, 255, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: slideIn 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .phase-header:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.5);
    }
    
    .success-box {
        background: rgba(76, 175, 80, 0.2);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(76, 175, 80, 0.6);
        color: #fff;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
        font-weight: 600;
        font-size: 1.05rem;
        animation: slideIn 0.5s ease-out, pulse 2s infinite;
    }
    
    .error-box {
        background: rgba(244, 67, 54, 0.2);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(244, 67, 54, 0.6);
        color: #fff;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(244, 67, 54, 0.3);
        font-weight: 600;
        font-size: 1.05rem;
        animation: slideIn 0.5s ease-out;
    }
    
    .ast-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(102, 126, 234, 0.5);
        border-radius: 20px;
        padding: 2.5rem;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 1.05rem;
        line-height: 1.8;
        overflow-x: auto;
        white-space: pre;
        color: #1a202c;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        animation: slideIn 0.8s ease-out;
        transition: all 0.3s ease;
    }
    
    .ast-container:hover {
        transform: scale(1.01);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.25);
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(102, 126, 234, 0.6) !important;
        border-radius: 15px !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        font-size: 15px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.3s ease !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border: 2px solid rgba(102, 126, 234, 1) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.3) !important;
        transform: scale(1.01);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 30px !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 3rem !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02) !important;
    }
    
    .stSidebar {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    .stSidebar .stSelectbox, .stSidebar .stCheckbox {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.25) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        transition: all 0.3s ease !important;
        animation: slideIn 0.7s ease-out !important;
    }
    
    .stMetric:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stMetric label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        margin: 1rem 0 !important;
    }
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
    }
    
    h1, h2, h3, h4 {
        color: white !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .info-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        border: 2px solid rgba(255, 255, 255, 0.4);
        color: white;
        font-weight: 600;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .info-badge:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

def load_example_programs() -> Dict[str, str]:
    """Load example MiniLang programs."""
    examples = {
        "Basic Variables": """// Basic variable declarations and arithmetic
int a = 10;
int b = 5;
float pi = 3.14;
bool flag = true;

int sum = a + b;
float result = pi * a;

print(sum);
print(result);""",

        "For Loop": """// For loop - Sum of numbers 1 to 10
int sum = 0;

for (int i = 1; i <= 10; i = i + 1) {
    sum = sum + i;
}

print(sum);""",

        "Do-While Loop": """// Do-while loop - Countdown from 5
int count = 5;

do {
    print(count);
    count = count - 1;
} while (count > 0);""",

        "Function - Add": """// Function to add two numbers
function int add(int a, int b) {
    int result = a + b;
    return result;
}

int x = 10;
int y = 20;
int sum = add(x, y);
print(sum);""",

        "Function - Factorial": """// Recursive factorial function
function int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        int result = n * factorial(n - 1);
        return result;
    }
}

int num = 5;
int fact = factorial(num);
print(fact);""",

        "Function - Even Check": """// Function to check if number is even
function bool isEven(int n) {
    int remainder = n - (n / 2 * 2);
    bool result = remainder == 0;
    return result;
}

int num = 8;
bool even = isEven(num);
if (even) {
    print(1);
} else {
    print(0);
}""",

        "Conditional Statements": """// If-else statements
int score = 85;
bool passed = false;

if (score >= 60) {
    passed = true;
    print(passed);
} else {
    passed = false;
    print(passed);
}

print(score);""",

        "While Loop": """// While loop example
int counter = 5;

while (counter > 0) {
    print(counter);
    counter = counter - 1;
}

print(counter);""",

        "Nested Loops": """// Nested for loops
for (int i = 1; i <= 3; i = i + 1) {
    for (int j = 1; j <= 3; j = j + 1) {
        int product = i * j;
        print(product);
    }
}""",

        "All Features": """// Comprehensive example
function bool isEven(int n) {
    int remainder = n - (n / 2 * 2);
    bool result = remainder == 0;
    return result;
}

function int power(int base, int exp) {
    int result = 1;
    for (int i = 0; i < exp; i = i + 1) {
        result = result * base;
    }
    return result;
}

int x = 2;
int y = 3;
int z = power(x, y);
print(z);

bool even = isEven(z);
if (even) {
    print(1);
} else {
    print(0);
}

int counter = 3;
do {
    print(counter);
    counter = counter - 1;
} while (counter > 0);""",

        "Error Example": """// This program contains errors
int x = true;  // Type error
print(undeclaredVar);  // Undefined variable
bool result = x + 5;  // Invalid operation"""
    }
    return examples

def display_tokens(tokens):
    """Display tokens in a formatted table."""
    if not tokens:
        return
    
    token_data = []
    for i, token in enumerate(tokens):
        if token.type.name != 'EOF':  # Skip EOF token
            token_data.append({
                "Index": i + 1,
                "Type": token.type.name,
                "Value": str(token.value),
                "Line": token.line,
                "Column": token.column
            })
    
    if token_data:
        st.dataframe(token_data, width="stretch")

def capture_ast_output(ast):
    """Capture AST output as clean string for web display."""
    return get_web_ast_string(ast)

def display_symbol_table(symbol_table):
    """Display symbol table in a formatted way."""
    if not symbol_table or not symbol_table.symbols:
        st.write("No symbols in table.")
        return
    
    symbol_data = []
    for name, symbol in symbol_table.symbols.items():
        symbol_data.append({
            "Variable": name,
            "Type": symbol.type,
            "Initialized": "✓" if symbol.initialized else "✗",
            "Value": str(symbol.value) if symbol.value is not None else "None"
        })
    
    st.dataframe(symbol_data, width="stretch")

def main():
    # Premium header with glassmorphism
    st.markdown('<h1 class="main-header">⚡ MiniLang Compiler</h1>', unsafe_allow_html=True)
    
    # Enhanced glass card design for info section
    st.markdown("""
    <div class="glass-card" style="text-align: center; margin-bottom: 2.5rem; padding: 3rem 2rem;">
        <div style="margin-bottom: 2.5rem;">
            <p style="font-size: 2rem; color: white; font-weight: 700; margin-bottom: 1rem; text-shadow: 0 4px 15px rgba(0,0,0,0.4); line-height: 1.4;">
                🎯 A Comprehensive Three-Phase Compiler
            </p>
            <p style="font-size: 1.3rem; color: rgba(255,255,255,0.95); font-weight: 500; text-shadow: 0 2px 8px rgba(0,0,0,0.3); line-height: 1.6; max-width: 900px; margin: 0 auto;">
                Built for the <strong>MiniLang</strong> programming language with full support for variables, functions, loops (for, while, do-while), and type checking
            </p>
            <p style="font-size: 1.1rem; color: rgba(255,255,255,0.85); font-weight: 500; text-shadow: 0 2px 8px rgba(0,0,0,0.3); line-height: 1.5; max-width: 800px; margin: 1rem auto 0;">
                💡 <em>Core compiler implemented in C++17 • Web interface uses Python fallback</em>
            </p>
        </div>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 2rem;">
            <span class="info-badge" style="font-size: 1.05rem; padding: 0.8rem 1.8rem;">
                👥 <strong>Authors:</strong> Shozab Mehdi (22k-4522) • Taha Sharif (22k-4145)
            </span>
            <span class="info-badge" style="font-size: 1.05rem; padding: 0.8rem 1.8rem;">
                📚 <strong>Course:</strong> CS-4031 - Compiler Construction
            </span>
            <span class="info-badge" style="font-size: 1.05rem; padding: 0.8rem 1.8rem;">
                🏆 <strong>Implementation:</strong> Hybrid C++/Python System
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for examples and settings
    with st.sidebar:
        st.header("📚 Example Programs")
        examples = load_example_programs()
        selected_example = st.selectbox(
            "Choose an example:",
            list(examples.keys()),
            help="Select a pre-written MiniLang program to test"
        )
        
        st.header("⚙️ Compiler Settings")
        show_tokens = st.checkbox("Show Token Analysis", value=True)
        show_ast = st.checkbox("Show AST Tree", value=True)
        show_symbol_table = st.checkbox("Show Symbol Table", value=True)
        
        st.header("📖 Language Reference")
        with st.expander("Data Types"):
            st.code("""
int    - Integer numbers
float  - Floating-point numbers  
bool   - Boolean values (true/false)
            """)
        
        with st.expander("Operators"):
            st.code("""
Arithmetic: +, -, *, /
Relational: >, <, >=, <=, ==, !=
Logical:    and, or, not
Assignment: =
            """)
        
        with st.expander("Control Flow"):
            st.code("""
if (condition) { ... } else { ... }
while (condition) { ... }
for (init; condition; update) { ... }
do { ... } while (condition);
            """)
        
        with st.expander("Functions"):
            st.code("""
function returnType name(params) {
    statements
    return expression;
}

// Example:
function int add(int a, int b) {
    return a + b;
}
            """)

    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); padding: 1rem; border-radius: 15px; margin-bottom: 1rem; border: 2px solid rgba(255, 255, 255, 0.3);">
            <h2 style="margin: 0; text-align: center; font-size: 1.8rem;">💻 Code Editor</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Load selected example
        default_code = examples[selected_example]
        
        # Code editor
        source_code = st.text_area(
            "Write your MiniLang code:",
            value=default_code,
            height=400,
            help="Enter your MiniLang source code here. Use the examples from the sidebar to get started."
        )
        
        # Compile button
        compile_button = st.button("🚀 Compile Code", type="primary", width="stretch")
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); padding: 1rem; border-radius: 15px; margin-bottom: 1rem; border: 2px solid rgba(255, 255, 255, 0.3);">
            <h2 style="margin: 0; text-align: center; font-size: 1.8rem;">🎨 Compilation Results</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if compile_button and source_code.strip():
            # Create compiler instance
            compiler = MiniLangCompiler()
            
            # Phase 1: Lexical Analysis
            st.markdown('<div class="phase-header">Phase 1: Lexical Analysis</div>', unsafe_allow_html=True)
            
            with st.spinner("Tokenizing source code..."):
                scanner = Scanner(source_code)
                tokens = scanner.tokenize()
            
            if tokens:
                st.markdown('<div class="success-box">✅ Lexical analysis completed successfully!</div>', unsafe_allow_html=True)
                st.info(f"Generated {len(tokens)} tokens")
                
                if show_tokens:
                    with st.expander("View Tokens", expanded=False):
                        display_tokens(tokens)
            else:
                st.markdown('<div class="error-box">❌ Lexical analysis failed!</div>', unsafe_allow_html=True)
                st.stop()
            
            # Phase 2: Syntax Analysis
            st.markdown('<div class="phase-header">Phase 2: Syntax Analysis</div>', unsafe_allow_html=True)
            
            with st.spinner("Parsing tokens into AST..."):
                parser = Parser(tokens)
                ast = parser.parse()
            
            if ast:
                st.markdown('<div class="success-box">✅ Syntax analysis completed successfully!</div>', unsafe_allow_html=True)
                st.info("Abstract Syntax Tree (AST) generated")
                
                if show_ast:
                    with st.expander("🌳 View Abstract Syntax Tree", expanded=True):
                        ast_output = capture_ast_output(ast)
                        st.markdown("""
                        <div style="text-align: center; margin-bottom: 1.5rem; padding: 1rem; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); border-radius: 15px;">
                            <h3 style="color: white; margin-bottom: 0.5rem; font-size: 1.5rem;">🌲 Abstract Syntax Tree</h3>
                            <p style="color: rgba(255, 255, 255, 0.9); font-size: 1rem;">Clean vertical layout showing the parsed program hierarchy</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f'<div class="ast-container">{ast_output}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">❌ Syntax analysis failed!</div>', unsafe_allow_html=True)
                st.stop()
            
            # Phase 3: Semantic Analysis
            st.markdown('<div class="phase-header">Phase 3: Semantic Analysis</div>', unsafe_allow_html=True)
            
            with st.spinner("Performing type checking and semantic analysis..."):
                type_checker = TypeChecker()
                semantic_success = type_checker.analyze(ast)
            
            if semantic_success:
                st.markdown('<div class="success-box">✅ Semantic analysis completed successfully!</div>', unsafe_allow_html=True)
                st.info("No semantic errors found")
                
                if show_symbol_table:
                    with st.expander("View Symbol Table", expanded=False):
                        display_symbol_table(type_checker.symbol_table)
                
                # Final success message
                st.success("🎉 Compilation completed successfully!")
                
            else:
                st.markdown('<div class="error-box">❌ Semantic analysis failed!</div>', unsafe_allow_html=True)
                st.error(f"Found {len(type_checker.errors)} semantic errors:")
                
                for i, error in enumerate(type_checker.errors, 1):
                    st.error(f"{i}. {error.message}")
        
        elif compile_button:
            st.warning("⚠️ Please enter some MiniLang code to compile.")
    
    # Enhanced footer with metrics
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 2rem 0;">
        <h3 style="color: white; font-size: 2rem; text-shadow: 0 2px 10px rgba(0,0,0,0.3); font-weight: 800;">📊 Project Highlights</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(20px); border-radius: 20px; padding: 2rem 1.5rem; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); border: 2px solid rgba(255, 255, 255, 0.4); text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
            <div style="color: white; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">Language Features</div>
            <div style="color: white; font-size: 1rem; font-weight: 500; line-height: 1.4;">Variables, Functions, Loops</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(20px); border-radius: 20px; padding: 2rem 1.5rem; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); border: 2px solid rgba(255, 255, 255, 0.4); text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚙️</div>
            <div style="color: white; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">Compiler Phases</div>
            <div style="color: white; font-size: 1rem; font-weight: 500; line-height: 1.4;">3 (Lexer, Parser, Semantic)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(20px); border-radius: 20px; padding: 2rem 1.5rem; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); border: 2px solid rgba(255, 255, 255, 0.4); text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🛡️</div>
            <div style="color: white; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">Error Detection</div>
            <div style="color: white; font-size: 1rem; font-weight: 500; line-height: 1.4;">Comprehensive</div>
        </div>
        """, unsafe_allow_html=True)
    
    # About section
    with st.expander("ℹ️ About MiniLang Compiler"):
        st.markdown("""
        ### About This Project
        
        This MiniLang compiler is a comprehensive implementation of compiler construction principles, 
        featuring all three major phases of compilation:
        
        1. **Lexical Analysis**: Converts source code into tokens
        2. **Syntax Analysis**: Builds an Abstract Syntax Tree (AST)
        3. **Semantic Analysis**: Performs type checking and error detection
        
        ### Key Features
        - ✅ Complete support for variables, functions, and loops (for, while, do-while)
        - ✅ Function declarations with parameters and recursion support
        - ✅ Strong type system with automatic type checking
        - ✅ Comprehensive error detection and reporting
        - ✅ Interactive web interface with real-time compilation
        - ✅ Visual AST representation
        - ✅ Symbol table management with function tracking
        
        ### Technologies Used
        - **Python** for compiler implementation
        - **Streamlit** for web interface
        - **Recursive Descent Parsing** for syntax analysis
        - **Visitor Pattern** for AST traversal and semantic analysis
        """)

if __name__ == "__main__":
    main()