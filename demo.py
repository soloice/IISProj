from ntbasic import *
from elgamal import *


# some test data

ckr = ElGamalCracker()
print "Shanks", ckr.shanks(809, 3, 525)   #this should be 309
print "Pollard-Rho", ckr.pollardrhoDLP(809, 3, 525)   #this should be 309
print "Pohlig-Hellman", ckr.pollardrhoDLP(809, 3, 525)   #this should be 309

print "Shanks", ckr.shanks(383, 5, 228)   #this should be 224
print "Pollard-Rho", ckr.pollardrhoDLP(383, 5, 228)   #this should be 224
print "Pohlig-Hellman", ckr.pollardrhoDLP(383, 5, 228)   #this should be 224

print "Shanks", ckr.shanks(251, 71, 210)   #this should be 197
print "Pollard-Rho", ckr.pollardrhoDLP(251, 71, 210)   #this should be 197
print "Pohlig-Hellman", ckr.pohligHellman(251, 71, 210)   #this should be 197


n = 22708823198678103974314518195029102158525052496759285596453269189798311427475159776411276642277139650833937
print factorDict(n-1)   # n-1 = 2**4 * 104729**8 * 224737**8 * 350377**4
alpha = findPrimitiveRoot(n)

for i in xrange(3):
    # Note: the calculation may take a few seconds
    beta = random.randint(1, n-2)
    print "Beta = ", beta
    x = ckr.pohligHellman(n, alpha, beta)
    print "Pohlig-Hellman", x
    print "Beta'= ", powermod(alpha, x, n), "\n" #this should be beta



key = ElGamalKey(2579, 2, 765, 949)  #generatea a new key
key.show()


# repeat 5 times
for i in xrange(5):
    plain = input("please input plaintext x(x<2579):")
    #repeat 5 times
    for j in xrange(5):
        cipher = key.encrypt(plain)
        deciphered = key.decrypt(cipher)
        print "plaintext, cipher, deciphered = ", plain, cipher, deciphered


key = ElGamalKey(1196545829632411, 2, 931336951895464, 112946787244369)
print factorDict(key.p-1)
print "Pohlig-Hellman Test: ", ckr.pohligHellman(key.p, key.alpha, key.beta)

alpha1, beta1, q = 1014219278917711, 658574069871474, 1250191549;
# x should be 506510169
x = ckr.shanks(key.p, alpha1, beta1, q)    
print "Shanks Test: ", x, powermod(alpha1, x, key.p)


# x might be 504956623725916, 334099195681831, 691940272560552, ..., or something else
# because alpha1 is not a generator(i.e. primative root) of group Z_{key.p}
# If we try to run this routine several times, the result may vary from each other.
# Some times Pollard-Rho Algorithm might fail, but it is rather rare.

for i in xrange(15):
    x = ckr.pollardrhoDLP(key.p, alpha1, beta1)
    print "Pollard-Rho DLP Test: ", x, powermod(alpha1, x, key.p)