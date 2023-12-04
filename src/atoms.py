# Fundamental value types in the language
from typing import Callable
from .ast import Node

unique_id = 0
def get_unique_id() -> int:
    """
    Get a unique id for a node.
    """
    global unique_id
    unique_id += 1
    return unique_id - 1

class Atom():
    """
    A fundamental value type in the language.
    """
    def __init__(self, name, type):
        """
        Initialize an atom with a name and a type.
        """
        self.uid = get_unique_id()
        self.name = name
        self.type = type

    def __str__(self):
        return self.memory_repr()
    
    def raw_str(self):
        """
        Returns the raw value without any formatting.
        For example, a string atom will return the string **without** quotes.
        """
        return str(self)
    
    def formatted_str(self):
        """
        Returns the formatted value.
        For example, a string atom will return the string **with** quotes.
        """
        return str(self)

    def memory_repr(self):
        """
        Returns the memory representation of the value.
        """
        return f"<{self.uid}:{self.type}>"

class ValueAtom(Atom):
    """
    An atomic value node in the abstract syntax tree.
    """
    def __init__(self, type: str, value):
        """
        Initialize an atomic value node with a value.

        Parameters
        ----------
            valueType: The type of the value in lower case.
                       E.g. "string", "number", "boolean", "unit", "tuple", "list".
            value: The value of the node.
        """
        super().__init__("Value", type)
        self.value = value

    def listValueToStr(self):
        return list(map(lambda a: str(a), self.value))
    
    def raw_str(self):
        return self.format(True)

    def formatted_str(self):
        return self.format(False)

    def format(self, raw: bool) -> str:
        if self.type == "string":
            return self.value if raw else f"'{self.value}'"
        elif self.type == "boolean":
            return str(self.value).lower()
        elif self.type == "unit":
            return "()"
        elif self.type == "tuple":
            return '(' + ", ".join(self.listValueToStr()) + ')'
        elif self.type == "list":
            return '[' + ", ".join(self.listValueToStr()) + ']'
        elif self.type == "map":
            return '#{' + ", ".join(map(lambda t: f"{t[0]}: {t[1]}", self.value.items())) + '}'
        return str(self.value)


    def memory_repr(self):
        return f"<{self.uid}:{self.type}:{self.value}>"

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, ValueAtom) and self.valueType == __o.valueType and self.value == __o.value

class FunctionAtom(Atom):
    """
    A function node in the abstract syntax tree.
    """
    def __init__(self, argumentNames: list[str], body: Node, environment, name: str = None):
        """
        Initialize a function node with a function name, argument names, body and the environment in which it was defined.
        """
        super().__init__("Function", "function")
        self.argumentNames = argumentNames
        self.body = body
        self.environment = environment
        self.name = name if name is not None else "lambda"

    def memory_repr(self):
        return f"<{self.uid}:{self.name}({', '.join(self.argumentNames)})>"

class BuiltinFunctionAtom(Atom):
    """
    A builtin function node in the abstract syntax tree.
    """
    def __init__(self, functionName: str, func: Callable):
        """
        Initialize a builtin function node with a function name and a function.
        """
        super().__init__("Built-in function", "function")
        self.functionName = functionName
        self.func = func

    def memory_repr(self):
        return f"<built-in: {self.functionName}>"
