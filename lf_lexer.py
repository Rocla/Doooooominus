import ply.lex as lex

class LF_Lexer:
    t_INTEGER = r'\d+'
    t_REAL = r'\d+\,\d+'
    t_LEFTPARENTHESIS = r'\('
    t_RIGHTPARENTHESIS = r'\)'
    t_DOT = r'.'

    t_ignore = ' \t'

    def __init__(self, tokens, reserved_words):
        self.tokens = tokens
        self.reserved_words = reserved_words

    def t_comment(self, t):
        r'comment.+.'
        t.lexer.lineno += 1

    def t_ID(self, t):
        r'[A-Za-z_]\w*'
        t.type = self.reserved_words.get(t.value, "ID")
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def tokenize(self, data):
        self.lexer.input(data)

    # **kwargs for dictionaries
    def setup(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_error(self, t):
        print "Invalid token: %s" % t.value[0]
        t.lexer.skip(1)

    def print_tokens(self, verbose=False):
        if verbose:
            print("")
            while True:
                token = self.lexer.token()
                if not token:
                    break
                print(token)
            print("")
