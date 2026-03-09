# RSA from scratch - no libraries

def start():
    # choosing two large prime numbers 
   p=int(input("Enter p : "))
   q=int(input ("Enter q : "))
   n= p*q

   phi= (p-1)*(q-1)
   e=encryption_exponent(phi)
   d=decryption_exponent(e,phi) 
   return n,e,d
 

def gcd(e,phi):
    
    while phi!=0:
        r=e%phi
        e=phi
        phi=r    
    return e
 
 
def encryption_exponent(phi):

# Choose encryption exponent e, such that
# 1 < e < Φ(n), and
# gcd(e, Φ(n)) = 1, that is e should be co-prime with Φ(n).
# GCD = 1 is only possible when the numbers are different and coprime.

#  0 and 1 is useless for RSA 

 e=2
 while (True): 
     if gcd(e,phi)==1:
         return e              
     else:
        e=e+1
 

def decryption_exponent(e,phi):    
    # finding a number d such that (exd) mod phi = 1
     d=2  
     while (True):
      if (e*d)%phi==1:  
          return d
      else:
          d=d+1
    
    
def encrypt_message(e,n,M):
    #  cipher=M**e%n too computation heavy
     cipher=pow(M,e,n)
     return cipher
        

def decrypt_message(d,n,C):
    # decipher=C**d%n too computation heavy
    decipher=pow(C,d,n)
    return decipher

n,e,d=start()

message=input("Enter the message for encryption : ")

# M must satisfy M < n for RSA to work properly.
#  So taking the larger prime numbers

cipher_list=[]
decipher_list=[]

for char in message:
    M=ord(char)
    C=encrypt_message(e,n,M)
    cipher_list.append(C)

for char in cipher_list:
    D=decrypt_message(d,n,char)
    decipher_list.append(chr(D))


decipher="".join(decipher_list)
print(decipher)