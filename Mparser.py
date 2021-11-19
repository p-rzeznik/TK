import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ('nonassoc', 'IFS'),
    ("nonassoc", 'ELSE'),
    ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ('left', 'UNEQUAL', 'EQUAL'),
    ('left', '<', '>', 'LESSEQUAL', 'GREATEREQUAL'),
    ("left", '+', '-'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", '*', '/'),
    ("left", 'DOTMUL', 'DOTDIV')

)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


# dict for ids
IDs = {}
# var for return
return_value = None


def p_start(p):
    """start : LINE"""


def p_line(p):
    """LINE : IDX ';' LINE
            | IFX LINE
            | WHILEX LINE
            | FORX LINE
            | RETURNX ';' LINE
            | PRINTX ';' LINE
            | BLOCK LINE
            | EMPTY"""
    p[0] = p[1]


def p_oneline(p):
    """ONELINE : IDX ';'
                | IFX
                | WHILEX
                | FORX
                | RETURNX ';'
                | PRINTX ';' """
    p[0] = p[1]


def p_block(p):
    """BLOCK : '{' LINE '}' """
    p[0] = p[2]


def p_empty(p):
    """EMPTY :"""


# idx
def p_idx_assign(p):
    """IDX : ID '=' EXPRESSION
           | ID '=' MATRIX
           | ID '=' TABLE
           | ID '[' EXPRESSION ']' '=' EXPRESSION
           | ID '[' EXPRESSION ',' EXPRESSION ']' '=' EXPRESSION"""
    # IDs[p[1]] = p[3]


def p_idx_opassign(p):
    """IDX : ID ADDASSIGN EXPRESSION
           | ID SUBASSIGN EXPRESSION
           | ID MULASSIGN EXPRESSION
           | ID DIVASSIGN EXPRESSION """
    # if p[2] == "ADDASSIGN": IDs[p[1]] += p[3]
    # elif p[2] == "SUBASSIGN": IDs[p[1]] -= p[3]
    # elif p[2] == "MULASSIGN": IDs[p[1]] *= p[3]
    # elif p[2] == "DIVASSIGN": IDs[p[1]] /= p[3]


# MACIERZE
def p_zerosx(p):
    """ZEROSX : ZEROS '(' EXPRESSION ')'"""
    # p[0] = zeros(p[3])


def p_onesx(p):
    """ONESX : ONES '(' EXPRESSION ')'"""
    # p[0] = ones(p[3])


def p_eyex(p):
    """EYEX : EYE '(' EXPRESSION ')'"""
    # p[0] = eye(p[3])


def p_matrix(p):
    """MATRIX : '[' MATRIXINSIDE ']'
                | MATRIXEXPR
                | ZEROSX
                | ONESX
                | EYEX"""



def p_matrixinside(p):
    """MATRIXINSIDE : TABLE ',' MATRIXINSIDE
                    | TABLE"""


def p_table(p):
    """TABLE : '[' VALUES ']'"""


def p_values(p):
    """VALUES :  EXPRESSION ',' VALUES
            | EXPRESSION"""



def zeros(dim):
    return [[0 for _ in range(dim)] for _ in range(dim)]


def ones(dim):
    return [[1 for _ in range(dim)] for _ in range(dim)]


def eye(dim):
    return [[1 if x==y else 0 for x in range(dim)]for y in range(dim)]


def p_matrixop(p):
    """MATRIXEXPR : EXPRESSION DOTADD EXPRESSION
               | EXPRESSION DOTSUB EXPRESSION
               | EXPRESSION DOTMUL EXPRESSION
               | EXPRESSION DOTDIV EXPRESSION
               | EXPRESSION "'" """


# IF
def p_ifx_if(p):
    """IFX :    IF '(' CONDITION ')' ONELINE %prec IFS
            |   IF '(' CONDITION ')' BLOCK %prec IFS
            |   IF '(' CONDITION ')' ONELINE ELSE ONELINE
            |   IF '(' CONDITION ')' ONELINE ELSE BLOCK
            |   IF '(' CONDITION ')' BLOCK ELSE ONELINE
            |   IF '(' CONDITION ')' BLOCK ELSE BLOCK """


