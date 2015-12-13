__author__ = 'forrest'

INTEGER = 'INTEGER'
EOF = 'EOF'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return '({type}, {value})'.format(type = self.type, value = self.value)

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

            self.error()

        return Token(EOF, None)

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        operand = []
        operator = []

        while self.current_token.value is not None:
            if self.current_token.type == INTEGER:
                operand.append(self.current_token.value)
            else:
                operator.append(self.current_token)
            self.current_token = self.get_next_token()

        while len(operator) != 0:
            op = operator.pop()
            result = 0
            if op.type == PLUS:
                right = operand.pop()
                left = operand.pop()
                result = right + left
            elif op.type == MINUS:
                right = operand.pop()
                left = operand.pop()
                result = left - right
            operand.append(result)

        return operand[0]


def main():
    while True:
        try:
            text = input('>>> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()