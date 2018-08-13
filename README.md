# Fuci
学习记录

--2018.07.31
  '''
  pypy automata.py
  dfa -- 将状态通过字符串编码
  各个状态能够接受的字符，每个字符有一个unicode字典序，
  各个状态有编码，0，1，2，3
  
  1、首先将所有的接受字符进行排序, 得到max_size = max_char + 1。
     eg； max(DFA可以接受的输入字符) => max_char 。 then max_size = a + 1
  
  2、那么对每一个状态生成max_size长的字符串，内容是chr(state[DEFAULT])，也就是当前状态接受DEFAULT输入后到的下一状态表示的字符。
  eg ： state 0  接受default后跳转到 state97 , chr(97) == 'a' , 则生成  state_str =  'a'*max_size

  3、将上一步生成的state_str 中的字符进行替换
     eg: 如state 0  接受 'a' 到 状态 98 , 那么 state_str[ord('a')] = chr(98)

  4、 对每一个状态生成state_str，进行拼接，生成最终的state_str

  5、 这样的话， state_str[currentState * self.max_size + ord(inChar)] 可以读取到下一状态代表的字符，ord 后 就是下一状态的编码。  ,如果接受的inChar 大于了 max_size ,则当成default

  6、 ## 有两种dfa，1是非贪婪匹配，匹配成功直接返回，出错直接返回-1 ，叫做NonGreedyDFA
      ## 2是 贪婪匹配，匹配成功后继续匹配，直到出错为止，返回最近的一次成功匹配，没有返回错误。
      ## 不过automate的实现，只能检查前两次的匹配，如果不成功，就返回错误 -1
  '''
--2018.08.02

# 按位取反..等价于加一后取负
#x = 1000000000000000000000000000
# ~x := -(x+1) := -x - 1 
def bitNot(x):
    assert !x.isFinite() && x.isInteger()
    return ~x

--

----2018.08.08
    今天完成了NFA的匹配,准备完成词法分析的时候，发现一个问题
    我的NFA是组合的，那么生成出来的NFA的结束状态对应哪个token？？
    使用NFA 到 DFA 算法 和 DFA最小化算法的时候，能不能保持住状态对应的token！！！

    想来还是找一个折中的方法，先匹配出来，然后在switch 对比token好了
----
2018.08.11
最近简单看了下python的C编译器的词法分析器，并没有使用DFA之类的技术，而是手写的。
每次进入新的一行会首先是处理每行开始的空格，计算出空格数量，然后根据数量，计算出当前行的缩进等级
，并产生相应的‘INDENT’或‘DEDENT’token。

同样python库自带的tokenize,也是用相同思路实现的，先构造匹配数字、忽略字符(空格、制表符等)、字符串等的匹配，组合成一个正则表达式。
用这个组合的表达式匹配出字符串token后，在进行各种if判断（判断是不是def、async、await、字符串），返回相应的token。
期间也会进行缩进层级的判断维护，匹配字符串的时候还要注意\的处理。

而pypy的词法分析也基本是相同的过程，唯一不同的是pypy没有采用正则表达式，而是安装一般的编译原理的书籍实现了NFA，DFA，
通过组合出得DFA的进行匹配。
----