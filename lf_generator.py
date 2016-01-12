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
            node = nodes.pop(len(nodes) - 1)

            #indent the code
            for i in range(node.get_ast_depth()):
                c.append("\t")

            if isinstance(node, Print_Node):
                c.append("print ")

            elif isinstance(node, Number_Node):
                c.append(str(node.value))

            elif isinstance(node, Operation_Node):
                c.append(str(node.operation))

            elif isinstance(node, While_Node):
                c.append("while ")

            elif isinstance(node, Then_Node):
                c.append(":")
                c.append("\n")

            elif isinstance(node, Else_Node):
                c.append("else ")

            elif isinstance(node, If_Node):
                c.append("if ")

            elif isinstance(node, Assignment_Node):
                c.append(node.target_id)
                c.append(" = ")
                for child in node.get_children():
                    nodes.append(child)
                c.append("\n")

            elif isinstance(node, Expression_Node):
                c.append(str(node.expression_string))

            elif isinstance(node, Node):
                print "unexpected case in generator : generic node given"
                for child in node.get_children():
                    nodes.append(child)

            else:
                print "unexpected case in generator : no node type found"
                
            #for child in node.get_children():
            #    nodes.append(child)


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
