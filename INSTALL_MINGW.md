# Alternative: Install MinGW Without Chocolatey

## Option 1: WinLibs (Easiest - No extraction needed)

1. Download: https://winlibs.com/
2. Click: "Download -> GCC 13.2.0 + LLVM/Clang/LLD/LLDB 17.0.6 + MinGW-w64 11.0.1 (MSVCRT) - release 1"
3. Extract to `C:\mingw64`
4. Add to PATH:
   ```powershell
   $env:Path += ";C:\mingw64\bin"
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\mingw64\bin", "User")
   ```
5. Test: `g++ --version`

## Option 2: MSYS2 (Recommended)

1. Download: https://www.msys2.org/
2. Run installer -> Install to `C:\msys64`
3. Open "MSYS2 MSYS" from Start Menu
4. Run: `pacman -S mingw-w64-x86_64-gcc`
5. Add to PATH:
   ```powershell
   $env:Path += ";C:\msys64\mingw64\bin"
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\msys64\mingw64\bin", "User")
   ```

## Option 3: TDM-GCC (Simple installer)

1. Download: https://jmeubank.github.io/tdm-gcc/
2. Run installer
3. Follow wizard (default options)
4. Automatically adds to PATH

## Option 4: Use Visual Studio (If installed)

If you have Visual Studio with C++ tools:

```powershell
# Find Visual Studio Developer Command Prompt
# Then use cl.exe instead of g++
cl /std:c++17 /EHsc /O2 /Fe:minilang_compiler.exe main.cpp
```

## Quick Test After Installation

```powershell
# Restart PowerShell first!
g++ --version

# If it works, compile:
cd C:\Users\TAHA\Documents\cc_project\cpp_core
g++ -std=c++17 -O2 -o minilang_compiler.exe main.cpp
```

## I Recommend: WinLibs (Fastest)

1. Go to: https://winlibs.com/
2. Download ZIP (no installation needed)
3. Extract anywhere (e.g., `C:\mingw64`)
4. Add to PATH
5. Done!
