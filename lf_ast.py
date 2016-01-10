import sys


class Node:
    def __init__(self, parent=None, children=None, node_name=None, current_depth=None, current_symbols=None):
        """
        :param parent: pointer parent
        :param children: list of children
        :param node_name: name of the node
        :param current_depth: depth of self
        :param current_symbols: symbols accessible from self
        """
        if current_symbols is None:
            current_symbols = []
        if children is None:
            children = []
        self.parent = parent
        self.children = list(children)
        self.ast_depth = current_depth
        self.node_label = node_name
        self.current_symbols = current_symbols

    # Parent
    def get_parent(self):
        return self.parent

    def set_parent(self, new_node):
        self.parent = new_node

    # Children
    def get_children(self):
        return self.children

    def get_number_of_children(self):
        return len(self.children)

    def set_children(self, new_children):
        self.children = new_children

    def add_children(self, nodes):
        for node in nodes:
            self.children.append(node)

    def add_child(self, node):
        self.children.append(node)

    def get_name(self):
        return self.node_label

    def set_name(self, label):
        self.node_label = label

    # AST

    def set_ast_depth(self, new_index):
        self.ast_depth = new_index

    def get_ast_depth(self):
        return self.ast_depth

    def get_current_symbols(self):
        return self.current_symbols

    def set_current_symbols(self, new_current_symbols):
        self.current_symbols = new_current_symbols

    def get_symbol_type(self, symbol):
        tmp_node = self
        while tmp_node is not None:
            for element in tmp_node.current_symbols:
                if element[0] == symbol:
                    return element[1]
            tmp_node = tmp_node.get_parent()
        return False

    def add_symbol(self, symbol, symbol_type):
        tmp_node = self
        while tmp_node is not None:
            for element in tmp_node.current_symbols:
                if element[0] == symbol:
                    if element[1] != symbol_type:
                        print("ERROR of type: the variable " + symbol[2:] + " was initialized as: " + element[1])
                        sys.exit()
            tmp_node = tmp_node.get_parent()
        self.current_symbols.append([symbol, symbol_type, len(self.current_symbols)])

    def check_symbol(self, symbol):
        tmp_node = self
        while tmp_node is not None:
            for element in tmp_node.current_symbols:
                if element[0] == symbol:
                    return True
            tmp_node = tmp_node.get_parent()
        return False


class AST:
    def __init__(self, root=None, current_node=None):
        self.root = root
        self.current_node = current_node

    def setup_ast(self):
        nodes = [self.get_root()]
        while len(nodes) != 0:
            node = nodes.pop(len(nodes) - 1)
            node.get_children().reverse()
            for child in node.get_children():
                nodes.append(child)

    def get_root(self):
        return self.root

    def set_root(self, node):
        self.root = node

    def get_current_node(self):
        return self.current_node

    def set_current_node(self, node):
        self.current_node = node

    def print_current_symbols(self):
        print("\nThe known symbols so far are:")
        for symbol in self.current_node.get_current_symbols():
            print(symbol)

    def print_ast(self):
        print("\nAbstract syntax tree: [depth] [node name]")
        nodes = [self.get_root()]
        while len(nodes) != 0:
            node = nodes.pop(len(nodes) - 1)
            separator = ""
            for i in range(node.get_ast_depth()):
                separator += "- "
            print(str(node.get_ast_depth()) + " " + str(separator) + str(node.get_name()))

            if isinstance(node, Expression_Node):
                separator = "   "
                for i in range(node.get_ast_depth()):
                    separator += " "
                print(separator + " type: " + node.get_expression_type())
                print(separator + " stack: " + node.get_expression_string())

            for child in node.get_children():
                nodes.append(child)


