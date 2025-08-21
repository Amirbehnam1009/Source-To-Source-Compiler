from ply import lex
import ply.yacc as yacc

code = "#include <stdio.h>\nint main()\n{}"
# Our Tokens
tokens = [
    "PROGRAM", 'EMPTY', 'END', 'IF', 'THEN', 'ELSE', 'WHILE', 'PRINT', 'SWITCH', 'OF', 'DONE', 'DEFAULT', 'AND', 'OR',
    'MOD',
    'NOT', 'ASSIGN', 'PLUS', 'MINUS', 'MUL', 'DIV', 'GT', 'LT', 'EQ', 'NEQ', 'GTEQ', 'LTEQ', 'INTEGER_CONSTANT',
    'REAl_CONSTANT', 'ID', 'SEMICOLON', 'COLON', 'COMMA', 'LPAREN', 'RPAREN', "VAR", "INTEGER", "REAL", "BEGIN",
]

# Reserved Words
reserved = {
    "program": 'PROGRAM',
    "var": "VAR",
    "int": 'INTEGER',
    "real": 'REAL',
    "begin": 'BEGIN',
    "end": "END",
    "if": 'IF',
    "then": 'THEN',
    "else": 'ELSE',
    "while": 'WHILE',
    "print": 'PRINT',
    "switch": 'SWITCH',
    "of": 'OF',
    "done": 'DONE',
    "default": 'DEFAULT',
    "and": 'AND',
    "or": 'OR',
    "mod": 'MOD',
    "not": 'NOT',
    "Error": 'ERROR',
}
# t_EMPTY = r'^$'
t_OR = r'OR'
t_AND = r'AND'
t_NOT = r'NOT'
# Operators
t_ASSIGN = r'\:='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_GT = r'\>'
t_LT = r'\<'
t_EQ = r'\='
t_NEQ = r'\<>'
t_GTEQ = r'\>='
t_LTEQ = r'\<='
# Delimeters
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'
# Ignore
t_ignore = " \t\n"
precedence = (
    ('nonassoc', 'END'),
    ('nonassoc', 'IF'),
    ('nonassoc', 'THEN'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', 'WHILE'),
    ('nonassoc', 'SWITCH'),
    ('nonassoc', 'PRINT'),
    ('nonassoc', 'OF'),
    ('nonassoc', 'DONE'),
    ('nonassoc', 'DEFAULT'),
    ('nonassoc', 'INTEGER_CONSTANT'),
    ('nonassoc', 'REAl_CONSTANT'),
    ('nonassoc', 'ID'),
    ('left', 'COMMA'),
    ('right', 'ASSIGN'),
    ('right', 'LPAREN'),
    ('left', 'RPAREN'),
    ('left', 'SEMICOLON'),
    ('left', 'COLON'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'GT', 'LT', 'GTEQ', 'LTEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('right', 'NOT'),
)


def t_REAl_CONSTANT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER_CONSTANT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r"""[a-zA-Z\x80-\xff_][a-zA-Z0-9\x80-\xff_]*"""
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_ERROR(t):
    r"""([0-9]+[a-zA-Z_]+)
        |([\*\+\-\%\/][\s]*[\*\+\-\%\/][\*\+\-\%\/ ]*)
        |([\w\d]*(\.[\w\d]*){2,})
        """
    t.type = 'ERROR'
    return t


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise Exception('Error', t.value)


vars = []


def p_declaration(p):
    """statement : VAR ID INTEGER
                 | VAR ID REAL"""
    vars.append([p[2], p[3], 0])
    symbol_table.append(['declare', p[2], p[3]])


"""def p_declaration_list(p):
    declaration-list : identifier-list COLON type
                        | declaration-list SEMICOLON identifier-list COLON type"""


def p_expression_const(p):
    """expression : INTEGER_CONSTANT
                  | REAl_CONSTANT"""
    p[0] = p[1]


def p_expression_var(p):
    """expression : ID"""
    res = p[1]
    for var in vars:
        if var[0] == p[1]:
            if var[1] == 'int':
                res = int(var[2])
            elif var[1] == 'float':
                res = float(var[2])
    p[0] = res


def p_expression_not(p):
    """expression : NOT expression
                  | MINUS expression"""
    if p[1] == 'not':
        p[0] = not p[2]
    elif p[1] == '-':
        p[0] = -1 * p[2]
    symbol_table.append([p[1], p[2]])


def p_expression_para(p):
    """expression : LPAREN expression RPAREN """
    p[0] = p[2]


def p_expression(p):
    """expression : expression MUL expression
               | expression DIV expression
               | expression PLUS expression
               | expression MINUS expression
               | expression MOD expression
               | expression GT expression
               | expression LT expression
               | expression EQ expression
               | expression NEQ expression
               | expression LTEQ expression
               | expression GTEQ expression
               | expression AND expression
               | expression OR expression"""
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == 'mod':
        if type(p[1]) == float or type(p[3]) == float:
            raise Exception
        p[0] = p[1] % p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '<>':
        p[0] = p[1] != p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == 'and':
        p[0] = p[1] and p[3]
    elif p[2] == 'or':
        p[0] = p[1] or p[3]
    symbol_table.append(['expression', p[1], p[2], p[3]])


def p_statement_assign(p):
    'statement : ID ASSIGN expression'
    for var in vars:
        if var[0] == p[1]:
            var[2] = p[3]
            symbol_table.append(['assign', var[0], var[2]])


def p_statement_list(p):
    """statement-list : statement
                      | statement-list SEMICOLON statement"""
    pass


def p_statement_compound(p):
    """statement-compound : BEGIN statement-list END"""
    symbol_table.append(['statement-compound'])


def p_program(p):
    """program : PROGRAM ID statement-compound"""

    symbol_table.append(['program', p[2]])


def p_statement_print(p):
    """statement : PRINT LPAREN expression RPAREN """
    symbol_table.append(['print', p[3]])
    print(p[3])

def p_error(p):
    print("------------------\n!!!!!SYNTAX_ERROR!!!!!\n unexpected "+p.type+"\n------------------\n")
symbol_table = []
lexer = lex.lex()
file = open('Test.txt')
text_input = file.read()
file.close()

try:
    parser = yacc.yacc(start="program")
    result = parser.parse(text_input)
except:
    print("------------------\n!!!!!  ERROR  !!!!!\nmod can only work on INTEGER values!!!!!\n------------------\n")
print(symbol_table)
