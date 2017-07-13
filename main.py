import numpy as np
import random
from scipy import special

####################################################
##                Helper Functions                ##
####################################################

# Most people are reliable. Return a list of rho.
def humanGenerator(a = 9, b = 1, n = 10):
    return np.random.beta(a, b, n).tolist()


# Most targets are easy. Return a list of theta (probability of positive).
def taskGenerator(a = 0.2, b = 0.2, n = 10):
    return np.random.beta(a, b, n).tolist()


# Return a list of index of people online.
def getOnline(human_list):
    online_num = 0
    if len(human_list)<200:
        online_num = 0.5*len(human_list)
    else:
        online_num = 100
    return random.sample(range(len(human_list)), online_num)


def initialization_vanilla_var():
    human_list = humanGenerator()
    task_list = taskGenerator()
    return human_list, task_list


def h_func(x):
    return np.maximum(1-x,x)


def addone(s, index, task_list):
    rand_indicator = random.random()
    if rand_indicator < task_list[index]:
        s[index,0] = s[index,0]+1
    else:
        s[index,1] = s[index,1]+1


"""
Instructions to beta function:

E.X. special.betainc(2,4,0.5)

The inputs are (num of 1s, num of -1s, threshold), the result is the probability
of theta < threshold, so that I(a,b) in the paper is:

(1-special.betainc(a,b,0.5))

Here a is the number of 1 and vice versa which is the same as what indicated
in the paper. Ties are broken by selecting the smallest index.
"""
def parse_vanilla(task_list, numiter):
    task_num = len(task_list)
    s = np.ones([task_num, 2])
    print "s = "
    print s

    for i in xrange(numiter):
        a_plus_b = np.sum(s, axis = 1).astype(float)
        a = s[:,0].astype(float)
        b = s[:,1].astype(float)
        p1 = a/a_plus_b
        p2 = b/a_plus_b

        iab = 1-special.betainc(a,b,0.5)
        ia1b = 1-special.betainc(a+1,b,0.5)
        iab1 = 1-special.betainc(a,b+1,0.5)

        r1 = h_func(ia1b)-h_func(iab)
        r2 = h_func(iab1)-h_func(iab)

        r = p1*r1+p2*r2
        for curr_i in xrange(len(r)):
            curr_r = r[curr_i]
            if curr_r<0:
                r[curr_i] = 0

        index = np.random.choice(np.flatnonzero(r == r.max()))
        addone(s, index, task_list)

        # print "last r = "
        # print r
        # print "s = "
        # print s
    print s
    print "--------"
    print p1
    print "--------"
    print r1
    print "--------"
    print p2
    print "--------"
    print r2
    print "--------"
    print r

def parse_full(human_list, task_list, numiter):
    pass

####################################################
##                  Main Function                 ##
####################################################

# An option to tune the parameters
print ""
option = raw_input("Do you want to use the initial settings? y/n: ")

if option == "n":
    print "[Human Parameters]"
    a = float(raw_input("a = "))
    b = float(raw_input("b = "))
    n = int(raw_input("n = "))
    human_list = humanGenerator(a,b,n)
    print "[Task Parameters]"
    a = float(raw_input("a = "))
    b = float(raw_input("b = "))
    n = int(raw_input("n = "))
    task_list = taskGenerator(a,b,n)
else:
    human_list, task_list = initialization_vanilla_var()

option = raw_input("Please choose the mode: 1-homo, 2-hetero: ")
numiter = int(raw_input("Please input the number of iterations: "))
if option == "1":
    parse_vanilla(task_list, numiter)
elif option == "2":
    # human_online_index = getOnline(human_list)
    parse_full(human_list, task_list, numiter)
else:
    print "Invalid Input..."
