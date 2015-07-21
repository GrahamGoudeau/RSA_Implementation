from __future__ import print_function
import os
import fractions
import sys
import key_gen
import math

args = ['-k', '-e', '-d']

def printf(string):
    print(string, end="")

def print_usage():
    print ("Usage: [" + sys.argv[0] + "] [-option]")
    print ("[-k] [number of bits (0 mod 8) in p,q] : generate a new key triple of"
            "the form (N = pq, e [public], d [private])")
    print ("[-e] [filename] [N = pq] [e (public)]")
    print ("[-d] [stuff]")

def print_key(N, e, d):
    print("\n", end="")
    print("="*40)
    print("N = p*q (where p,q are each " + str(bit_len) + " bit-" +
        "primes): ")
    print(str(N))
    print("Encryption exponent (public): ")
    print(str(e))
    print("Decryption exponent (private): ")
    print(str(d))
    print("="*40)

def encrypt(filename, N, e):
    with open(filename, 'rb') as f:
        contents = f.read()
        length = len(contents)

        # reserve two leftmost bits to ensure m < N
        bits_take_amount = math.log(float(N), 2) - 2
        # pad to a multiple of the number of bytes we take each time
        add = 0
        while (length + add) % bits_take_amount != 0:
            contents += ('\0')
            add += 1

        length += add
        # get the raw bits of the content
        content_bits = ""
        for i in xrange(length):
            content_bits += bin(ord(contents[i]))[2:].zfill(8)

        # if N=2^k, we encrypt every k-2 bits
        counter = 0
        output = ''
        bit_string = ''
        content_bits_length = len(content_bits)
        for i in xrange(content_bits_length):
            bit_string += content_bits[i]
            counter += 1
            if counter == bits_take_amount:
                m = int('00' + bit_string, base=2)
                counter = 0
                bit_string = ''
                output += bin(pow(m, e, N))[2:]

        output_len = len(output)
        counter = 0
        output_byte = ''
        for i in xrange(output_len):
            output_byte += output[i]
            counter += 1
            # if the counter is at the end of a byte:
            if counter == 7:
                # print the actual encrypted byte
                print(chr(int(output_byte, base=2)), end="")
                output_byte = ''
                counter = 0

def get_raw_bits(f):
    contents = f.read()
    contents_length = len(contents)

    for i in xrange(len(contents)): pass

def true_encrypt(filename):
    with open(filename, 'rb') as f:
        contents = f.read()
        for byte in contents:
            print(chr((ord(byte) + 1) % 256), end="")

def decrypt(filename):
    with open(filename, 'rb') as f:
        contents = f.read()
        for byte in contents:
            val = (ord(byte) - 1) % 256
            print(chr(val), end="")

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in args:
        print_usage()

    elif sys.argv[1] == '-k':
        if len(sys.argv) != 3:
            print_usage()
        elif int(sys.argv[2]) % 8 != 0:
            print("Prime bit length must be 0 (mod 8)")
        else:
            bit_len = int(sys.argv[2])
            N, e, d = key_gen.key_gen(bit_len / 8)
            print_key(N, e, d)
    elif sys.argv[1] == '-e':
        if len(sys.argv) != 5:
            print_usage()
        else:
            #encrypt(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
            true_encrypt(sys.argv[2])
    elif sys.argv[1] == '-d':
        if len(sys.argv) != 5:
            print_usage()
        else:
            decrypt(sys.argv[2])
    else: pass

if __name__ == "__main__":
    main()
