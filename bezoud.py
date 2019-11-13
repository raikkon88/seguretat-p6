import random
from utils import generateRandomValue
from utils import getNumber

def bezoud(a, b):
# a i b > 0
# retorna per aquest ordre : 
#   mcd(a,b)
#   a que ens han passat com entrada
#   b que ens han passat com entrada
#   Q Pot ser negatiu
#   P Pot ser negatiu
    ina = a
    inb = b
    qant = 0
    pant = 1
    qact = 1
    pact = 0
    iteration = 0

    while(a % b != 0):
        quo = a // b
        qtmp = quo * qact + qant
        ptmp = quo * pact + pant
        qant = qact
        pant = pact 
        qact = qtmp
        pact = ptmp

        tmp = b
        b = a % b 
        a = tmp
        iteration += 1

    if(iteration % 2 == 0): 
        pact *= -1
    else: 
        qact *= -1

    return b, ina, inb, qact, pact