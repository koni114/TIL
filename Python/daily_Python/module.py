l = 9
r = 11

def oddNumbers(l, r):
    return [value for value in range(l, r+1) if value % 2 == 1]
