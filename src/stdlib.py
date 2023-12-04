import math
import os
import subprocess

from .environment import Environment
from typing import Callable
from .atoms import Atom, BuiltinFunctionAtom, Atom, ValueAtom

# Helper functions
def addBuiltin(name, func: Callable[[list[Atom]], Atom], env: Environment):
    env.set(name, BuiltinFunctionAtom(name, func))

def expect_args(args: list[Atom], expected: list[int], name: str):
    if len(args) not in expected:
        expected_str = (", ".join(str(e) for e in expected[:-1]) +
                        " or " + str(expected[-1])
                        if len(expected) > 1
                        else expected[0])
        raise Exception(f"Function '{name}' expected {expected_str} arguments but got {len(args)}!")

def init_io(env: Environment):
    """
    Initialize standard IO functions.
    """
    def _print(args: list[Atom]) -> Atom:
        args = map(lambda a: a.raw_str(), args)
        print(*args)
        return ValueAtom("unit", None)
    def _input(args: list[Atom]) -> Atom:
        expect_args(args, [0, 1], "input")
        prompt = args[0].raw_str() if len(args) == 1 else ""
        return ValueAtom("string", input(prompt))
    addBuiltin("print", _print, env)
    addBuiltin("input", _input, env)

def init_sys(env: Environment):
    """
    Initialize system OS functions.
    """
    def _exit(args: list[Atom]) -> Atom:
        expect_args(args, [0, 1], "exit")
        code = args[0].value if len(args) == 1 else 0
        os._exit(code)
    def _system_run(args: list[Atom]) -> Atom:
        expect_args(args, [1, 2], "system_run")
        cmd = args[0].raw_str()
        shell = args[1].value if len(args) == 2 else True
        subprocess.call(cmd, shell=shell)
        return ValueAtom("unit", None)
    def _system_output(args: list[Atom]) -> Atom:
        expect_args(args, [1, 2], "system_output")
        cmd = args[0].raw_str()
        shell = args[1].value if len(args) == 2 else True
        return ValueAtom("string", subprocess.check_output(cmd, shell=shell).decode("utf-8"))
    addBuiltin("exit", _exit, env)
    addBuiltin("system_run", _system_run, env)
    addBuiltin("system_output", _system_output, env)

def init_fs(env: Environment):
    """
    Initialize file system functions.
    """
    def _dir_create(args: list[Atom]) -> Atom:
        expect_args(args, [1], "dir_create")
        path = args[0].raw_str()
        os.mkdir(path)
        return ValueAtom("unit", None)
    def _dir_remove(args: list[Atom]) -> Atom:
        expect_args(args, [1], "dir_remove")
        path = args[0].raw_str()
        os.rmdir(path)
        return ValueAtom("unit", None)
    def _dir_exists(args: list[Atom]) -> Atom:
        expect_args(args, [1], "dir_exists")
        path = args[0].raw_str()
        return ValueAtom("bool", os.path.exists(path) and os.path.isdir(path))
    def _dir_files(args: list[Atom]) -> Atom:
        expect_args(args, [1], "dir_files")
        path = args[0].raw_str()
        return ValueAtom("list", os.listdir(path))
    def _file_create(args: list[Atom]) -> Atom:
        expect_args(args, [1], "file_create")
        path = args[0].raw_str()
        open(path, 'w').close()
        return ValueAtom("unit", None)
    def _file_remove(args: list[Atom]) -> Atom:
        expect_args(args, [1], "file_remove")
        path = args[0].raw_str()
        os.remove(path)
        return ValueAtom("unit", None)
    def _file_read(args: list[Atom]) -> Atom:
        expect_args(args, [1], "file_read")
        path = args[0].raw_str()
        with open(path, 'r') as f:
            return ValueAtom("string", f.read())
    def _file_write(args: list[Atom]) -> Atom:
        expect_args(args, [2], "file_write")
        path = args[0].raw_str()
        data = args[1].raw_str()
        with open(path, 'w') as f:
            f.write(data)
            return ValueAtom("unit", None)
    def _file_append(args: list[Atom]) -> Atom:
        expect_args(args, [2], "file_append")
        path = args[0].raw_str()
        data = args[1].raw_str()
        with open(path, 'a') as f:
            f.write(data)
            return ValueAtom("unit", None)
    def _file_exists(args: list[Atom]) -> Atom:
        expect_args(args, [1], "file_exists")
        path = args[0].raw_str()
        return ValueAtom("bool", os.path.exists(path) and os.path.isfile(path))
    addBuiltin("dir_create", _dir_create, env)
    addBuiltin("dir_remove", _dir_remove, env)
    addBuiltin("dir_exists", _dir_exists, env)
    addBuiltin("file_create", _file_create, env)
    addBuiltin("file_remove", _file_remove, env)
    addBuiltin("file_read", _file_read, env)
    addBuiltin("file_write", _file_write, env)
    addBuiltin("file_append", _file_append, env)
    addBuiltin("file_exists", _file_exists, env)
    addBuiltin("dir_files", _dir_files, env)

