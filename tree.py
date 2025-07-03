import os
import re

# Common non-source directories to exclude
DEFAULT_IGNORED_DIRS = {
    'build', '.git', '.vscode', 'out', 'bin', 'obj'
}

def should_ignore_dir(dirname, exclude_build):
    if not exclude_build:
        return False
    if dirname in DEFAULT_IGNORED_DIRS:
        return True
    if dirname.startswith('cmake-build'):
        return True
    return False

def generate_tree(root, prefix='', exclude_build=False):
    lines = []
    entries = sorted(os.listdir(root))
    entries = [e for e in entries if not e.startswith('.') or e in {'.vscode', '.git'}]
    for i, entry in enumerate(entries):
        path = os.path.join(root, entry)
        if os.path.isdir(path) and should_ignore_dir(entry, exclude_build):
            continue
        connector = '└── ' if i == len(entries) - 1 else '├── '
        lines.append(f"{prefix}{connector}{entry}")
        if os.path.isdir(path):
            extension = '    ' if i == len(entries) - 1 else '│   '
            lines.extend(generate_tree(path, prefix + extension, exclude_build))
    return lines

def extract_includes(file_path):
    includes = []
    pattern = re.compile(r'#include\s+[<"](.+?)[">]')
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    includes.append(match.group(1))
    except Exception as e:
        includes.append(f"# Error reading file: {e}")
    return includes

def extract_cmake_targets(file_path):
    targets = []
    pattern_exec = re.compile(r'add_executable\s*\(([^)]+)\)', re.IGNORECASE)
    pattern_lib = re.compile(r'add_library\s*\(([^)]+)\)', re.IGNORECASE)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for match in pattern_exec.findall(content):
                targets.append(f"[Executable] {match.strip()}")
            for match in pattern_lib.findall(content):
                targets.append(f"[Library] {match.strip()}")
    except Exception as e:
        targets.append(f"# Error reading CMakeLists.txt: {e}")
        content = ""
    return targets, content

def scan_project(root_dir, exclude_build=False):
    output_lines = []
    output_lines.append("# Project Structure\n")
    output_lines.append(os.path.basename(root_dir) + "/")
    output_lines += generate_tree(root_dir, exclude_build=exclude_build)

    output_lines.append("\n# Header Include Analysis\n")
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not should_ignore_dir(d, exclude_build)]
        for file in filenames:
            if file.endswith(('.cpp', '.cc', '.c', '.hpp', '.h')):
                full_path = os.path.join(dirpath, file)
                rel_path = os.path.relpath(full_path, root_dir)
                includes = extract_includes(full_path)
                output_lines.append(f"\n## {rel_path}")
                for inc in includes:
                    output_lines.append(f"- #include \"{inc}\"")

    output_lines.append("\n# CMakeLists.txt Analysis\n")
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not should_ignore_dir(d, exclude_build)]
        for file in filenames:
            if file == "CMakeLists.txt":
                full_path = os.path.join(dirpath, file)
                rel_path = os.path.relpath(full_path, root_dir)
                targets, content = extract_cmake_targets(full_path)
                output_lines.append(f"\n## {rel_path}")
                if targets:
                    output_lines.append("### Targets:")
                    for t in targets:
                        output_lines.append(f"- {t}")
                output_lines.append("### Content:")
                output_lines.append("```cmake")
                output_lines.append(content.strip())
                output_lines.append("```")

    return '\n'.join(output_lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate C++ project structure, includes, and CMake overview")
    parser.add_argument("path", help="Path to the root directory of your C++ project")
    parser.add_argument("-o", "--output", help="Output markdown file name", default="project_summary.md")
    parser.add_argument("--exclude-build", action="store_true", help="Exclude build/.git/cmake-build*/ folders")
    args = parser.parse_args()

    summary = scan_project(args.path, exclude_build=args.exclude_build)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"✅ Project summary and include/CMake analysis saved to: {args.output}")
