from collections import Iterable

class DFANode:

    def __init__(self,alphabet,status,finish,transition):
        
        assert all([None != i for i in status]) # status 不包含 None
        
        assert status[0] == 0
        assert all([isinstance(i,int) and i >=0 for i in status]) # status 是数字
        
        self.alphabet = alphabet # 字母表 : []
        self.status = status # 状态集合 : [int]
        self.finish = finish #结束状态: [int]
        self.nowstate = status[0] # 默认开始状态为第一个状态
        self.transition = transition ## 状态转移表，用dict来表示 eg: {'status1':{'a':'status2}}
        self.ismathed = False # 是否匹配成功
        self.unknownstate = 'This status can\'t arrive '+ str(status) + str(alphabet)
        self.nodes = [self]

        self.op = None ## 如果op 不为空，代表是一个复合DFANode

    def _in(self,char):
        
        assert self.nowstate in self.status
        
        is_match_success = False         
        next_status = self.transition[self.nowstate].get(char,self.unknownstate)
        
        if next_status == self.unknownstate:
            print("in : " ,char)
            self.ismathed = False
        else : # 进入下一状态成功
            print("in : " ,char," trans: ",self.nowstate," -> ", next_status)
            is_match_success = True
            self.ismathed = any([self.nowstate == i for i in self.finish.keys()]) ## 当前是否处于结束状态
            
        self.nowstate = next_status
        return is_match_success

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

