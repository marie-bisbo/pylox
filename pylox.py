import sys
import cmd
from typing import IO

had_error = False

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

def run_file(path: str) -> None:
    if had_error:
        sys.exit(65)

def run(line: str) -> None:
    for word in line.split():
        print(word)

def run_prompt() -> None:
    had_error = False
    prompt = Prompt()
    prompt.cmdloop("Starting prompt...")

def error(line: int, message: str) -> None:
    report(line, "", message)

def report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error {where} : {message}")
    had_error = True

if __name__ == "__main__":
    main()

