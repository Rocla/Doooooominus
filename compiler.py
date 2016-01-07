import os
import sys

from lf_lexer import LF_Lexer
from lf_parser import LF_Parser

# List of reserved words
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
    #'humilior vel idem': 'LOWEREQUAL', # do it in the parser
    #'maior vel idem': 'GREATEREQUAL', # do it in the parser
    'diversus': 'NOTEQUAL',

    # Words
    'principium': 'STRINGSTART',
    'sententia': 'SENTENTIA',
    'finis': 'STRINGSTOP',

    # Comment
    'comment': 'COMMENT'

}

# List of tokens
tokens = (

    # Variables
    'ID',

    # Numbers
    'INTEGER',
    'REAL',

    # Parenthesis
    'LEFTPARENTHESIS',
    'RIGHTPARENTHESIS',

    # Delimiters
    'DOT',

) + tuple(map(lambda s: s.upper(), reserved_words))

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
    #output = open(args[1], 'w+')

    # Run of the Latin F*ck lexer
    lexer = LF_Lexer(tokens, reserved_words)
    lexer.setup()
    lexer.tokenize(input)
    #lexer.print_tokens(True)

    # Run of the Latin F*ck parser
    parser = LF_Parser(tokens)
    parser.setup()
    parser.parse(input, debug=0)

    print("aedificavit prospere!")

if __name__ == "__main__":
    #main(["input/source-code.txt", "compiled/source-code.txt"])
    main(["input/source-code-simple.txt", "compiled/source-code.txt"])