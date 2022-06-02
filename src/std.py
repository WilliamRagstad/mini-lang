
import math
import os
import subprocess
from llvmlite import ir, binding

from .atoms import BuiltinFunctionAtom, ValueAtom
from .environment import Environment


# Helper function
def addBuiltin(name, func, env):
    env.set(name, BuiltinFunctionAtom(name, func))


def addStdlib(env: Environment):
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

def compileStdlib(module: ir.Module):
    ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.IntType(32)]), "print")
