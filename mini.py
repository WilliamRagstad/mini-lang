import sys
from src.options import Options
from src.interpreter import interpret, repl
from src.compiler import compileFile

# === Global variables ===

USAGE = f"""Welcome to the mini programming language interpreter!
Usage: mini (options) [file.mini]

Options:
    -h, --help      Print this help message and exit
    -r, --repl      Start the REPL
    -c, --compile   Compile to a standalone executable
    --debug         Enable debug mode
    --optimize      Enable optimizations
    --print-ir      Print the generated LLVM IR
    --print-asm     Print the generated assembly

Examples:
    mini -r             Enter the REPL
    mini file.mini      Interpret/Evaluate the input file
    mini -c file.mini   Compile the input file
\n"""

# === Helper functions ===
def print_error(msg: str):
    print(f"{msg}, try -h or --help to show usage.")
    sys.exit(1)

# === Main ===
def main(args: list):
    options = Options()
    if '--debug' in args:
        options.debug = True
        args.remove('--debug')
    if '--optimize' in args:
        options.optimize = True
        args.remove('--optimize')
    if '--print-ir' in args:
        options.printIR = True
        args.remove('--print-ir')
    if '--print-asm' in args:
        options.printAssembly = True
        args.remove('--print-asm')

    if len(args) == 0 or '-h' in args or '--help' in args:
        print(USAGE)
        sys.exit(0)
    elif '-r' in args or '--repl' in args:
        repl(options)
    elif '-c' in args or '--compile' in args:
        if len(args) != 2:
            print_error("-c or --compile requires a filepath argument.")
        options.setFilepath(args[-1])
        compileFile(args[-1], options)


    # Evaluate
    elif len(args) > 1:
        print_error("Too many arguments")
    elif len(args) == 1:
        options.setFilepath(args[-1])
        interpret(args[-1], options)
    else:
        print_error("Unknown option")

if __name__ == '__main__':
  # Call main with args
  main(sys.argv[1:])
