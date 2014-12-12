Course Project for Introduction to Information Security
==========================================================

Author: Soloice, 12/12/2014

This project aims to focus on ElGamal Encryption System.
- We are able to simulate both encryption and decryption procedure with given or randomly generated keys.
- In addition, we implemented 3 kinds of crack methods, which are:
    - Shanks' baby-step-giant-step Algorithm
    - Pollard-Rho Algorithm
    - Pohlig-Hellman Algorithm

Here are some instructions for all program files:
- ntbasic.py: Basic functions for Number Theory, such as Miller-Rabin Primality Test.
- elgamal.py: Implements of ElGamal encryption and decryption, and ElGamal key cracker(Discrete Logarithm Problem Solver).
- demo.py: You may want to run this file to make out all things we can do.
- leveltest.py: Test file for crack algorithms for different difficulty level.
- cracktest.py: This file contains a timer to record the performance of 3 crack methods implemented.


Note: all codes are written in Python.

Run as:
- python demo.py
- python leveltest.py
- python cracktest.py
