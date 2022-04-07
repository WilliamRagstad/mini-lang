from io import open, TextIOBase, StringIO
from .lexer import tokenize
from .parser import parse
from .evaluator import evaluate
from .environment import Environment
from .atoms import BuiltinFunctionAtom

# Helper functions
def globalEnvironment():
    env = Environment("global", None)
    env.set("print", BuiltinFunctionAtom("print", lambda *args: print(*args)))
    env.set("input", BuiltinFunctionAtom("input", lambda p: input(p)))
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
        print("Result:")
        print(result)
    return result, env

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
        if line == "":
            continue
        result = execute(StringIO(line), env, debug)
        if result is not None:
            print(result)