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
    
    def structural_eq(self, other: "Atom") -> bool:
        """
        Check if two atoms are structurally equal.
        """
        raise Exception(f"Structural equality not implemented for base class '{self.__class__.__name__}'!")
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Atom):
            return self.structural_eq(__value)
        return False
    
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

class IntrinsicAtom(Atom):
    """
    An intrinsic value node in the abstract syntax tree.
    This is not intended to be created by the user.
    """
    def __init__(self, type: str, value):
        """
        Initialize an intrinsic value node with a value.

        Parameters
        ----------
            type: The type of the value in lower case.
                       E.g. "string", "number", "bool", "unit", "tuple", "list".
            value: The value of the node.
        """
        super().__init__("Intrinsic", type)
        self.value = value

    def memory_repr(self):
        return f"<{self.uid}:intrinsic:{self.type}:{self.value}>"

    def structural_eq(self, other: "Atom") -> bool:
        return isinstance(other, IntrinsicAtom) and self.type == other.type and self.value == other.value

class ValueAtom(Atom):
    """
    An atomic value node in the abstract syntax tree.
    """
    def __init__(self, type: str, value):
        """
        Initialize an atomic value node with a value.

        Parameters
        ----------
            type: The type of the value in lower case.
                       E.g. "string", "number", "bool", "unit", "tuple", "list".
            value: The value of the node.
        """
        super().__init__("Value", type)
        self.value = value

    def listValueToStr(self):
        return list(map(lambda a: a.formatted_str(), self.value))
    
    def raw_str(self):
        return self.format(True)

    def formatted_str(self):
        return self.format(False)

    def format(self, raw: bool) -> str:
        if self.type == "string":
            if raw: return self.value
            escaped = self.value.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
            return f"'{escaped}'"
        elif self.type == "bool":
            return str(self.value).lower()
        elif self.type == "unit":
            return "()"
        elif self.type == "tuple":
            return '(' + ", ".join(self.listValueToStr()) + ')'
        elif self.type == "list":
            return '[' + ", ".join(self.listValueToStr()) + ']'
        elif self.type == "map":
            if not isinstance(self.value, dict):
                raise Exception(f"ValueAtom of type 'map' has value of type '{type(self.value)}'!")
            value: dict[str, ValueAtom] = self.value
            return '#{' + ", ".join(map(lambda t: f"{t[0]}: {t[1].formatted_str()}", value.items())) + '}'
        return str(self.value)


    def memory_repr(self):
        return f"<{self.uid}:{self.type}:{self.formatted_str()}>"

    def structural_eq(self, other: "Atom") -> bool:
        if isinstance(other, ValueAtom) and self.type == other.type:
            match self.type:
                case "map":
                    # todo
                    pass
                case "tuple" | "list":
                    if len(self.value) != len(other.value): return False
                    return all(map(lambda t: t[0].structural_eq(t[1]), zip(self.value, other.value)))
                case "unit": return True # Unit is always equal
                case _: return self.value == other.value
        return False

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
    
    def structural_eq(self, other: "Atom") -> bool:
        return isinstance(other, FunctionAtom) and self.uid == other.uid # Compare by uid

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

    def structural_eq(self, other: "Atom") -> bool:
        return isinstance(other, BuiltinFunctionAtom) and self.uid == other.uid # Compare by uid