import math
import random
from ntbasic import *


class ElGamalKey:
    
    SMOOTH = 10**15     # bound for smooth numbers

    def __init__(self, p_, alpha_, a_, beta_):
        self.p, self.alpha, self.a, self.beta = p_, alpha_, a_, beta_

    def publicKey(self):
        return (self.p, self.alpha, self.beta)

    def privateKey(self):
        return self.a

    # generate a random key whose p in [rangep, ~2*rangep]
    # difficulty: 0 for random, 1 for easy, 2 for normal, 3 for difficult, 4 for crazy
    def randomKey(self, difficulty = 2, rangep = 0):
        if rangep==0:
            if difficulty==0:
                rangep = random.randint(10**10, 10**25)
            elif difficulty==1:
                rangep = 10**10
            elif difficulty==2:
                rangep = 10**15
            elif difficulty==3:
                rangep = 10**20
            else:
                rangep = 10**30
                
        # randomly choose a prime number as p
        self.p = random.randint(rangep, 2*rangep)
        if self.p%2==0:         # try odd numbers only
            self.p += 1
        cnt = 0
        while (True):
            self.p += 2
            cnt += 1
            if cnt>29 and cnt%30==0:
                print "Try to choose", self.p, ". Please be patient..."

            if millerRabin(self.p)==True:
                mydct = {}
                if (difficulty!=4):    # Just use smooth number for non-crazy case
                    mydct = factorDict(self.p-1)
                    if max(mydct.keys())>self.SMOOTH:
                        continue;
                self.alpha = findPrimitiveRoot(self.p, mydct)
                if (difficulty==1 or difficulty==2):
                    self.a = random.randint(1, self.p - 2)
                else:                                       # self.a is of the same order with self.p
                    self.a = random.randint(self.p/10, self.p*9/10)
                self.beta = powermod(self.alpha, self.a, self.p)
                return (self.p, self.alpha, self.a, self.beta)

        return (2579, 2, 765, 949) # this part should never be visited(though this is a valid key)


    # ElGamal Encryption
    def encrypt(self, x):
        r = random.randint(1, self.p - 2)
        y1 = powermod(self.alpha, r, self.p)
        y2 = x * powermod(self.beta, r, self.p) % self.p
        return (y1, y2)
    
    # ElGamal Decryption
    def decrypt(self, y):
        return y[1] * powermod(inverse(y[0], self.p), self.a) % self.p # y[1] * y[0]^(-a) (mod p)

    # used for debug
    def show(self):
        print "p, alpha, a, beta = ", self.p, self.alpha, self.a, self.beta







