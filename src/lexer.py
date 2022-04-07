
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

    Parameters
    ----------
    source : TextIOBase
        The source code input text stream.

    Returns
    -------
    str
        The next character.
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

def read_string(quote: str) -> Token:
    """
    Read a string from source.

    Parameters
    ----------
    source : TextIOBase
        The source code input text stream.
    quote : str
        The quote character.

    Returns
    -------
    Token
        A token with the string value.
    """
    s = ""
    while can_read():
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

def read_identifier(start: str) -> Token:
    """
    Read an identifier from source.

    Parameters
    ----------
    source : TextIOBase
        The source code input text stream.
    start : str
        The first character of the identifier.

    Returns
    -------
    Token
        A token with the identifier value.
    """
    i = start
    c = None # Next character
    while can_read():
        c = next_char()
        if c.isalnum() or c == '_':
            i += c
        else:
            break
    return Token("Identifier", i), c

def read_number(start: str) -> Token:
    """
    Read a number from source.

    Parameters
    ----------
    source : TextIOBase
        The source code input text stream.
    start : str
        The first character of the number.

    Returns
    -------
    Token
        A token with the number value.
    """
    i = start
    c = None # Next character
    while can_read():
        c = next_char()
        if c.isdigit():
            i += c
        else:
            break
    return Token("Number", i), c

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
                tokens.append(Token("AssignmentOperator", c))
            else:
                tokens.append(Token("LogicalOperator", c))
        elif c in ['(', ')', '{', '}', '[', ']']:
            tokens.append(Token("Bracket", c))
        elif c in ['.', ',', ';', ':', '?']:
            tokens.append(Token("Separator", c))
        elif c.isalpha() or c == '_':
            t, nc = read_identifier(c)
            if t.value in ['if', 'else', 'while', 'for', 'return', 'break', 'continue', 'true', 'false']:
                tokens.append(Token("Keyword", t.value))
            elif t.value in ['int', 'float', 'string', 'bool']:
                tokens.append(Token("Type", t.value))
            elif t.value in ['print', 'input']:
                tokens.append(Token("Builtin", t.value))
            elif t.value in ['true', 'false']:
                tokens.append(Token("Boolean", t.value == 'true'))
            else:
                tokens.append(Token("Identifier", t))
        elif c in ['"', "'"]:
            tokens.append(Token("String", read_string(c)))
        elif c.isdigit():
            t, nc = read_number(c)
            tokens.append(Token("Number", float(t.value)))
        else:
            raise Exception(f"Unexpected character: {c}")
    if nc != None and nc != '':
        raise Exception(f"Unexpected character: '{nc}'")
    return tokens