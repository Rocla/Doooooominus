import ply.yacc as yacc

import ast
from lexical import tokens
import sys

precedence = (
#     ('left', 'ID'),
#     ('left', 'NUMBER'),
)

# dictionary of names (for storing variables)
names = {}

def p_assign(p):
   """assign : ID EST expr"""
   for element in p:
       print(element)

def p_expression_id(p):
    """expression : ID expression"""
    for element in p:
        print(element)
#
#
# def p_expression_num(p):
#     """expression : NUMBER"""


def p_expression_comment(p):
    """expression : COMMENT"""


def p_expression_string(p):
    """expression : STRING"""


def p_expression_add(p):
    """expression : ADDO"""


def p_expression_multiply(p):
    """expression : MULTIPLICO"""


def p_expression_if(p):
    """expression : ALTERUM"""


def p_expression_else(p):
    """expression : AUT"""


def p_expression_while(p):
    """expression : ITERUM"""


def p_expression_or(p):
    """expression : VEL"""


def p_expression_and(p):
    """expression : ET"""


def p_expression_xor(p):
    """expression : XOR"""


def p_expression_not(p):
    """expression : NON"""


def p_expression_tab(p):
    """expression : TABULATION"""


def p_expression_true(p):
    """expression : VERA"""


def p_expression_false(p):
    """expression : FALSA"""


def p_expression_then(p):
    """expression : ERGO"""


def p_expression_print(p):
    """expression : SCRIPTOR"""


# def p_expression_addop(p):
#     """expression : expression ADDO expression"""
#     if p[2] == '+':
#         p[0] = p[1] + p[3]
#     elif p[2] == '-':
#         p[0] = p[1] - p[3]

#
# def p_expression_mulop(p):
#     """expression : expression MUL_OP expression"""
#     if p[2] == '*':
#         p[0] = p[1] * p[3]
#     elif p[2] == '/':
#         p[0] = p[1] / p[3]


def p_error(p):
    #print("Syntax error in line %d " % p.lineno)
    parser.errok()
    #parser.token(), parser.restart()


parser = yacc.yacc(outputdir='tmp')

if __name__ == "__main__":
    result = yacc.parse(open("compiled/source-code.txt").read())
    print(result)
