from io import StringIO
from src.atoms import Atom, ValueAtom
from src.interpreter import execute, globalEnvironment

def eval(input: str) -> Atom:
    res, _ = execute(StringIO(input), globalEnvironment())
    return res

