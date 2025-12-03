@echo off
REM MiniLang Compiler - Build Script
REM Authors: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)

echo =====================================
echo   MiniLang C++ Compiler Builder
echo =====================================
echo.

REM Check if g++ is available
where g++ >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: g++ compiler not found!
    echo.
    echo Please install MinGW:
    echo   choco install mingw
    echo.
    echo Or download from: https://www.mingw-w64.org/
    pause
    exit /b 1
)

echo [1/3] Checking g++ version...
g++ --version | findstr "g++"
echo.

cd cpp_core

REM Download JSON library if not exists
if not exist json.hpp (
    echo [2/3] Downloading JSON library...
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/nlohmann/json/develop/single_include/nlohmann/json.hpp' -OutFile 'json.hpp'"
    echo.
) else (
    echo [2/3] JSON library already exists
    echo.
)

REM Compile
echo [3/3] Compiling C++ compiler core...
g++ -std=c++17 -O2 -o minilang_compiler.exe main.cpp

if %errorlevel% equ 0 (
    echo.
    echo =====================================
    echo   BUILD SUCCESSFUL!
    echo =====================================
    echo.
    echo Executable: cpp_core\minilang_compiler.exe
    echo.
    echo Testing compiler...
    echo int x = 42; print(x); | minilang_compiler.exe -
    echo.
    echo Ready to use!
    cd ..
) else (
    echo.
    echo =====================================
    echo   BUILD FAILED!
    echo =====================================
    echo.
    echo Check the error messages above.
    cd ..
    pause
    exit /b 1
)

pause
