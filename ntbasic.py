import math
import random

# return d = gcd(a, b)
def gcd(a, b):
    if (b==0):
        return a
    else:
        return gcd(b, a%b)

# return (x,y,d) such that a*x+b*y = d = gcd(a,b)
def exGcd(a, b):
    if (b==0):
        return (1,0,a);
    else:
        (y,x,d) = exGcd(b, a%b)   # which means y*b + x*(a%b) = d, i.e. y*b + x*(a-a/b*b) = d <=> a*x + b*(y-a/b*x) = d
        return (x, y-a/b*x, d)

# return inva in {1, 2, ..., p-1} such that inva*a = 1(mod p)
# This is a wrapper function for exGcd(a, p)
def inverse(a, p):
    (inva, tmp1, tmp2) = exGcd(a, p)
    return inva % p;

# return a list whose element x satiefies a*x = b (mod m) and in the range of {0, 1, ..., m-1}
# return [] if not feasible
# This is a wrapper function for exGcd(a, p)
def solvemod(a, b, m):
    (x, y, d) = exGcd(a, m);
    if b%d==0:
        #print "have ", d, " answers"
        x0, delta = b/d*x%m, m/d
        return [(x0+delta*i)%m for i in xrange(d)]
    else:
        print a, b, d, m, " Not feasible!"
        return []

# return a**b%p. If p=0, no modulo is taken.
def powermod(a, b, p=0):
    res, tmp = 1, a
    if p!=0:
        while b>0:
            if (b&1L)==1L:
                res = res * tmp % p
            tmp = tmp * tmp % p
            b >>= 1
            #print "result,tmp = ", res,tmp
    else:
        while b>0:
            if (b&1L)==1L:
                res = res * tmp
            tmp = tmp * tmp
            b >>= 1
            
    return res


"""Miller-Rabin Primility Test"""
# tell if n is a prime(assume n>1)
def millerRabin(n):
    if n==1:
        print "Alert! n = 1!"
        return False

    basis = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    length = len(str(n))*2 # if n is extremely large, add more basis
    if (length>18):
        for i in xrange(length):
            basis.append( random.randint(29, n-2) )

    for base in basis:  # try to divide n by small prime numbers
        if n==base:
            return True
        if n%base==0:
            return False

    mod = n-1
    m, k = mod, 0
    while ((m&1)==0):
        m >>= 1
        k += 1

    for base in basis:
        tmp = powermod(base, m, n)
        if (tmp==1 or tmp==mod):    # now n passes Miller-Rabin Test of this base
            continue;

        
        for i in xrange(1,k):
            tmp = tmp * tmp % n
            if tmp==mod:            # n passes Primality Test of this base
                break
            if tmp==1:            # n is a composite
                return False;
        if tmp!=mod:
            return False

    return True


# Pollard-Rho Algorithm for Number Theory
# Using pseudo sequence f(x) = x*x + I_AM_FEELING_LUCKY % n
# return a factor of n(n>100 expected, or we may get into an endless loop)
def pollardrhoNT(n):

    I_AM_FEELING_LUCKY = 15323

    res = 0
    while (res==0):
        x = random.randint(1, n-1)
        y = x
        i1,i2 = 1, 2
        while (True):
            i1 += 1
            x = (x*x + I_AM_FEELING_LUCKY)%n
            d = gcd(y+n-x, n)   # d = gcd(y-x, n)
            if (d!=1 and d!=n):
                return d
            if (y==x):          # We may get into an endless loop
                res = 0         # Try to run this algorithm again with another initial value
                #print "Fail... Try again"
                break;
            if (i1==i2):        
                y = x;
                i2 <<= 1

    return 0    # this part should never be visited


# returns a list which contains all its prime factors
# assume n is larger than 100(if n is too small, Pollard-Rho may get into an endless loop)
def factorList(n):

    # using Pollard-Rho Algorithm to factor n
    if millerRabin(n)==True:
        return [n]
    else:
        factor1 = pollardrhoNT(n)
        #print factor1, n/factor1
        return factorList(factor1) + factorList(n/factor1)


# returns a dictionary which contains all its prime factors
# this is a wrapper function for factorList(n)
# assume n>1
def factorDict(n):

    factors = []

    # try to figure out all prime factors < 100
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 
            53, 59, 61, 61, 67, 71, 73, 79, 83, 89, 91, 97]
    for i in small:
        while (n%i==0):
            factors.append(i)
            n /= i
    if n>1:
        factors = factors + factorList(n)
    s = set(factors)
    ans = {}
    for i in s:
        ans[i] = factors.count(i)
    return ans


# return the smallest primitive root of p
# Algorithm: enumerate 2, 3, ... until a primary root is found.
def findPrimitiveRoot(p, factors={}):
    g, m = 2, p-1
    if factors=={}:
        factors = factorDict(m)
    while (True):
        isRoot = True
        for f in factors.keys():
            if powermod(g, m/f, p)==1:
                isRoot = False
                break;
        if isRoot==True:
            print "Find primary root: ", g
            return g
        else:
            if g>20:        # Give some hints when it takes too long
                print g, "is not primary root.  Please be patient..."
            g += 1
    return -1 # this should never happen


# returns the unique solution for linear modulo equation groups x = a[i] (mod m[i])
# assume that for all i!=j, (m[i], m[j]) = 1.
# Using Chinese Remainder Theorem
def CRT(a, m):
    M = reduce(lambda x,y:x*y, m)
    Mi = map(lambda x:M/x, m)
    invMi = map(inverse, Mi, m)
    return sum(map(lambda x,y,z:x*y*z, a, Mi, invMi)) % M
