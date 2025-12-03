# Build script for Windows
# Compile the C++ compiler core

Write-Host "Building MiniLang C++ Compiler Core..." -ForegroundColor Green

# Check if g++ is available
if (!(Get-Command g++ -ErrorAction SilentlyContinue)) {
    Write-Host "Error: g++ not found. Please install MinGW or MSYS2." -ForegroundColor Red
    exit 1
}

# Download JSON library if not exists
if (!(Test-Path "cpp_core\json.hpp")) {
    Write-Host "Downloading JSON library..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/nlohmann/json/develop/single_include/nlohmann/json.hpp" -OutFile "cpp_core\json.hpp"
}

# Compile
Write-Host "Compiling..." -ForegroundColor Yellow
g++ -std=c++17 -Wall -Wextra -O2 -o cpp_core\minilang_compiler.exe cpp_core\main.cpp

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful! Executable: cpp_core\minilang_compiler.exe" -ForegroundColor Green
} else {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}
