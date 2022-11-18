import sys
import subprocess
from pathlib import Path
import shutil
import os

deps: set[str] = set()

def add_deps(file: str) -> None:
    result = subprocess.run(['dumpbin.exe', '/DEPENDENTS', file], capture_output=True, text=True).stdout
    splitted = result.splitlines()
    
    in_section = False

    new_deps = set()
    for line in splitted:
        if 'Image has the following dependencies:' in line:
            in_section = True
            continue

        if 'Summary' in line and in_section:
            break

        if in_section:
            stripped = line.strip()
            if stripped:
                assert stripped.endswith('.dll')
                new_deps.add(stripped)

    to_add = new_deps - deps
    deps.update(to_add)
    for dep in to_add:
        add_deps(dep)

if __name__ == '__main__':
    assert len(sys.argv) == 2
    filename = sys.argv[1]
    add_deps(filename)

    extract_path = Path('extracted')
    extract_path.mkdir(parents=True, exist_ok=True)

    for dll in deps:
        try:
            shutil.copy(dll, os.path.join(extract_path, dll))
        except FileNotFoundError:
            pass