class ElGamalCracker:


    SMOOTH = 2 * 10**15

    """ Shanks Algorithm:
    alpha^x = alpha^(i*m + j) = beta
    <=> (alpha^m)^i = b*(alpha^(-1))^j
    i,j in {0, 1, ..., m-1}
    """
    # return x in {0, 1, ..., q-1} such that alpha^x = beta(mod p), return -1 if fails
    # by default, q = p-1, i.e. 0 <= x <= p-2
    # if we have more priori knowledge about the range of x(i.e. q << p), this routine will run much faster
    def shanks(self, p, alpha, beta, q=0):
        if q==0:
            q = p-1

        if q>self.SMOOTH:    # or we will get a memory error
            print "Alert: too looooooooooong ... Mission aborted."
            return -1

        m = long(math.ceil(math.sqrt(q)))
        invAlpha, tmp = inverse(alpha, p), beta #get invAlpha = alpha^(-1)
        dict1 = {}
        j = 0
        while (j<m):
            dict1[tmp] = j              # dict1[b*invAlpha^j] = j
            tmp = tmp*invAlpha%p
            j += 1

        #alpham = alpha^m
        alpham = powermod(alpha, m, p)
        tmp, i = 1, 0
        while (i<m):
            if dict1.has_key(tmp):      # tmp = alpham^i
                return i*m + dict1[tmp]
            tmp = tmp*alpham%p
            i += 1
            
        return -1;  #this part should never be visited


    # calculate the pseudo random sequence in Pollard-Rho Algorithm
    def next(self, xi, ai, bi, alpha, beta, p):
        c = xi % 3
        if c==1:
            return (beta*xi%p, ai, bi+1)
        elif c==2:
            mod = p-1
            return (xi*xi%p, 2*ai%mod, 2*bi%mod)
        else:
            return (alpha*xi%p, ai+1, bi)

    """Pollard-Rho Algorithm for Discrete Logarithm Problem"""
    # return x in {0, 1, ..., p-2} such that alpha^x = beta(mod p)
    # return -1 if failed
    def pollardrhoDLP(self, p, alpha, beta):

        res, mod = [], p-1
        cnt = 0
        while (res==[]):
            cnt += 1
            print "Pollard-Rho DLP Trial # ", cnt

            #random initialize
            a1, b1 = random.randint(1, p-2), random.randint(1, p-2)
            #print "alpha, beta, a1, b1 = ", alpha, beta, a1, b1
            x1 = powermod(alpha, a1, p) * powermod(beta, b1, p) % p
            x2, a2, b2 = self.next(x1, a1, b1, alpha, beta, p)
            
            while (True):
                #print "Pollard-Rho Debug: 1 ",x1,a1,b1
                #print "Pollard-Rho Debug: 2 ",x2,a2,b2
                if (x1==x2):
                    res = solvemod((b1-b2)%mod, (a2-a1)%mod, mod)
                    if res==[]:
                        print "May you good luck next time!"
                        break;
                    else:
                        for x in res:
                            if powermod(alpha, x, p)==beta:
                                print "Now you get discrete logarithm: ", x
                                return x

                        return -1 # this part should never be visited
                else:
                    x1, a1, b1 = self.next(x1, a1, b1, alpha, beta, p)
                    x2, a2, b2 = self.next(x2, a2, b2, alpha, beta, p)
                    x2, a2, b2 = self.next(x2, a2, b2, alpha, beta, p)

        return -1;  # this part should never be visited


    # return x in {0, 1, ..., q-1} such that alpha^x = beta(mod p)
    # return -1 if failed
    # use brute force search for sufficiently small q
    # use Shank's baby step giant step for large q
    # use Pollard-Rho Algorithm for larger q(this algorithm is to prevent memory error
    def search(self, p, alpha, beta, q):
        #print "p, alpha, beta, q = ", p, alpha, beta, q
        if q<300:
            #print "Searching using Brute Force Algorithm"
            xi = 1
            for i in xrange(q):
                if xi==beta:
                    return i
                xi = xi * alpha % p
        elif q<self.SMOOTH:
            #print "Searching using Shanks Algorithm"
            return self.shanks(p, alpha, beta, q)
        else:
            #print "Searching using Pollard-Rho Algorithm"
            return self.pollardrhoDLP(p, alpha, beta)
        return -1   # this should never happen

    """Pohlig-Hellman Algorithm for Discrete Logarithm Problem"""
    # return x in {0, 1, ..., p-2} such that alpha^x = beta(mod p)
    def pohligHellman(self, p, alpha, beta):
        factors = factorDict(p-1)
        xi, qe = [], []
        for q,e in factors.items():
            gamma, lj, qj, pqj = 1, 0, inverse(q, p), (p-1)/q
            xtmp, alpha_ = 0, powermod(alpha, pqj, p)
            for j in xrange(e):
                gamma = gamma * powermod(alpha, lj*qj, p) % p
                beta_ = powermod(beta*inverse(gamma, p), pqj, p)
                lj, qj, pqj = self.search(p, alpha_, beta_, q), qj*q%p, pqj/q;
                xtmp = (xtmp + lj*qj)%p
            xi.append(xtmp)
            qe.append(qj*q%p)
            #print (q, xi[-1], qe[-1])

        return CRT(xi, qe)
