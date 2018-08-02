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
            self.ismathed = next_status in self.finish
        
        self.nowstate = next_status

        return is_match_success

    def match(self,string):
        print('---------match: ',string,' -----')
        chars = list(string)
        for char in chars:

            match_char_success = self._in(char)
            if not match_char_success:
                break
        
        match_string_success = self.ismathed
        
        if match_string_success: 
            print('----------match success : ' , self.nowstate, '------------')
        else :
            print('----------match error -----------')
        
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

    def mini(self):
        None

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

    def __init__(self,alphabet,status,finish,transition,start_status = 0):
        '''
            status: 是状态集合，纯数字, 都大于0
            eg: [0,1,2,3]

            alphabet: 字母表，接受字符的集合
            eg: ['a','b']

            finish: 结束状态集合：
            eg: [1,2]  表示状态1、状态2是结束状态

            transition： 状态转换字典,key是状态，值也是一个字典，用来存储接受字符后跳转到的状态
            eg: {0:{'a':[1],'b':[1,2]}} 表示状态0， 接受'a' 跳转到1，接受'b'跳转到[1,2]
            用None表示接受Eplison

            默认开始状态为状态0

        '''

        assert status[0] == 0
        assert all([isinstance(i,int) and i >=0 for i in status]) # status是大于0的数字
        
        self.alphabet = alphabet # 字母表 : []
        self.status = status # 状态集合 : [int]
        self.finish = finish #结束状态: [int]
        self.nowstate =  start_status # 默认开始状态为0
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
        '''
            返回状态status接受char后能够达到的状态集合\n
            eg: nfa1.moveto([0,1],'a') 返回 [1,2,3]\n
            代表nfa1的0,1状态接受'a'后可以到达[1,2,3]状态\n

            如果状态不存在，或者状态都不没有接受char的边,
            返回空数组[]
        '''

        if isinstance(status,Iterable):
            ##获取每个状态接受char能够到达的状态
            table = [ c for s in status for c in self.moveto(s,char)] 
            ##去重排序
            table = list(set(table))
            table.sort()
            return table
        elif isinstance(status,int):
            #如果状态不存在，或不接受char,返回[]
            table = self.transition.get(status,{})
            return table.get(char,[])

        return []

    def epsilon_closure(self,status):
        ''' 
            
            返回状态的Epsilon闭包\n
            status: [int] or int 

        '''
        ## 修改int型为集合：[int]
        status = [status] if isinstance(status,int) else status

        ##获取status能够epslion跳转到状态
        stack = [ next_s for s in status for next_s in self.transition.get(s,{}).get(None,[])]
       
        ##把status能够epslion跳转到状态,加入闭包
        closure = stack.copy()
        
        ##闭包都包括自身
        closure.extend(status)

        ##用来存储处理过状态
        used = []

        while len(stack) != 0:
            s = stack.pop()
            #对stack中没有获取过epslion边的，进行处理。
            #添加epslion跳转后的状态进入闭包和栈中
            if s not in used:
                c= self.transition.get(s,{}).get(None,[])
                closure.extend(c)
                stack.extend(c)
                used.append(s)
    
        #去重，排序
        closure = list(set(closure))
        closure.sort()
        
        return closure

    def toDFA(self):
        
        '''
            子集构造算法
        '''

        s0 = self.nowstate  #开始状态

        #开始状态的闭包，做为准备构造的DFA的第一个状态
        #tuple是为了固化，[]无法当作字典的key
        e_s0 = tuple(self.epsilon_closure(s0))

        #构造中使用的栈
        stack = [e_s0] 

        tranistion = {} ## 生成的DFA状态
        
        alphabet = self.alphabet #字符表
        
        #给构造DFA途中生成的状态进行标记
        label = [e_s0] 
        
        while len(stack) != 0:
            s = stack.pop()
            
            label_s =  label.index(s) if s in label else len(label)

            ## 状态s的跳转表
            s_table = tranistion.get(label_s,{})
            
            for char in alphabet:
                next_s = self.moveto(s,char)
                
                ## next_s空，则跳过
                if not next_s:
                    continue

                next_s_epsilon_closure = tuple(self.epsilon_closure(next_s))

                # print('status ' , label.index(s) ,' char ', char , ' moveto ', str(next_s_epsilon_closure))


                if next_s_epsilon_closure not in label:
                    stack.append(next_s_epsilon_closure)
                    label.append(next_s_epsilon_closure)
                # print('stack len: ' , len(stack))

                # s_table[char] = [label.index(next_s_epsilon_closure)]
                s_table[char] = label.index(next_s_epsilon_closure)
            
            tranistion[label_s] = s_table

        ##构造finish集合, 构造DFA中的产生的状态中，包含有NFA中的结束状态的，都是新的结束状态
        finish = [ label.index(i) for i in label if any([ j in i for j in self.finish ]) ]

        # return NFA(alphabet,list(range(len(label))),finish,tranistion)

        return DFANode(alphabet,list(range(len(label))),finish,tranistion)

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


