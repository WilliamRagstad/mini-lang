#!/usr/bin/env python3
import sys
from src.error import print_error_help
from src.colors import BOLD, BRIGHT_YELLOW, GREEN, RED, RESET, YELLOW
from src.interpreter import interpret, repl

# === Global variables ===

USAGE = f"""{BRIGHT_YELLOW}Welcome to the {GREEN}mini{BRIGHT_YELLOW} interpreter!{RESET}

{BOLD}Usage:{RESET} mini (options) <file>

{BOLD}Options:{RESET}
    -h, --help      Print this help message and exit
    -r, --repl      Start the REPL
    --debug     Enable debug mode

{BOLD}Examples:{RESET}
    mini -r         Enter the REPL
    mini main.m     Evaluate the input file
"""

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
