# RSA Public-Key Cryptosystem
 An implementation of an RSA Public Key Cryptosystem as described [here](http://www.di-mgt.com.au/rsa_alg.html).  To generate primes and random filler bytes, the implementation takes advantage of `os.urandom`, which according to [the Python 2 documentation](https://docs.python.org/2/library/os.html#miscellaneous-functions) should be suitable for cryptographic applications.  In order to verify that a number is prime, `prime_gen.py` uses a [deterministic variant](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Deterministic_variants_of_the_test) of the Miller-Rabin primality test.

### Key generation
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

### Encryption
Say we have some sensitive data in a file called `secret_battle_plans.txt`.  Using the key we just generated, we can encrypt our secret data with the `-e` flag.  The accepted argument order is

    [rsa.py] -e [N (modulus)] [e (public exponent)] [filename to be encrypted]

where `N` and `e` must both be in hex format.  Encrypted bytes will be printed to `stdout`.  The plaintext is encoded using [PKCS #1 v1.5](https://tools.ietf.org/html/rfc2437#section-9) before applying the RSA algorithm to it.

A concrete example, using the key we generated above:
```
~/Documents/RSA_Implementation > python rsa.py -e ed6e5c6f3a6ba17c0df39421bca3753b0c347ac3f676a414bbf0ae523198d561 10001 secret_battle_plans.txt > encrypted_battle_plans.txt
```

### Decryption
Similarly to encryption, we can decrypt a file containing encrypted bytes with the `-d` flag and the following arguments:
```
[rsa.py] -d [N (modulus)] [d (private exponent)] [filename to be decrypted]
```
where again `N` and `d` are in hex format, and decrypted bytes are sent to `stdout`.  The decrypted bytes are expected to conform to PKCS #1 v1.5 as linked to above.

To decrypt our sensitive data, we use the modulus and private exponent generated earlier:
```
~/Documents/RSA_Implementation > python rsa.py -d ed6e5c6f3a6ba17c0df39421bca3753b0c347ac3f676a414bbf0ae523198d561 3b4c84e982bdbee72cd4d8fa5412bf043530ee1f9b4582443848aadfa977d401 encrypted_battle_plans.txt > unencrypted_battle_plans.txt
```

