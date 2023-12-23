from io import TextIOBase

from .stdlib import init_stdlib

from .error import print_error

from .parser import Parser
from .lexer import Lexer
from .evaluator import evaluate
from .environment import Environment


def globalEnvironment():
    env = Environment("global", None)
    init_stdlib(env)
    return env

def execute(input: TextIOBase, env: Environment, debug = False):
    try:
        lexer = Lexer(input, debug)
        parser = Parser(lexer, debug)
        if debug:
            print("== Tokens ==")
        ast = parser.parse()
        if debug:
            print("== AST ==")
            print('  ' + '\n  '.join(str(e) for e in ast.expressions))
            print("== Evaluation ==")
        result = evaluate(ast, env, debug)
        if debug:
            print("== END ==")
            print("Result:", result, "//", result.type)
        return result, env # Return the result and the environment
    except Exception as e:
        if debug:
            import traceback
            traceback.print_exc()
        else:
            print_error(e)
        return None # Return None if an error occured
