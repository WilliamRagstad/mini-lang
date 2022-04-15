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
    def __init__(self, expressions: list[Node]):
        """
        Initialize a program node with a list of expressions.
        """
        super().__init__("Program")
        self.expressions = expressions

class AtomicNode(Node):
    """
    An atomic expression node in the abstract syntax tree.
    """
    def __init__(self, valueType: str, value):
        """
        Initialize an atomic expression node with a value.
        """
        super().__init__("Atomic")
        self.valueType = valueType
        self.value = value

    def __str__(self):
        value = f"'{self.value}'" if self.valueType == "string" else str(self.value)
        return f"{self.valueType}({value})"

class BlockNode(Node):
    """
    A block node in the abstract syntax tree.
    """
    def __init__(self, expressions: list[Node]):
        """
        Initialize a block node with a list of expressions.
        """
        super().__init__("Block")
        self.expressions = expressions

    def __str__(self):
        return '{' + '; '.join(map(str, self.expressions)) + '}'

class TupleNode(Node):
    """
    A tuple node in the abstract syntax tree.
    """
    def __init__(self, elements: list[Node]):
        """
        Initialize a tuple node with a list of elements.
        """
        super().__init__("Tuple")
        self.elements = elements

    def __str__(self):
        return '(' + ", ".join(map(str, self.elements)) + ')'

class ListNode(Node):
    """
    A list node in the abstract syntax tree.
    """
    def __init__(self, elements: list[Node]):
        """
        Initialize a list node with a list of elements.
        """
        super().__init__("List")
        self.elements = elements

    def __str__(self):
        return '[' + ", ".join(map(str, self.elements)) + ']'

class AssignmentNode(Node):
    """
    An assignment node in the abstract syntax tree.
    """
    def __init__(self, identifier: str, expression: Node, docstring: str = None):
        """
        Initialize an assignment node with an identifier and an expression.
        """
        super().__init__("Assignment")
        self.identifier = identifier
        self.expression = expression
        self.docstring = docstring

    def __str__(self):
        return f"{self.identifier} = {self.expression}"

class UnaryNode(Node):
    """
    A unary node in the abstract syntax tree.
    """
    def __init__(self, operator: str, rhs: Node):
        """
        Initialize a unary expression node with an operator and a right
        expression.
        """
        super().__init__("Unary")
        self.operator = operator
        self.rhs = rhs

    def __str__(self):
        return f"{self.operator}({self.rhs})"

class BinaryNode(Node):
    """
    A binary expression node in the abstract syntax tree.
    """
    def __init__(self, operator: str, left: Node, right: Node):
        """
        Initialize a binary expression node with an operator, left and right
        expressions.
        """
        super().__init__("Binary")
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

class IndexingNode(Node):
    """
    An indexing node in the abstract syntax tree.
    """
    def __init__(self, lhs: Node, index: Node):
        """
        Initialize an indexing node with an identifier and an index.
        """
        super().__init__("Indexing")
        self.lhs = lhs
        self.index = index

    def __str__(self):
        return f"{self.lhs}[{self.index}]"

class FunctionCallNode(Node):
    """
    A function call node in the abstract syntax tree.
    """
    def __init__(self, functionName: str, arguments: list[Node]):
        """
        Initialize a function call node with a function name and a list of
        arguments.
        """
        super().__init__("FunctionCall")
        self.functionName = functionName
        self.arguments = arguments

    def __str__(self):
        return f"{self.functionName}({', '.join(map(str, self.arguments))})"

class LambdaNode(Node):
    """
    A lambda function node in the abstract syntax tree.
    """
    def __init__(self, params: list[str], body: Node):
        """
        Initialize a lambda function node with a list of parameters and a body.
        """
        super().__init__("Lambda")
        self.params = params
        self.body = body

    def __str__(self):
        return f"({self.params} => {self.body})"

class IfNode(Node):
    """
    An if node in the abstract syntax tree.
    Contains a condition and body togehter with an optional if else statements and else body.
    """
    def __init__(self, condition: Node, ifBody: Node, elseIfs: list[tuple[Node, Node]] = [], elseBody: Node = None):
        """
        Initialize an if node with a condition, if body and an optional else body and else ifs.
        """
        super().__init__("If")
        self.condition = condition
        self.ifBody = ifBody
        self.elseBody = elseBody
        self.elseIfs = elseIfs
