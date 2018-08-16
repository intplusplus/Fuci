import re
import collections

'TODO: 写一个简单的BNF'
'''
    1. 左边只能有一个非终结符
    2. 右边用空格隔开所有独立单元，如终结符、非终结符
    3. 定义用:= 表示
    4. 非终结符只能是大写字母
    5. 终结符总能小写字母,和其它字符

    
    示例:
    E := E + A 
    A := print ( a + b ) 
    
garmar0.1:    
    S -> NT BLANK := BLANK E  (1)
    E -> NT BLANK E           (2) 
    E -> T BLANK E            (3)
    E -> NT                   (4)
    E -> T                    (5)
    E -> eplision   ;空       (6)
    NT -> [A-Z]+[0-9]*        (7)
    T -> [^A-Z\s\r\n]+        (8)
    BLANK -> \s+   ;空白符     (9)

       NULLABLE     FIRST               FOLLOW
  S      no         [A-z]               [^\r\s\n]
  E      yes        [^\s\r\n]           [^\r\s\n]
  NT     no         [A-Z]               [A-Z0-9]
  T      no         [^A-Z\s\r\n]        [^A-Z\s\r\n]
  BLANK  no         \s                    \s


预测分析表(t.1)
       [A-z]    [^\r\s\n]    [^A-Z\s\r\n]     \s      [A-Z0-9]
S      (1)
E      (2)(4)    (5)            (3)(5)
NT     (7)                      
T                               (7)
BLANK                                         (9)

上表化简(t.2)
       [A-z]          [^A-Z\s\r\n]     \s     
S      (1)
E      (2)(4)(5)         (3)(5)
NT     (7)                      
T                         (7)
BLANK                                  (9)

'''
token_tuple = collections.namedtuple('token',['type','line_number','value'])

class ASTNode:
    '''
        抽象语法树，设计成一个多叉树，
        用一个数组来存储孩子节点
    '''
    def __init__(self):
        self.children = []
        self.value = None
        self.parent = None

    def creat_children(self,tokens):
        ast_list = []
        for t in tokens:
            i = ASTNode()
            i.value = t
            i.parent = self
            ast_list.append(i)
        self.children.extend(ast_list)
        return ast_list

    def creat_child(self):
        c = ASTNode()
        c.parent = self
        self.children.append(c)
        return c 


def tokenizer(source):
    #token := (类型，行号，值)
    
    tokens = []
    lines = [i for i in source.split('\n') if i]
    for line_number,line in enumerate(lines):
        line_tokens = []
        b = 0
        while b < len(line):
            #匹配NT
            match = re.match(r'[A-Z]+[0-9]*',line[b:])
            if match:
                token = token_tuple('NT',line_number,match.group())
                line_tokens.append(token)
                # print(token)
                b = b + match.span()[1]
                continue
            #匹配BLANK
            match = re.match(r'\s+',line[b:])
            if match:
                token = token_tuple('BLANK',line_number,match.group())
                line_tokens.append(token)
                # print(token)
                b = b + match.span()[1]
                continue
            
            #匹配T
            match = re.match(r'[^A-Z\s\r\n]+',line[b:])
            if match:
                token = token_tuple('T',line_number,match.group())
                line_tokens.append(token)
                # print(token)
                b = b + match.span()[1]
                continue
            
            print('token error start : ',line[b:])
            break
        tokens.append(line_tokens)
    return tokens

def parser(tokens):
    ''' garmar0.1:   
        S -> L NEWLINE L          (0)
        S -> L                    (1)   
        L -> NT BLANK := BLANK E  (2)
        E -> NT BLANK E           (3) 
        E -> T BLANK E            (4)
        E -> NT                   (5)
        E -> T                    (6)
        E -> eplision   ;空       (7)
        NT -> [A-Z]+[0-9]*        (8)
        T -> [^A-Z\s\r\n]+        (9)
        BLANK -> \s+   ;空白符     (10)

        #语法(3)(4)可以合并成E -> E BLANK E
        既有左递归，又有右递归，不知道怎么处理
        但是从语义上来说很明确，BLANK只是一个分隔符，没有操作在里面
        所以每次读取两个token，然后选择替换成(3),(4)就可以的。
        开始是固定读取4个token，检测是不是NT BLANK := BLANK，然后构造(1)就OK了
    '''

    root = ASTNode()
    root.value = token_tuple('S','-1','?')
    print('--begin parser--')
    print(root.value)
    for line in tokens:

        line_number = line[0].line_number
        
        ###打印当前行
        print('*'*20)
        print('line ' , line_number)
        print([tok.value for tok in line])
        print('-'*20)        
        ###

        node = root.creat_child()
        p = 0 #用来指示当前解析到的位置
        
        while p <= len(line):
        
            # S -> NT BLANK := BLANK E
            if p == 0 and [t.type for t in line[:4]] == ['NT','BLANK' , 'T' ,'BLANK']: 
                if line[2].value != ':=':
                    print('S -> NT BLANK := BLANK E , := error')
                    break
                node.creat_children(line[0:4]+[token_tuple('E',line_number,'?')])
                # print('S -> NT BLANK := BLANK E')
                print([tok.value for tok in line[:4]])
                p = 4
                node.value = token_tuple('L',line_number,'?')
                node = node.children[-1] ## 每次解析完，最后一个节点应当是E

            else : 
                if p == 0:
                    print('parser S -> NT BLANK := BLANK E error')
                    break
                #解析E
                #剩下超过3个token,那么是
                #E-> NT BLANK E
                #E-> T BLANK E
                #这两种情况
                if p + 2 < len(line) : 
                    if line[p+1].type == 'BLANK':
                        node.creat_children(line[p:p+2]+[token_tuple('E',line_number,'?')])
                        print(line[p].value ,'',line[p+1].type)
                        p = p + 2
                        node = node.children[-1]
                    else :
                        print('parser error')
                        break

                else :
                    ## 只剩下0|1|2个token 这3中情况,
                    ## 剩下0个，那么最后一个E推出空，对应 E-> eplision
                    ## 剩下1个，对应 E->(NT|T)
                    ## 剩下2个，对应 E -> (NT|T) BLANK E, 最后一个E->eplision
                    
                    if p == len(line):  # 剩0个
                        node.value.value = ''
                        print('E-> ')
                        break
                    elif p + 1 == len(line): #剩1个，p
                        if line[p].type not in ['NT','T']:
                            print('line : ',line_number,' error ')
                            break
                        c = node.creat_child()
                        c.value = line[p]
                        print('E-> ',line[p].value)
                        break
                    elif p + 2 == len(line): ##剩2个,p,p+1
                        if line[p].type not in ['NT','T'] or line[p + 1].type != 'BLANK':
                            print('line : ', line_number,' error ')
                            break
                        node.creat_children(line[p:])
                        print('E-> ',line[p].value , ' ',line[p+1].type)
                        break

    if len(root.children) > 1: ###行数大于1,那么S->L NEWLINE L
        new_line_nodes = [ASTNode() for i in range(len(root.children))]

        for n in new_line_nodes:
            n.parent = root
            n.value = token_tuple('NEWLINE','-1','NEWLINE')


        from itertools import chain
        root.children = list(chain.from_iterable(zip(root.children, new_line_nodes)))
        del root.children[-1]
        del chain

    return root
                    

# parser([])  

enf = '''
E := E OP E
E := ( E )
E := - E
E := id
OP := +
OP := -
OP := *
OP := /
'''

t =  tokenizer(enf)
root = parser(t)

def print_ast(root):
    print(root.value)
    if root.children :
        for c in root.children:
            print_ast(c)

print_ast(root)