from interpreter import *

def main():
    print('Pluto version 0.0.4')
    while True:
        try:
            text = input('>>> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)

if __name__ == '__main__':
    main()
