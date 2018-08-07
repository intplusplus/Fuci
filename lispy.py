import math
import  operator as op

## (c) Peter Norvig, 2010-16; See http://norvig.com/lispy.html
## 学习 https://zhuanlan.zhihu.com/p/29186794


Symbol = str
List = list
Number = (int,float)
Env = dict

def tokenize(line):
    return line.replace('(',' ( ').replace(')',' ) ').split()

# print(tokenize('(begin (define r 10) (* pi (* r r) ) )'))

##将token 转换成数组,
def parse(program):
    return read_from_tokens(tokenize(program),0)

def read_from_tokens(tokens,begin):

    stack = []
    while  begin < len(tokens):
        token  = tokens[begin]
        begin = begin + 1
        if  token == '(':
            # print('begin : ',begin, ' into ( ')
            # print(stack)
            L = []
            stack.append(L)
        elif  token == ')':
            # print('begin : ',begin, ' into ) ')
            # print(stack)
            L = stack.pop()
            if  stack == [] :
                # print('----finish----')
                # print(L)
                return L
            else :
                stack[-1].append(L)
        else  :
            L = stack[-1]
            # print('begin : ',begin, ' into symbol ')
            value = None
            try:
                value = int(token)
            except ValueError:
                try: 
                    value = float(token)
                except ValueError:
                    value = Symbol(token)
            L.append(value)
            # print(stack)

# ast = parse('(begin (define r 10) (* pi (* r r) ) )')

class Procedure(object):
    "用户定义的Scheme过程。"
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))

class Env(dict):
    "环境是以{'var':val}为键对的字典，它还带着一个指向外层环境的引用。"
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "寻找变量出现的最内层环境。"
        return self if (var in self) else self.outer.find(var)

def standard_env():
    
    env = Env()
    env.update(vars(math))
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   lambda func,*t,**d : func(*t,**d),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    del env['__name__']
    del env['__doc__']
    del env['__package__']
    del env['__loader__']
    del env['__spec__']
    # print(env)
    return env

global_env = standard_env()

def eval(x, env=global_env):
    "对在某个环境下的表达式进行求值"

    if isinstance(x, Symbol):      # 变量引用
        return env.find(x)[x]      ##  先找到x所在的环境，在取值！！！
    elif not isinstance(x, List):  # 字面常量
        return x   
    elif x[0] == 'quote':          #引用
        (_,exp) = x
        return exp             
    elif x[0] == 'if':             # 条件
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':         # 定义
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'set!':          #赋值
        (_,var,exp) = x
        env.find(var)[var] = eval(exp,env)
    elif x[0] == 'lambda':        #匿名过程
        (_,parms,body) = x
        return Procedure(parms,body,env)
    else:                          # 过程调用
        proc = eval(x[0], env) ##x[0]是函数名，从env里取出函数
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

def repl(prompt='lis.py> '):
    "REPL的懒人实现。"
    while True:
        val = eval(parse(input(prompt)))
        if val is not None: 
            print(schemestr(val))

def schemestr(exp):
    "将一个Python对象转换回可以被Scheme读取的字符串。"
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')' 
    else:
        return str(exp)

repl()