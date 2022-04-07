# Fundamental value types in the language
from typing import Callable

from .environment import Environment
from .parser import Node

class Atom():
    """
    A fundamental value type in the language.
    """
    def __init__(self, name, type):
        """
        Initialize an atom with a name and a type.
        """
        self.name = name
        self.type = type
    
    def __str__(self):
        return f"<{self.type}>"

class UnitAtom(Atom):
    """
    A unit atom in the language.
    """
    def __init__(self):
        """
        Initialize a unit atom.
        """
        super().__init__("Unit", "unit")
    
    def __str__(self):
        return f"()"

class ValueAtom(Atom):
    """
    An atomic value node in the abstract syntax tree.
    """
    def __init__(self, valueType: str, value):
        """
        Initialize an atomic value node with a value.
        """
        super().__init__("Value", valueType)
        self.valueType = valueType
        self.value = value
    
    def __str__(self):
        value = '"' + str(self.value) + '"' if self.valueType == "string" else str(self.value)
        return f"<{self.valueType}: {value}>"

class FunctionAtom(Atom):
    """
    A function node in the abstract syntax tree.
    """
    def __init__(self, functionName: str, argumentNames: list[str], body: list[Node], environment: Environment):
        """
        Initialize a function node with a function name, argument names, body and the environment in which it was defined.
        """
        super().__init__("Function", "function")
        self.functionName = functionName
        self.argumentNames = argumentNames
        self.body = body
        self.environment = environment

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