#!/usr/bin/env python3
from io import StringIO
import os
import sys
from src.atoms import ValueAtom
from src.error import print_error_help
from src.colors import BOLD, BRIGHT_YELLOW, GREEN, LOGO, RESET
from src.interpreter import execute, globalEnvironment

# === Global variables ===

USAGE = f"""{BRIGHT_YELLOW}Welcome to the {LOGO} {BRIGHT_YELLOW}interpreter!{RESET}

{BOLD}Usage:{RESET} mini (options) <file>

{BOLD}Options:{RESET}
    -h, --help      Print this help message and exit
    -r, --repl      Start the REPL
    --debug         Enable debug mode

{BOLD}Examples:{RESET}
    mini -r         Enter the REPL
    mini main.m     Evaluate the input file
"""


# Interpreter mode
def interpret(filepath: str, debug = False):
    if not os.path.exists(filepath):
        print_error_help(f"File '{filepath}' does not exist!")
    with open(filepath, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        _ = execute(f, globalEnvironment(), debug)

# Repl mode
def repl(debug = False):
    print(f"{BRIGHT_YELLOW}Welcome to the {LOGO} {BRIGHT_YELLOW}REPL!")
    env = globalEnvironment()
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            continue
        except KeyboardInterrupt:
            break
        if line == "":
            continue
        try:
            result = execute(StringIO(line), env, debug)
            if result is None: continue
            value, env = result
            if isinstance(value, ValueAtom) and value.type == "unit": continue
            print(value.formatted_str())
        except Exception as e:
            if debug:
                import traceback
                traceback.print_exc()
            else:
                print(e)

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
        sys.exit(0)

    # Evaluate
    elif len(args) > 1:
        print_error_help("Too many arguments, expected a single file!")
    elif len(args) == 1:
        interpret(args[-1], debug)
    else:
        print_error_help("Unknown option")

if __name__ == '__main__':
    main(sys.argv[1:])
