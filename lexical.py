import ply.lex as lex
import os
import sys

"---------------------------------------"
"   TOKEN                               "
"---------------------------------------"

reserved_words = [
    'alterum',  # if
    'aut',  # else
    'iterum',  # while
    'scriptor',  # print line
    'et',  # and
    'vel',  # or
    'xor',
    'non',  # not
    'vera',  # true
    'falsa',  # false
    'est',  # is
    'ergo',  # then
    'multiplico',  # multiply
    'addo',  # add

]

tokens = (
    'ID',
    'NUMBER',
    'STRING',
    'COMMENT',  #
    'TABULATION',
) + tuple(map(lambda s: s.upper(), reserved_words))

"---------------------------------------"
"   RULES                               "
"---------------------------------------"

literals = '(){}'
# ignore tabulation and withe space
t_ignore = ' '


#'sententia',  # string

def t_STRING(t):
    r'sententia[^sententia]+sententia'
    return t

def t_ID(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_COMMENT(t):
    r'\#'
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_TABULATION(t):
    r'\t'
    return t


"---------------------------------------"
"   OUTPUT                              "
"---------------------------------------"


def t_error(t):
    print(" Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


"---------------------------------------"
"   MAIN TEST                           "
"---------------------------------------"

lex.lex()


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

    output = args[1]

    # Start lex
    print("Starting lex")

    tokensList = []
    lex.input(open(input).read())
    fileResult = open(output, 'w+')

    while 1:
        tok = lex.token()
        if not tok:
            break

        result = "%s %s" % (tok.type, tok.value) #%d tok.lineno
        fileResult.write(result + "\n")
        print(result)
        tokensList.append(tok)

    print("Token creation ended with success. Number of tokensList : %d" % len(tokensList))


if __name__ == "__main__":
    #main(["input/source-code.txt", "compiled/source-code.txt"])
    main(["input/source-code-simple.txt", "compiled/source-code.txt"])
    #main(sys.argv[1:])
