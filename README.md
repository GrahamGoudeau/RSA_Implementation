# RSA Public-Key Cryptography Implementation
 An implementation of an RSA Public Key Cryptosystem as described [here](http://www.di-mgt.com.au/rsa_alg.html).  To generate primes and random filler bytes, the implementation takes advantage of `os.urandom`, which according to [the Python 2 documentation](https://docs.python.org/2/library/os.html#miscellaneous-functions) should be suitable for cryptographic applications.  In order to verify that a number is prime, `prime_gen.py` uses a [deterministic variant](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Deterministic_variants_of_the_test) of the Miller-Rabin primality test.

New RSA keys can be generated with the `-k` flag, along with the modulus size in bits:

    python rsa.py -k [modulus size in bits = 2^k]

where the modulus size is a power of 2 greater than 2^6.

An example key generation:
```
~/Documents/RSA_Implementation > python rsa.py -k 256
========================================
N = p*q (where p,q are each 128 bit-primes) and N is 256 bits:
ed6e5c6f3a6ba17c0df39421bca3753b0c347ac3f676a414bbf0ae523198d561
Encryption exponent (public):
10001
Decryption exponent (private):
3b4c84e982bdbee72cd4d8fa5412bf043530ee1f9b4582443848aadfa977d401
========================================
```
In this case N and the encryption exponent become the user's public key, and N and the decryption exponent become the user's private key.

With a key in hand, files can be encrypted and decrypted.  Say we have
