import sys
import os
import shlex
import subprocess
from pathlib import Path

BUILTINS = {"exit", "echo", "type", "pwd", "cd"}


def find_in_path(name: str) -> str | None:
    """Return the absolute path of the first matching executable, or None."""
    path_env = os.environ.get("PATH", "")
    for directory in path_env.split(os.pathsep):
        candidate = Path(directory) / name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        try:
            line = input()
        except EOFError:
            break

        try:
            tokens = shlex.split(line, posix=True)
        except ValueError as e:
            print(f"shell: syntax error: {e}", file=sys.stderr)
            continue

        if not tokens:
            continue

        name = tokens[0]
        args = tokens[1:]

        if name == "exit":
            break
        elif name == "pwd":
            print(os.getcwd())
        elif name == "cd":
            if not args:
                continue
            path = args[0]
            target = os.path.expanduser(path)
            try:
                os.chdir(target)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
        elif name == "echo":
            print(" ".join(args))
        elif name == "type":
            if not args:
                continue
            target_name = args[0]
            if target_name in BUILTINS:
                print(f"{target_name} is a shell builtin")
            else:
                executable_path = find_in_path(target_name)
                if executable_path:
                    print(f"{target_name} is {executable_path}")
                else:
                    print(f"{target_name}: not found")
        else:
            if find_in_path(name):
                subprocess.run([name, *args])
            else:
                print(f"{line}: command not found")


if __name__ == "__main__":
    main()