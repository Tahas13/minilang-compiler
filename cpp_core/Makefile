# MiniLang Compiler - C++ Core
# Authors: Shozab Mehdi (22k-4522), Taha Sharif (22k-4145)

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
TARGET = minilang_compiler.exe

all: $(TARGET)

$(TARGET): main.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) main.cpp

clean:
	del /Q $(TARGET)

.PHONY: all clean
