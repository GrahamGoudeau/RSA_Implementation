import os
import fractions
import sys
import prime_gen

exponent_choices = [3, 5, 17, 257, 65537]

# source: http://pages.pacificcoast.net/~cazelais/222/xeuclid.pdf
def xgcd(a,b):
	if b == 0:
		return [1,0,a]
	else:
		x,y,d = xgcd(b, a%b)
		return [y, x - (a//b)*y, d]

# returns (N - the modulus, e - public exponent, d - secret exponent)
def key_gen(byte_len):
	print "Generating " + str(byte_len * 8) + "-bit primes"
	p = prime_gen.prime_gen(byte_len)
	q = prime_gen.prime_gen(byte_len)

	N = p * q
	L = (p - 1) * (q - 1)

	while True:
		exponent_choice = ord(os.urandom(1)) % len(exponent_choices)
		e = exponent_choices[exponent_choice]
		if fractions.gcd(e, L) == 1: break

	x, _, _ = xgcd(e, L)
	d = x % L

	return (N, e, d)
