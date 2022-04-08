from io import open, TextIOBase, StringIO
from .lexer import tokenize
from .parser import parse
from .evaluator import evaluate
from .environment import Environment
from .atoms import Atom, BuiltinFunctionAtom, UnitAtom, ValueAtom

# Helper functions
def globalEnvironment():
    env = Environment("global", None)
    def _print(*args):
        print(*args)
        return UnitAtom()
    def _input(p):
        return ValueAtom("string", input(p))
    env.set("print", BuiltinFunctionAtom("print", _print))
    env.set("input", BuiltinFunctionAtom("input", _input))
    return env

def execute(input: TextIOBase, env: Environment, debug = False):
    tokens = tokenize(input, debug)
    if debug:
        print("Tokens:")
        print('    ' + '\n    '.join(str(t) for t in tokens))
    ast = parse(tokens, debug)
    if debug:
        print("AST:")
        print(ast)
    result = evaluate(ast, env, debug)
    if debug:
        print("Result:", result)
    return result, env

def printValue(value: Atom):
    if value is None or isinstance(value, UnitAtom):
        return
    if isinstance(value, ValueAtom):
        if value.valueType == "string":
            print(f"'{value.value}'")
        elif value.valueType == "number":
            print(int(value.value) if value.value.is_integer() else value.value)
        else:
            print(value.value)
    else:
        print(value)

# Interpreter mode
def interpret(filepath: str, debug = False):
    with open(filepath, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        execute(f, globalEnvironment(), debug)

# Repl mode
def repl(debug = False):
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
        result, env = execute(StringIO(line), env, debug)
        printValue(result)