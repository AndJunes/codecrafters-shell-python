import sys
import os
from pathlib import Path

BUILTINS = {"exit", "echo", "type"}


def buscar_en_path(name: str) -> str | None:
    """Devuelve la ruta absoluta del primer ejecutable que matchee, o None."""
    path_env = os.environ.get("PATH", "")
    for directorio in path_env.split(os.pathsep):
        candidato = Path(directorio) / name
        if candidato.is_file() and os.access(candidato, os.X_OK):
            return str(candidato)
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
        elif command.startswith("echo "):
            print(command[5:])
        elif command.startswith("type "):
            name = command[5:]
            if name in BUILTINS:
                print(f"{name} is a shell builtin")
            else:
                ruta = buscar_en_path(name)
                if ruta:
                    print(f"{name} is {ruta}")
                else:
                    print(f"{name}: not found")
        else:
            print(f"{command}: command not found")

    if __name__ == "__main__":
        main()