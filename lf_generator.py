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
        c = []

        #Travel the tree and generate code
        nodes = [self.ast.get_root()]
        while len(nodes) != 0:
            #start a new node, a new line
            node = nodes.pop(len(nodes) - 1)

            #indent the code
            for i in range(node.get_ast_depth()):
                c.append("\t")

            if isinstance(node, Print_Node):
                print "mhhhh, fill my with good stuff"
                
            elif isinstance(node, Number_Node):
                print "mhhhh, fill my with good stuff"

            elif isinstance(node, Operation_Node):
                print "mhhhh, fill my with good stuff"

            elif isinstance(node, While_Node):
                print "mhhhh, fill my with good stuff"

            elif isinstance(node, Then_Node):
                print "mhhhh, fill my with good stuff"

            elif isinstance(node, Else_Node):
                print "mhhhh, fill my with good stuff"

            elif isinstance(node, If_Node):
                print "mhhhh, fill my with good stuff"

            elif isinstance(node, Assignment_Node):
                print "mhhhh, fill my with good stuff"

            elif isinstance(node, Expression_Node):
                print "mhhhh, fill my with good stuff"

            elif isinstance(node, Node):
                print "mhhhh, fill my with good stuff"

            else:
                print "unexpected case in generator : generic node given"

            for child in node.get_children():
                nodes.append(child)

        self.output = lst_import + c

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
