import sys
import os
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
            command = input()
        except EOFError:
            break

        if command == "exit":
            break
        elif command.startswith("cd "):
            path = command[3:]
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f'{command}: {path}: No such file or directory')
        elif command == 'pwd':
            print(os.getcwd())
        elif command.startswith("echo "):
            print(command[5:])
        elif command.startswith("type "):
            name = command[5:]
            if name in BUILTINS:
                print(f"{name} is a shell builtin")
            else:
                executable_path = find_in_path(name)
                if executable_path:
                    print(f"{name} is {executable_path}")
                else:
                    print(f"{name}: not found")
        else:
            parts = command.split()
            if parts and find_in_path(parts[0]):
                subprocess.run(parts)
            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()