from .atoms import Atom, BuiltinFunctionAtom, FunctionAtom, ValueAtom
from .ast import AssignmentNode, AtomicNode, BinaryNode, BlockNode, FunctionCallNode, IfNode, IndexingNode, LambdaNode, ListNode, MapNode, Node, ProgramNode, TupleNode, UnaryNode
from .environment import Environment

# Global variables
debug = False

# Helper functions
def dprint(*args):
    """
    Print debug messages.
    """
    if debug:
        print(*args)

def compatible_types(lhs: Atom, rhs: Atom, types: list[str]) -> bool:
    """
    Check if the two atoms are compatible with the given types.
    """
    if not isinstance(lhs, ValueAtom):
        raise Exception(f"Left hand side in expression is not an atomic value")
    if not isinstance(rhs, ValueAtom):
        raise Exception(f"Right hand side in expression is not an atomic value")
    if lhs.valueType in types and rhs.valueType in types:
        return True
    else:
        raise Exception(f"Incompatible types: {lhs.valueType} and {rhs.valueType}")

def compatible_type(value: Atom, types: list[str]) -> bool:
    """
    Check if the given value is compatible with the given types.
    """
    if not isinstance(value, ValueAtom):
        raise Exception(f"Value is not an atomic value")
    if value.valueType in types:
        return True
    else:
        raise Exception(f"Incompatible types: {value.valueType} and {types}")

