import math
import os
import subprocess
from io import open, TextIOBase, StringIO

from .parser import Parser
from .lexer import Lexer
from .evaluator import evaluate
from .environment import Environment
from .atoms import BuiltinFunctionAtom, ValueAtom

# Helper functions
def addBuiltin(name, func, env):
    env.set(name, BuiltinFunctionAtom(name, func))

def globalEnvironment():
    env = Environment("global", None)
    def _print(*args):
        print(*args)
        return ValueAtom("unit", None)
    addBuiltin("print", _print, env)
    addBuiltin("input", lambda p: ValueAtom("string", input(p)), env)
    # System functions
    def _system_run(cmd, shell):
        subprocess.call(cmd, shell=shell)
        return ValueAtom("unit", None)
    def _system_output(cmd, shell):
        return ValueAtom("string", subprocess.check_output(cmd, shell=shell).decode("utf-8"))
    addBuiltin("exit", lambda c: os._exit(c), env)
    addBuiltin("system_run", _system_run, env)
    addBuiltin("system_output", _system_output, env)
    # File system functions
    def _file_read(path):
        with open(path, 'r') as f:
            return ValueAtom("string", f.read())
    def _file_write(path, data):
        with open(path, 'w') as f:
            f.write(data)
            return ValueAtom("unit", None)
    def _file_append(path, data):
        with open(path, 'a') as f:
            f.write(data)
            return ValueAtom("unit", None)
    def _mkdir(path):
        os.mkdir(path)
        return ValueAtom("unit", None)
    def _rmdir(path):
        os.rmdir(path)
        return ValueAtom("unit", None)
    def _mkfile(path):
        open(path, 'w').close()
        return ValueAtom("unit", None)
    def _rmFile(path):
        os.remove(path)
        return ValueAtom("unit", None)
    addBuiltin("dir_create", _mkdir, env)
    addBuiltin("dir_remove", _rmdir, env)
    addBuiltin("file_create", _mkfile, env)
    addBuiltin("file_remove", _rmFile, env)
    addBuiltin("file_read", _file_read, env)
    addBuiltin("file_write", _file_write, env)
    addBuiltin("file_append", _file_append, env)
    addBuiltin("file_exists", lambda path: ValueAtom("bool", os.path.exists(path)), env)
    addBuiltin("is_file", lambda path: ValueAtom("bool", os.path.isfile(path)), env)
    addBuiltin("is_dir", lambda path: ValueAtom("bool", os.path.isdir(path)), env)
    addBuiltin("dir_files", lambda path: ValueAtom("list", os.listdir(path)), env)
    # Standard input/output functions
    # Math functions
    addBuiltin("sqrt", lambda x: ValueAtom("number", x ** 0.5), env)
    addBuiltin("sin", lambda x: ValueAtom("number", math.sin(x)), env)
    addBuiltin("cos", lambda x: ValueAtom("number", math.cos(x)), env)
    addBuiltin("tan", lambda x: ValueAtom("number", math.tan(x)), env)
    return env

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
        execute(f, globalEnvironment(), options)

# Repl mode
def repl(options):
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
            result, env = execute(StringIO(line), env, options)
            if isinstance(result, ValueAtom) and result.valueType == "unit": continue
            print(str(result))
        except Exception as e:
            print(e)
            if options["debug"]:
                raise e
