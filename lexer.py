# Token types
OPERAND = 'OPERAND'             # [0-9]
ID = 'ID'                       # [a-z][A-Z][0-9]_
PLUS = 'PLUS'                   # +
MINUS = 'MINUS'                 # -
MUL = 'MUL'                     # *
DIV = 'DIV'                     # /
LPAREN = 'LPAREN'               # (
RPAREN = 'RPAREN'               # )
LESSTHAN = 'LESSTHAN'           # <
GREATERTHAN = 'GREATERTHAN'     # >
LTE = 'LTE'                     # <=
GTE = 'GTE'                     # >=
EQUAL = 'EQUAL'                 # =
NOTEQUAL = 'NOTEQUAL'           # !=
ASSIGNMENT = 'ASSIGNMENT'       # :=
AND = 'AND'                     # and
OR = 'OR'                       # or
NOT = 'NOT'                     # not
IF = 'IF'                       # if
THEN = 'THEN'                   # then
ELSE = 'ELSE'                   # else
WHILE = 'WHILE'                 # while
DO = 'DO'                       # do
END = 'END'                     # end
SEMICOLON = 'SEMICOLON'         # ;
EOF = 'EOF'                     # EOF

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invilid syntax')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def operand(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return float(result)

    def keywords(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        if result == 'and':
            return Token(AND, 'and')
        elif result == 'or':
            return Token(OR, 'or')
        elif result == 'not':
            return Token(NOT, 'not')
        elif result == 'if':
            return Token(IF, 'if')
        elif result == 'then':
            return Token(THEN, 'then')
        elif result == 'else':
            return Token(ELSE, 'else')
        elif result == 'while':
            return Token(WHILE, 'while')
        elif result == 'do':
            return Token(DO, 'do')
        elif result == 'end':
            return Token(END, 'end')
        else:
            return Token(ID, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return Token(OPERAND, self.operand())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '<':
                if self.text[self.pos + 1] == '=':
                    self.advance()
                    self.advance()
                    return Token(LTE, '<=')
                else:
                    self.advance()
                    return Token(LESSTHAN, '<')

            if self.current_char == '>':
                if self.text[self.pos + 1] == '=':
                    self.advance()
                    self.advance()
                    return Token(GTE, '>=')
                else:
                    self.advance()
                    return Token(GREATERTHAN, '>')

            if self.current_char == '=':
                self.advance()
                return Token(EQUAL, '=')

            if self.current_char == ':':
                if self.text[self.pos + 1] == '=':
                    self.advance()
                    self.advance()
                    return Token(ASSIGNMENT, ':=')
                else:
                    self.error()

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char.isalnum():
                return self.keywords()

            self.error()
        return Token(EOF, None)
