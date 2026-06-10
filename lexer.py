import re

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line})"

class Lexer:
    KEYWORDS = {
        'number': 'TYPE_INT',
        'sach_ya_jhoot': 'TYPE_BOOL',
        'jumla': 'TYPE_STRING',
        'kuch_nahi': 'TYPE_VOID',
        'agar': 'IF',
        'har': 'FOR',
        'jabtak': 'WHILE',
        'wapis': 'RETURN',
        'sach': 'BOOL_LIT',
        'jhoot': 'BOOL_LIT'
    }

    TOKEN_SPEC = [
        ('NUMBER',   r'\d+'),
        ('STRING', r'"[^"]*"'),
        ('ID',       r'[a-zA-Z][a-zA-Z0-9_]*'),
        ('LOGICAL_OP', r'&&|\|\|'),
        ('REL_OP',   r'==|!=|<=|>=|<|>'),
        ('ASSIGN_OP', r'=|+=|-=|\*=|/=|%='),
        ('ARITH_OP', r'[+\-*/]'),
        ('SEMI', r';'),
        ('L_CURLY', r'\{'),
        ('R_CURLY', r'\}'),
        ('L_PAREN', r'\('),
        ('R_PAREN', r'\)'),
        ('COMMA', r','),
        ('NEWLINE',  r'\n'),
        ('SKIP',     r'[ \t\r]+'),
        ('MISMATCH', r'.'),
    ]

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        line_num = 1
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.TOKEN_SPEC)
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                self.tokens.append(Token('NUMBER', value, line_num))
            elif kind == 'ID':
                kind = self.KEYWORDS.get(value, 'ID')
                self.tokens.append(Token(kind, value, line_num))
            elif kind == 'STRING':
                self.tokens.append(Token('STRING', value[1:-1], line_num))
            elif kind == 'LOGICAL_OP':
                self.tokens.append(Token('LOGICAL_OP', value, line_num))
            elif kind == 'REL_OP':
                self.tokens.append(Token('REL_OP', value, line_num))
            elif kind == 'ASSIGN_OP':
                self.tokens.append(Token('ASSIGN_OP', value, line_num))
            elif kind == 'ARITH_OP':
                self.tokens.append(Token('ARITH_OP', value, line_num))
            elif kind in ['SEMI', 'L_CURLY', 'R_CURLY', 'L_PAREN', 'R_PAREN', 'COMMA']:
                self.tokens.append(Token(kind, value, line_num))
            elif kind == 'NEWLINE':
                line_num += 1
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise SyntaxError(f"Lexical Error at line {line_num}: Unexpected character '{value}'")
        self.tokens.append(Token('EOF', '', line_num))
        return self.tokens
