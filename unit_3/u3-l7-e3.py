def stdDevOfLengths(L):
    """
    L: a list of strings

    returns: float, the standard deviation of the lengths of the strings,
      or NaN if L is empty.
    """
    N = len(L)
    if N == 0:
        return float("NaN")
    else:
        sum_e = 0
        for e in L:
            sum_e += len(e)
        mean = sum_e / N
        sum_dev_squared = 0
        for e in L:
            sum_dev_squared += (len(e) - mean)**2
        return (sum_dev_squared / N)**0.5
        

# Test
L = ['a', 'z', 'p']
print(stdDevOfLengths(L))
L = ['apples', 'oranges', 'kiwis', 'pineapples']
print(stdDevOfLengths(L))
