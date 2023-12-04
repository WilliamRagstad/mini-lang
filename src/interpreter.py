import os
from io import open, TextIOBase, StringIO

from .stdlib import init_stdlib

from .error import print_error, print_error_help

from .colors import BRIGHT_YELLOW, GREEN, RESET

from .parser import Parser
from .lexer import Lexer
from .evaluator import evaluate
from .environment import Environment
from .atoms import ValueAtom


def globalEnvironment():
    env = Environment("global", None)
    init_stdlib(env)
    return env

def execute(input: TextIOBase, env: Environment, debug = False):
    lexer = Lexer(input, debug)
    parser = Parser(lexer, debug)
    if debug:
        print("== Tokens ==")
    ast = parser.parse()
    if debug:
        print("== AST ==")
        print('  ' + '\n  '.join(str(e) for e in ast.expressions))
        print("== Evaluation ==")
    try:
        result = evaluate(ast, env, debug)
    except Exception as e:
        if debug:
            import traceback
            traceback.print_exc()
        else:
            print_error(e)
        return None # Return None if an error occured
    if debug:
        print("== END ==")
        print("Result:", result, "//", result.type)
    return result, env

# Interpreter mode
def interpret(filepath: str, debug = False):
    if not os.path.exists(filepath):
        print_error_help(f"File '{filepath}' does not exist!")
    with open(filepath, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        _ = execute(f, globalEnvironment(), debug)

# Repl mode
def repl(debug = False):
    print(f"{BRIGHT_YELLOW}Welcome to the {GREEN}mini{BRIGHT_YELLOW} REPL!{RESET}")
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