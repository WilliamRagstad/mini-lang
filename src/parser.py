from tokenize import Token

# Helper classes
class Node():
    """
    A base node in the abstract syntax tree.
    """
    def __init__(self, name):
        """
        Initialize a node with a name
        """
        self.name = name
    
    def __str__(self):
        return self.name

class ProgramNode(Node):
    """
    A program node in the abstract syntax tree.
    """
    def __init__(self, expressions):
        """
        Initialize a program node with a list of expressions.
        """
        super().__init__("Program")
        self.expressions = expressions

class AtomicExpressionNode(Node):
    """
    An atomic expression node in the abstract syntax tree.
    """
    def __init__(self, valueType, value):
        """
        Initialize an atomic expression node with a value.
        """
        super().__init__("AtomicExpression")
        self.valueType = valueType
        self.value = value
    
    def __str__(self):
        return f"{self.name} {self.valueType}({self.value})"

class AssignmentNode(Node):
    """
    An assignment node in the abstract syntax tree.
    """
    def __init__(self, identifier: str, expression: Node):
        """
        Initialize an assignment node with an identifier and an expression.
        """
        super().__init__("Assignment")
        self.identifier = identifier
        self.expression = expression

class BinaryExpressionNode(Node):
    """
    A binary expression node in the abstract syntax tree.
    """
    def __init__(self, operator: str, left: Node, right: Node):
        """
        Initialize a binary expression node with an operator, left and right
        expressions.
        """
        super().__init__("BinaryExpression")
        self.operator = operator
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"{self.name} ({self.left} {self.operator} {self.right})"

class FunctionCallNode(Node):
    """
    A function call node in the abstract syntax tree.
    """
    def __init__(self, functionName, arguments):
        """
        Initialize a function call node with a function name and a list of
        arguments.
        """
        super().__init__("FunctionCall")
        self.functionName = functionName
        self.arguments = arguments

# Global variables
tokens: list[Token] = []
debug = False

# Helper functions
def dprint(*args):
    """
    Print debug messages.
    """
    if debug:
        print(*args)

def parse_expression() -> Node:
    """
    Parse an expression from a list of tokens.
    """
    t = tokens.pop(0)
    lhs = None
    if t.name == "Identifier":
        if len(tokens) == 0:
            dprint(f"Found identifier '{t.value}'")
            return AtomicExpressionNode("Identifier", t.value)
        nt = tokens[0]
        if nt.name == 'Bracket' and nt.value == '(':
            tokens.pop(0) # Remove the opening bracket
            lhs = parse_function_call(t.value)
        elif nt.name == 'AssignmentOperator':
            tokens.pop(0) # Remove the assignment operator
            lhs = AssignmentNode(
                t.value,
                parse_expression()
            )
        else:
            dprint(f"Found identifier '{t.value}'")
            lhs = AtomicExpressionNode("Identifier", t.value)
    elif t.name in ["String", "Number", "Boolean"]:
        dprint(f"Found {t.name} '{t.value}'")
        return AtomicExpressionNode(t.name.lower(), t.value)
    else:
        raise Exception(f"Unexpected {t.name} token: '{t.value}'")
    
    if lhs is None:
        # Should never happen
        raise Exception(f"Unexpected {t.name} token: '{t.value}'")
    
    # Parse binary expression
    while len(tokens) > 0:
        t = tokens[0]
        if t.name.endswith("Operator"):
            tokens.pop(0) # Remove the operator token
            rhs = parse_expression()
            lhs = BinaryExpressionNode(t.value, lhs, rhs)
        else:
            break

    return lhs

def parse_function_call(functionName: str) -> FunctionCallNode:
    """
    Parse a function call from a list of tokens.
    """
    arguments = []
    expectArguement = False
    dprint(f"Parsing function call '{functionName}'...")
    while len(tokens) > 0:
        t = tokens[0]
        if t.name == "Bracket" and t.value == ')':
            if expectArguement:
                raise Exception("Expected argument")
            tokens.pop(0) # Remove the closing bracket
            break
        dprint("Parsing argument...")
        arguments.append(parse_expression())

        if len(tokens) == 0:
            raise Exception("Expected ')'")

        expectArguement = False
        t = tokens[0]
        if t.name == "Separator" and t.value == ',':
            tokens.pop(0)
            expectArguement = True
    dprint(f"Found function call '{functionName}' with {len(arguments)} arguments")
    return FunctionCallNode(functionName, arguments)


# Parse function
def parse(_tokens: list[Token], _debug = False) -> ProgramNode:
    """
    Parse a list of tokens into an abstract syntax tree.
    """
    global tokens, debug
    tokens = _tokens
    debug = _debug
    program = ProgramNode([])
    if len(tokens) == 0:
        return program
    while len(tokens) > 0:
        program.expressions.append(parse_expression())
    return program