def evaluate_expression(expression: Node, env: Environment) -> Atom:
    if isinstance(expression, AtomicNode):
        if expression.valueType == "identifier":
            dprint(f"Evaluating identifier '{expression.value}'")
            val = env.get(expression.value)
            if val is None:
                raise Exception(f"identifier '{expression.value}' is not defined")
            return val
        else:
            return ValueAtom(expression.valueType, expression.value)
    elif isinstance(expression, TupleNode):
        if len(expression.elements) == 0:
            return ValueAtom("unit", None)
        elif len(expression.elements) == 1:
            return evaluate_expression(expression.elements[0], env)
        else:
            return ValueAtom("tuple", list(map(lambda e: evaluate_expression(e, env), expression.elements)))
    elif isinstance(expression, ListNode):
        return ValueAtom("list", list(map(lambda e: evaluate_expression(e, env), expression.elements)))
    elif isinstance(expression, MapNode):
        map_values: dict[str | int, Atom] = {}
        for key, value in expression.pairs.items():
            if not isinstance(key, AtomicNode):
                raise Exception(f"Key in map is not an atomic value")
            if key.valueType == "number" and key.value.is_integer():
                key.value = int(key.value)
                key.valueType = "integer"
            if key.valueType not in ["identifier", "string", "integer"]:
                raise Exception(f"Key in map is not an identifier, string or integer number")
            value = evaluate_expression(value, env)
            map_values[key.value] = value
        return ValueAtom("map", map_values)
    elif isinstance(expression, BlockNode):
        return evaluate_expressions(expression.expressions, Environment(f"<block>", env))
    elif isinstance(expression, AssignmentNode):
        dprint(f"Evaluating assignment {expression.identifier} = {expression.expression}")
        value = evaluate_expression(expression.expression, env)
        env.set(expression.identifier, value)
        return value
    elif isinstance(expression, FunctionCallNode):
        return evaluate_function_call(expression, env)
    elif isinstance(expression, LambdaNode):
        return FunctionAtom(expression.params, expression.body, env)
    elif isinstance(expression, IndexingNode):
        indexAtom = evaluate_expression(expression.index, env)
        if not isinstance(indexAtom, ValueAtom):
            raise Exception(f"Indexing expression does not evaluate to an atomic value")
        if indexAtom.valueType == "number":
            # Make sure it's an integer
            if not indexAtom.value.is_integer():
                raise Exception(f"Indexing expression does not evaluate to an integer or string")
            index = int(indexAtom.value)
        elif indexAtom.valueType == "string":
            index = indexAtom.value
        else:
            raise Exception(f"Indexing expression does not evaluate to an integer or string")
        value = evaluate_expression(expression.lhs, env)
        if isinstance(value, ValueAtom):
            if value.type not in ["list", "tuple", "map"]:
                raise Exception(f"Cannot index a value of type '{value.type}'")
            element = value.value[index]
            dprint(f"Indexing {value.type}: {value.value} with index {index} -> {element}")
            return element
        else:
            raise Exception(f"Expression of type {value.type} does not support indexing")
    elif isinstance(expression, IfNode):
        cond = evaluate_expression(expression.condition, env)
        if not isinstance(cond, ValueAtom) or not cond.valueType == "boolean":
            raise Exception(f"Condition does not evaluate to a boolean")
        if cond.value:
            return evaluate_expression(expression.ifBody, env)
        else:
            # Iterate over the else-ifs
            for cond, body in expression.elseIfs:
                cond = evaluate_expression(cond, env)
                if not isinstance(cond, ValueAtom) or not cond.valueType == "boolean":
                    raise Exception(f"Condition does not evaluate to a boolean")
                if cond.value:
                    return evaluate_expression(body, env)
            # Evaluate the else body
            return evaluate_expression(expression.elseBody, env)
    elif isinstance(expression, UnaryNode):
        op = expression.operator
        rhs = evaluate_expression(expression.rhs, env)
        if op == "MINUS" and compatible_type(rhs, ["number"]):
            return ValueAtom("number", -rhs.value)
        elif op == "NOT" and compatible_type(rhs, ["boolean"]):
            return ValueAtom("boolean", not rhs.value)
        else:
            raise Exception(f"Unkown unary operator '{op}'")
    elif isinstance(expression, BinaryNode):
        op = expression.operator
        lhs = evaluate_expression(expression.left, env)
        rhs = evaluate_expression(expression.right, env)
        if expression.operator in ["PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MODULO", "POWER", "EQUAL", "NOTEQUAL",
                                   "LESS", "GREATER", "LESSEQUAL", "GREATEREQUAL", "AND", "OR"]:
            return evaluate_binary_atom_expression(expression.operator, lhs, rhs, env)
        elif op == "PLUSEQUAL" and compatible_types(lhs, rhs, ["string", "number"]):
            if not (isinstance(expression.left, AtomicNode) and expression.left.valueType == "identifier"):
                raise Exception(f"Left hand side of mutating assignment operator '{op}' must be an identifier")
            if lhs.valueType == "string" or rhs.valueType == "string":
                new_value = ValueAtom("string", lhs.value + str(rhs.value))
            else:
                new_value = ValueAtom("number", lhs.value + rhs.value)
            env.set(expression.left.value, new_value)
            return new_value
        else:
            raise Exception(f"Unknown binary operator '{op}'")
    else:
        raise Exception(f"Unknown expression type '{type(expression)}'")

