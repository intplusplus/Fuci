###虎书 gammar 3-5
'''
S -> if E then S else S 
S -> begin S L
S -> print E
L -> end
L -> ; S L
E -> num = num
'''

from enum import Enum,auto

class Token(Enum):
    IF = auto()
    THEN = auto()
    ELSE = auto()
    BEGIN = auto()
    END = auto()
    PRINT = auto()
    SEMI = auto()
    NUM = auto()
    EQ = auto()

tok = None

def S():
    if tok == Token.IF:
        eat(Token.IF)
        E()
        eat(Token.THEN)
        S()
        eat(Token.ELSE)
        S()
    elif tok == Token.BEGIN:
        eat(Token.BEGIN)
        S()
        L()
    elif tok == Token.PRINT:
        eat(Token.PRINT)
        E()
    else:
        error()

def L():
    if tok == Token.END:
        eat(Token.END)
    elif tok == Token.SEMI:
        eat(Token.SEMI)
        S()
        L()
    else :
        error()

def E():
    eat(Token.NUM)
    eat(Token.EQ)
    eat(Token.NUM)

def error():
    print('error')

def eat(token : Token):
    if tok == token:
        print('----------')
        print('eat ', token, ' success')
        advance()
        print('now tok :' , tok)
        print('now tokens : ', tokens)
        print('----------')
    else :
        error()

def advance():

    def getToken():
        return tokens.pop()

    # tokens.pop()
    global tok
    # tok = tokens[0]
    if tokens:
        tok = tokens.pop()

# tokens = [ Token.PRINT, Token.NUM ,Token.EQ, Token.NUM ]
tokens = [ Token.PRINT, Token.NUM ,Token.EQ, Token.NUM ]
tokens.reverse()
tok = tokens.pop()
S()

'''


'''

garmar = {}
garmar['S'] = [ ['E','$'] ]
garmar['E'] = [ ['T','E1'] ]
garmar['T'] = [ ['F','T1'] ]
garmar['E1'] = [['+','T','E1'] ,['-','T','E1'], [None] ]
garmar['T1'] = [['*','F','T1'] ,['/','F','T1'], [None] ]
garmar['F'] = [['id'] ,['num'], ['(','E',')'] ]
