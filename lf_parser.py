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
        print_instruction = Print_Node()
        print_instruction.set_name("print")
        print_instruction.set_ast_depth(self.get_ast_depth())
        print_instruction.set_parent(self.ast.get_current_node())
        self.ast.get_current_node().add_child(print_instruction)

        expression = Expression_Node()
        expression.set_name("expression")
        expression.set_ast_depth(self.get_ast_depth())
        expression.set_parent(print_instruction)
        expression.set_expression_ast_root(p[2])
        expression.build_stack_expression()

        print_instruction.add_child(expression)
        print_instruction.set_expression_type(expression.get_expression_type())

    def p_instruction_assignment(self, p):
        """instruction : ID ASSIGN expression DOT"""
        assignment_instruction = Assignment_Node()
        assignment_instruction.set_name("assignment")
        assignment_instruction.set_target_id("variable_" + p[1])
        assignment_instruction.set_ast_depth(self.get_ast_depth())
        assignment_instruction.set_parent(self.ast.get_current_node())

        self.ast.get_current_node().add_child(assignment_instruction)

        expression = Expression_Node()
        expression.set_name("expression")
        expression.set_ast_depth(self.get_ast_depth())
        expression.set_parent(assignment_instruction)
        expression.set_expression_ast_root(p[3])

        expression.build_stack_expression()

        assignment_instruction.add_child(expression)
        assignment_instruction.set_expression_type(expression.get_expression_type())
        assignment_instruction.get_parent().add_symbol("variable_" + p[1], expression.get_expression_type())

    def p_value_id(self, p):
        """value : ID"""
        number = Number_Node()
        number.set_value("variable_" + p[1])
        p[0] = number

        if not self.ast.get_current_node().check_symbol("variable_" + p[1]):
            print("ERROR: " + p[1] + " is not a declared variable")
            if self.verbose:
                print self.ast.print_current_symbols()
            sys.exit()

        number.set_is_variable(True)
        number.set_value_type(self.ast.get_current_node().get_symbol_type("variable_" + p[1]))

    def p_value_id_signed(self, p):
        """value : sign_arithmetic_operation ID
        | term_arithmetic_operation ID"""
        number = Number_Node()
        number.set_sign(p[1])
        number.set_value("variable_" + p[2])
        p[0] = number

        if not self.ast.get_current_node().check_symbol("variable_" + p[2]):
            print("ERROR: " + p[2] + " is not a declared variable")
            if self.verbose:
                print self.ast.print_current_symbols()
            sys.exit()

        number.set_is_variable(True)
        number.set_value_type(self.ast.get_current_node().get_symbol_type("variable_" + p[2]))

    def p_value_integer(self, p):
        """value : INTEGER"""
        number = Number_Node()
        number.set_value(p[1])
        number.set_value_type("integer")
        p[0] = number

    def p_value_integer_signed(self, p):
        """value : sign_arithmetic_operation INTEGER
        | term_arithmetic_operation INTEGER"""
        number = Number_Node()
        number.set_sign(p[1])
        number.set_value(p[2])
        number.set_value_type("integer")
        p[0] = number

    def p_value_real(self, p):
        """value : REAL"""
        number = Number_Node()
        universal_number_check = p[1].replace(',', '.')
        number.set_value(universal_number_check)
        number.set_value_type("real")
        p[0] = number

    def p_value_real_signed(self, p):
        """value : sign_arithmetic_operation REAL
        | term_arithmetic_operation REAL"""
        number = Number_Node()
        number.set_sign(p[1])
        number.set_value(p[2])
        number.set_value_type("real")
        p[0] = number

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
        """expression : expression relational_equality_operation  comparison"""
        logic_operation = Operation_Node()
        logic_operation.set_operation(p[2])
        logic_operation.add_child(p[1])
        logic_operation.add_child(p[3])
        p[0] = logic_operation

    def p_expression_comparison(self, p):
        """expression : comparison"""
        p[0] = p[1]

    def p_comparison_arithmetic_expression_operations(self, p):
        """comparison : comparison relational_inequality_operation arithmetic_expression"""
        logic_operation = Operation_Node()
        logic_operation.set_operation(p[2])
        logic_operation.add_child(p[1])
        logic_operation.add_child(p[3])
        p[0] = logic_operation

    def p_comparison_arithmetic_expression(self, p):
        """comparison : arithmetic_expression"""
        p[0] = p[1]

    def p_arithmetic_expression_arithmetic_operation(self, p):
        """arithmetic_expression : arithmetic_expression sign_arithmetic_operation expression_term"""
        logic_operation = Operation_Node()
        logic_operation.set_operation(p[2])
        logic_operation.add_child(p[1])
        logic_operation.add_child(p[3])
        p[0] = logic_operation

    def p_arithmetic_expression_expression_term(self, p):
        """arithmetic_expression : expression_term"""
        p[0] = p[1]

    def p_expression_term_arithmetic_operation(self, p):
        """expression_term : expression_term term_arithmetic_operation value"""
        logic_operation = Operation_Node()
        logic_operation.set_operation(p[2])
        logic_operation.add_child(p[1])
        logic_operation.add_child(p[3])
        p[0] = logic_operation

    def p_expression_term_value(self, p):
        """expression_term : value"""
        p[0] = p[1]

    def p_instruction_if_start(self, p):
        """if_start : IF"""
        condition_if = If_Node()
        condition_if.set_name("if")
        condition_if.set_ast_depth(self.get_ast_depth())
        condition_if.set_parent(self.ast.get_current_node())

        self.ast.get_current_node().add_child(condition_if)

        self.ast.set_current_node(condition_if)

    def p_instruction_if_expression(self, p):
        """if_expression : expression"""
        expression_if = Expression_Node()
        expression_if.set_name("if_expression")
        expression_if.set_ast_depth(self.get_ast_depth())
        expression_if.set_parent(self.ast.get_current_node())
        expression_if.set_expression_ast_root(p[1])

        expression_if.build_stack_expression()

        self.ast.get_current_node().add_child(expression_if)
        self.ast.get_current_node().set_expression_type(expression_if.get_expression_type())

    def p_instruction_if_then_begin(self, p):
        """if_then_begin : THEN BEGIN"""
        condition_then = Then_Node()
        condition_then.set_name("then")
        condition_then.set_ast_depth(self.get_ast_depth())
        condition_then.set_parent(self.ast.get_current_node())

        self.ast.get_current_node().add_child(condition_then)

        self.ast.set_current_node(condition_then)

        self.ast_depth_increment()

    def p_instruction_if_else_begin(self, p):
        """if_else_begin : ELSE BEGIN"""
        condition_else = Else_Node()
        condition_else.set_name("else")
        condition_else.set_ast_depth(self.get_ast_depth() - 1)
        condition_else.set_parent(self.ast.get_current_node().get_parent())

        self.ast.get_current_node().get_parent().add_child(condition_else)

        self.ast.set_current_node(condition_else)

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
        condition_while = While_Node()
        condition_while.set_name("while")
        condition_while.set_ast_depth(self.get_ast_depth())
        condition_while.set_parent(self.ast.get_current_node())

        self.ast.get_current_node().add_child(condition_while)

        self.ast.set_current_node(condition_while)

    def p_instruction_while_expression(self, p):
        """while_expression : expression"""
        expression_while = Expression_Node()
        expression_while.set_name("while_expression")
        expression_while.set_ast_depth(self.get_ast_depth())
        expression_while.set_parent(self.ast.get_current_node())
        expression_while.set_expression_ast_root(p[1])

        expression_while.build_stack_expression()

        self.ast.get_current_node().add_child(expression_while)
        self.ast.get_current_node().set_expression_type(expression_while.get_expression_type())
        self.ast_depth_increment()

    def p_instruction_while_body(self, p):
        """while_body : DO statements DONE DOT"""

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
