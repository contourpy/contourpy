import math

# Splits integer n into two integer factors that are as close as possible to
# the sqrt of n, and returns them in decreasing order.  Worst case returns
# (n, 1). 
def two_factors(n):
    i = math.ceil(math.sqrt(n))
    while n % i != 0:
        i -= 1
    j = n // i
    if i > j:
        return i, j
    else:
        return j, i
