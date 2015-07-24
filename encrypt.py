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
        N_bin_len = len(bin(N)[2:])
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
        #encrypted_binary_stream_len = 0
        for m in data_array:
            m_len = len(m)
            PS_len = k - m_len - 3

            # get the random filler content
            PS = generate_PS(PS_len)

            # build the actual chunk to be encrypted
            EB = '\0' + chr(2) + PS + '\0' + m
            bin_string = ''
            for EB_byte in EB:
                # add each byte of EB to the binary string
                new_bits = bin(ord(EB_byte))[2:].zfill(8)
                bin_string += new_bits
                # isn't this always 8?
                #encrypted_binary_stream_len += len(new_bits)

            m_integer = int(bin_string, base=2)
            c = pow(m_integer, e, N)
            encrypted_binary_stream += bin(c)[2:].zfill(N_bin_len)

        encrypted_binary_stream_len = len(encrypted_binary_stream)
        output_bytes = [encrypted_binary_stream[i:i + 8] for i in range(0, encrypted_binary_stream_len, 8)]
        for byte in output_bytes:
            print(chr(int(byte, base=2)), end="")

def print_valid_bytes(m, N_bin_len):
    m_bin = bin(m)[2:].zfill(N_bin_len)

    m_bytes = [m_bin[i:i + 8] for i in range(0, N_bin_len, 8)]
    if not int(m_bytes[0], base=2) == 0 or not int(m_bytes[1], base=2) == 2:
        raise ValueError("MALFORMED BLOCK - MUST CONFORM TO PKCS#1 v1.5 ENCODING SCHEME")

    # PKCS scheme: 0x00 | 0x02 | [random nonzero bytes] | 0x00 | data
    zero_blocks_seen = 0
    for byte in m_bytes:
        # if we have seen both the indicated zero blocks
        if zero_blocks_seen >= 2:
            print(chr(int(byte, base=2)), end="")

        if int(byte) == 0:
            zero_blocks_seen += 1


def decrypt(N, d, filename):
    with open(filename, 'rb') as input_file:
        N_bin_len = len(bin(N)[2:])
        contents = input_file.read()
        file_len_bytes = len(contents)

        # k = |N| bytes
        k = int(math.floor(math.log(float(N), 16)) + 1) / 2

        # break the data into k sized blocks to be decrypted
        data_array = [contents[i:i + k] for i in range(0, file_len_bytes, k)]
        int_data_array = []
        for block in data_array:
            binary_string = ''
            for byte in block:
                binary_string += bin(ord(byte))[2:].zfill(8)

            int_data_array.append(int(binary_string, base=2))

        #print(int_data_array)
        # decrypt each integer in the int data array
        for index,block in enumerate(int_data_array):
            m = pow(block, d, N)
            #print(bin(m)[2:].zfill(N_bin_len))
            print_valid_bytes(m, N_bin_len)

if __name__ == "__main__":
    #print("N, e/d, filename, option")
    N = int(sys.argv[1], base=16)
    #print("N:", int(sys.argv[1], 16))
    e = int(sys.argv[2], base=16)
    #print("e:", sys.argv[2])
    filename = sys.argv[3]
    #print("filename:", sys.argv[3])
    if sys.argv[4] == '-e': encrypt(N, e, filename)
    if sys.argv[4] == '-d': decrypt(N, e, filename)
