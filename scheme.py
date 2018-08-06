import math
import  operator as op


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

ast = parse('(begin (define r 10) (* pi (* r r) ) )')

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
    print(env)
    return env

global_env = standard_env()

def eval(x, env=global_env):
    "对在某个环境下的表达式进行求值"

    if isinstance(x, Symbol):      # 变量引用
        return env[x]
    elif not isinstance(x, List):  # 字面常量
        return x                
    elif x[0] == 'if':             # 条件
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':         # 定义
        (_, var, exp) = x
        env[var] = eval(exp, env)
    else:                          # 过程调用
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)
