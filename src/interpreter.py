from io import open, TextIOBase, StringIO

from .parser import Parser
from .lexer import Lexer
from .evaluator import evaluate
from .environment import Environment, globalEnvironment
from .atoms import ValueAtom
from .std import addStdlib

def execute(input: TextIOBase, env: Environment, options):
    debug = options["debug"]
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
def interpret(filepath: str, options):
    with open(filepath, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        execute(f, addStdlib(globalEnvironment()), options)

# Repl mode
def repl(options):
    print("Welcome to the mini interpreter!")
    env = addStdlib(globalEnvironment())
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
            result, env = execute(StringIO(line), env, options)
            if isinstance(result, ValueAtom) and result.valueType == "unit": continue
            print(str(result))
        except Exception as e:
            print(e)
            if options["debug"]:
                raise e