# LOOP (do lini dochodzą brake, continue i loopif)
def p_loopline(p):
    """LOOPLINE : IDX ';' LOOPLINE
                | WHILEX LOOPLINE
                | FORX LOOPLINE
                | RETURNX ';' LOOPLINE
                | PRINTX ';' LOOPLINE
                | LOOPBLOCK LOOPLINE
                | EMPTY
                | LOOPIFX LOOPLINE
                | BREAK ';' LOOPLINE
                | CONTINUE ';' LOOPLINE"""
    p[0] = p[1]


def p_oneloopline(p):
    """ONELOOPLINE : IDX ';'
                    | WHILEX
                    | FORX
                    | RETURNX ';'
                    | PRINTX ';'
                    | LOOPIFX
                    | BREAK ';'
                    | CONTINUE ';' """
    p[0] = p[1]


def p_loopblock(p):
    """LOOPBLOCK : '{' LOOPLINE '}'"""


def p_loopifx_if(p):
    """LOOPIFX :    IF '(' CONDITION ')' ONELOOPLINE %prec IFS
                |   IF '(' CONDITION ')' LOOPBLOCK %prec IFS
                |   IF '(' CONDITION ')' ONELOOPLINE ELSE ONELOOPLINE
                |   IF '(' CONDITION ')' ONELOOPLINE ELSE LOOPBLOCK
                |   IF '(' CONDITION ')' LOOPBLOCK ELSE ONELOOPLINE
                |   IF '(' CONDITION ')' LOOPBLOCK ELSE LOOPBLOCK """


# WHILE
def p_whilex(p):
    """WHILEX : WHILE '(' CONDITION ')' ONELOOPLINE
                | WHILE '(' CONDITION ')' LOOPBLOCK"""


# FOR
def p_forx(p):
    """FORX : FOR ID '=' EXPRESSION ':' EXPRESSION ONELOOPLINE
            | FOR ID '=' EXPRESSION ':' EXPRESSION LOOPBLOCK"""


#C ONDITION
def p_condition(p):
    """CONDITION : EXPRESSION EQUAL EXPRESSION
                    | EXPRESSION UNEQUAL EXPRESSION
                    | EXPRESSION LESSEQUAL EXPRESSION
                    | EXPRESSION GREATEREQUAL EXPRESSION
                    | EXPRESSION '>' EXPRESSION
                    | EXPRESSION '<' EXPRESSION """


# PRINT
def p_printx(p):
    """PRINTX : PRINT PRINTMANY """


def p_printmany(p):
    """PRINTMANY :  STRING
                |  EXPRESSION
                |  STRING ',' PRINTMANY
                |  EXPRESSION ',' PRINTMANY"""


# return
def p_returnx_return(p):
    """RETURNX : RETURN EXPRESSION """
    global return_value
    return_value = p[2]


# expression
def p_expression_number(p):
    """EXPRESSION : NUMBER"""
    p[0] = p[1]


def p_expression_float(p):
    """EXPRESSION : FLOATNUMBER"""
    p[0] = p[1]


def p_expression_id(p):
    """EXPRESSION : ID"""
    p[0] = p[1]


def p_expression_sum(p):
    """EXPRESSION : EXPRESSION '+' EXPRESSION
                  | EXPRESSION '-' EXPRESSION"""


def p_expression_mul(p):
    """EXPRESSION : EXPRESSION '*' EXPRESSION
                  | EXPRESSION '/' EXPRESSION"""


def p_expression_group(p):
    """EXPRESSION : '(' EXPRESSION ')'"""
    p[0] = p[2]


def p_expression_unarynegation(p):
    """EXPRESSION : '-' EXPRESSION"""


parser = yacc.yacc()