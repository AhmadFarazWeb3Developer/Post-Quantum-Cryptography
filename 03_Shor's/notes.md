# Classic Simulation of Shor's Algorithm

## Real Shor's

- Pick a random number $a$
- Check $GCD$
- Quantum Fourier Transformation find periods
- Extract periods from factors
- Done in polynomial times

## Simulation

- Pick a random number $a$
- Check $GCD$
- Finds period step by step
- Extract periods from factors
- Done slowly but correctly

## Working

1. Finding the period by the modular exponentiation formula
   ${a^x} \ mod \ n = 1$
   $a$ is any random number good to start from $2$.
   $x$ is loop integer starting from $1$

2. Once the period found check whether it is $even$ or $odd$. $Odd$ is not usable for $GCD$. Update the $a$ if $odd$.

3. Now find the mid point, it finds the mathematical mid point of the cycle
   $mid-point = a^{x/2} \ mod \ n $
   It will give us the number
