
class Decimal:
    s ## sign
    e ## exponent 底
    d ## 用来存数的数组 [1234,42324,34432]??
    

    def __init__(self,value):
        None
    
    def abs(sefl):
        new_decimal = Decimal(self)
        if new_decimal.s == 0 :
            new_decimal.s = 1
        
        return new_decimal

    def cmp(self,y):
        x = self
        y = Decimal(y)

        # sign differ  
        # 0 or -1 := -1  
        # 1 or 0 := 1
        if x.s != y.s : return x.s or -y.s

        # 此时 x.s = y.s 
        # 负数情况下，底大的数学小，正数情况下，底大的数大
        #      (^)  x.e > y.e   Ture , False
        #  x.s < 0
        #     True              False   True    
        #     False             True    False
        if x.e != y.e : 
            return  1 if (x.e > y.e) ^ (x.s < 0) else  -1

        #底相同
        #按位比较
        xdl = x.d.length
        ydl = x.d.length

        for i in len(min(xdl,ydl)):
            ## 比较方法同上 比较底的方法一样
            if x.d[i] != y.d[i] : return 1 if (x.d[i] > y.d[i]) ^ (x.s < 0) else  -1

        ## 位相同的情况下，比较长度
        return 0 if xdl == ydl  else ( 1 if xdl > ydl ^ x.s < 0 else -1)

    def isint(self):
        #??
        return self.e > len(self.d) - 2

    def log(sefl,base = 10):
        #log[base](x) = ln(x) / ln(base)

        x = self
        pr = x.precision,
        
        # base (0,1) or (1,+inf)
        assert base > 1 or (base >0 and base < 1)
        assert x.s > 0

        if x.s == 1 return Decimal(0,precision = pr)

        # r = divide(ln(x, pr + 5), ln(base, pr + 5), pr + 5);
        # return round(r,pr)

    def round(self,sd,rm):
        '''
        sd: round 到的位数
        '''
        x = self
        xd = x.d

        #先计算第一个数字(xd[0])有几位:n
        n = 1
        k = xd[0]
        while k >=10:
            k /= 10
            n += 1

        
        




