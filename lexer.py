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
        'jhoot': 'BOOL_LIT',
        'badlo': 'SWITCH',
        'soorat': 'CASE',
        'baqi': 'DEFAULT'
    }

    TOKEN_SPEC = [
        ('NUMBER',   r'\d+'),
        ('STRING_LIT', r'"[^"]*"'),
        ('ID',       r'[a-zA-Z][a-zA-Z0-9_]*'),
        ('OP_LOGIC', r'&&|\|\|'),
        ('OP_REL',   r'==|!=|<=|>=|<|>'),
        ('OP_ASSIGN', r'\+=|-=|\*=|/=|%=|='),
        ('OP_ARITH', r'[+\-*/]'),
        ('SYM_SEMI', r';'),
        ('SYM_COLON', r':'),
        ('SYM_LBRACE', r'\{'),
        ('SYM_RBRACE', r'\}'),
        ('SYM_LPAREN', r'\('),
        ('SYM_RPAREN', r'\)'),
        ('SYM_COMMA', r','),
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
            elif kind == 'STRING_LIT':
                self.tokens.append(Token('STRING_LIT', value[1:-1], line_num))
            elif kind == 'OP_LOGIC':
                self.tokens.append(Token('OP_LOGIC', value, line_num))
            elif kind == 'OP_REL':
                self.tokens.append(Token('OP_REL', value, line_num))
            elif kind == 'OP_ASSIGN':
                self.tokens.append(Token('OP_ASSIGN', value, line_num))
            elif kind == 'OP_ARITH':
                self.tokens.append(Token('OP_ARITH', value, line_num))
            elif kind in ['SYM_SEMI', 'SYM_COLON', 'SYM_LBRACE', 'SYM_RBRACE', 'SYM_LPAREN', 'SYM_RPAREN', 'SYM_COMMA']:
                self.tokens.append(Token(kind, value, line_num))
            elif kind == 'NEWLINE':
                line_num += 1
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise SyntaxError(f"Lexical Error at line {line_num}: Unexpected character '{value}'")
        self.tokens.append(Token('EOF', '', line_num))
        return self.tokens
