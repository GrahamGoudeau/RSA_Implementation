import math
import os
import sys
import fractions

OPT_KEY_LEN_BITS = 128
OPT_KEY_LEN_BYTES = OPT_KEY_LEN_BITS / 8

# generate a number representable in 'byte_len' number of bytes
def number_gen(byte_len):
	byte_arr = os.urandom(byte_len)
	bit_string = ""
	for byte in byte_arr:
		# convert ascii value to binary, pad out to 8 bits
		bit_string += (bin(ord(byte))[2:].zfill(8))

	# set top two bits and lowest bit to '1'
	# eventually we want n = pq to have its highest bit as '1'
	bit_string = '11' + bit_string[2:]
	bit_string = bit_string[:-1] + '1'

	return int(bit_string, base=2)

def factor_powers_2(n):
	powers = 0
	while n % 2 == 0:
		n = n / 2
		powers += 1

	return powers

# use Miller-Rabin primality test to determine if prime
# algorithm source: en.wikipedia.org/wiki/Miller-Rabin_primality_test#Deterministic_variants_of_the_test
def is_prime(p):
	pred = p - 1
	s = factor_powers_2(pred)
	d = pred / (2 ** s)

	witness_set = range(2, int(min(pred, math.floor((2 * math.log(p)) ** 2)) + 1))

	for a in witness_set:
		if pow(a, d, p) != 1:
			got_condition = True
			for r in range(0, s):
				if pow(a, pow(2,r) * d, p) == pred: got_condition = False

			if got_condition:
				return False

	return True

# takes length in bytes of prime to be generated
def prime_gen(byte_len):
	p = number_gen(byte_len)

	while not is_prime(p): 
		p += 2

	return p

if __name__ == "__main__":
	for index,i in enumerate(sys.argv):
		if index == 0: continue
		sys.argv[index] = int(i)

	p = prime_gen(OPT_KEY_LEN_BYTES)
	q = prime_gen(sys.argv[1])
	print "confirmed prime: " + str(p)	