class Expression_Node(Node):
    def __init__(self, parent=None, children=None, node_name=None, current_depth=None, current_symbols=None,
                 expression_ast_root=None, expression_type=None, expression_stack=None, expression_string=None):
        Node.__init__(self, parent, children, node_name, current_depth, current_symbols)
        self.expression_ast_root = expression_ast_root
        self.expression_type = expression_type
        self.expression_stack = expression_stack
        self.expression_string = expression_string

    def get_expression_ast_root(self):
        return self.expression_ast_root

    def set_expression_ast_root(self, new_expression_ast_root):
        self.expression_ast_root = new_expression_ast_root

    def get_expression_stack(self):
        return self.expression_stack

    def set_expression_stack(self, new_expression_stack):
        self.expression_stack = new_expression_stack

    def get_expression_type(self):
        return self.expression_type

    def set_expression_type(self, new_expression_type):
        self.expression_type = new_expression_type

    def get_expression_string(self):
        return self.expression_string

    def set_expression_string(self, new_expression_string):
        self.expression_string = new_expression_string

    def build_expression_stack(self):
        nodes = [self.get_expression_ast_root()]
        expression_stack = []
        expression_string = ""
        expression_type_matching = []

        while len(nodes) != 0:
            node = nodes.pop(len(nodes) - 1)

            if isinstance(node, Number_Node):
                expression_stack.append((node.get_value(), node))
                if not node.get_value_type() in expression_type_matching:
                    expression_type_matching.append(node.get_value_type())

            if isinstance(node, Operation_Node):
                expression_stack.append((node.get_operation(), node))

            for child_nodes in node.get_children():
                nodes.append(child_nodes)

        expression_stack.reverse()
        for element in expression_stack:
            expression_string += str(element[0])

        self.expression_stack = expression_stack
        self.expression_string = expression_string

        if len(expression_type_matching) != 1:
            print("ERROR: There are different types in this expression: " + self.expression_string)
            print("Note that the expressions must be all Integer elements or all Real elements.")
            print(expression_type_matching)
            sys.exit()

        self.set_expression_type(expression_type_matching[0])


class Assignment_Node(Node):
    def __init__(self, parent=None, children=None, node_name=None, current_depth=None, current_symbols=None,
                 target_id=None, expression_node=None, expression_type=None):
        Node.__init__(self, parent, children, node_name, current_depth, current_symbols)
        self.target_id = target_id
        self.expression_node = expression_node
        self.expression_type = expression_type

    def get_target_id(self):
        return self.target_id

    def set_target_id(self, new_id):
        self.target_id = new_id

    def get_expression_node(self):
        return self.expression_node

    def set_expression_node(self, new_expression_node):
        self.expression_node = new_expression_node

    def get_expression_type(self):
        return self.expression_type

    def set_expression_type(self, new_expression_type):
        self.expression_type = new_expression_type


class If_Node(Node):
    def __init__(self, parent=None, children=None, node_name=None, current_depth=None, current_symbols=None,
                 expression_type=None):
        Node.__init__(self, parent, children, node_name, current_depth, current_symbols)
        self.expression_type = expression_type

    def get_expression_type(self):
        return self.expression_type

    def set_expression_type(self, new_expression_type):
        self.expression_type = new_expression_type


class Else_Node(Node):
    def __init__(self, parent=None, children=None, current_depth=None, node_name=None, current_symbols=None):
        Node.__init__(self, parent, children, node_name, current_depth, current_symbols)


class Then_Node(Node):
    def __init__(self, parent=None, children=None, current_depth=None, node_name=None, current_symbols=None):
        Node.__init__(self, parent, children, node_name, current_depth, current_symbols)


class While_Node(Node):
    def __init__(self, parent=None, children=None, node_name=None, current_depth=None, current_symbols=None,
                 expression_node=None, expression_type=None):
        Node.__init__(self, parent, children, node_name, current_depth, current_symbols)
        self.expression_node = expression_node
        self.expression_type = expression_type

    def get_expression_node(self):
        return self.expression_node

    def set_expression_node(self, new_node):
        self.expression_node = new_node

    def get_expression_type(self):
        return self.expression_type

    def set_expression_type(self, new_expression_type):
        self.expression_type = new_expression_type


class Operation_Node(Node):
    def __init__(self, parent=None, children=None, node_name=None, current_depth=None, current_symbols=None,
                 operation=None):
        Node.__init__(self, parent, children, node_name, current_depth, current_symbols)
        self.operation = operation

    def get_operation(self):
        return self.operation

    def set_operation(self, new_operation):
        self.operation = new_operation


class Number_Node(Node):
    def __init__(self, parent=None, children=None, node_name=None, current_depth=None, current_symbols=None,
                 sign=None, value=None, value_type=None, variable=False):
        Node.__init__(self, parent, children, node_name, current_depth, current_symbols)
        self.sign = sign
        self.value = value
        self.value_type = value_type
        self.variable = variable

    def get_sign(self):
        return self.sign

    def set_sign(self, new_sign):
        self.sign = new_sign

    def get_value(self):
        return self.value

    def set_value(self, new_value):
        self.value = new_value

    def get_value_type(self):
        return self.value_type

    def set_value_type(self, new_value_type):
        self.value_type = new_value_type

    def set_is_variable(self, variable):
        self.variable = variable

    def is_variable(self):
        return self.variable


class Print_Node(Node):
    def __init__(self, parent=None, children=None, node_name=None, current_depth=None, current_symbols=None,
                 expression_type=None):
        Node.__init__(self, parent, children, node_name, current_depth, current_symbols)
        self.expression_type = expression_type

    def set_expression_type(self, new_expression_type):
        self.expression_type = new_expression_type

    def get_expression_type(self):
        return self.expression_type