class NFA:

    def __init__(self,alphabet,status,finish,transition):
        
        assert status[0] == 0
        assert all([isinstance(i,int) and i >=0 for i in status]) # status 是数字
        
        self.alphabet = alphabet # 字母表 : []
        self.status = status # 状态集合 : [int]
        self.finish = finish #结束状态: [int]
        self.nowstate = status[0] # 默认开始状态为第一个状态
        self.transition = transition ## 状态转移表，用dict来表示 eg: {'status1':{'a':'status2}}
        self.ismathed = False # 是否匹配成功
        self.unknownstate = 'This status can\'t arrive '+ str(status) + str(alphabet)

    def __and__(self,node):
        
        assert isinstance(node,NFA)
        
        A = self
        B = node 

        #新的字母表
        alphabet = list(set(A.alphabet + B.alphabet))
        
        #偏移量，用来把B的状态偏移到合适的数字
        a_offset = 1
        b_offset = max(A.status) + a_offset + 1

        #新的状态集合
        status = [0] + [ a_offset + i  for i in A.status] + [ b_offset + i  for i in B.status]

        #B的结束状态为新的结束状态集合
        finish = [i+b_offset for i in  B.finish]

        #新的状态转移字典
        transition = {0:{None:[1]}}
        transition.update(NFA.transition_add(A,a_offset)) 
        transition.update(NFA.transition_add(B,b_offset))

        ## 将A的结束状态 ，都添加一条接受None的边到 B的开始状态
        for i in A.finish:
            new_table = transition.get(i+a_offset,{})

            next_status = new_table.get(None,[])
            
            next_status.append(b_offset + B.status[0])
            
            new_table[None] = next_status

            transition[i+a_offset] = new_table

        return NFA(alphabet,status,finish,transition)

    def __or__(self,node):
        assert isinstance(node,NFA)
        ## A + B
        A = self
        B = node

        #新的字母表
        alphabet = list(set(A.alphabet + B.alphabet))
        
        ## a | b 要添加一个起始和结束状态

        new_A_status = [1 + i for i in A.status]
        new_B_status = [max(new_A_status) + 1 + i for i in B.status]

        #新的状态集合
        status = [0] + new_A_status + new_B_status + [max(new_B_status) + 1]

        #新的结束状态
        finish = [max(status)]

        #新的状态转移字典
        transition = {0:{None:[min(new_A_status),min(new_B_status)]}}


        ## 将A的状态转移字段合并进新的转移字段,A的状态偏移量为1,
        for k,v in A.transition.items():
            new_status = k + 1
            transition[k + 1] = {}

            for char,ns in A.transition[k].items():
                transition[k + 1][char] =  [i + 1 for i in ns] if isinstance(ns,Iterable) else [ns + 1]

        ## 将A的结束状态 ，都添加一条接受None的边到结束状态
        for k in A.finish:
            finish_dict = transition.get(k+1,{})
            finish_table = finish_dict.get(None,[])
            finish_table = finish_table + [finish[0]]
            finish_dict[None] = finish_table
            transition[k+1] = finish_dict

        ## 同上相同
        ## 将B的状态转移字段合并进新的转移字段,B的状态偏移量为max(new_A_status) + 1,
        for k,v in B.transition.items():
            offset = max(new_A_status) + 1
            transition[k + offset] = {}

            for char,ns in B.transition[k].items():
                transition[k + offset][char] =  [i + offset for i in ns] if isinstance(ns,Iterable) else [ns + offset]

                     
        ## 将B的结束状态 ，都添加一条接受None的边到结束状态
        for k in B.finish:
            finish_dict = transition.get(k+offset,{})
            finish_table = finish_dict.get(None,[])
            finish_table = finish_table + [finish[0]]
            finish_dict[None] = finish_table
            transition[k+offset] = finish_dict

        return NFA(alphabet,status,finish,transition)

    def __invert__(self):
        ##A
        A = self

        #新的字母表
        alphabet = A.alphabet.copy()
        
        #偏移量，用来把B的状态偏移到合适的数字
        offset = 1

        #新的状态集合
        status = [0] + [1] + [ i + offset + 1 for i in A.status ]

        #新的结束状态
        finish = [status[-1]]

        transition = { 0:{None:[1,status[-1]]} }

        transition.update(NFA.transition_add(A,offset))

        # print(transition)

        #给旧的结束状态添加两条None的边，一条添加到新的结束状态，一条添加到旧的开始状态
        for f in A.finish:
            i = A.transition.get(f,{})
            t = i.get(None,[])
            t = t + [1,finish[0]]
            i[None] = t
            transition[f + 1] = i

        # print(transition)

        return NFA(alphabet,status,finish,transition)

    def __repr__(self):
        
        r = ''' 
        alphabet : {0}
        status : {1}
        finish : {2}
        transition : {3}
        '''.format(self.alphabet,self.status,self.finish,self.transition)

        return r

    def moveto(self,status,char):
        '返回状态status接受char后能够达到的状态集合'

        if isinstance(status,Iterable):
            table = [ c for s in status for c in self.moveto(s,char)]
            table = list(set(table)).sort()
            
            return table
        elif isinstance(status,int):
            table = self.transition[status]
            return table.get(char,[])

    def epsilon_closure(self,status):
        ''' status: [int] or int '''

        if isinstance(status , Iterable):
            closure = [ c for s in status for c in self.epsilon_closure(s)]
            closure = list(set(closure))
            closure.sort()
            return closure
        elif isinstance(status,int):

            closure = self.transition.get(status,{}).get(None,[])
            stack = closure.copy()
            used = []

            while len(stack) != 0:
                s = stack.pop()
                if s not in used:
                    c= self.transition.get(s,{}).get(None,[])
                    closure.extend(c)
                    stack.extend(c)
                    used.append(s)
        
            if status not in closure: #闭包都包括自身
                closure.append(status)

            closure = list(set(closure))

            closure.sort()
            return closure

    def toDFA(self):
        None

    @classmethod
    def from_char(cls,char):
        alphabet = [char]
        status = [0,1]
        finish = [1]
        # 规定转换状态都是[],这样就不用检查了
        transition = {0:{char:[1]},1:{}}
        return NFA(alphabet = alphabet,status = status, finish = finish, transition = transition)

    @classmethod
    def transition_add(cls,nfa,offest):
        assert isinstance(nfa,NFA)

        ts = nfa.transition
        nts = {}
        for status,transition_dict in ts.items():
            ntd = {}
            for inchar, to_stauts in transition_dict.items():
                ntd[inchar] = [i+offest for  i in to_stauts]
            nts[status + offest] = ntd
        
        return nts


#ab*(a*|b*)ba*

a = NFA.from_char('a')
b = NFA.from_char('b')
ab = a & b
ba = b & a
a_clouser = ~a
b_clouser = ~b
ab_clouser = ~ab
ba_clouser = ~ba
nfa = ab_clouser & (a_clouser | b_clouser) & ba_clouser
print(nfa)

for i in nfa.status:
    print('status ' ,i,' e_closure: ' ,nfa.epsilon_closure(i))

print(nfa.epsilon_closure([11,15,24]))