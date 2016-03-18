import salsa20
import os
from struct import pack
import math
import numpy as np

#   number of ciphertext blocks
B = 655536
ctxt_blocks = []
#   cryptographically-secure random 32-byte key
k = os.urandom(32)
#   initialization vector (nonce)
iv = 0
#   number of rounds
r = 4

# Some constants
N = 2**8
E = (B/N)

def distinguish(ctxt_blocks):
    # We only look at the 0th byte value (we could look at any from 0 to 64, but that's overkill)
    indexArrays = []
    for x in range(len(ctxt_blocks[0])):
    	indexArrays.append([])

    for i in range(len(ctxt_blocks)):
    	for j in range(len(ctxt_blocks[0])):
        	indexArrays[j].append(ctxt_blocks[i][j])

    salsaCount = 0
    rightArrays = []    
    selectArrays = []
    #for idx in [2, 4, 9, 12, 13, 16, 17, 18, 19, 20, 21, 22, 27, 30, 31, 34, 35, 38, 40, 42, 46, 48, 53, 54, 55, 56, 57]:
    #	selectArrays.append(indexArrays[idx])
    for idx, i_zero in enumerate(indexArrays):
	    # count the occurence of every specific byte value of 0 to 256
	    O = [0]*256
	    for i in i_zero:
	        index = ord(i)
	        O[index] += 1

	    chi_squared = 0
	    for O_i in O:
	        chi_squared += float((float(E)-float(O_i))**2.0/float(E))

	    std_dev = math.sqrt(2*(N-1))
	    thresholdHIGH = (N-1) + 3*std_dev
	    thresholdLOW = (N-1) - 3*std_dev

	    if chi_squared > thresholdHIGH or chi_squared < thresholdLOW:
	    	salsaCount += 1
	        rightArrays.append(idx)

    print "salsa count" + str(salsaCount)
    if salsaCount > 1: # too many false positives if > 0
    	return 0
    return 1