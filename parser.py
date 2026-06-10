from lexer import Lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def error(self, message):
        raise SyntaxError(f"Syntax Error at line {self.current_token.line}: {message}")

    def consume(self, expected_type=None):
        if expected_type and self.current_token.type != expected_type:
            self.error(f"Expected {expected_type}, but found {self.current_token.type} ('{self.current_token.value}')")
        
        token = self.current_token
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        return token

    def match(self, expected_type):
        return self.current_token.type == expected_type

    def match_type(self):
        return self.current_token.type in ['TYPE_INT', 'TYPE_BOOL', 'TYPE_STRING', 'TYPE_VOID']

    def parse_program(self):
        while self.current_token.type != 'EOF':
            self.parse_global_element()
        print("Parsing successful!")

    def parse_global_element(self):
        if self.match_type():
            # Lookahead: Function declaration or Variable declaration
            type_token = self.current_token
            self.consume()
            id_token = self.consume('ID')
            if self.match('SYM_LPAREN'):
                self.parse_function_decl_body()
            else:
                self.consume('SYM_SEMI')
        else:
            self.parse_statement()

    def parse_function_decl_body(self):
        self.consume('SYM_LPAREN')
        if not self.match('SYM_RPAREN'):
            self.parse_parameter_list()
        self.consume('SYM_RPAREN')
        self.parse_block()

    def parse_parameter_list(self):
        self.parse_parameter()
        while self.match('SYM_COMMA'):
            self.consume('SYM_COMMA')
            self.parse_parameter()

    def parse_parameter(self):
        if not self.match_type():
            self.error("Expected type in parameter list")
        self.consume()
        self.consume('ID')

    def parse_block(self):
        self.consume('SYM_LBRACE')
        while not self.match('SYM_RBRACE') and self.current_token.type != 'EOF':
            if self.match_type():
                self.parse_declaration()
            else:
                self.parse_statement()
        self.consume('SYM_RBRACE')

    def parse_declaration(self):
        if not self.match_type():
            self.error("Expected type for declaration")
        self.consume()
        self.consume('ID')
        # Optional initialization
        if self.match('OP_ASSIGN'):
            self.consume('OP_ASSIGN')
            self.parse_expression()
        self.consume('SYM_SEMI')

    def parse_statement(self):
        if self.match('IF'):
            self.parse_if_stmt()
        elif self.match('WHILE'):
            self.parse_while_loop()
        elif self.match('FOR'):
            self.parse_for_loop()
        elif self.match('RETURN'):
            self.parse_return_stmt()
        elif self.match('ID'):
            # Lookahead: Assignment or Function Call
            id_token = self.consume('ID')
            if self.match('OP_ASSIGN'):
                self.consume('OP_ASSIGN')
                self.parse_expression()
                self.consume('SYM_SEMI')
            elif self.match('SYM_LPAREN'):
                self.parse_function_call_body()
                self.consume('SYM_SEMI')
            else:
                self.error("Expected '=' or '(' after identifier")
        elif self.match('SYM_LBRACE'):
            self.parse_block()
        else:
            self.error(f"Unexpected token {self.current_token.type} ('{self.current_token.value}')")

    def parse_if_stmt(self):
        self.consume('IF')
        self.consume('SYM_LPAREN')
        self.parse_expression()
        self.consume('SYM_RPAREN')
        self.parse_block()

    def parse_while_loop(self):
        self.consume('WHILE')
        self.consume('SYM_LPAREN')
        self.parse_expression()
        self.consume('SYM_RPAREN')
        self.parse_block()

    def parse_for_loop(self):
        self.consume('FOR')
        self.consume('SYM_LPAREN')
        # Part 1: Init (Declaration or Assignment or empty)
        if self.match_type():
            self.consume() # type
            self.consume('ID')
            self.consume('OP_ASSIGN')
            self.parse_expression()
        elif self.match('ID'):
            self.consume('ID')
            self.consume('OP_ASSIGN')
            self.parse_expression()
        self.consume('SYM_SEMI')

        # Part 2: Condition
        self.parse_expression()
        self.consume('SYM_SEMI')

        # Part 3: Update
        self.consume('ID')
        self.consume('OP_ASSIGN')
        self.parse_expression()

        self.consume('SYM_RPAREN')
        self.parse_block()

    def parse_return_stmt(self):
        self.consume('RETURN')
        if not self.match('SYM_SEMI'):
            self.parse_expression()
        self.consume('SYM_SEMI')

    def parse_function_call_body(self):
        self.consume('SYM_LPAREN')
        if not self.match('SYM_RPAREN'):
            self.parse_argument_list()
        self.consume('SYM_RPAREN')

    def parse_argument_list(self):
        self.parse_expression()
        while self.match('SYM_COMMA'):
            self.consume('SYM_COMMA')
            self.parse_expression()

    def parse_expression(self):
        self.parse_relational()

    def parse_relational(self):
        self.parse_additive()
        while self.match('OP_REL') or self.match('OP_LOGIC'):
            self.consume()
            self.parse_additive()

    def parse_additive(self):
        self.parse_multiplicative()
        while self.match('OP_ARITH') and self.current_token.value in ['+', '-']:
            self.consume()
            self.parse_multiplicative()

    def parse_multiplicative(self):
        self.parse_primary()
        while self.match('OP_ARITH') and self.current_token.value in ['*', '/']:
            self.consume()
            self.parse_primary()

    def parse_primary(self):
        if self.match('NUMBER'):
            self.consume('NUMBER')
        elif self.match('ID'):
            id_token = self.consume('ID')
            if self.match('SYM_LPAREN'):
                self.parse_function_call_body()
        elif self.match('BOOL_LIT'):
            self.consume('BOOL_LIT')
        elif self.match('STRING_LIT'):
            self.consume('STRING_LIT')
        elif self.match('SYM_LPAREN'):
            self.consume('SYM_LPAREN')
            self.parse_expression()
            self.consume('SYM_RPAREN')
        else:
            self.error(f"Invalid expression at {self.current_token.value}")
