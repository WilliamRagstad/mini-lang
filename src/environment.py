
from .atoms import Atom


class Environment():
    """
    The Environment class is used to store the values of
    variables in a scope during the execution of a program.
    """
    def __init__(self, name: str, parent):
        """
        Initialize an environment with a name and a parent environment.
        """
        self.name = name
        self.parent: Environment = parent
        self.values: dict[str, Atom] = {}

    def set(self, name: str, value: Atom) -> None:
        self.values[name] = value

    def get(self, name: str):
        if name in self.values:
            return self.values[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None

    def __str__(self):
        return f"Environment<{self.name}> {self.values}"

def globalEnvironment():
    return Environment("global", None)
