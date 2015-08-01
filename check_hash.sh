#!/bin/bash

tar -c rsa.py key_gen.py prime_gen.py algorithm.py | gzip -n > rsa_implementation.tar.gz
md5 rsa_implementation.tar.gz
