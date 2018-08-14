import re

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

    garmar:
    S -> NT BLANK := BLANK E
    E -> NT BLANK E
    E -> T BLANK E
    E -> NT
    E -> T
    E -> eplision   ;空
    NT -> [A-Z]+[0-9]*
    T -> [^A-Z\s\r\n]+
    BLANK -> \s+   ;空白符

       NULLABLE     FIRST               FOLLOW
  S      no         [A-z]               [^\r\s\n]
  E      yes        [^\s\r\n]           [^\r\s\n]
  NT     no         [A-Z]               [A-Z0-9]
  T      no         [^A-Z\s\r\n]        [^A-Z\s\r\n]
  BLANK  no         \s                    \s


预测分析表
       [A-z]    [^\r\s\n]    [^A-Z\s\r\n]     \s      [A-Z0-9]
S      
E
NT
T
BLANK




'''




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
                token = ('NT',line_number,match.group())
                line_tokens.append(token)
                print(token)
                b = b + match.span()[1]
                continue
            #匹配BLANK
            match = re.match(r'\s+',line[b:])
            if match:
                token = ('BLANK',line_number,match.group())
                line_tokens.append(token)
                print(token)
                b = b + match.span()[1]
                continue
            
            #匹配T
            match = re.match(r'[^A-Z\s\r\n]+',line[b:])
            if match:
                token = ('T',line_number,match.group())
                line_tokens.append(token)
                print(token)
                b = b + match.span()[1]
                continue
            
            print('token error start : ',line[b:])
            break
        tokens.append(line_tokens)
    return tokens

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
print(t)