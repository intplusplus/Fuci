
## 不知道为什么相对引用不行
# from ..DFA import NFA

import sys
import os
file_path = __file__
i = os.path.split(__file__)
sys.path.append(os.path.abspath(i[0]+ r'\..\..'))
from Fuci.DFA import NFA


'''
    测试
'''
# (ab)*(a*|b*)(ba)*

a = NFA.from_char('a')
b = NFA.from_char('b')
ab = a & b
ba = b & a
a_clouser = ~a
b_clouser = ~b
ab_clouser = ~ab
ba_clouser = ~ba
nfa = ab_clouser & (a_clouser | b_clouser) & ba_clouser

dfa = nfa.toDFA()


dfa.match('ab') #true
dfa.match('a')  #true
dfa.match('b')  #true
dfa.match('ba') #true
dfa.match('aba') #true
dfa.match('abb') #true
dfa.match('abba') #true
dfa.match('ababa') #true
dfa.match('abbba') #true
dfa.match('bba')  #true
dfa.match('baba') #true 
dfa.match('abbaba') #true
dfa.match('abababa') #true
dfa.match('abbbaba') #true
