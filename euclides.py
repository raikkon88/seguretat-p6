import random
from utils import generateRandomValue
from utils import getNumber


digits = 500000

def sonCoprimers(a,b):
# a i b > 0
# Retorna cert si a i b son coprimers
    return euclides(a, b) == 1

def euclides(a, b):
# a i b > 0
# Retorna el MCD(a, b)
    while(a % b != 0):
        tmp = b
        b = a % b 
        a = tmp

    return b

def euclides_test():
    print("algoritme d'euclides")
    print("--------------------")
    print("Entra si vols que s'autogenerin els numeros o si prefereixes entrar-los tu.")
    print("- 0 -> Generats amb un nombre aleatori de 1 a " + str(digits) + " digits")
    print("- 1 -> A manija")
    option = getNumber("Escull una opcio : ")
    a = 0
    b = 0
    if(option == 0): 
        a = generateRandomValue(random.randint(1, digits))
        b = generateRandomValue(random.randint(1, digits))
    else:    
        a = getNumber("enter the first number: ")
        b = getNumber("enter the second number: ")

    print("Els nombres que s'utilitzen son : ")
    print("")
    print(a)
    print("")
    print(b)
    print("")
    print("Calculem el MCD ...")
    print("")
    # Considerem a com a divident i b com a divisor
    while(a % b != 0):
        tmp = b
        b = a % b 
        a = tmp

    
    print("El maxim comu divisor es el " + str(b))
    