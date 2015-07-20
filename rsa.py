from __future__ import print_function
import os
import fractions
import sys
import key_gen

args = ['-k', '-e', '-d']

def printf(string):
	print(string, end="")

def print_usage():
	print ("Usage: [" + sys.argv[0] + "] [-option]")
	print ("[-k] [number of bits (0 mod 8) in p,q] : generate a new key triple of"
			"the form (N = pq, e [public], d [private])")
	print ("[-e] [stuff]")
	print ("[-d] [stuff]")

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
	elif sys.argv[1] == '-e':
		pass

if __name__ == "__main__":
	main()
