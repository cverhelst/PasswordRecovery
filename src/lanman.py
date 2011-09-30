#!/usr/bin/python

# Lanman hash implementation in python using the pycrypto module
# (c) 2011 Richard Moore, rich@sectools.co.uk

import sys
from Crypto.Cipher import DES

lm_constant = 'KGS!@#$%'

def halfHash(half):
    key = [0]*8
   
    key[0] = ord(half[0]) >> 1
    key[1] = (ord(half[0]) & 0x01) << 6 | ord(half[1]) >> 2	
    key[2] = (ord(half[1]) & 0x03) << 5 | ord(half[2]) >> 3
    key[3] = (ord(half[2]) & 0x07) << 4 | ord(half[3]) >> 4
    key[4] = (ord(half[3]) & 0x0f) << 3 | ord(half[4]) >> 5
    key[5] = (ord(half[4]) & 0x1f) << 2 | ord(half[5]) >> 6
    key[6] = (ord(half[5]) & 0x3f) << 1 | ord(half[6]) >> 7
    key[7] = ord(half[6]) & 0x7f
    expanded_key = ''.join([chr(k << 1) for k in key])

    half_des = DES.new(expanded_key, DES.MODE_ECB)
    half_hash = half_des.encrypt(lm_constant)

    return half_hash.encode('hex')

def lmhash(password):
    password = password.upper()

    if len(password) < 14:
        password += '\0' * (14-len(password))

    left = password[:7]
    right = password[7:]

    return halfHash(left) + halfHash(right)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s password' % (sys.argv[0])
        sys.exit(0)

        print repr(sys.argv)
    print lmhash(sys.argv[1])
