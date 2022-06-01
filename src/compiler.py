from io import open
import llvmlite.ir as ir


from .ast import Node
from .parser import Parser
from .lexer import Lexer

def compile(filepath: str, options):
    print("Compiling...")
    with open(filepath, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        debug = options["debug"]
        lexer = Lexer(f, debug)
        parser = Parser(lexer, debug)
        ast = parser.parse()
    program = generate(ast)
    print("Done!")
    print("Successfully generated program:")
    print(program)
    return program


def generate(ast: Node):
    pass
