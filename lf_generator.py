from lf_ast import *


class LF_Generator:

    def __init__(self, ast):
        self.ast = ast
        self.output = []

    def generate(self):
        print("\nGenerate the python code from ast")

        #Lit of the import name needed encounter  when generation
        lst_import = []
        #List of the code generated
        lst_code = []

        #Travel the tree and generate code
        self.recurationDelLaMouerta(self.ast.get_root(), lst_import, lst_code, 0)
        self.output = lst_import + lst_code

    def recurationDelLaMouerta(self, node, lst_import, c, indent):
        if isinstance(node, Print_Node):
            for i in range(indent):
                c.append("T\tT")
            c.append("print ")
            for child in node.get_children():
                self.recurationDelLaMouerta(child, lst_import, c, indent)
            c.append("\n")

        elif isinstance(node, Number_Node):
            c.append(str(node.value))

        elif isinstance(node, Operation_Node):
            c.append(str(node.operation))

        elif isinstance(node, While_Node):
            c.append("while ")

        #elif isinstance(node, Then_Node):

        elif isinstance(node, Else_Node):
            c.append("else ")

        elif isinstance(node, If_Node):
            for i in range(indent):
                c.append("T\tT")
            c.append("if ")
            t = list(node.get_children())
            self.recurationDelLaMouerta(t.pop(1), lst_import, c, indent)
            c.append(":")
            c.append("\n")
            for child in t:
                self.recurationDelLaMouerta(child, lst_import, c, indent+1)
            c.append("\n")
            c.append("\n")


        elif isinstance(node, Assignment_Node):
            for i in range(indent):
                c.append("T\tT")
            c.append(node.target_id)
            c.append(" = ")
            for child in node.get_children():
                self.recurationDelLaMouerta(child, lst_import, c, indent)
            c.append("\n")

        elif isinstance(node, Expression_Node):
            c.append(str(node.expression_string))
            for child in node.get_children():
                self.recurationDelLaMouerta(child, lst_import, c, indent)

        elif isinstance(node, Node):
            print "unexpected case in generator : generic node given"
            for child in node.get_children():
                self.recurationDelLaMouerta(child, lst_import, c, indent)

        else:
            print "unexpected case in generator : no node type found"


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
