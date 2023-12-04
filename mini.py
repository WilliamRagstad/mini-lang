#!/usr/bin/env python3
import sys
from src.interpreter import interpret, repl

# === Global variables ===

USAGE = f"""Welcome to the mini interpreter!
Usage: mini (options) <file>

Options:
    -h, --help      Print this help message and exit
    -r, --repl      Start the REPL
    --debug     Enable debug mode

Examples:
    mini -r         Enter the REPL
    mini main.m     Evaluate the input file
"""

# === Helper functions ===
def print_error(msg: str):
    print(f"{msg}, try -h or --help to show usage.")
    sys.exit(1)

# === Main ===
def main(args: list):
    debug = False
    if '--debug' in args:
        debug = True
        args.remove('--debug')
    if len(args) == 0 or '-h' in args or '--help' in args:
        print(USAGE)
        sys.exit(0)
    elif '-r' in args or '--repl' in args:
        repl(debug)

    # Evaluate
    elif len(args) > 1:
        print_error("Too many arguments")
    elif len(args) == 1:
        interpret(args[-1], debug)
    else:
        print_error("Unknown option")

if __name__ == '__main__':
    main(sys.argv[1:])
