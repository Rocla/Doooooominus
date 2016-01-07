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
        self.reserved = reserved_words

    def t_ID(self, t):
        r'[A-Za-z_]\w*'
        if t.value in self.reserved:
            t.type = t.value.upper()
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def tokenize(self, data):
        self.lexer.input(data)

    def setup(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_error(self, t):
        print "Invalid char: %s" % t.value[0]
        t.lexer.skip(1)

    def print_tokens(self, print_tokens=False):
        if print_tokens:
            while True:
                token = self.lexer.token()
                if not token:
                    break
                print(token)
