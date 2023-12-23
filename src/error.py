
import sys

from .colors import BRIGHT_BLACK, RED, RESET


def print_error(msg: str):
    print(f"{RED}Error: {msg}{RESET}")


def print_error_help(msg: str, exit = True):
    print_error(msg)
    print(f"\n{BRIGHT_BLACK}Try -h or --help to show usage.{RESET}")
    if exit: sys.exit(1)
