import ply.lex as lex

# Define tokens
tokens = [
    'FLOAT',
    'INT',
    'LPAREN',
    'RPAREN',
    'NAME',
    'DEFINE',
    'LAMBDA',
    'QUOTE',
    'DOUBLE_QUOTE'
]

# Define regular expressions for tokens
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_NAME          = r'(?!define|lambda\b)[a-zA-Z_\?!@#\$%\^&\*\+\-\\=:;]{1}[0-9a-zA-Z_\?!@#\$%\^&\*\+\-\\=:;]*'
t_DEFINE        = r'define'
t_LAMBDA        = r'lambda'

def t_FLOAT(t):
    r'\d+\.\d+|\-\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+|\-\d+'
    t.value = int(t.value) # Convert string to integer
    return t

def t_QUOTE(t):
    r"'[^']*'"
    t.value = t.value[1:len(t.value)-1]
    return t

def t_DOUBLE_QUOTE(t):
    r'"[^"]*"'
    t.value = t.value[1:len(t.value)-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore spaces
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


"""
# Test the lexer
lexer.input( '(lambda (x) (+ x 1))' )

tokenized = []
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
"""

"""
if __name__ == "__main__":
    data = '(define f (x y) (+ x y))\n(f 10 20)'
    tokenized = tokenize(data)
    for tok in tokenized:
        print(tok)
"""


