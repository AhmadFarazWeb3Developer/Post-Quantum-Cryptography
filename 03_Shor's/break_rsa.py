import math

n = 15
a = 2




def find_period():
 x=1
 while True:
    print(f"{a}^{x} mod {n} = {a**x % n}")
    if  a**x % n ==1:
     return x
    x=x+1
    
def find_midpoint(r,n):
    mid_point=pow(a,r//2,n)
    return mid_point


r=find_period()

print("period : ",r)

if r % 2 != 0:
    print("r is odd — change a and retry")
else:
    print("r is even — we can continue")
     
 
mid_point=find_midpoint(r,n)     



print(mid_point)
    


#  whats the game of GCD now ?

factor1 = math.gcd(mid_point - 1, n)
factor2 = math.gcd(mid_point + 1, n)

print("factor1 = ", factor1)
print("factor2 = ", factor2)

