import utils
import sys
import os
# import random
from Crypto.Random import get_random_bytes
from euclides import sonCoprimers
from modular import invers_modular

sys.setrecursionlimit(5000)


def loop(b, function, byteNumber):
    a = int.from_bytes(get_random_bytes(byteNumber), 'big')
    while not function(a,b): 
        a = int.from_bytes(get_random_bytes(byteNumber), 'big')
    return a


def getSecurePrime(byteNumber):
# a > 0
# retorna el primer nombre primer a partir de a
# El nombre d'iteracions per comprovar fermat és de 10, per tant fa 10 operacions peró es mira els primers 2,3,5,7.
    return loop(10, utils.fermat, byteNumber)

def getSecureEuler(byteNumber, euler):
# a > 0
# retorna el valor per un exponent de mida byteNumber coprimer amb euler
    return loop(euler, sonCoprimers, byteNumber)

def getKeys(randomLength):
    # TODO : S'ha de mirar que els factors primers de p i q siguin grans (no haurien de ser 3, 5 ,7)
    p = getSecurePrime(randomLength)
    q = getSecurePrime(randomLength + 1)

    print("Pas 1 -> Generem dos nombres aleatoris grans i similars en nombre de bits pero que difereixin, (que no siguin propers) :")
    print("p = " + str(p))
    print("q = " + str(q))
    print()

    print("Pas 2 -> Calculem n, on n=p*q :")
    n = p*q
    print("n = " + str(n))
    print()

    print("Pas 3 -> Claculem Euler(n) : ")
    euler = (p-1)*(q-1)
    print("euler = " + str(euler))
    print()

    print("Pas 4 -> Cerquem un e € Naturals i coprimer amb euler(n):")
    e = getSecureEuler(32, euler)
    print("e = " + str(e))
    print()

    print("Pas 5 -> Cerquem una d € Naturals i e*d (mod euler(n)) == 1 (mod euler(n))" )
    d = invers_modular(e, euler)
    print("d = " + str(d))
    print()
    print()

    kpb = [n,e]
    kpr = [n,d]

    return kpb, kpr

def breakKeys(N):
# N > 0. 
# Retorna p i q, els factors primers de N. 
    return utils.factors_primers(N)