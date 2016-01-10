import ply.yacc as yacc
from lf_ast import *


class LF_Parser:
    def __init__(self, tokens, verbose=False):
        self.parser = None
        self.verbose = verbose
        self.tokens = tokens
        self.ast_depth = 0
        self.ast = AST()

        root = Node()
        root.set_name("root")
        root.set_ast_depth(0)

        self.ast.set_root(root)
        self.ast.set_current_node(root)

    def setup(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def get_ast_depth(self):
        return self.ast_depth

    def set_ast_depth(self, depth):
        self.ast_depth = depth

    def parse(self, data, **kwargs):
        self.parser.parse(data, **kwargs)

    def ast_depth_increment(self, verbose=False):
        if verbose or self.verbose:
            print self.ast_depth
        self.ast_depth += 1

    def ast_depth_decrement(self, verbose=False):
        if verbose or self.verbose:
            print self.ast_depth
        self.ast_depth -= 1

    def setup_ast(self):
        self.ast.setup_ast()

    def get_ast(self):
        return self.ast

    def set_ast(self, new_ast):
        self.ast = new_ast

    def print_ast(self, verbose=False):
        if verbose or self.verbose:
            self.ast.print_ast()


    # PARSING FOR INCRTUCTIONS STARTS HERE

    def p_base(self, p):
        """base :"""

    def p_base_statements(self, p):
        """base : statements"""

    def p_statements_instruction(self, p):
        """statements : instruction"""

    def p_instruction_instruction(self, p):
        """statements : statements instruction"""

    def p_instruction_print(self, p):
        """instruction : PRINT expression DOT"""
        print_node = Print_Node()
        print_node.set_name("print")
        print_node.set_ast_depth(self.get_ast_depth())
        print_node.set_parent(self.ast.get_current_node())
        self.ast.get_current_node().add_child(print_node)

        expression_node = Expression_Node()
        expression_node.set_name("expression")
        expression_node.set_ast_depth(self.get_ast_depth())
        expression_node.set_parent(print_node)
        expression_node.set_expression_ast_root(p[2])
        expression_node.build_expression_stack()

        print_node.add_child(expression_node)
        print_node.set_expression_type(expression_node.get_expression_type())

    def p_instruction_assignment(self, p):
        """instruction : ID ASSIGN expression DOT"""
        assign_node = Assignment_Node()
        assign_node.set_name("assignment")
        assign_node.set_target_id("variable_" + p[1])
        assign_node.set_ast_depth(self.get_ast_depth())
        assign_node.set_parent(self.ast.get_current_node())

        self.ast.get_current_node().add_child(assign_node)

        expression_node = Expression_Node()
        expression_node.set_name("expression")
        expression_node.set_ast_depth(self.get_ast_depth())
        expression_node.set_parent(assign_node)
        expression_node.set_expression_ast_root(p[3])

        expression_node.build_expression_stack()

        assign_node.add_child(expression_node)
        assign_node.set_expression_type(expression_node.get_expression_type())
        assign_node.get_parent().add_symbol("variable_" + p[1], expression_node.get_expression_type())

    def p_value_id(self, p):
        """value : ID"""
        number_node = Number_Node()
        number_node.set_value("variable_" + p[1])
        p[0] = number_node

        if not self.ast.get_current_node().check_symbol("variable_" + p[1]):
            print("ERROR: " + p[1] + " is not a declared variable")
            if self.verbose:
                print self.ast.print_current_symbols()
            sys.exit()

        number_node.set_is_variable(True)
        number_node.set_value_type(self.ast.get_current_node().get_symbol_type("variable_" + p[1]))

    def p_value_id_signed(self, p):
        """value : sign_arithmetic_operation ID
        | term_arithmetic_operation ID"""
        number_node = Number_Node()
        number_node.set_sign(p[1])
        number_node.set_value("variable_" + p[2])
        p[0] = number_node

        if not self.ast.get_current_node().check_symbol("variable_" + p[2]):
            print("ERROR: " + p[2] + " is not a declared variable")
            if self.verbose:
                print self.ast.print_current_symbols()
            sys.exit()

        number_node.set_is_variable(True)
        number_node.set_value_type(self.ast.get_current_node().get_symbol_type("variable_" + p[2]))

    def p_value_integer(self, p):
        """value : INTEGER"""
        number_node = Number_Node()
        number_node.set_value(p[1])
        number_node.set_value_type("integer")
        p[0] = number_node

    def p_value_integer_signed(self, p):
        """value : sign_arithmetic_operation INTEGER
        | term_arithmetic_operation INTEGER"""
        number_node = Number_Node()
        number_node.set_sign(p[1])
        number_node.set_value(p[2])
        number_node.set_value_type("integer")
        p[0] = number_node

    def p_value_real(self, p):
        """value : REAL"""
        number_node = Number_Node()
        number_node.set_value(p[1])
        number_node.set_value_type("real")
        p[0] = number_node

    def p_value_real_signed(self, p):
        """value : sign_arithmetic_operation REAL
        | term_arithmetic_operation REAL"""
        number_node = Number_Node()
        number_node.set_sign(p[1])
        number_node.set_value(p[2])
        number_node.set_value_type("real")
        p[0] = number_node

    def p_value_expression_parenthesis(self, p):
        """value : LEFTPARENTHESIS expression RIGHTPARENTHESIS"""
        p[0] = p[2]

    def p_sign_arithmetic_operation(self, p):
        """sign_arithmetic_operation : PLUS
        | MINUS"""
        p[0] = p[1]

    def p_term_arithmetic_operation(self, p):
        """term_arithmetic_operation : TIMES
        | DIVIDE"""
        p[0] = p[1]

    def p_relational_equality_operation(self, p):
        """relational_equality_operation : EQUAL
        | NOTEQUAL"""
        p[0] = p[1]

    def p_relational_inequality_operation(self, p):
        """relational_inequality_operation : LOWEREQUAL
        | GREATEREQUAL
        | LOWERTHEN
        | GREATERTHEN"""
        p[0] = p[1]

    def p_expression_equality_comparison(self, p):
        """expression : expression relational_equality_operation comparison"""
        operation_node = Operation_Node()
        operation_node.set_operation(p[2])
        operation_node.add_child(p[1])
        operation_node.add_child(p[3])
        p[0] = operation_node

    def p_expression_comparison(self, p):
        """expression : comparison"""
        p[0] = p[1]

    def p_comparison_arithmetic_expression_operations(self, p):
        """comparison : comparison relational_inequality_operation arithmetic_expression"""
        operation_node = Operation_Node()
        operation_node.set_operation(p[2])
        operation_node.add_child(p[1])
        operation_node.add_child(p[3])
        p[0] = operation_node

    def p_comparison_arithmetic_expression(self, p):
        """comparison : arithmetic_expression"""
        p[0] = p[1]

    def p_arithmetic_expression_arithmetic_operation(self, p):
        """arithmetic_expression : arithmetic_expression sign_arithmetic_operation expression_term"""
        operation_node = Operation_Node()
        operation_node.set_operation(p[2])
        operation_node.add_child(p[1])
        operation_node.add_child(p[3])
        p[0] = operation_node

    def p_arithmetic_expression_expression_term(self, p):
        """arithmetic_expression : expression_term"""
        p[0] = p[1]

    def p_expression_term_arithmetic_operation(self, p):
        """expression_term : expression_term term_arithmetic_operation value"""
        operation_node = Operation_Node()
        operation_node.set_operation(p[2])
        operation_node.add_child(p[1])
        operation_node.add_child(p[3])
        p[0] = operation_node

    def p_expression_term_value(self, p):
        """expression_term : value"""
        p[0] = p[1]

    def p_instruction_if_start(self, p):
        """if_start : IF"""
        ifnode = If_Node()
        ifnode.set_name("if")
        ifnode.set_ast_depth(self.get_ast_depth())
        ifnode.set_parent(self.ast.get_current_node())

        self.ast.get_current_node().add_child(ifnode)

        self.ast.set_current_node(ifnode)

    def p_instruction_if_expression(self, p):
        """if_expression : expression"""
        if_expression_node = Expression_Node()
        if_expression_node.set_name("if_expression")
        if_expression_node.set_ast_depth(self.get_ast_depth())
        if_expression_node.set_parent(self.ast.get_current_node())
        if_expression_node.set_expression_ast_root(p[1])

        if_expression_node.build_expression_stack()

        self.ast.get_current_node().add_child(if_expression_node)
        self.ast.get_current_node().set_expression_type(if_expression_node.get_expression_type())

    def p_instruction_if_then_begin(self, p):
        """if_then_begin : THEN BEGIN"""
        then_node = Then_Node()
        then_node.set_name("then")
        then_node.set_ast_depth(self.get_ast_depth())
        then_node.set_parent(self.ast.get_current_node())

        self.ast.get_current_node().add_child(then_node)

        self.ast.set_current_node(then_node)

        self.ast_depth_increment()

    def p_instruction_if_else_begin(self, p):
        """if_else_begin : ELSE BEGIN"""
        else_node = Else_Node()
        else_node.set_name("else")
        else_node.set_ast_depth(self.get_ast_depth() - 1)
        else_node.set_parent(self.ast.get_current_node().get_parent())

        self.ast.get_current_node().get_parent().add_child(else_node)

        self.ast.set_current_node(else_node)

    def p_instruction_if_statement(self, p):
        """instruction : if_start if_expression if_then_begin statements END DOT"""
        self.ast_depth_decrement()

        self.ast.set_current_node(self.ast.get_current_node().get_parent().get_parent())

    def p_instruction_if_then_else_statement(self, p):
        """instruction : if_start if_expression if_then_begin statements END if_else_begin statements END DOT"""
        self.ast_depth_decrement()

        self.ast.set_current_node(self.ast.get_current_node().get_parent().get_parent())

    def p_instruction_while_start(self, p):
        """while_start : WHILE"""
        whilenode = While_Node()
        whilenode.set_name("while")
        whilenode.set_ast_depth(self.get_ast_depth())
        whilenode.set_parent(self.ast.get_current_node())

        self.ast.get_current_node().add_child(whilenode)

        self.ast.set_current_node(whilenode)

    def p_instruction_while_expression(self, p):
        """while_expression : expression"""
        while_expression_node = Expression_Node()
        while_expression_node.set_name("while_expression")
        while_expression_node.set_ast_depth(self.get_ast_depth())
        while_expression_node.set_parent(self.ast.get_current_node())
        while_expression_node.set_expression_ast_root(p[1])

        while_expression_node.build_expression_stack()

        self.ast.get_current_node().add_child(while_expression_node)
        self.ast.get_current_node().set_expression_type(while_expression_node.get_expression_type())

    def p_instruction_while_body(self, p):
        """while_body : DO statements DONE DOT"""
        self.ast_depth_increment()

    def p_instruction_while_statement(self, p):
        """instruction : while_start while_expression while_body"""
        self.ast_depth_decrement()

        self.ast.set_current_node(self.ast.get_current_node().get_parent())

    def p_error(self, p):
        print("!!! defecerunt processus !!!")
        if p is not None:
            print("Token type:     %s" % (str(p.type)))
            print("Value:          %s" % (str(p.value)))
            print("Linea numerus:  %s" % (str(p.lineno)))
            print("Token position: %s" % (str(p.lexpos)))
        sys.exit()




