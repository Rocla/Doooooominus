import sys
import ply.yacc as yacc
# from lf_ast import *


class LF_Parser:

    def p_base_empty(self, p):
        """base :"""

    def p_error(self, p):
        print("!!! defecerunt processus !!!")
        if p is not None:
            print("Token type:     %s" % (str(p.type)))
            print("Value:          %s" % (str(p.value)))
            print("Linea numerus:  %s" % (str(p.lineno)))
            print("Token position: %s" % (str(p.lexpos)))
        sys.exit()

    def __init__(self, tokens):
        self.tokens = tokens
        self.tree_depth = 0

    def parse(self, data, **kwargs):
        self.parser.parse(data, **kwargs)

    def setup(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def tree_depth_increase(self, verbose=False):
        if verbose:
            print self.tree_depth
        self.tree_depth += 1

    def tree_depth_decrease(self, verbose=False):
        if verbose:
            print self.tree_depth
        self.tree_depth -= 1

    def set_tree_depth(self, depth):
        self.tree_depth = depth

    def get_tree_depth(self):
        return self.tree_depth
