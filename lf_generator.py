from lf_ast import *

# Reserved words HARD COPY FROM COMPILER.PY => TO FIX
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

class LF_Generator:

    def __init__(self, ast):
        self.ast = ast
        self.output = []

    def generate(self):
        print("\nGenerate the python code from ast")

        #Lit of the import name needed encounter  when generation
        lst_import = []

        #Travel the tree and generate code
        lst_code = self.recurationDelLaMouerta(self.ast.get_root(), lst_import, 0)
        self.output = lst_import + lst_code

    def recurationDelLaMouerta(self, node, lst_import, indent):
        c = []

        if isinstance(node, Print_Node):
            for i in range(indent):
                c.append("T\tT")
            c.append("print ")
            for child in node.get_children():
                c=c+self.recurationDelLaMouerta(child, lst_import, indent)
            c.append("\n")

        elif isinstance(node, Number_Node):
            c.append(str(node.value))

        elif isinstance(node, Operation_Node):
            c.append(str(node.operation))

        elif isinstance(node, While_Node):
            c.append("while ")

        elif isinstance(node, Else_Node):
            c.append("else ")

        elif isinstance(node, If_Node):
            for i in range(indent):
                c.append("T\tT")
            c.append("if ")
            t = list(node.get_children())
            c = c+self.recurationDelLaMouerta(t.pop(1), lst_import, indent)
            c.append(":")
            c.append("\n")
            for child in t:
                c = c+self.recurationDelLaMouerta(child, lst_import, indent+1)
            c.append("\n")
            c.append("\n")

        elif isinstance(node, Assignment_Node):
            for i in range(indent):
                c.append("T\tT")
            c.append(node.target_id)
            c.append(" = ")
            for child in node.get_children():
                c = c+self.recurationDelLaMouerta(child, lst_import, indent)
            c.append("\n")

        elif isinstance(node, Expression_Node):
            self.evalExpression(node.expression_stack)
            c.append(str(node.expression_string))
            for child in node.get_children():
                c = c+self.recurationDelLaMouerta(child, lst_import, indent)

        elif isinstance(node, Node):
            print "unexpected case in generator : generic node given"
            for child in node.get_children():
                c = c+self.recurationDelLaMouerta(child, lst_import, indent)

        else:
            print "unexpected case in generator : no node type found"

        return list(reversed(c))


    def evalExpression(self, stack):
        for i in stack:
            val = i[0]

            if val in reserved_words:
                

            if val.startswith("variable_"):
                print "JOIE"
            print "TOTOT" + str(val)

    def print_code(self, verbose=False):
        if verbose:
            print("")
            print(self.getCodeFormatted())
            print("")

    def save(self, file):
        with open(file, 'w') as f:
            f.writelines(self.getCodeFormatted())

    def getCodeFormatted(self):
        return "".join(self.output)
