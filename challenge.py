import salsa20
#   import the distinguisher function and B and r paramaters from my_salsa
#   B: number of 64-byte blocks to generate
#   r: number of Salsa20 rounds
from my_salsa import distinguish, B, r
import os
from struct import pack, unpack

"""
    `distinguish` should take a list of `B` 64-byte ciphertext blocks as
    a parameter and return `0` if it determines the bytes are output of Salsa20
    or `1` if the bytes are random.
"""

def challenge_distinguisher():
    coin = ord(os.urandom(1)[0]) % 2
    ctxt_blocks = []
    if coin == 0:
        #print "THIS ACTUALLY IS A SALSA"
        #   salsa bytes
        sk = os.urandom(32)
        #   initialization vector (nonce)
        iv = 0
        for i in range(B):
            salsa = salsa20.Salsa20(sk, pack("<Q", iv), r)
            ctxt = salsa.encrypt('\x00'*64)
            ctxt_blocks.append(ctxt)
            iv += 1
    else:
        #print "NOT SALSA"
        #   random bytes
        for i in range(B):
            ctxt_blocks.append(os.urandom(64))
    if distinguish(ctxt_blocks) == coin:
        return True
    return False

if __name__ == "__main__":
    print "Testing distinguisher for " + str(B) + " blocks of " + str(r) + "-round Salsa"
    trials = 20
    correct = 0
    for i in range(trials):
        if challenge_distinguisher():
            correct += 1
    print "Number of correct guesses: " + str(correct) + " out of " + str(trials)