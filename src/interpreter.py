from io import open, TextIOBase, StringIO

from .parser import Parser
from .lexer import Lexer
from .evaluator import evaluate
from .environment import Environment
from .atoms import BuiltinFunctionAtom, ValueAtom

# Helper functions
def globalEnvironment():
    env = Environment("global", None)
    def _print(*args):
        print(*args)
        return ValueAtom("unit", None)
    def _input(p):
        return ValueAtom("string", input(p))
    env.set("print", BuiltinFunctionAtom("print", _print))
    env.set("input", BuiltinFunctionAtom("input", _input))
    return env

def execute(input: TextIOBase, env: Environment, debug = False):
    lexer = Lexer(input, debug)
    parser = Parser(lexer, debug)
    if debug:
        print("== Tokens ==")
    ast = parser.parse()
    if debug:
        print("== AST ==")
        print('    ' + '\n    '.join(str(e) for e in ast.expressions))
        print("== Evaluation ==")
    result = evaluate(ast, env, debug)
    if debug:
        print("== END ==")
        print("Result:", result)
    return result, env

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
            if isinstance(result, ValueAtom) and result.valueType == "unit": continue
            print(str(result))
        except Exception as e:
            print(e)
            if debug:
                raise e
