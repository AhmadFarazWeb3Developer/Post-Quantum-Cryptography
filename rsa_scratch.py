# RSA from scratch - no libraries

p = 17
q = 19

n = p*q


# Choose encryption exponent e, such that
# 1 < e < Φ(n), and
# gcd(e, Φ(n)) = 1, that is e should be co-prime with Φ(n).
# GCD = 1 is only possible when the numbers are different and coprime.

e = 11 
phi= (p-1)*(q-1)




#  gcd(e, phi) == 1



# Calculate decryption exponent d, such that

d = e**-1 % Φ_n


public_key = (n, e)
private_key=(n,d)


message="This is message"


# C = M**e mod n, where C is the Cipher text and e and n are parts of public key.

cipher = message**e % n,

# M = C**d mod n, where M is the message and d and n are parts of private key.
decrypted_message = cipher**d % n 

