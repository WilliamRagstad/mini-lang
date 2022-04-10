
from io import TextIOBase

# Global variables

source: TextIOBase = None
line = 1
column = 0
debug = False

# Helper classes
class Token():
    """
    The smallest unit of the language.
    """
    def __init__(self, name, value):
        """
        Initialize a token with a name and a value.
        """
        global line, column
        self.name = name
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        """
        Return a string representation of the token.
        """
        return f"{self.name}: '{self.value}' at {self.line}:{self.column}"

# Helper functions
def dprint(*args):
    """
    Print debug messages.
    """
    if debug:
        print(*args)

def can_read() -> bool:
    """
    Check if source can be read.

    Returns
    -------
    bool
        True if source can be read, False otherwise.
    """
    global source
    return source.readable()

def next_char() -> str | None:
    """
    Get the next character from source.

    Returns
    -------
    str
        The next character from the source stream.
    """
    global source, line, column
    if not can_read():
        return None
    c = source.read(1)
    if c == '\n':
        line += 1
        column = 0
    else:
        column += 1
    return c

def read_string(quote: str, start: str) -> Token:
    """
    Read a string from source.

    Parameters
    ----------
    quote : str
        The quote character.

    Returns
    -------
    Token
        A token with the string value.
    """
    firstChar = True
    s = ""
    while can_read():
        if firstChar:
            c = start
            firstChar = False
        else:
            c = next_char()
        if c == quote:
            return Token("String", s)
        elif c == '\\':
            c = next_char()
            if c == 'n':
                s += '\n'
            elif c == 't':
                s += '\t'
            elif c == 'r':
                s += '\r'
            elif c == '\\':
                s += '\\'
            elif c == '"':
                s += '"'
            elif c == "'":
                s += "'"
            else:
                raise Exception(f"Unexpected character: {c}")
        else:
            s += c
    raise Exception(f"Unexpected end of file")

def read_identifier(start: str, next: str) -> Token:
    """
    Read an identifier from source.

    Parameters
    ----------
    start : str
        The first character of the identifier.
    next : str
        The next character in the stream.

    Returns
    -------
    Token
        A token with the identifier value.
    """
    if not (next.isalnum() or next == '_'):
        return Token("Identifier", start), next
    i = start + next
    c = None # Next character
    while can_read():
        c = next_char()
        if c.isalnum() or c == '_':
            i += c
        else:
            break
    return Token("Identifier", i), c

def read_number(start: str, next: str):
    """
    Read a number from source.

    Parameters
    ----------
    start : str
        The first character of the number.

    Returns
    -------
    Token
        A token with the number value.
    """
    if not (next.isdigit() or next == '.'):
        return Token("Number", float(start)), next
    n = start + next
    c: str = None # Next character
    haveDecimalPoint = next == '.'
    while can_read():
        c = next_char()
        if c.isdigit():
            n += c
        elif c == '.':
            if haveDecimalPoint:
                break
            n += c
            haveDecimalPoint = True
        else:
            break
    return Token("Number", float(n)), c

# Lexer function
def tokenize(_source: TextIOBase, _debug = False) -> list[Token]:
    """
    Tokenize source code and return a list of tokens.

    Parameters
    ----------
    source : TextIOBase
        The source code input text stream.
    debug : bool, optional
        If true, print debug messages.
    
    Returns
    -------
    list[Token]
        A list of tokens.
    """
    global source, debug
    source = _source
    debug = _debug
    tokens = []
    if can_read(): nc = next_char()
    else: return tokens
    while can_read():
        c = nc
        nc = next_char()
        if c == ' ' or c == '\n' or c == '\t':
            continue
        elif c == '\0' or c == '' or c == None:
            break
        elif c in ['+', '-', '*', '/', '%', '^']:
            if nc == '=':
                tokens.append(Token("MutationOperator", c + nc))
                nc = next_char() # Consume the equal sign
            else:
                tokens.append(Token("ArithmeticOperator", c))
        elif c in ['&', '|', '=', '<', '>', '!']:
            if nc == '=':
                tokens.append(Token("ComparisonOperator", c + nc))
                nc = next_char() # Consume the equal sign
            elif c == '=':
                if nc == '>':
                    tokens.append(Token("RightArrow", c + nc))
                    nc = next_char()
                else:
                    tokens.append(Token("AssignmentOperator", c))
            else:
                tokens.append(Token("LogicalOperator", c))
        elif c in ['(', ')', '{', '}', '[', ']']:
            tokens.append(Token("Bracket", c))
        elif c in ['.', ',', ';', ':', '?']:
            tokens.append(Token("Separator", c))
        elif c.isalpha() or c == '_':
            t, nc = read_identifier(c, nc)
            if t.value in ['if', 'else', 'while', 'for', 'return', 'break', 'continue', 'match', 'case', 'default']:
                tokens.append(Token("Keyword", t.value))
            elif t.value in ['true', 'false']:
                tokens.append(Token("Boolean", t.value == 'true'))
            else:
                tokens.append(t)
        elif c in ['"', "'"]:
            tokens.append(read_string(c, nc))
            nc = next_char() # Consume the quote
        elif c.isdigit():
            t, nc = read_number(c, nc)
            tokens.append(t)
        else:
            raise Exception(f"Unexpected character: {c}")
    if nc != None and nc != '':
        raise Exception(f"Unexpected character: '{nc}'")
    return tokens