# 🚀 Quick Start Guide - MiniLang Compiler with C++ Core

## ⚡ Fast Track Setup (5 minutes)

### Step 1: Install MinGW (C++ Compiler)

**Using Chocolatey (Easiest):**
```powershell
# Install Chocolatey first (if not installed): https://chocolatey.org/install
choco install mingw -y
```

**Manual Install:**
1. Download: https://github.com/niXman/mingw-builds-binaries/releases
2. Extract to `C:\mingw64`
3. Add to PATH: `C:\mingw64\bin`
4. Restart PowerShell

**Verify:**
```powershell
g++ --version
```

---

### Step 2: Compile C++ Core (30 seconds)

```powershell
cd cpp_core

# Download JSON library
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/nlohmann/json/develop/single_include/nlohmann/json.hpp" -OutFile "json.hpp"

# Compile
g++ -std=c++17 -O2 -o minilang_compiler.exe main.cpp

# Test
"int x = 42; print(x);" | .\minilang_compiler.exe -
```

You should see JSON output! ✅

---

### Step 3: Run Web App

```powershell
cd ..
streamlit run streamlit_app.py
```

Visit: **http://localhost:8501**

---

## ✅ What You Should See

### In Terminal:
```
Building MiniLang C++ Compiler Core...
✅ C++ compiler available: cpp_core\minilang_compiler.exe
```

### In Web Browser:
- Beautiful gradient interface
- Code editor with examples
- "Compile Code" button
- AST tree visualization
- Symbol table display

---

## 🎯 Quick Test

1. Open web app: http://localhost:8501
2. Select "Basic Variables" from sidebar
3. Click "🚀 Compile Code"
4. See:
   - ✅ Lexical analysis complete
   - ✅ Syntax analysis complete
   - ✅ Semantic analysis complete
   - 🌳 AST tree displayed
   - 📊 Symbol table shown

---

## 🐛 Quick Fixes

### Problem: "g++ not recognized"
**Solution:**
```powershell
# Install MinGW
choco install mingw -y

# Or download manually and add to PATH
$env:Path += ";C:\mingw64\bin"

# Restart PowerShell
```

### Problem: "Python fallback mode"
**Solution:**
```powershell
cd cpp_core
g++ -std=c++17 -O2 -o minilang_compiler.exe main.cpp
cd ..
```

### Problem: Compilation errors
**Solution:**
```powershell
# Ensure JSON library is downloaded
cd cpp_core
Test-Path json.hpp  # Should be True

# Try compilation with verbose output
g++ -std=c++17 -O2 -o minilang_compiler.exe main.cpp -v
```

---

## 📦 File Checklist

Before presenting, ensure you have:

- ✅ `cpp_core/minilang_compiler.exe` exists
- ✅ Web app runs: `streamlit run streamlit_app.py`
- ✅ All examples compile successfully
- ✅ No errors in console

---

## 🎓 For Presentation

**Show your professor:**

1. **C++ Source Code** (`cpp_core/*.h`, `main.cpp`)
2. **Compiled Executable** (`minilang_compiler.exe`)
3. **Test Compilation**:
   ```powershell
   echo "int x = 42; print(x);" | cpp_core\minilang_compiler.exe -
   ```
4. **Web Interface** (http://localhost:8501)

**Emphasize:**
- ✅ **All compilation logic is in C++** (scanner.h, parser.h, semantic.h)
- ✅ **Python is only for UI** (web interface)
- ✅ **Three complete phases** implemented in C++
- ✅ **Professional architecture** with JSON communication

---

## 🎯 Final Check

Run this command to verify everything:

```powershell
# Test C++ core
echo "int x = 10; int y = x + 5; print(y);" | cpp_core\minilang_compiler.exe -

# Should output JSON with:
# - "success": true
# - tokens array
# - ast object
# - symbol_table object
```

---

## 🚀 You're Ready!

Your compiler:
- ✅ Has a real C++ implementation
- ✅ Works correctly
- ✅ Has a beautiful interface
- ✅ Is professionally built

**Good luck with your presentation!** 🎓
