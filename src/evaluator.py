from .atoms import Atom, BuiltinFunctionAtom, FunctionAtom, UnitAtom, ValueAtom
from .environment import Environment
from .parser import AtomicExpressionNode, BinaryExpressionNode, FunctionCallNode, Node, ProgramNode

# Global variables

debug = False

# Helper functions
def dprint(*args):
    """
    Print debug messages.
    """
    if debug:
        print(*args)

def evaluate_expression(expression: Node, env: Environment) -> Atom:
    if isinstance(expression, AtomicExpressionNode):
        return ValueAtom(expression.valueType, expression.value)
    elif isinstance(expression, FunctionCallNode):
        return evaluate_function_call(expression, env)
    elif isinstance(expression, BinaryExpressionNode):
        lhs = evaluate_expression(expression.left, env)
        rhs = evaluate_expression(expression.right, env)
        if expression.operator == "+":
            return lhs + rhs
        elif expression.operator == "-":
            return lhs - rhs
        elif expression.operator == "*":
            return lhs * rhs
        elif expression.operator == "/":
            return lhs / rhs
        elif expression.operator == "%":
            return lhs % rhs
        elif expression.operator == "==":
            return lhs == rhs
        elif expression.operator == "!=":
            return lhs != rhs
        elif expression.operator == ">":
            return lhs > rhs
        elif expression.operator == "<":
            return lhs < rhs
        elif expression.operator == ">=":
            return lhs >= rhs
        elif expression.operator == "<=":
            return lhs <= rhs
        elif expression.operator == "&":
            return lhs and rhs
        elif expression.operator == "|":
            return lhs or rhs
        else:
            raise Exception(f"Unknown operator '{expression.operator}'")

def evaluate_function_call(fc: FunctionCallNode, env: Environment) -> Atom:
    funcVal = env.get(fc.functionName)
    if funcVal is None:
        raise Exception(f"Function '{fc.functionName}' is not defined")
    
    if isinstance(funcVal, BuiltinFunctionAtom):
        # Check that all arguments are of value types, and then map them to their values
        values = []
        for arg in fc.arguments:
            argValue = evaluate_expression(arg, env)
            if not isinstance(argValue, ValueAtom):
                raise Exception(f"Argument '{arg}' does not evaluate to an atomic value")
            values.append(argValue.value)
        return funcVal.func(*values)
    elif isinstance(funcVal, FunctionAtom):
        # Build a new environment for the function call
        # where the arguments are bound to the parameters
        funcEnv = Environment(f"<function {fc.functionName}>", funcVal.env)
        if len(fc.arguments) != len(funcVal.argNames):
            raise Exception(f"Function '{fc.functionName}' expects {len(funcVal.argNames)} arguments, but got {len(fc.arguments)}")
        for name, exp in zip(funcVal.argNames, fc.arguments):
            funcEnv.set(name, evaluate_expression(exp, env))
        return evaluate_expressions(funcVal.body, funcEnv)
    else:
        raise Exception(f"The variable '{fc.functionName}' is not a function")

def evaluate_expressions(expressions: list[Node], env: Environment) -> Atom:
    """
    Evaluate a list of expressions and return the last result.
    """
    result = UnitAtom()
    for expression in expressions:
        result = evaluate_expression(expression, env)
    return result

# Evaluator function
def evaluate(program: ProgramNode, env: Environment, _debug = False) -> Atom:
    """
    Evaluate a program node.
    """
    global debug
    debug = _debug
    dprint("Evaluating program:")
    return evaluate_expressions(program.expressions, env)