def init_math(env: Environment):
    """
    Initialize math functions.
    """
    def _abs(args: list[Atom]) -> Atom:
        expect_args(args, [1], "abs")
        return ValueAtom("number", abs(args[0].value))
    def _ceil(args: list[Atom]) -> Atom:
        expect_args(args, [1], "ceil")
        return ValueAtom("number", math.ceil(args[0].value))
    def _floor(args: list[Atom]) -> Atom:
        expect_args(args, [1], "floor")
        return ValueAtom("number", math.floor(args[0].value))
    def _round(args: list[Atom]) -> Atom:
        expect_args(args, [1], "round")
        return ValueAtom("number", round(args[0].value))
    def _sqrt(args: list[Atom]) -> Atom:
        expect_args(args, [1], "sqrt")
        return ValueAtom("number", math.sqrt(args[0].value))
    def _sin(args: list[Atom]) -> Atom:
        expect_args(args, [1], "sin")
        return ValueAtom("number", math.sin(args[0].value))
    def _cos(args: list[Atom]) -> Atom:
        expect_args(args, [1], "cos")
        return ValueAtom("number", math.cos(args[0].value))
    def _tan(args: list[Atom]) -> Atom:
        expect_args(args, [1], "tan")
        return ValueAtom("number", math.tan(args[0].value))
    addBuiltin("abs", _abs, env)
    addBuiltin("ceil", _ceil, env)
    addBuiltin("floor", _floor, env)
    addBuiltin("round", _round, env)
    addBuiltin("sqrt", _sqrt, env)
    addBuiltin("sin", _sin, env)
    addBuiltin("cos", _cos, env)
    addBuiltin("tan", _tan, env)

def init_type(env: Environment):
    """
    Initialize type functions.
    """
    def _type(args: list[Atom]) -> Atom:
        expect_args(args, [1], "type")
        return ValueAtom("string", args[0].type)
    def _is_type(args: list[Atom]) -> Atom:
        expect_args(args, [2], "is_type")
        return ValueAtom("bool", args[0].type == args[1].raw_str())
    addBuiltin("type", _type, env)
    addBuiltin("is_type", _is_type, env)

def init_list(env: Environment):
    """
    Initialize list operations.
    """
    def _list_append(args: list[Atom]) -> Atom:
        expect_args(args, [2], "list_append")
        args[0].elements.append(args[1])
        return ValueAtom("unit", None)
    def _list_remove(args: list[Atom]) -> Atom:
        expect_args(args, [2], "list_remove")
        args[0].elements.remove(args[1])
        return ValueAtom("unit", None)
    def _list_size(args: list[Atom]) -> Atom:
        expect_args(args, [1], "list_size")
        return ValueAtom("number", len(args[0].elements))
    def _list_contains(args: list[Atom]) -> Atom:
        expect_args(args, [2], "list_contains")
        return ValueAtom("bool", args[1] in args[0].elements)
    def _list_index(args: list[Atom]) -> Atom:
        expect_args(args, [2], "list_index")
        return ValueAtom("number", args[0].elements.index(args[1]))
    def _list_slice(args: list[Atom]) -> Atom:
        expect_args(args, [3], "list_slice")
        return ValueAtom("list", args[0].elements[args[1].value:args[2].value])
    addBuiltin("list_append", _list_append, env)
    addBuiltin("list_remove", _list_remove, env)
    addBuiltin("list_size", _list_size, env)
    addBuiltin("list_contains", _list_contains, env)
    addBuiltin("list_index", _list_index, env)
    addBuiltin("list_slice", _list_slice, env)

def init_tuple(env: Environment):
    """
    Initialize tuple operations.
    """
    def _tuple_size(args: list[Atom]) -> Atom:
        expect_args(args, [1], "tuple_size")
        return ValueAtom("number", len(args[0].elements))
    def _tuple_contains(args: list[Atom]) -> Atom:
        expect_args(args, [2], "tuple_contains")
        return ValueAtom("bool", args[1] in args[0].elements)
    def _tuple_index(args: list[Atom]) -> Atom:
        expect_args(args, [2], "tuple_index")
        return ValueAtom("number", args[0].elements.index(args[1]))
    def _tuple_slice(args: list[Atom]) -> Atom:
        expect_args(args, [3], "tuple_slice")
        return ValueAtom("tuple", args[0].elements[args[1].value:args[2].value])
    addBuiltin("tuple_size", _tuple_size, env)
    addBuiltin("tuple_contains", _tuple_contains, env)
    addBuiltin("tuple_index", _tuple_index, env)
    addBuiltin("tuple_slice", _tuple_slice, env)

def init_map(env: Environment):
    """
    Initialize map operations.
    """
    def _map_size(args: list[Atom]) -> Atom:
        expect_args(args, [1], "map_size")
        return ValueAtom("number", len(args[0].value))
    def _map_contains(args: list[Atom]) -> Atom:
        expect_args(args, [2], "map_contains")
        return ValueAtom("bool", args[1] in args[0].pairs)
    def _map_keys(args: list[Atom]) -> Atom:
        expect_args(args, [1], "map_keys")
        return ValueAtom("list", list(args[0].pairs.keys()))
    def _map_values(args: list[Atom]) -> Atom:
        expect_args(args, [1], "map_values")
        return ValueAtom("list", list(args[0].pairs.values()))
    def _map_get(args: list[Atom]) -> Atom:
        expect_args(args, [2], "map_get")
        return args[0].pairs[args[1]]
    def _map_set(args: list[Atom]) -> Atom:
        expect_args(args, [3], "map_set")
        args[0].pairs[args[1]] = args[2]
        return ValueAtom("unit", None)
    def _map_remove(args: list[Atom]) -> Atom:
        expect_args(args, [2], "map_remove")
        del args[0].pairs[args[1]]
        return ValueAtom("unit", None)
    addBuiltin("map_size", _map_size, env)
    addBuiltin("map_contains", _map_contains, env)
    addBuiltin("map_keys", _map_keys, env)
    addBuiltin("map_values", _map_values, env)
    addBuiltin("map_get", _map_get, env)
    addBuiltin("map_set", _map_set, env)
    addBuiltin("map_remove", _map_remove, env)

def init_stdlib(env: Environment):
    """
    Initialize the standard library.
    """
    init_io(env)
    init_sys(env)
    init_fs(env)
    init_math(env)
    init_type(env)
    init_list(env)
    init_tuple(env)
    init_map(env)
