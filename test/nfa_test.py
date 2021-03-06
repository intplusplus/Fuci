
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
def test_nfa_to_dfa():

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

def test_chain_str():
    nfa = NFA.chain_str('ab')
    print(nfa)

def test_group_str():
    nfa = NFA.group_str('abc')
    print(nfa)

def tset_min_dfa():
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
    dfa.minDFA()

def test_match():
    nfa = NFA.from_char('a') | NFA.chain_str('ab') | NFA.chain_str('abc') | NFA.chain_str('abcde')
    dfa = nfa.toDFA().minDFA()
    print(dfa)
    #----贪婪-------
    print(dfa.match('a',0)) #a
    print(dfa.match('ab',0)) #ab
    print(dfa.match('abc',0)) #abc
    print(dfa.match('abcde',0)) #abcde
    print(dfa.match('b',0)) #false
    print(dfa.match('ac',0)) #a
    print(dfa.match('abcd',0)) #abc
    print(dfa.match('',0)) #false
    #----非贪婪-------
    print(dfa.match('abcd',0,False)) #true a
    print(dfa.match('d',0,False)) #false
 
test_match()

# i = ( NFA.group_str('123456789') & (~NFA.group_str('0123456789'))).toDFA().minDFA()
# print(i)


# integer = NFA.group_str('123456789') & (~NFA.group_str('0123456789'))
# integer.toDFA().minDFA()