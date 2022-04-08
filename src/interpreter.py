from io import open, TextIOBase, StringIO
from .lexer import tokenize
from .parser import parse
from .evaluator import evaluate
from .environment import Environment
from .atoms import Atom, BuiltinFunctionAtom, TupleAtom, UnitAtom, ValueAtom

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
        print('    ' + '\n    '.join(str(e) for e in ast.expressions))
    result = evaluate(ast, env, debug)
    if debug:
        print("Result:", result)
    return result, env

def printValue(value: Atom, end = "\n"):
    if value is None or isinstance(value, UnitAtom):
        return
    elif isinstance(value, TupleAtom):
        print("(", end="")
        for i in range(len(value.value)):
            printValue(value.value[i], '')
            if i < len(value.value) - 1:
                print(", ", end="")
        print(")", end=end)
    elif isinstance(value, ValueAtom):
        if value.valueType == "string":
            print(f"'{value.value}'", end=end)
        elif value.valueType == "number":
            print(int(value.value) if value.value.is_integer() else value.value, end=end)
        else:
            print(value.value, end=end)
    else:
        print(value, end=end)

# Interpreter mode
def interpret(filepath: str, debug = False):
    with open(filepath, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        execute(f, globalEnvironment(), debug)

# Repl mode
def repl(debug = False):
    print("Welcome to the mini interpreter!")
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
            result, env = execute(StringIO(line), env, debug)
            printValue(result)
        except Exception as e:
            print(e)
            if debug:
                raise e
