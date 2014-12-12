from ntbasic import *
from elgamal import *


key = ElGamalKey(2579, 2, 765, 949)  #generatea a new key
key.show()
print "Smooth bound:", key.SMOOTH
ckr = ElGamalCracker()


level = "Random Easy Normal Difficult Crazy".split()
for d in xrange(5):
    print "Level:", level[d]
    for i in xrange(3):
        key.randomKey(d)
        key.show()
        print factorDict(key.p-1)
        print "Calculated private key(Pohlig-Hellman): ", ckr.pohligHellman(key.p, key.alpha, key.beta)
        print "Actual private key: ", key.privateKey(), "\n"
    print "\n"
