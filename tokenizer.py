import sys
import os
from DFA import NFA
from enum import Flag, auto

Integer = (NFA.group_str('123456789') & ~NFA.group_str('0123456789'))
Whitespace = ~NFA.group_str(' \f\t')
Operator = NFA.group_str('+-*/=<>:;.,@')
Bracket = NFA.group_str('{}[]()')
Id = NFA.group_str('abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_') & ~NFA.group_str('abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
##实现不对，暂时代替
String = NFA.from_char('"') & NFA.group_str('abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') & NFA.from_char('"')

whole_dfa = (Integer | Whitespace | Operator | Bracket | Id | String).toDFA().minDFA()

chars = '12312312 + - * / "asdfasd" adfas_asdfasd'
tokens = []
s = 0

while s < len(chars) :
    whole_dfa.match(chars,s)


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
