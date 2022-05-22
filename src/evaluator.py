from .atoms import Atom, BuiltinFunctionAtom, FunctionAtom, ValueAtom
from .ast import AtomicNode, BinaryNode, BlockNode, IfNode, LambdaNode, ListNode, MapNode, Node, ProgramNode, TupleNode, UnaryNode
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
    Check if the given value is a `ValueAtom` and compatible with the given types.
    """
    if not isinstance(value, ValueAtom):
        raise Exception(f"Value is not an atomic value")
    if value.valueType in types:
        return True
    else:
        raise Exception(f"Incompatible types: {value.valueType} and {types}")

def is_identifier(expression: Node) -> bool:
    return isinstance(expression, AtomicNode) and expression.valueType == "identifier"

def is_identifier_members(expression: Node) -> bool:
    return isinstance(expression, BinaryNode) and expression.operator == "DOT" and (
        is_identifier(expression.left) or is_identifier_members(expression.left)
    ) and is_identifier(expression.right)

def get_left_most_bin_term(expression: Node, op: str) -> Node:
    """
    Get the base of a member expression.
    """
    if isinstance(expression, BinaryNode) and expression.operator == op:
        return get_left_most_bin_term(expression.left, op)
    else:
        return expression

def flatten_bin_terms(expression: Node, op: str, includeBase: bool) -> list:
    """
    Get the path of a member expression.
    """
    if isinstance(expression, BinaryNode) and expression.operator == op:
        return flatten_bin_terms(expression.left, op, includeBase) + [expression.right.value]
    else:
        return [expression.value] if includeBase else []

def set_nested_value(obj: ValueAtom, path: list, rhs: Atom) -> ValueAtom:
    """
    Set the value of a member expression.
    """
    if len(path) == 0: raise Exception("Member path is empty")
    elif len(path) == 1:
        obj.value[path[0]] = rhs
        return obj
    else:
        obj.value[path[0]] = set_nested_value(obj.value[path[0]], path[1:], rhs)
        return obj

# Evaluation functions

def evaluate_expression(expression: Node, env: Environment) -> Atom:
    if isinstance(expression, AtomicNode):
        if is_identifier(expression):
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
    elif isinstance(expression, LambdaNode):
        return FunctionAtom(expression.params, expression.body, env)
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

        if op == "ASSIGNMENT":
            dprint(f"Evaluating assignment {expression.left} = {expression.right}")
            if is_identifier(expression.left):
                rhs = evaluate_expression(expression.right, env)
                env.set(expression.left.value, rhs)
                return rhs
            elif is_identifier_members(expression.left):
                rhs = evaluate_expression(expression.right, env)
                base = get_left_most_bin_term(expression.left, "DOT")
                if is_identifier(base):
                    obj = env.get(base.value)
                    if obj is None: raise Exception(f"Object '{base.value}' is not defined")
                    path = flatten_bin_terms(expression.left, "DOT", False)
                    obj = set_nested_value(obj, path, rhs)
                    env.set(base.value, obj)
                    return rhs
                else:
                    raise Exception(f"Cannot set member of non-identifer values")
            elif isinstance(expression.left, BinaryNode) and expression.left.operator == "INDEX":
                rhs = evaluate_expression(expression.right, env)
                base = get_left_most_bin_term(expression.left, "INDEX")
                if is_identifier(base):
                    lst = env.get(base.value)
                    if lst is None: raise Exception(f"List '{base.value}' is not defined")
                    path = flatten_bin_terms(expression.left, "INDEX", False) # List of indices
                    lst = set_nested_value(lst, path, rhs)
                    env.set(base.value, lst)
                    return rhs
                pass
            elif isinstance(expression.left, BinaryNode) and expression.left.operator == "CALL":
                # Function declaration
                functionName = expression.left.left
                if not is_identifier(functionName):
                    raise Exception(f"Function name is not an identifier")
                args = expression.left.right
                # Check that the arguments is a a tuple of identifiers
                if not isinstance(args, TupleNode):
                    raise Exception(f"Function arguments are not a tuple")
                argNames: list[str] = []
                for a in args.elements:
                    if not isinstance(a, AtomicNode) or a.valueType != "identifier":
                        raise Exception(f"Function argument '{a}' is not an identifier")
                    argNames.append(a.value)
                # Assign the right hand side as body of the function
                body = expression.right
                value = FunctionAtom(argNames, body, env, functionName.value)
                # Update the environment
                env.set(functionName.value, value)
                return value
            else:
                raise Exception(f"Invalid assignment, left hand side is not an identifier, function or valid pattern")

        lhs = evaluate_expression(expression.left, env)
        if op == "DOT":
            # Member access, last identifier is the member name and the rest is the object
            dprint(f"Evaluating member access {lhs}.{expression.right} ({expression.right.__class__})")
            if not is_identifier(expression.right):
                raise Exception(f"Cannot access member of {lhs.type} with non-identifier key")
            if not (isinstance(lhs, ValueAtom) and lhs.type in ["map", "tuple", "list"]):
                raise Exception(f"Cannot access member of {lhs.type}")
            if lhs.valueType == "map":
                if expression.right.value not in lhs.value:
                    raise Exception(f"Map does not contain key '{expression.right.value}'")
                return lhs.value[expression.right.value]
            raise Exception(f"Cannot access member of {lhs.type}, not implemented yet")

        rhs = evaluate_expression(expression.right, env)
        # The rest of the operators rely on the right hand side being evaluated first
        # Try to evaluate binary operators first
        binOpResult = evaluate_binary_atom_expression(op, lhs, rhs, env)
        if binOpResult is not None:
            return binOpResult
        if op == "PLUSEQUAL" and compatible_types(lhs, rhs, ["string", "number"]):
            if not is_identifier(expression.left):
                raise Exception(f"Left hand side of mutating assignment operator '{op}' must be an identifier")
            if lhs.valueType == "string" or rhs.valueType == "string":
                new_value = ValueAtom("string", lhs.value + str(rhs.value))
            else:
                new_value = ValueAtom("number", lhs.value + rhs.value)
            env.set(expression.left.value, new_value)
            return new_value

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
            for key, lhs in rhs.value.items():
                lhs.value[key] = lhs
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
    elif op == "INDEX" and compatible_type(lhs, ["list", "tuple", "map"]):
        if not isinstance(rhs, ValueAtom):
            raise Exception(f"Indexing expression in not a valid value type: {rhs}")
        if rhs.valueType in ["number", "string"]:
            element = lhs.value[rhs.value]
            dprint(f"Indexing {lhs.type}: {lhs.value} with index {rhs.value} -> {element}")
            return element
        else:
            raise Exception(f"Indexing expression does not evaluate to a number or string")
    elif op == "CALL":
        # The tuple may have been evaluated to a single value
        args = [rhs]
        if isinstance(rhs, ValueAtom):
            if rhs.valueType == "tuple":
                args: list[Atom] = rhs.value
            elif rhs.valueType == "unit":
                args = []
        # args = list(map(lambda e: evaluate_expression(e, env), rhs.value))
        if isinstance(lhs, FunctionAtom):
            return evaluate_function_call(lhs, args, env)
        elif isinstance(lhs, BuiltinFunctionAtom):
            return evaluate_builtin_function_call(lhs, args, env)
        else:
            raise Exception(f"Cannot call non-function: {lhs}")

    return None

def evaluate_function_call(function: FunctionAtom, args: list[Atom], env: Environment) -> Atom:
    # Build a new environment for the function call
    # where the arguments are bound to the parameters
    funcEnv = Environment(f"<function {function.name}>", function.environment)
    if len(args) != len(function.argumentNames):
        raise Exception(f"Function '{function.name}' expects {len(function.argumentNames)} arguments, but got {len(args)}")
    for name, val in zip(function.argumentNames, args):
        funcEnv.set(name, val)
    return evaluate_expression(function.body, funcEnv)

def evaluate_builtin_function_call(function: BuiltinFunctionAtom, args: list[Atom], env: Environment) -> Atom:
    # Check that all arguments are of value types, and then map them to their values
    values = []
    for a in args:
        if not isinstance(a, ValueAtom):
            raise Exception(f"Argument '{a}' does not evaluate to an atomic value")
        values.append(repr(a))
    return function.func(*values)

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
