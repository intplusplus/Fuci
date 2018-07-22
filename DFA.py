from collections import Iterable

class DFANode:

    def __init__(self,alphabet,status,finish,transition):
        
        assert all([None != i for i in status]) # status 不包含 None
        
        self.alphabet = alphabet # 字母表
        self.status = status # 状态集合
        self.finish = finish #结束状态, {'status': token}
        self.nowstate = status[0] # 默认开始状态为第一个状态
        self.transition = transition ## 状态转移表，用dict来表示 eg: {'status1':{'a':'status2}}
        self.ismathed = False # DFA 是否匹配成功
        self.nodes = [self]

        self.op = None ## 如果op 不为空，代表是一个复合DFANode

    def _in(self,char):
        
        assert self.nowstate in self.status
        
        match_success = False
        # print('char {0} now: {1} getnext'.format(char,self.nowstate))
        next_status = self.transition[self.nowstate].get(char,None)
        
        next_status = None if next_status not in self.status else next_status

        print("in : " ,char," trans: ",self.nowstate," -> ", next_status)

        if next_status : # next_status != None
            self.nowstate = next_status
            self.ismathed = any([self.nowstate == i for i in self.finish.keys()])
            match_success = True
        else : 
            self.ismathed = False
        
        return match_success

    def match(self,string):

        chars = list(string)
        for char in chars:
            match_char_success = self._in(char)
            if not match_char_success:
                break
        
        match_string_success = self.ismathed
        
        if match_string_success: 
            print('match success : ' , self.finish[self.nowstate])
        
        print('match error')
        self._reinit()
        return match_string_success

    def _reinit(self):
        self.ismathed = False
        self.nowstate = self.status[0]

    @classmethod
    def from_string(cls,string,token_name):
        chars = list(string)
        alphabet = list(set(chars))
        status = list(range(len(chars) + 1))
        finish = {status[-1]:token_name}
        transition = dict(zip(status,[{j:i} for i,j in enumerate(chars,start=1)]+[{}]))
        return DFANode(alphabet = alphabet,status = status, finish = finish, transition = transition)


    def __or__(self,dfanode):
        assert isinstance(dfanode , (DFANode,DFA))
        return DFA(self,dfanode,'|')

    def __and__(self,dfanode):
        assert isinstance(dfanode ,(DFANode,DFA))
        return DFA(self,dfanode,'&')

    # def __str__(self):
    #     return '''  finish:  {0}  
    #                 transition: {1}'''.format(str(self.finish),str(self.transition)), 

class DFA:

    def __init__(self,a,b,op):
        assert (op != None and a != None and b != None)
        self.dfanodes = [a,b]
        self.op = op

    def match(self,string):
        if self.op: ## 符合Node
            if self.op == '&':
                return self.dfanodes[0].match(string) and self.dfanodes[1].match(string) 
            elif self.op == '|':
                return self.dfanodes[0].match(string) or self.dfanodes[1].match(string) 

    def __and__(self,node):
        assert isinstance(node,(DFA,DFANode))

        DFA(self,node,'&')

        return DFA(self,node,'&')

    def __or__(self,dfa):
        assert isinstance(node,(DFA,DFANode))

        DFA(self,node,'|')

        return DFA(self,node,'|')

    def __repr__(self):
        return "DFA"


transition = {
    '1':dict(zip(list("0123456789"),['5']+['2']*9)),
    '2':dict(zip(list("0123456789."),['2']*10 + ['3'])),
    '3':dict(zip(list("0123456789"),['4']*10)),
    '4':dict(zip(list("0123456789"),['4']*10)),
    '5':dict(zip(list("."),['6'])),
    '6':dict(zip(list("0123456789"),['7']*10)),
    '7':dict(zip(list("0123456789"),['7']*10)),
}

## 整数加小数
node = DFANode(alphabet =list("0123456789."),status=list("1234567"),finish=dict(zip(list("2457"),['整数','小数','整数','小数'])),transition = transition)
# node.match('124.12')

# i = DFANode.from_string('IF','IF')

# print(i.nowstate)
# print(i.finish)
# print(i.transition)
# i.match('IF')

i = DFANode.from_string('I00','I00')
i.match('I')
print(i.nowstate)
print(i.finish)
print(i.transition)