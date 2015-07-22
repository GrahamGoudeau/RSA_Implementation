from __future__ import print_function
import os
import fractions
import sys
import key_gen
import encrypt
import math

args = ['-k', '-e', '-d']

def printf(string):
    print(string, end="")

def print_usage():
    print ("Usage: [" + sys.argv[0] + "] [-option]")
    print ("[-k] [# bits in the modulus N (power of two)] : generate a key of "
            "the form (N = pq, e [public], d [private])")
    print ("[-e] [filename] [N = pq] [e (public)]")
    print ("[-d] [stuff]")

def print_key(N, e, d, bit_len):
    print("\n", end="")
    print("="*40)
    print("N = p*q (where p,q are each " + str(bit_len / 2) + " bit-" +
        "primes) and N is " + str(bit_len) + " bits: ")
    # convert X into its hex form, take away the 0x and 'L' character at the end
    N_str = str(hex(N))[2:]
    if N_str[-1:] == 'L':
        N_str = N_str[:-1]
    print(N_str)
    print("Encryption exponent (public): ")
    print(str(hex(e))[2:])
    print("Decryption exponent (private): ")
    d_str = str(hex(d))[2:]
    if d_str[-1:] == 'L':
        d_str = d_str[:-1]
    print(d_str)
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

def is_power_of_two(n):
    # n is of the form 10000...0 and n-1 is of the form 1111...1
    return (n & (n - 1) == 0) and (n != 0)

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in args:
        print_usage()

    elif sys.argv[1] == '-k':
        if len(sys.argv) != 3:
            print_usage()
        elif not is_power_of_two(int(sys.argv[2])) or int(sys.argv[2]) < pow(2,7):
            print("Modulus bit length must be power of two, 2^k with k > 6")
        else:
            bit_len = int(sys.argv[2])
            # bit_len / (# bits in a byte * 2 (each key half the total length))
            N, e, d = key_gen.key_gen(bit_len / 16)
            print_key(N, e, d, bit_len)
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
