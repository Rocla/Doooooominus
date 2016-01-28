from lf_ast import *

# Reserved words HARD COPY FROM COMPILER.PY => TO FIX
arithmetic_words = {

    # Arithmetic operators
    'multiplico': '*',
    'addo': '+',
    'minus': '-',
    'divide': '/',

    # Logic operators
    'et': ' and ',
    'vel': ' or ',
    'xor': ' xor ',
    'non': ' not ',

    # Relational operators
    'humilior': '<',
    'maior': '>',
    'idem': '==',
    'diversus': '!=',
    'humiliorem': '<=',
    'miaom': '>=',
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
        lst_code = self.recurationDelLaMouerta(self.ast.get_root(), lst_import)
        self.output = lst_import + lst_code

    def recurationDelLaMouerta(self, node, lst_import, indent=0):
        c = []

        if isinstance(node, Print_Node):
            for i in range(indent):
                c.append("\t")
            c.append("print ")
            for child in node.get_children():
                c=c+self.recurationDelLaMouerta(child, lst_import, indent)
            c.append("\n")

        elif isinstance(node, Number_Node):
            v = node.value
            c.append(v)

        elif isinstance(node, Operation_Node):
            c.append(str(node.operation))

        elif isinstance(node, While_Node):
            for i in range(indent):
                c.append("\t")
            c.append("while ")
            t = list(node.get_children())
            c = c+self.recurationDelLaMouerta(t.pop(len(t)-1), lst_import, indent)
            c.append(": \n")
            for child in t:
                c = c+list(reversed(self.recurationDelLaMouerta(child, lst_import, indent+1)))
            #c.append("\n")

        elif isinstance(node, Else_Node):
            for child in node.get_children():
                c = c+self.recurationDelLaMouerta(child, lst_import, indent+1)
            c.append("else :\n")

        elif isinstance(node, Then_Node):
            for child in node.get_children():
                c = c+self.recurationDelLaMouerta(child, lst_import, indent+1)

        elif isinstance(node, If_Node):
            for i in range(indent):
                c.append("\t")
            c.append("if ")
            t = list(node.get_children())
            c = c+self.recurationDelLaMouerta(t.pop(len(t)-1), lst_import, indent)
            c.append(":\n")

            for child in reversed(t):
                c = c+self.recurationDelLaMouerta(child, lst_import, indent)


        elif isinstance(node, Assignment_Node):
            for i in range(indent):
                c.append("\t")
            c.append(node.target_id)
            c.append(" = ")
            for child in node.get_children():
                c = c+self.recurationDelLaMouerta(child, lst_import, indent)
            c.append("\n")

        elif isinstance(node, Expression_Node):
            s = list(reversed(node.expression_stack))
            m = []
            while len(s) > 0:
                if s[len(s)-1][0] in arithmetic_words:
                    m1 = m.pop()
                    m2 = m.pop()
                    sub = ""
                    sub += str(self.recurationDelLaMouerta(m2[1], lst_import, indent)[0])
                    sub += str(arithmetic_words[s.pop()[0]])
                    sub += str(self.recurationDelLaMouerta(m1[1], lst_import, indent)[0])
                    m.insert(0, ("("+sub+")", Number_Node(value="("+sub+")")))
                else:
                    x = s.pop()
                    m.append((x))

            tmp = "".join([x[0] for x in m])
            if tmp.startswith("(") and tmp.endswith(")"):
                tmp = tmp[1:len(tmp)-1]
            c.append(tmp)


        elif isinstance(node, Node):
            for child in node.get_children():
                c = c+self.recurationDelLaMouerta(child, lst_import, indent)

        else:
            print "unexpected case in generator : no node type found"

        return list(reversed(c))

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

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False
