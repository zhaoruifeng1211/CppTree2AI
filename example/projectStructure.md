# Project Structure

MyProject/
├── CMakeLists.txt
├── include/
│   └── mylib/
│       ├── A.hpp
├── src/
│   ├── main.cpp
│   └── A.cpp

# Header Include Analysis

## src/main.cpp
- #include "A.hpp"
- #include <iostream>

# CMakeLists.txt Analysis

## CMakeLists.txt
### Targets:
- [Executable] MyApp main.cpp utils.cpp
### Content:
```cmake
cmake_minimum_required(VERSION 3.16)
project(MyApp)
add_executable(MyApp main.cpp utils.cpp)
