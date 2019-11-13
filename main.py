from keygen import getKeys
from utils import factors_primers
from utils import readFileAsString
from modular import potencia_modular_eficient
import sys

# Per simplicitat i per no perdre temps en canviar el nom del fitxer.
DECODED_FILE = "desxifrat.txt"
ENCODED_FILE = "xifrat.txt"

def encode(string, e, n):
# string és el text per xifrar, e és exponent, b és mòdul
# int(bytes(string)) < n
# Retorna string codificat en bytes
    m = int.from_bytes(string.encode('utf-8'), byteorder='big')
    if(m > n): 
        raise Exception("Invalid string length. Must be smaller")
    enter = potencia_modular_eficient(m, e, n)
    encoded = enter.to_bytes((enter.bit_length() + 7) // 8, 'big')
    return encoded

def decode(decbytes, d, n):
# bytes és el text en decbytes per desxifrar, d és exponent, b és mòdul
# int(bytes) < n
# Retorna decbytes descodificat amb d com string
    toDecode = int.from_bytes(decbytes, byteorder='big')
    if(toDecode > n): 
        raise Exception("Invalid string length. Must be smaller")
    decodedInt = potencia_modular_eficient(toDecode, d, nr)
    decoded = str(decodedInt.to_bytes((decodedInt.bit_length() + 7) // 8, 'big'), 'utf-8')
    return decoded

# Desglosso el nom del fitxer... 
filename = sys.argv[1].split('.')
encodedFileName = filename[0] + "-" + ENCODED_FILE
decodedFileName = filename[0] + "-" + DECODED_FILE

# Recollim la mida dels nombres primers amb els què treballem
length = int(sys.argv[2])

# Generem les claus per poder codificar i descodificar
# [Clau pública, Clau privada] -> [n,e], [n,d] -> En aquest cas nb i nr tenen el mateix valor.
[[nb,e], [nr,d]] = getKeys(length)

# Recollim el fitxer d'entrada
string = readFileAsString(sys.argv[1])

# Codifiquem ...
encoded = encode(string, e, nb)
f = open(encodedFileName, 'wb')
f.write(encoded)
f.close()

# Llegim el fitxer que hem desat... 
f = open(encodedFileName, 'rb')
bytesToDecode = f.read()


# Descodifiquem ... 
decoded = decode(bytesToDecode, d, nr)
print(decoded)

# Guardem el resultat com a descodificat ...
f = open(decodedFileName, 'w')
f.write(decoded)
f.close()


