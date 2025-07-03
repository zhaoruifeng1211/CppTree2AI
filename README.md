# 🛠️ CppTree2AI (C++ Project Summary Generator)
Project structure tree generated for AI-assisted analysis of C++ projects

This Python script generates a Markdown summary of a C++ project, including:

- 📁 Project directory structure (with optional exclusion of build directories)
- 📎 `#include` dependencies from each `.cpp` / `.hpp` / `.h` file
- ⚙️ Contents and target declarations (`add_executable`, `add_library`) from all `CMakeLists.txt` files

This summary is useful for:
- Understanding project organization, especially when working with conversational AI assistants
- Refactoring and modularization
- Sharing concise overviews without exposing source code

---

## 🔧 Features

- Recursively traverses the entire project directory
- Detects and extracts `#include` statements from source/header files
- Parses all `CMakeLists.txt` to extract build targets and full contents
- Supports optional exclusion of build directories (e.g., `build`, `cmake-build-*`, `.git`)
- Outputs a single Markdown file for easy sharing or review

---

## 📦 Requirements

- Python 3.6+

No external dependencies are required.

---

## 🚀 Usage

### 1. Command line

```bash
python generate_project_summary.py /path/to/your/project -o summary.md --exclude-build
