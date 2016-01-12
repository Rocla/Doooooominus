import sys
import os
from lf_lexer import LF_Lexer
from lf_parser import LF_Parser
from lf_generator import LF_Generator

# Reserved words
reserved_words = {

    # Conditions
    'alterum': 'IF',
    'aut': 'ELSE',
    'ergo': 'THEN',
    'initium': 'BEGIN',
    'exitus': 'END',
    'facite': 'DO',
    'iterum': 'WHILE',
    'perfectus': 'DONE',

    # Display
    'scriptor': 'PRINT',

    # Assignment
    'est': 'ASSIGN',

    # Arithmetic operators
    'multiplico': 'TIMES',
    'addo': 'PLUS',
    'minus': 'MINUS',
    'divide': 'DIVIDE',

    # Logic operators
    'et': 'AND',
    'vel': 'OR',
    'xor': 'XOR',
    'non': 'NOT',
    'vera': 'TRUE',
    'falsa': 'FALSE',

    # Relational operators
    'humilior': 'LOWERTHEN',
    'maior': 'GREATERTHEN',
    'idem': 'EQUAL',
    # 'humilior vel idem': 'LOWEREQUAL', # do it in the parser
    # 'maior vel idem': 'GREATEREQUAL', # do it in the parser
    'diversus': 'NOTEQUAL',

    # Words
    'principium': 'STRINGSTART',
    'sententia': 'SENTENTIA',
    'finis': 'STRINGSTOP',

    # Comment
    'comment': 'COMMENT',

    # Brain fuck specific
    'dextram': 'GORIGHT',
    'sinistram': 'GOLEFT',
    'incrementum': 'INCREMENT',
    'decrementum': 'DECREMENT',
    'dum': 'WHILESTART',
    'dumes': 'WHILEEND',
    'imprimo': 'BFPRINT',
    'lectito': 'READ',

}

# Tokens
tokens = [

    # Variable
    'ID',

    # Numbers
    'INTEGER',
    'REAL',

    # Parenthesis
    'LEFTPARENTHESIS',
    'RIGHTPARENTHESIS',

    # Delimiter
    'DOT',

    # TMP: Relational operators
    'LOWEREQUAL',
    'GREATEREQUAL',

]

tokens += list(reserved_words.values())


def main(args):
    # Handle command-line arguments
    if len(args) != 2:
        print >> sys.stderr, "Usage: python lexical INPUT-FILE OUTPUT-FILE"
        sys.exit(1)

    input = args[0]
    if not os.path.exists(input):
        print >> sys.stderr, input + ": File does not exist"
        sys.exit(1)

    if not os.path.isfile(input):
        print >> sys.stderr, input + ": Not a file"
        sys.exit(1)

    input = open(args[0], "r").read()
    # output = open(args[1], 'w+')

    # Run of the Latin F*ck lexer
    lexer = LF_Lexer(tokens, reserved_words)
    lexer.setup()
    lexer.tokenize(input)
    lexer.print_tokens(True)

    # Run of the Latin F*ck parser
    parser = LF_Parser(tokens, False)
    parser.setup()
    parser.parse(input, debug=0)
    parser.setup_ast()
    parser.print_ast(False)

    generator = LF_Generator(parser.ast)
    generator.generate()
    generator.save(args[1])

    print("")
    print("aedificavit prospere!")


if __name__ == "__main__":
    # main(["input/source-code", "compiled/source-code"])
    main(["input/source-code-simple", "compiled/source-code"])
