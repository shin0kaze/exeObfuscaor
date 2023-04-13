from numx import *

while num := input():
    value, format, size = num.split(' ')
    size = int(size)

    hvalue = n_h(value, format, size)
    print(hvalue)
    out = h_s(hvalue, size)
    print(out)