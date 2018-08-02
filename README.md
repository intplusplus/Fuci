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