import sys
import ply.lex as lex

tokens = [
    'ID',
    'IFS',
    'NUMBER',
    'FLOATNUMBER',
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'LESSEQUAL',
    'GREATEREQUAL',
    'UNEQUAL',
    'EQUAL',
    'STRING',
    'COMMENT'
]

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_UNEQUAL = r'!='
t_EQUAL = r'=='

literals = "+-*/=()[]{}:',;<>"

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = tokens + list(reserved.values())

t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_FLOATNUMBER(t):
    r'(\d*\.\d+([eE]-?\d+)?)|(\d+\.([eE]-?\d+)?)|(\d+[eE]-?\d+)'
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'(\"[^\"]*\")'
    return t


def t_COMMENT(t):
    r'\#.*'
    return ''


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
