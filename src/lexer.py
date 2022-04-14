from io import TextIOBase

# Token class
class Token():
    """
    The smallest unit of the language.
    """
    def __init__(self, name: str, line, column, value = None):
        """
        Initialize a token with a name and a value.
        """
        self.name = name
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        """
        Return a string representation of the token.
        """
        return f"{self.name}: '{self.value}' at {self.line}:{self.column}"

# Lexer class
class Lexer:
    def __init__(self, source: TextIOBase, debug = False):
        self.__source = source
        self.__line = 1
        self.__column = 1
        self.__debug = debug
        self.__peeked_char: str | None = None # The last character that was peeked
        self.__peeked_token: Token | None = None # The last token that was peeked
        self.__prev_comment: Token | None = None # The last comment that was read before the previous token

    # Helper functions
    def __dprint(self, *args):
        """
        Print debug information.
        """
        if self.__debug:
            print(*args)
    def __token(self, name: str, value = None) -> Token:
        """
        Create a token with the given name and value.
        """
        return Token(name, self.__line, self.__column, value)

    def __error(self, msg: str):
        """
        Raise an error with the given message.
        """
        raise Exception(f"Syntax Error at {self.__line}:{self.__column}: {msg}")

    # Tokenizer functions
    def __can_read(self) -> bool:
        """
        Check if source can be read.

        Returns
        -------
        bool
            True if source can be read, False otherwise.
        """
        return self.__source.readable()

    def __next_char(self):
        """
        Get the next character from source.

        Returns
        -------
        str | None
            The next character from the source stream.
            Or None if the end of the stream has been reached.
        """
        if self.__peeked_char is not None:
            c = self.__peeked_char
            self.__peeked_char = None # Reset peeked char
        else:
            if not self.__can_read():
                return None
            c = self.__source.read(1)
        if c == '\n':
            self.__line += 1
            self.__column = 1
        else:
            self.__column += 1
        return c

    def __peek_char(self):
        """
        Get the next character from source without consuming it.

        Returns
        -------
        str | None
            The next character from the source stream.
            Or None if the end of the stream has been reached.
        """
        if self.__peeked_char is not None:
            return self.__peeked_char
        else:
            if not self.__can_read():
                c = None
            else:
                c = self.__source.read(1)
            # Put the character in the queue
            self.__peeked_char = c
            return c

    def __read_string(self, quote: str) -> Token:
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
        s = ""
        while self.__can_read():
            c = self.__next_char()
            if c == quote:
                return self.__token("STRING", s)
            elif c == '\\':
                c = self.__next_char()
                if c == 'n':
                    s += '\n'
                elif c == 't':
                    s += '\t'
                elif c == 'r':
                    s += '\r'
                elif c == '\\':
                    s += '\\'
                elif c in ['"', "'"]:
                    s += c
                else:
                    self.__error("Invalid escape sequence: \\" + c)
            else:
                s += c
        self.__error("Unterminated string")

    def __read_identifier(self, first: str) -> Token:
        """
        Read an identifier from source.

        Returns
        -------
        Token
            A token with the identifier value.
        """
        s = first
        nc = self.__peek_char()
        while nc.isalnum() or nc == '_':
            s += self.__next_char()
            if self.__can_read():
                nc = self.__peek_char()
            else:
                break
        return self.__token("IDENTIFIER", s)

    def __read_number(self, first: str) -> Token:
        """
        Read a number from source.

        Returns
        -------
        Token
            A token with the number value.
        """
        s = first
        decimalPoint = False
        nc = self.__peek_char()
        while nc.isdigit() or nc == '.':
            if nc == '.':
                if decimalPoint:
                    break
                decimalPoint = True
            s += self.__next_char()
            if self.__can_read():
                nc = self.__peek_char()
            else:
                break
        return self.__token("NUMBER", float(s))

    def __read_token(self) -> Token:
        """
        Tokenize the next character from source.

        Returns
        -------
        Token
            The next token from the source stream.
        """
        c = self.__next_char()
        if c in ['', '\0', None]: return self.__token("EOF")
        nc = self.__peek_char() # Look ahead one character: LL(1)

        # Whitespace
        if c in [' ', '\t', '\n', '\r']:
            return self.__read_token() # Skip whitespace
        if c in ['"', "'"]:
            return self.__read_string(c)
        if c.isdigit():
            return self.__read_number(c)
        if c.isalpha() or c == '_':
            t = self.__read_identifier(c)
            if t.value in ["true", "false"]:
                return self.__token("BOOLEAN", t.value == "true")
            if t.value in ["if", "else", "match", "class", "enum", "while", "for", "break", "continue", "return"]:
                return self.__token("KEYWORD", t.value)
            return t
        if c == '/' and nc == '/':
            self.__next_char() # Consume the '/'
            comment = ""
            while self.__can_read() and self.__peek_char() != '\n':
                comment += self.__next_char()
            return self.__token("COMMENT", comment)
        if c == '/' and nc == '*':
            self.__next_char() # Consume the '*'
            comment = ""
            while self.__can_read():
                c = self.__next_char()
                if c == '*' and self.__peek_char() == '/':
                    self.__next_char()
                    break
                comment += c
            return self.__token("COMMENT", comment)
        # Operators
        if c == '+' and nc == '=': return self.__token("PLUSEQUAL", c + self.__next_char())
        if c == '-' and nc == '=': return self.__token("MINUSEQUAL", c + self.__next_char())
        if c == '*' and nc == '=': return self.__token("TIMESEQUAL", c + self.__next_char())
        if c == '/' and nc == '=': return self.__token("DIVEQUAL", c + self.__next_char())
        if c == '%' and nc == '=': return self.__token("MODEQUAL", c + self.__next_char())
        if c == '^' and nc == '=': return self.__token("POWEQUAL", c + self.__next_char())
        if c == '<' and nc == '=': return self.__token("LESSEQUAL", c + self.__next_char())
        if c == '>' and nc == '=': return self.__token("GREATEREQUAL", c + self.__next_char())
        if c == '!' and nc == '=': return self.__token("NOTEQUAL", c + self.__next_char())
        if c == '=' and nc == '=': return self.__token("EQUAL", c + self.__next_char())
        if c == '=' and nc == '>': return self.__token("RIGHTARROW", c + self.__next_char())
        if c == '&' and nc == '&': return self.__token("AND", c + self.__next_char())
        if c == '|' and nc == '|': return self.__token("OR", c + self.__next_char())
        if c == '+': return self.__token("PLUS", c)
        if c == '-': return self.__token("MINUS", c)
        if c == '*': return self.__token("MULTIPLY", c)
        if c == '/': return self.__token("DIVIDE", c)
        if c == '%': return self.__token("MODULO", c)
        if c == '^': return self.__token("POWER", c)
        if c == '<': return self.__token("LESS", c)
        if c == '>': return self.__token("GREATER", c)
        if c == '=': return self.__token("ASSIGNMENT", c)
        if c == '!': return self.__token("NOT", c)
        if c == '&': return self.__token("BITWISEAND", c)
        if c == '|': return self.__token("BITWISEOR", c)
        if c == '~': return self.__token("BITWISENOT", c)
        if c == '?': return self.__token("QUESTIONMARK", c)
        if c == '.': return self.__token("DOT", c)
        if c == ',': return self.__token("COMMA", c)
        if c == ':': return self.__token("COLON", c)
        if c == ';': return self.__token("SEMICOLON", c)
        if c == '{': return self.__token("LBRACE", c)
        if c == '}': return self.__token("RBRACE", c)
        if c == '(': return self.__token("LPAREN", c)
        if c == ')': return self.__token("RPAREN", c)
        if c == '[': return self.__token("LBRACKET", c)
        if c == ']': return self.__token("RBRACKET", c)
        self.__error("Unexpected character: " + c)


    def is_done(self):
        """
        Check if the lexer is done.

        Returns
        -------
        bool
            True if the lexer is done, False otherwise.
        """
        return not self.__can_read() or self.peek_token().name == "EOF"

    def reset_peek(self):
        """
        Reset the peek token.
        """
        self.__peeked_token = None

    def peek_token(self, allow_comment = False) -> Token:
        """
        Peek at the next token.

        Returns
        -------
        Token
            The next token.
        """
        if self.__peeked_token is not None:
            return self.__peeked_token
        else:
            t = self.next_token(allow_comment)
            self.__peeked_token = t
            return t

    def next_token(self, allow_comment = False) -> Token:
        """
        Get the next token from the source.

        Returns
        -------
        Token
            The next token from the source.
        """
        if self.__peeked_token is not None:
            t = self.__peeked_token
            self.reset_peek()
            return t
        else:
            t = self.__read_token()
            if not allow_comment and t.name == "COMMENT":
                self.__prev_comment = t
                return self.next_token(False)
            return t

    def prev_comment(self):
        return self.__prev_comment
