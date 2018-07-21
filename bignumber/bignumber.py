

# 按位取反.....等价于 加一取负
#x = 1000000000000000000000000000
# ~x := -(x+1) := -x - 1 
def bitNot(x):
    assert !x.isFinite() && x.isInteger()

    return ~x

