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

class AtomicNode(Node):
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

class TupleNode(Node):
    """
    A tuple node in the abstract syntax tree.
    """
    def __init__(self, elements):
        """
        Initialize a tuple node with a list of elements.
        """
        super().__init__("Tuple")
        self.elements = elements
    
    def __str__(self):
        return '(' + ", ".join(str(e) for e in self.elements) + ')'

class ListNode(Node):
    """
    A list node in the abstract syntax tree.
    """
    def __init__(self, elements):
        """
        Initialize a list node with a list of elements.
        """
        super().__init__("List")
        self.elements = elements
    
    def __str__(self):
        return '[' + ", ".join(str(e) for e in self.elements) + ']'

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
    
    def __str__(self):
        return f"{self.name} {self.identifier} = {self.expression}"

class UnaryNode(Node):
    """
    A unary node in the abstract syntax tree.
    """
    def __init__(self, operator: str, rhs: Node):
        """
        Initialize a unary expression node with an operator and a right
        expression.
        """
        super().__init__("UnaryExpression")
        self.operator = operator
        self.rhs = rhs
    
    def __str__(self):
        return f"{self.name} {self.operator}({self.rhs})"

class BinaryNode(Node):
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
    
    def __str__(self):
        return f"{self.name} {self.functionName}({', '.join(str(a) for a in self.arguments)})"

class LambdaFunctionNode(Node):
    """
    A lambda function node in the abstract syntax tree.
    """
    def __init__(self, params: list[str], body: Node):
        """
        Initialize a lambda function node with a list of parameters and a body.
        """
        super().__init__("LambdaFunction")
        self.params = params
        self.body = body
    
    def __str__(self):
        return f"{self.name} ({self.params} => {self.body})"

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
            return AtomicNode("Identifier", t.value)
        nt = tokens[0]
        if nt.name == 'Bracket':
            if nt.value == '(':
                tokens.pop(0) # Remove the opening bracket
                lhs = parse_function_call(t.value)
            elif nt.value == '[':
                tokens.pop(0)
                indexingExpr = parse_expression()
                if tokens[0].value != ']':
                    raise Exception("Expected ']'")
                tokens.pop(0) # Remove the closing bracket
                lhs = ListNode([indexingExpr])
        elif nt.name == 'AssignmentOperator':
            tokens.pop(0) # Remove the assignment operator
            rhs = parse_expression()
            lhs = AssignmentNode(t.value, rhs)
            dprint(f"Found assignment '{t.value}' = {rhs}")
        else:
            dprint(f"Found identifier '{t.value}'")
            lhs = AtomicNode("Identifier", t.value)
    elif t.name in ["String", "Number", "Boolean"]:
        lhs = AtomicNode(t.name.lower(), t.value)
    elif t.name == "Keyword":
        raise Exception(f"Keyword '{t.value}' is not implemented!")
    elif t.name == "Bracket":
        if t.value == '(':
            dprint("Found tuple")
            lhs = parse_tuple()
            # Check for trailing right arrow
            if len(tokens) > 0:
                t = tokens[0]
                if t.name == "RightArrow":
                    tokens.pop(0) # Remove the arrow
                    # Validate so that the tuple is only identifiers
                    argumentNames = []
                    for e in lhs.elements:
                        if not (isinstance(e, AtomicNode) or e.name == "Identifier"):
                            raise Exception(f"Tuple argument '{e}' is not an identifier!")
                        argumentNames.append(e.value)

                    # Parse lambda expression
                    dprint("Found lambda expression")
                    body = parse_expression()
                    lhs = LambdaFunctionNode(argumentNames, body)
        elif t.value == '[':
            dprint("Found list")
            elements: list[Node] = []
            expectExpression = False
            while len(tokens) > 0:
                t = tokens[0]
                if t.name == "Bracket" and t.value == ']':
                    if expectExpression:
                        raise Exception(f"Expected expression but found '{t.value}'")
                    tokens.pop(0) # Remove the closing bracket
                    break
                elements.append(parse_expression())
                # parse comma
                if len(tokens) == 0:
                    raise Exception("Expected ']' but found end of file")
                t = tokens[0]
                # Check that it is a comman and expect another expression if so
                if t.name == "Separator" and t.value == ',':
                    tokens.pop(0) # Remove the comma
                    expectExpression = True
                else:
                    expectExpression = False
            lhs = ListNode(elements)
            
    elif t.name.endswith("Operator") and t.value in ["-", "!"]:
        dprint("Found unary operator")
        rhs = parse_expression()
        lhs = UnaryNode(t.value, rhs)
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
            lhs = BinaryNode(t.value, lhs, rhs)
        else:
            break

    return lhs

def parse_tuple() -> TupleNode:
    """
    Parse a tuple from a list of tokens.
    """
    # The previous token should have been the opening bracket
    elements: list[Node] = []
    expectExpression = False
    while len(tokens) > 0:
        t = tokens[0]
        if t.name == "Bracket" and t.value == ')':
            if expectExpression:
                raise Exception(f"Expected expression but found '{t.value}'")
            tokens.pop(0) # Remove the closing bracket
            break
        elements.append(parse_expression())
        # parse comma
        if len(tokens) == 0:
            raise Exception("Expected ')' but found end of file")
        t = tokens[0]
        # Check that it is a comman and expect another expression if so
        if t.name == "Separator" and t.value == ',':
            tokens.pop(0) # Remove the comma
            expectExpression = True
        else:
            expectExpression = False

    # if len(elements) == 0:
    #     return UnitNode()
    # if len(elements) == 1:
    #    return elements[0]
    # Leave this logic to the evaluator
    return TupleNode(elements)

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
