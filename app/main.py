import sys

BUILTINS = {'exit', 'echo', 'type'}

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
                print(f"{name}: not found")
        else:
            print(f"{command}: command not found")



if __name__ == "__main__":
    main()
