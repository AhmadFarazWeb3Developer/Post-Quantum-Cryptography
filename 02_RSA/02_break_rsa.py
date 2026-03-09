#  For breaking RSA we know the public key (e,n) and cipher 
# for decrypting of cipher the attacker need d
# for e * d mod phi = 1
# for finding the d the attacker need phi
# for phi the attacker need p and q


n=143  # dividend
e=7
cipher=48

# n=p*q


def find_factors():
    
    for i in range(2,int(n**0.5)+1): # one factor must be ≤ √n.
        if n%i==0:
            p=i # divisor
            q= n//i # quotent
            break
    
    return p,q 


def find_d():
    d=2
    while(True):        
        if (e*d) % phi== 1:
            return d
        else:
            d=d+1
    

def decrypt(d,n,C):
   return pow(C,d,n)
    
    
p,q=find_factors()


phi= (p-1)* (q-1)

d=find_d()

decipher=decrypt(d,n,cipher)

print(decipher) #9
 