def evaluate_binary_atom_expression(op: str, lhs: Atom, rhs: Atom, env: Environment) -> Atom:
    dprint(f"Evaluating binary expression '{lhs} {op} {rhs}'")
    if op == "PLUS" and compatible_types(lhs, rhs, ["string", "number", "boolean", "list", "tuple", "map"]):
        if lhs.valueType == "string" or rhs.valueType == "string":
            return ValueAtom("string", repr(lhs) + repr(rhs))
        elif lhs.valueType == "list" and rhs.valueType == "list":
            return ValueAtom("list", lhs.value + rhs.value)
        elif lhs.valueType == "number" and rhs.valueType == "number":
            return ValueAtom("number", lhs.value + rhs.value)
        elif lhs.valueType == "tuple" and rhs.valueType == "tuple":
            # Ensure that the tuples have the same length
            if len(lhs.value) != len(rhs.value):
                raise Exception(f"Tuple length mismatch: {len(lhs.value)} and {len(rhs.value)}")
            new_value = []
            for i in range(len(lhs.value)):
                dprint(f"Evaluating {lhs.value[i]} {op} {rhs.value[i]}")
                new_value.append(evaluate_binary_atom_expression("PLUS", lhs.value[i], rhs.value[i], env))
            return ValueAtom("tuple", new_value)
        elif lhs.valueType == "map" and rhs.valueType == "map":
            # Concate the maps
            for key, value in rhs.value.items():
                lhs.value[key] = value
            return lhs
        else:
            raise Exception(f"Cannot add {lhs.valueType} and {rhs.valueType}")
    elif op == "MINUS" and compatible_types(lhs, rhs, ["number"]):
        return ValueAtom("number", lhs.value - rhs.value)
    elif op == "MULTIPLY" and compatible_types(lhs, rhs, ["number"]):
        return ValueAtom("number", lhs.value * rhs.value)
    elif op == "DIVIDE" and compatible_types(lhs, rhs, ["number"]):
        return ValueAtom("number", lhs.value / rhs.value)
    elif op == "MODULO" and compatible_types(lhs, rhs, ["number"]):
        return ValueAtom("number", lhs.value % rhs.value)
    elif op == "POWER" and compatible_types(lhs, rhs, ["number"]):
        return ValueAtom("number", lhs.value ** rhs.value)
    elif op == "EQUAL" and compatible_types(lhs, rhs, ["number", "string", "boolean", "unit", "tuple", "list", "map"]):
        if lhs.valueType != rhs.valueType:
            return ValueAtom("boolean", False)
        return ValueAtom("boolean", lhs.value == rhs.value)
    elif op == "NOTEQUAL" and compatible_types(lhs, rhs, ["number", "string", "boolean"]):
        return ValueAtom("boolean", lhs.value != rhs.value)
    elif op == "LESS" and compatible_types(lhs, rhs, ["number"]):
        return ValueAtom("boolean", lhs.value < rhs.value)
    elif op == "GREATER" and compatible_types(lhs, rhs, ["number"]):
        return ValueAtom("boolean", lhs.value > rhs.value)
    elif op == "LESSEQUAL" and compatible_types(lhs, rhs, ["number"]):
        return ValueAtom("boolean", lhs.value <= rhs.value)
    elif op == "GREATEREQUAL" and compatible_types(lhs, rhs, ["number"]):
        return ValueAtom("boolean", lhs.value >= rhs.value)
    elif op == "AND" and compatible_types(lhs, rhs, ["boolean"]):
        return ValueAtom("boolean", lhs.value and rhs.value)
    elif op == "OR" and compatible_types(lhs, rhs, ["boolean"]):
        return ValueAtom("boolean", lhs.value or rhs.value)
    else:
        raise Exception(f"Unknown binary operator '{op}'")

def evaluate_function_call(fc: FunctionCallNode, env: Environment) -> Atom:
    funcVal = env.get(fc.functionName)
    if funcVal is None:
        raise Exception(f"Function '{fc.functionName}' is not defined")

    if isinstance(funcVal, BuiltinFunctionAtom):
        # Check that all arguments are of value types, and then map them to their values
        values = []
        for arg in fc.arguments:
            dprint(f"Evaluating argument '{arg}'")
            argValue = evaluate_expression(arg, env)
            if not isinstance(argValue, ValueAtom):
                raise Exception(f"Argument '{arg}' does not evaluate to an atomic value")
            values.append(repr(argValue))
        return funcVal.func(*values)
    elif isinstance(funcVal, FunctionAtom):
        # Build a new environment for the function call
        # where the arguments are bound to the parameters
        funcEnv = Environment(f"<function {fc.functionName}>", funcVal.environment)
        if len(fc.arguments) != len(funcVal.argumentNames):
            raise Exception(f"Function '{fc.functionName}' expects {len(funcVal.argumentNames)} arguments, but got {len(fc.arguments)}")
        for name, exp in zip(funcVal.argumentNames, fc.arguments):
            funcEnv.set(name, evaluate_expression(exp, env))
        return evaluate_expression(funcVal.body, funcEnv)
    else:
        raise Exception(f"The variable '{fc.functionName}' is not a function")

def evaluate_expressions(expressions: list[Node], env: Environment) -> Atom:
    """
    Evaluate a list of expressions and return the last result.
    """
    result = ValueAtom("unit", None)
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
    return evaluate_expressions(program.expressions, env)
