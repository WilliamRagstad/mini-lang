from io import TextIOBase, open
import os
import llvmlite.ir as ir
import llvmlite.binding as llvm

from .ast import AtomicNode, IfNode, Node, ProgramNode
from .parser import Parser
from .lexer import Lexer


def compileFile(filepath: str, options):
    with open(filepath, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        program = compile(f, options)

    # All these initializations are required for code generation!
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    obj = target_machine.emit_object(program)
    print(obj)
    # Save the generated code to a file
    with open(filepath + ".o", mode='w', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        f.write(obj)
    target_machine.close()
    print("Building executable...")
    # Build the executable
    llvm.link_in_file(filepath + ".o")
    # Run GCC
    filename_path = os.path.splitext(filepath)[0]
    if os.system("gcc -o " + filename_path + " " + filepath + ".o") != 0:
        print("Compilation failed!")
    else:
        print("Done!")

# Types

bitTy = ir.IntType(1)
int8Ty = ir.IntType(8)
int32Ty = ir.IntType(32)
int64Ty = ir.IntType(64)
int8ptrTy = int8Ty.as_pointer()

# Globals

module = None

def compile(input: TextIOBase, options) -> ir.Module:
    global module
    print("Compiling...")
    debug = options["debug"]
    lexer = Lexer(input, debug)
    parser = Parser(lexer, debug)
    ast = parser.parse()
    # LLVM IR
    module = ir.Module("program")
    # https://clang.llvm.org/docs/CrossCompilation.html#target-triple
    module.triple = "x86_64-pc-linux-gnu"
    generate(ast)
    # TODO: Log statistics, performance analysis and benchmarks of compilation
    print("Generated module:")
    print(module)
    return module


def generate(ast: Node):
    global module
    if isinstance(ast, ProgramNode):
        b = ir.IRBuilder()
        b.append_basic_block("main")
        for n in ast.expressions:
            generate(n)
        return b.ret_void()
    elif isinstance(ast, AtomicNode):
        return generateAtomic(ast)
    elif isinstance(ast, IfNode):
        b = ir.IRBuilder()
        pred = generate(ast.condition)
        with b.if_else(pred) as (if_block, else_block):
            with if_block:
                generate(ast.if_body)
            with else_block:
                generate(ast.else_body)
    else:
        pass # raise Exception("Unknown AST node: " + str(ast))

def generateAtomic(ast: Node) -> ir.Value:
    if isinstance(ast, AtomicNode):
        if ast.valueType == "int":
            return ir.Constant(int32Ty, ast.value)
        elif ast.valueType == "bool":
            return ir.Constant(bitTy, 1 if ast.value else 0)
        elif ast.valueType == "unit":
            return ir.Undefined
        elif ast.valueType == "string":
            return ir.Constant(ir.ArrayType(int8Ty, len(ast.value)), bytearray(ast.value.encode("utf-8")))
        else:
            raise Exception("Unknown atomic type: " + str(ast))
    else:
        raise Exception("Unknown AST node: " + str(ast))

def generateCondition(ast: Node) -> bitTy:
    # Generate the condition and store it in a variable
    b = ir.IRBuilder()
    b.append_basic_block("condition")
