# Calculating GCD


a = 48
b = 12


list1=[i for i in range(1,a+1) if a%i==0]
list2=[i for i in range (1,b+1) if b%i==0]


common_factors = [i for i in list1 if i in list2  ]



print(common_factors)


print(max(common_factors))
           
           
