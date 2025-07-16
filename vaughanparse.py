import ply.yacc as yacc

from vaughanlex import tokens

start='statement'

def p_statement(p):
    '''statement : define
                 | expression'''
    p[0] = p[1]

def p_define(p):
    'define : LPAREN DEFINE NAME expression RPAREN'
    p[0] = ('define', p[3], p[4])

def p_expression_name(p):
    'expression : NAME'
    p[0] = ('name', p[1])

def p_expression_quote(p):
    'expression : QUOTE'
    p[0] = ('string_literal', p[1])

def p_expression_doublequote(p):
    'expression : DOUBLE_QUOTE'
    p[0] = ('string_literal', p[1])

def p_expression_int(p):
    'expression : INT'
    p[0] = ('int_literal', p[1])

def p_expression_float(p):
    'expression : FLOAT'
    p[0] = ('float_literal', p[1])

def p_expression_application(p):
    'expression : LPAREN NAME list RPAREN'
    p[0] = ('application', p[2], p[3])

def p_expression_lambda(p):
    'expression : LPAREN LAMBDA LPAREN params RPAREN expression RPAREN'
    p[0] = ('lambda', p[4], p[6])

def p_params_term(p):
    'params : NAME'
    p[0] = [p[1]]

def p_params_nonterm(p):
    'params : NAME params'
    p[0] = [p[1]] + p[2]

def p_expression_list(p):
    'expression : LPAREN list RPAREN'
    p[0] = ('list', p[2])
    
def p_list_tail(p):
    'list : expression'
    p[0] = [p[1]]

def p_list_head(p):
    'list : expression list'
    p[0] = [p[1]] + p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc(debug=True)

if __name__ == "__main__":
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)