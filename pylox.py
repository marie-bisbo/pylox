import sys
import cmd
from typing import IO

class Prompt(cmd.Cmd):
    prompt = "> "

    def do_hello(self, arg: str) -> None:
        print(f"Hello {arg}!")

    def default(self, line: str) -> None:
        run(line)

    def do_quit(self, arg: str) -> None:
        sys.exit(1)

    def do_EOF(self, line):
        return True

def main() -> None:
    num_arguments = len(sys.argv) - 1
    if num_arguments > 1:
        sys.exit(64)
    elif num_arguments == 1:
        run_file(sys.argv[0])
    else:
        run_prompt()

def run(line: str) -> None:
    for word in line.split():
        print(word)

def run_file(path: str) -> None:
    pass

def run_prompt() -> None:
    prompt = Prompt()
    prompt.cmdloop("Starting prompt...")

if __name__ == "__main__":
    main()

