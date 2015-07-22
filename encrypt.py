from __future__ import print_function
import os
import sys
import math
import prime_gen

def generate_PS(length):
    byte_str = ""
    counter = 0
    while counter < length:
        new_byte = os.urandom(1)
        if new_byte == '\0': continue

        byte_str += new_byte
        counter += 1

    return byte_str

# N must be a decimal power of 2
# use PKCS#1v1.5 encryption scheme to increase safety
def encrypt(N, e, filename):
    with open(filename, 'rb') as input_file:
        print(N)
        x = raw_input("N above")
        contents = input_file.read()
        file_len_bytes = len(contents)

        # k = |N| bytes
        # floor of math.log(n, 16) + 1 gives number of hex digits
        # number of hex digits / 2 gives number of bytes
        k = int(math.floor(math.log(float(N), 16)) + 1) / 2

        # D can be <= k - 11, but for simplicity we say D = k - 11
        D = k - 11

        # break the entire message up into chunks to encrypt
        # source:
        # http://stackoverflow.com/questions/6372228/how-to-parse-a-list-or-string-into-chucks-of-fixed-length
        data_array = [contents[i:i + D] for i in range(0, file_len_bytes, D)]
        encrypted_binary_stream = ''
        for m in data_array:
            m_len = len(m)
            PS_len = k - m_len - 3
            PS = generate_PS(PS_len)
            EB = '\0' + chr(2) + PS + '\0' + m
            bin_string = ''
            for c in EB:
                bin_string += bin(ord(c))[2:].zfill(8)

            m_integer = int(bin_string, base=2)
            c = pow(m_integer, e, N)
            print(hex(c)[2:])
            print(hex(N)[2:])

        
if __name__ == "__main__":
    N = int(sys.argv[1], base=16)
    print("N:", int(sys.argv[1], 16))
    e = int(sys.argv[2])
    print("e:", sys.argv[2])
    filename = sys.argv[3]
    print("filename:", sys.argv[3])
    encrypt(N, e, filename)
