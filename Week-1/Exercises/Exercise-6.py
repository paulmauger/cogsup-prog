"""
Write a script that lists all the prime numbers between 1 and 10000.
(A prime number is an integer greater or equal to 2 which has no divisors except 1 and itself). 
Hint: Write an is_factor helper function.
"""

from math import isqrt

#Implentation of the Sieve of Eratosthenes
def crible(n):
    
    n+=1 #because otherwise range(n) doesn't reach n
    
    list_primes = [True for _ in range(0, n)]
    list_primes[0] = False
    list_primes[1] = False 

    limit = isqrt(n)
    for idNum in range(2, limit):
        for j in range(idNum*idNum, n, idNum):
            list_primes[j] = False
    
    return [i for i, b in enumerate(list_primes) if b]


print(crible(10000))