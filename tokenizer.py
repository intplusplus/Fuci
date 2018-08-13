import sys
import os
from DFA import NFA
from enum import Flag, auto
import tokenize
import re

id_char = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890'
id_first_char = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

Integer = (NFA.group_str('123456789') & ~NFA.group_str('0123456789')).toDFA().minDFA()
Whitespace = (~NFA.group_str(' \f\t')).toDFA().minDFA()
Operator = NFA.group_str('+-*/=<>:;.,@').toDFA().minDFA()
Bracket = NFA.group_str('{}[]()').toDFA().minDFA()
Id = (NFA.group_str(id_first_char) & ~NFA.group_str(id_char)).toDFA().minDFA()
##实现不对，暂时代替
String = NFA.from_char('"') & ~NFA.group_str('abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') & NFA.from_char('"')

whole_dfa = (Integer | Whitespace | Operator | Bracket | Id | String).toDFA().minDFA()

chars = '12312312 + - * / "asdfasd" adfas_asdfasd'
token_values = []
tokens = []
s = 0

while s < len(chars) :
    
    finish_status, start,end =  whole_dfa.match(chars,s)
    print(start , '  ', end)
    if end == 0:
        print('end ' ,0)
        break 
    token_values.append(chars[start:end])
    s = end




print(tokens)

token_define = {
    'ENDMARKER':'',
    'NUMBER':'',
    'STRING':'',
    'NEWLINE':'',
    'INDENT':'',
    'DEDENT':'',
    'LPAR':"(",
    'RPAR': ")",
    'LSQB': "[",
    'RSQB': "]",
    'COLON': ":",
    'COMMA':  "," ,
    'SEMI' : ";" ,
    'PLUS' : "+" ,
    'MINUS': "-" ,
    'STAR' : "*" ,
    'SLASH': "/" ,
    'VBAR' : "|" ,
    'AMPER' : "&" ,
    'LESS' : "<" ,
    'GREATER': ">" ,
    'EQUAL' : "=" ,
    'DOT' :  "." ,
    'PERCENT': "%" ,
    'BACKQUOTE': "`",
    'LBRACE':"{" ,
    'RBRACE': "}" ,
    'EQEQUAL': "==" ,
    'NOTEQUAL': ["!=", "<>"] ,
    'LESSEQUAL': "<=" ,
    'GREATEREQUAL': ">=" ,
    'TILDE': "~" ,
    'CIRCUMFLEX': "^" ,
    'LEFTSHIFT': "<<" ,
    'RIGHTSHIFT': ">>" ,
    'DOUBLESTAR': "**" ,
    'PLUSEQUAL': "+=" ,
    'MINEQUAL': "-=" ,
    'STAREQUAL': "*=" ,
    'SLASHEQUAL' : "/=" ,
    'PERCENTEQUAL': "%=" ,
    'AMPEREQUAL': "&=" ,
    'VBAREQUAL': "|=" ,
    'CIRCUMFLEXEQUAL': "^=" ,
    'LEFTSHIFTEQUAL': "<<=" ,
    'RIGHTSHIFTEQUAL': ">>=" ,
    'DOUBLESTAREQUAL': "**=" ,
    'DOUBLESLASH':"//" ,
    'DOUBLESLASHEQUAL':"//=" ,
    'AT': "@" ,
    'ATEQUAL': "@=" ,
    'RARROW': "->",
    'ELLIPSIS': "...",
    'OP':'',
    'ASYNC':'',
    'AWAIT':'',
    'ERRORTOKEN':'',
}
