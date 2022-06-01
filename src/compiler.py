from io import TextIOBase, open
import os
from llvmlite import ir, binding

from .options import Options

from .ast import AtomicNode, BinaryNode, IfNode, Node, ProgramNode
from .parser import Parser
from .lexer import Lexer


def compileFile(filepath: str, options: Options):
    printingAsmOrIR = options.printAssembly or options.printIR
    if not printingAsmOrIR: print("Compiling...")
    with open(filepath, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        program = compile(f, options)

    # TODO: Log statistics, performance analysis and benchmarks of compilation

    if options.printIR:
        if options.debug: print("\n== Generated LLVM IR: Module ==")
        print(program)
        if options.debug: print("===============================")

    # All these initializations are required for code generation!
    binding.initialize()
    binding.initialize_native_target()
    binding.initialize_native_asmprinter()

    # Create a target machine representing the host
    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()
    mod = binding.parse_assembly(str(program))
    mod.verify()
    asm = target_machine.emit_assembly(mod)
    if options.printAssembly:
        if options.debug: print("\n== Generated LLVM Assembly ==")
        print(asm)
        if options.debug: print("===============================")

    # if options.debug: print("Saved LLVM IR to file:", options.objectFilepath)
    with open(options.objectFilepath, "wb") as f:
        f.write(target_machine.emit_object(mod))
    # obj = target_machine.emit_object(binding.ModuleRef(program, program.context))
    # print(obj)
    # Save the generated code to a file
    # with open(filepath + ".o", mode='w', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
    #     f.write(obj)
    target_machine.close()
    if not printingAsmOrIR: print("Building executable...")
    # Build the executable
    # binding.link_in_file(filepath + ".o")
    # Run GCC
    if os.system("gcc -o " + options.executableFilepath + " " + options.objectFilepath) != 0:
        print("Compilation failed!")
    else:
        if not printingAsmOrIR: print("Done!")
        # Remove the object file
        os.remove(options.objectFilepath)

# Types

bitTy = ir.IntType(1)
boolTy = ir.IntType(1)
int8Ty = ir.IntType(8)
charTy = ir.IntType(8)
int32Ty = ir.IntType(32)
int64Ty = ir.IntType(64)
floatTy = ir.FloatType()
doubleTy = ir.DoubleType()
# stringTy = charTy.as_pointer()

# Globals


def compile(input: TextIOBase, options: Options) -> ir.Module:
    lexer = Lexer(input, options.debug)
    parser = Parser(lexer, options.debug)
    if options.debug: print("== Tokens ==")
    ast: ProgramNode = parser.parse()
    if options.debug:
        print("== AST ==")
        print('    ' + '\n    '.join(str(e) for e in ast.expressions))

    module = ir.Module("program-" + options.filenameNoExt)
    # https://llvm.org/docs/LangRef.html#target-triple
    # https://clang.llvm.org/docs/CrossCompilation.html#target-triple
    # https://stackoverflow.com/questions/15036909/clang-how-to-list-supported-target-architectures
    module.triple = "x86_64-pc-linux-gnu"

    main = ir.Function(module, ir.FunctionType(int32Ty, []), "main")
    builder = ir.IRBuilder(main.append_basic_block("entry"))
    for n in ast.expressions:
        generate(n, module, builder)
    builder.ret(int32Ty(13))

    return module


def generate(ast: Node, module: ir.Module, builder: ir.IRBuilder):
    if isinstance(ast, AtomicNode):
        return generateAtomic(ast)
    elif isinstance(ast, IfNode):
        builder = ir.IRBuilder()
        pred = generate(ast.condition, module, builder)
        with builder.if_else(pred) as (if_block, else_block):
            with if_block:
                generate(ast.if_body, module, builder)
            with else_block:
                generate(ast.else_body, module, builder)
    elif isinstance(ast, BinaryNode):
        generateBinOp(ast, module, builder, "res")
    else:
        raise Exception("Unknown AST node: " + str(ast))

def generateAtomic(ast: Node) -> ir.Value:
    if isinstance(ast, AtomicNode):
        if ast.valueType == "number":
            return ir.Constant(int32Ty if ast.value.is_integer() else floatTy, ast.value)
        elif ast.valueType == "bool":
            return ir.Constant(boolTy, 1 if ast.value else 0)
        elif ast.valueType == "unit":
            return ir.Undefined
        elif ast.valueType == "string":
            return ir.Constant(ir.ArrayType(charTy, len(ast.value)), bytearray(ast.value.encode("utf-8")))
        else:
            raise Exception("Unknown atomic type: " + str(ast))
    else:
        raise Exception("Unknown AST node: " + str(ast))

def generateBinOp(ast: BinaryNode, module: ir.Module, builder: ir.IRBuilder, resultName: str):
    if ast.operator == "PLUS":
        builder.add(generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "MINUS":
        builder.sub(generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "MULTIPLY":
        builder.mul(generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "DIVIDE":
        builder.sdiv(generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "EQUAL":
        builder.icmp_signed("==", generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "NOTEQUAL":
        builder.icmp_signed("!=", generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "LESS":
        builder.icmp_signed("<", generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "GREATER":
        builder.icmp_signed(">", generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "LESSEQUAL":
        builder.icmp_signed("<=", generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "GREATEREQUAL":
        builder.icmp_signed(">=", generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "AND" or ast.operator == "BITWISEAND":
        builder.and_(generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "OR" or ast.operator == "BITWISEOR":
        builder.or_(generate(ast.lhs, module, builder), generate(ast.rhs, module, builder), resultName)
    elif ast.operator == "CALL":
        generateCall(ast.left, ast.right, module, builder, resultName)
    else:
        raise Exception("Unknown operator: " + str(ast.operator))

def generateCall(expr: Node, args: Node, module: ir.Module, builder: ir.IRBuilder, resultName: str):
    pass

def generateCondition(ast: Node) -> boolTy:
    global builder
    # Generate the condition and store it in a variable
    builder.append_basic_block("condition")
