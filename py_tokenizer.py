import token
import tokenize
from io import StringIO
import re

##or-- a,b => (a|b)
def group(*choices): return '(' + '|'.join(choices) + ')'
##any-- a,b => (a|b)*
def any(*choices): return group(*choices) + '*'
##maybe-- a,b => (a|b)?
def maybe(*choices): return group(*choices) + '?'

tokens= {}
ONE = [char for char in '~!@#$%^&*()_+{}|:"<>?`-=[]\;\',./']
TWO = ['<=','>=','!=','<<','>>']
THREE = ['"""',"'''"]
KEYWORD = ['if','for','in','else','select','table','and','or']

# Interger
Hex = r'0[xX](?:_?[0-9a-fA-F])+'
Bin = r'0[bB](?:_?[01])+'
Oct = r'0[oO](?:_?[0-7])+'
#前面是处理一个0,0*这两种情况
Dec = r'(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Interger = group(Hexnumber, Binnumber, Octnumber, Decnumber)

Whitespace = r'[ \f\t]*'
Comment = r'#[^\r\n]*'
Ignore = Whitespace + any(r'\\\r?\n' + Whitespace) + maybe(Comment)
Name = r'\w+'







# ['TILDE','HYPHEN','AT','POUND-KEY','DOLLAR','PER-CENT','POWER','AMPERSAND','MULTIPLIY','LEFT-PAREN',
# 'RIGHT-PAREN','UNDERLINE','PLUS','OPEN-BRACE','CLOSED-BRACE','VERTICAL','COLON','DOUBLE-QUOTES','']
# print(one_char)