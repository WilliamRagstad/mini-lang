
class Environment():
    """
    The Environment class is used to store the values of
    variables in a scope during the execution of a program.
    """
    def __init__(self, name, parent):
        """
        Initialize an environment with a name and a parent environment.
        """
        self.name = name
        self.parent = parent
        self.values = {}

    def set(self, name, value):
        self.values[name] = value
    
    def get(self, name):
        if name in self.values:
            return self.values[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None
