from lf_ast import *


class Function_Node:
    def __init__(self, function=None, children=None, expression_python=None):
        self.function = function
        if children is None:
            children = []
        self.children = children
        self.expression_python = expression_python

    def set_function(self, function):
        self.function = function

    def get_function(self):
        return self.function

    def set_children(self, children):
        self.children = children

    def get_children(self):
        return self.children

    def set_expression_python(self, expression_python):
        self.expression_python = expression_python

    def get_expression_python(self):
        return self.expression_python


class Python:

    def __init__(self, ast=None, variables=None, functions=None, stack=None):
        self.ast = ast
        if variables is None:
            variables = []
        self.variables = variables
        if functions is None:
            functions = []
        self.functions = functions
        if stack is None:
            stack = []
        self.stack = stack
        self.tabulations = ""

    def add_variable(self, variable):
        self.variables.append(variable)

    def remove_variable(self, variable):
        if variable in self.variables:
            self.variables.remove(variable)

    def get_ast(self):
        return self.ast

    def set_ast(self, ast):
        self.ast = ast

    def get_variables(self):
        return self.variables

    def set_variables(self, variables):
        self.variables = variables

    @property
    def generate_variables(self):
        i, v = 0, "v"
        while v + str(i) in self.variables:
            i += 1
        return v + str(i)

    def get_functions_list(self):
        return self.functions

    def set_functions_list(self, functions):
        self.functions = functions

    def get_stack(self):
        return self.stack

    def set_stack(self, stack):
        self.stack = stack

    @property
    def generate_functions(self):
        i, f = 0, "f"
        while f + str(i) + ":" in self.functions:
            i += 1
        self.functions.append((f + str(i) + ":"))
        return f + str(i) + ":"

    def set_sign(self, element, variable, stack):
        sign_number_node = Number_Node()
        if str(element[1].get_sign()) == "addo":
            sign = "+"
        else:
            sign = "-"
        sign_number_node.set_value(variable)
        sign_number_node.set_sign(sign)
        sign_number_node.set_is_variable(True)
        stack.append([str(variable), "=", str(sign_number_node.get_sign()), str(element[0])])
        element[0] = str(variable)
        element[1] = sign_number_node

    def set_unsign(self, element, variable, stack):
        unsign_number_node = Number_Node()
        unsign_number_node.set_value(variable)
        unsign_number_node.set_is_variable(True)
        stack.append([str(variable), "=", str(element[0])])
        element[0] = str(variable)
        element[1] = unsign_number_node

    def convert_stack(self, expression_stack):
        solution = []
        instruction = []

        is_two_expressions = False
        if len(expression_stack) <= 2:
            is_two_expressions = True

        while len(expression_stack) is not 0:
            element = expression_stack.pop(0)

            result = None

            if isinstance(element[1], Number_Node):
                solution.append([element[0], element[1]])

            if isinstance(element[1], Operation_Node):
                x = solution.pop(len(solution) - 1)
                y = solution.pop(len(solution) - 1)
                op = element[0]
                variable = None

                if x[1].is_variable and y[1].is_variable:
                    self.remove_variable(x[0])
                    self.remove_variable(y[0])
                    variable = self.generate_variables
                    self.add_variable(variable)
                else:
                    if x[1].is_variable:
                        self.remove_variable(x[0])
                    elif x[1].get_sign() is not None:
                        variable = self.generate_variables
                        self.add_variable(variable)
                        self.set_sign(x, variable, instruction)
                    else:
                        variable = self.generate_variables
                        self.add_variable(variable)
                        self.set_unsign(x, variable, instruction)

                    if y[1].is_variable:
                        self.remove_variable(y[0])
                    elif y[1].get_sign() is not None:
                        variable = self.generate_variables
                        self.add_variable(variable)
                        self.set_sign(y, variable, instruction)
                    else:
                        variable = self.generate_variables
                        self.add_variable(variable)
                        self.set_unsign(y, variable, instruction)

                self.remove_variable(x[0])
                self.remove_variable(y[0])
                self.add_variable(variable)

                if op == "addo":
                    result = [str(variable), " = ", str(y[0]), " + ", str(x[0])]
                if op == "minus":
                    result = [str(variable), " = ", str(y[0]), " - ", str(x[0])]
                if op == "multiplico":
                    result = [str(variable), " = ", str(y[0]), " * ", str(x[0])]
                if op == "divide":
                    result = [str(variable), " = ", str(y[0]), " / ", str(x[0])]
                if op == "maior":
                    result = [str(variable), " = ", str(y[0]), " > ", str(x[0])]
                if op == "humilior":
                    result = [str(variable), " = ", str(y[0]), " < ", str(x[0])]
                if op == "idem":
                    result = [str(variable), " = ", str(y[0]), " == ", str(x[0])]
                if op == "diversus":
                    result = [str(variable), " = ", str(y[0]), " is not ", str(x[0])]
                if op == ">=":
                    result = [str(variable), " = ", str(y[0]), " >= ", str(x[0])]
                if op == "<=":
                    result = [str(variable), " = ", str(y[0]), " <= ", str(x[0])]

                instruction.append(result)

                new_number_node = Number_Node()
                new_number_node.set_value(variable)
                new_number_node.set_is_variable(True)

                solution.append((variable, new_number_node))

        if is_two_expressions:
            x = solution.pop(len(solution) - 1)
            if x[1].get_sign() is not None:
                variable = self.generate_variables
                self.add_variable(variable)
                if str(element[1].get_sign()) == "addo":
                    sign = "+"
                else:
                    sign = "-"
                instruction.append([str(variable), " = ", str(sign), str(x[0])])
            else:
                variable = self.generate_variables
                self.add_variable(variable)
                instruction.append([str(variable), " = ", str(x[0])])

        return instruction

    def interpret_python(self, node):
        for child in node.get_children():
            if isinstance(child, Expression_Node):
                child.set_expression_python(self.convert_stack(child.get_expression_stack()))
                node.set_expression_python(child.get_expression_python())

    def build_python(self):
        root = self.ast.get_root()
        nodes = [root]

        while len(nodes) is not 0:

            node = nodes.pop(len(nodes) - 1)

            if isinstance(node, Assignment_Node):
                self.interpret_python(node)

                self.remove_variable(node.get_expression_python()[len(node.get_expression_python()) - 1][0])

                node.get_expression_python()[len(node.get_expression_python()) - 1][0] = node.get_target_id()

            if isinstance(node, If_Node):
                self.interpret_python(node)

                if len(node.get_children()) == 3:
                    node.get_children()[0] = node.get_children()[1]
                    node.get_children()[1] = node.get_children()[0]

            if isinstance(node, Then_Node):
                self.tabulations += "\t"
                else_function = self.generate_functions

                else_function_node = Function_Node()
                else_function_node.set_function(else_function)
                else_function_node.set_expression_python([[""]])

                node.get_children().insert(0, else_function_node)

                self.remove_variable(node.get_parent().get_expression_python()[len(node.get_parent().get_expression_python()) - 1][0])
                if len(node.get_parent().get_expression_python()[len(node.get_parent().get_expression_python()) - 1]) == 3:
                    element = node.get_parent().get_expression_python().pop(len(node.get_parent().get_expression_python()) - 1)
                    var = element[2]
                else:
                    var_0 = node.get_parent().get_expression_python()[len(node.get_parent().get_expression_python()) - 1]
                node.get_parent().get_expression_python().append(["if ", var_0[0], ":"])

            if isinstance(node, While_Node):
                self.tabulations += "\t"

            if isinstance(node, Print_Node):
                self.interpret_python(node)

                self.remove_variable(node.get_expression_python()[len(node.get_expression_python()) - 1][0])
                if len(node.get_expression_python()[len(node.get_expression_python()) - 1]) == 3:
                    element = node.get_expression_python().pop(len(node.get_expression_python()) - 1)
                    var = element[2]
                else:
                    var = node.get_expression_python()[len(node.get_expression_python()) - 1][0]
                node.get_expression_python().append(["print(", var, ")"])

            for child_node in node.get_children():
                nodes.append(child_node)

    def generate_python_code(self):
        root = self.ast.get_root()
        nodes = [root]
        tabulation = ""

        while len(nodes) is not 0:

            node = nodes.pop(len(nodes) - 1)

            if isinstance(node, If_Node):
                for element in range(0, len(node.get_expression_python())):
                    if element % 2 == 0:
                        tmp = [node.get_expression_python()[element][2:]]
                        tmp[0].insert(0, str("if "))
                        tmp[0].insert(0, str(tabulation))
                        tmp[0].append(":")
                        self.get_stack().append(tmp)
                        tabulation += "\t"

            if isinstance(node, Function_Node):
                for element in node.get_expression_python():
                    tabulation = tabulation[0:-1]

            if isinstance(node, Assignment_Node) or isinstance(node, While_Node) or isinstance(node, Print_Node):
                tmp = node.get_expression_python()
                tmp[0].insert(0, tabulation)
                self.get_stack().append(tmp)

            for child_node in node.get_children():
                nodes.append(child_node)

    def print_python_code(self, print_code=False):
        print("")
        print("Congrats your Python code has been generated")
        print("")
        if print_code:
            for instructions in self.get_stack():
                for instruction in instructions:
                    line = ""
                    for element in instruction:
                        line += str(element)
                    print line
