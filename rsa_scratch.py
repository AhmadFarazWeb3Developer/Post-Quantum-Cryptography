# RSA from scratch - no libraries

def start():
    # choosing two large prime numbers 
   p=10007
   q=10009
   n= p*q

   phi= (p-1)*(q-1)
   e=encryption_exponent(phi)
   d=decryption_exponent(e,phi)


   print("e : ",e)
   print("d : ",d)
   
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
     cipher=M**e%n
     return cipher
        

def decrypt_message(d,n,C):
    decipher=C**d%n
    return decipher

n,e,d=start()



# message=input("Enter the message for encryption : ")
M=123


# M=int.from_bytes(message.encode(),'big')




# M must satisfy M < n for RSA to work properly.
#  So taking the larger prime numbers

cipher=encrypt_message(e,n,M)
print("cipher",cipher)

decipher=decrypt_message(d,n,cipher)
# deC=decipher.to_bytes((decipher.bit_length()+7)//8,'big').decode()

print("decipher ",decipher)
