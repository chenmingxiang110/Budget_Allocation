import numpy as np
import random
from scipy import special

def h_func(x):
    return max(1-x,x)

ab = raw_input("Please input a and b such as \"a,b\": ")
ablist = ab.split(",")
a = float(ablist[0])
b = float(ablist[1])

p1 = a/(a+b)
p2 = b/(a+b)

iab = 1-special.betainc(a,b,0.5)
ia1b = 1-special.betainc(a+1,b,0.5)
iab1 = 1-special.betainc(a,b+1,0.5)

r1 = h_func(ia1b)-h_func(iab)
r2 = h_func(iab1)-h_func(iab)

r = p1*r1+p2*r2

print round(r,6)
