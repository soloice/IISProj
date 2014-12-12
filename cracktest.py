from ntbasic import *
from elgamal import *
from time import *


key = ElGamalKey(2579, 2, 765, 949)  #generatea a new key
key.show()
ckr = ElGamalCracker()

timephList, timeshList, timeprList = [], [], []
NUMBER_OF_TEST_CASES, DIFFICULTY = 20, 3
levels = map(lambda x:10**x, range(10, 15))

for level in levels:
    print "Level: 10 **", len(str(level))-1
    timeph, timesh, timepr = 0.0, 0.0, 0.0
    for i in xrange(NUMBER_OF_TEST_CASES):
        key.randomKey(DIFFICULTY, level)    # Here DIFFICULTY only controls smoothness
        print "Public key: ", key.publicKey()
        print factorDict(key.p-1)
        t1 = time()
        print "Calculated private key(Pohlig-Hellman): ", ckr.pohligHellman(key.p, key.alpha, key.beta)
        t2 = time()
        print "Calculated private key(Shanks): ", ckr.shanks(key.p, key.alpha, key.beta)
        t3 = time()
        print "Calculated private key(Pollard-Rho): ", ckr.pollardrhoDLP(key.p, key.alpha, key.beta)
        t4 = time()
        print "Actual private key: ", key.privateKey(), "\n"
        timeph += t2 - t1
        timesh += t3 - t2
        timepr += t4 - t3

    timephList.append(timeph/NUMBER_OF_TEST_CASES)
    timeshList.append(timesh/NUMBER_OF_TEST_CASES)
    timeprList.append(timepr/NUMBER_OF_TEST_CASES)

# write the performance of all crack algorithms into "time.csv"
myfile = open("time.csv", "w")
myfile.write("Level, Pohlig-Hellman, Shanks, Pollard-Rho\n")
for i in range(len(levels)):
    myfile.write(','.join(map(str, [levels[i], timephList[i], timeshList[i], timeprList[i]])) + '\n')
