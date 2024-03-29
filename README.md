# Pràctica 6 - RSA

# Què inclou l'entrega? 

Els següents mòduls son utilitzats per a la realització de la pràctica. També s'han rescatat mòduls de les pràctiques anteriors i s'hi han afegit funcions.

- **bezoud.py** : És utilitzat per el mòdul modular.py, es requereix per fer l'invers modular. 
- **euclides.py** : S'utiltiza per el càlcul de phi(n) 
- **utils.py** : Entrada i sortida + potenciació modular. 
- **modular.py** : Potenciació modular i invers modular
- **keygen.py** : Generació de claus Públiques i privades.
- **main.py** : Programa principal.

Els fitxers de text que s'han fet servir per a provar l'aplicatiu es troben al directori text. Hi han exemples de text pla i resultats de les execucions.

# Entrada

L'execució del programa requereix dos paràmetres. 

- El fitxer en pla del text que es vol codificar
- La llargada en bytes del nombre 'p' utilitzat per a la generació de N

S'han fet proves amb diferents llargades de clau, les llargades màximes recomenades son de 128 bytes que venen a ser 1024 bits. 

Exemple d'execució : 

```
python3 main.py text/text-paragraph.txt 128
```

Es poden emprar claus més petites peró quan més petita sigui la clau més petit haurà de ser el text per encripar. Recordem que l'enter generat del text no pot superar N. 

# Sortida

L'execució mostra els valors demanats a l'enunciat de la pràctica, concretament els valors per p, q, n, phi(n), e i d. La generació de les claus està llistada en passos i la funció phi(n) en aquest cas s'anomena euler. 

```
$ python3 main.py text/text-paragraph.txt 128
Pas 1 -> Generem dos nombres aleatoris grans i similars en nombre de bits pero que difereixin, (que no siguin propers) :
p = 40663279426731446999428761614942205432421197667556177831069638044879024352203666550751054071871033692612478325012149231243451699788223099839153592395766766944275876739899881496583532911964593653677542324276594347133097237065368343385508257157646814902047268124546071946028944461587361669179742656532887995961
q = 25019135763239509063239701255941154972216569555486773565013121132218627458218701012653520472311652732065382275097123485172510933850014682987624370601573282292823303585326895769980518122791687631672980704564180259756649466211667074734316233121561117676823853816273159489592551135996611436717624288792165573764153

Pas 2 -> Calculem n, on n=p*q :
n = 1017360108555938107783897835463943167354856338510465692080768247485634710371362877376417620666899219471312659527739074579235863691805543133124090280637836471233292214704517725468575849230403531558769806325682924817370764507327397231545185843548635252898394908652583348020420799054602036002462293572434159577664102608926668444062830098569855359371447496059877286847691940277401837124535031775491542784888965002141839738070814864527072490035909360813665348429359326520531131895058702397332125766721772966153041566059303979297810969163783709080816788408602039249463240395671189217251463913871169774884803650843211430586033

Pas 3 -> Claculem Euler(n) : 
euler = 1017360108555938107783897835463943167354856338510465692080768247485634710371362877376417620666899219471312659527739074579235863691805543133124090280637836471233292214704517725468575849230403531558769806325682924817370764507327397231545185843548635252898394908652583348020420799054602036002462293572434159577639042809884002203552590968552299262193798505306722957104847749507138330641964127096287271258505441236383844984648679230123318104486106454726201824235390277460763552432991906745855024111018120740826383319170847125194028405715051266003115047029883274757737339311273483655712883833412970976497999619394512968825920

Pas 4 -> Cerquem un e € Naturals i coprimer amb euler(n):
e = 34015205520637996445259025083771991092681881093880089893890776324621800500407

Pas 5 -> Cerquem una d € Naturals i e*d (mod euler(n)) == 1 (mod euler(n))
d = 497453704840451447429199191622224065419395651058045912520132909808221650960936887561480868300142592729792517193701199294522930302538262700337083691909930340176833138058892928832253472210743708117487998759568718540832317372204642546371661786199029223990492873882143068624119711798848080946652919829577119385288442951178326390799103602603707846945629375483740045109878371875927588016985248409620131573776232666547212092123003163342021223310134285235534127526638883467561018534065803862085064677128034550816308161454031392043807695125631515223973255047705570847724455067323025938045596134999159942915736780585563111752263


Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur vitae magna sodales, imperdiet felis nec, malesuada orci. Morbi sit amet blandit felis.
```

Finalment l'entrada del text no es mostra per pantalla peró sí la sortida. La sortida del text codificat i descodificat es desa en dos fitxers amb el format que es demana a l'enunciat. Es poden veure exemples d'execució al directori text. 

El fitxer amb el text codificat es desa en bytes per tal que la seva lectura sigui més fàcil, un dels problemes que m'he trobat és que al intentar desar el fitxer de bytes com un string la codificació no casava i donava error al escriure'l en utf-8. Per aquest motiu s'ha decidit desar-lo directament en bytes (la informació segueix estant encriptada). 

# Implementació del generador de claus

Funcions d'ordre superior emprades per a la lleugeresa del codi i els imports.  


```python

import os
import sys
sys.path.append(os.getcwd())
from Crypto.Random import get_random_bytes
from euclides import sonCoprimers
from modular import invers_modular
from modular import potencia_modular_eficient
from keygen import getKeys
import utils


def loop(b, function, byteNumber):
    a = int.from_bytes(get_random_bytes(byteNumber), 'big')
    while not function(a,b): 
        a = int.from_bytes(get_random_bytes(byteNumber), 'big')
    return a
```



Per implementar l'algoritme s'han utilitzat les instruccions definides en les transparències de l'assignatura. 

## 1. Triar dos nombres aleatòris prou grans i que siguin primers. 

La següent funció crida a la funció d'ordre superior demanant-li que executi a cada nombre generat aleatòriament el test de primalitat de fermat fins a 10, (1 .. 9). D'aquesta manera passarà pels nombres recomanats bàsics, el 2, 3, 5, 7 i 9. 


```python

def getSecurePrime(byteNumber):
# a > 0
# retorna el primer nombre primer a partir de a
# El nombre d'iteracions per comprovar fermat és de 10, per tant fa 10 operacions peró es mira els primers 2,3,5,7.
    return loop(10, utils.fermat, byteNumber)

pLength = 32

p = getSecurePrime(pLength)
q = getSecurePrime(pLength + 1)

print(p)
print(q)
```

```
60985840573698424789677586243562727591073886742382981600037315696576231018431
2251464580107834429899098652708681450681089703925957612056629370020199793188671
```



D'aquesta manera es poden generar p i q, s'utilitza el nombre entrat per consola per determinar la mida de p i s'utiltiza 1 byte més per determinar la mida de q. Aixó és per què p i q han d'estar separats en valor però propers en nombre de bits. Considero que una diferència de 8 bits fixe és escalable. 

## 2. Calcular N 

Calcula N és tant simple com fer p * q. 


```python
N = p*q
print(N)
```

```
137307459939785256365935124196789756137861182767754427905574545485588766400535466097966476861844594040884298143413187770783621957127336983551219467261395201
```



## 3. Calcular la funció phi(N)

La funció phi(n) es calcula mitjançant la multiplicació dels dos nombres anteriors corresponent als primers p i q. 


```python
euler = (p-1)*(q-1)
print(euler)
```

```
137307459939785256365935124196789756137861182767754427905574545485588766400533153647545795328989905264645345899234915607192953616533680316865502691237188100
```



## 4. Triar exponent clau pública 

Aquest nombre l'anomenem e i correpon a l'exponent de la clau pública, ha de complir que : 

- ha de ser menor a phi(N), en el nostre cas euler.
- Ha de ser coprimer amb phi(N). 

Per seleccionar-lo s'ha seguit : 


```python
def getSecureEuler(byteNumber, euler):
# a > 0
# retorna el valor per un exponent de mida byteNumber coprimer amb euler
    return loop(euler, sonCoprimers, byteNumber)

e = getSecureEuler(32, euler)
print(e)
```

```
105146145322594843373145589344145854927258684153354662635356377698526665106393
```



En aquest cas s'utilitza una mida fixe de 32 bytes peró es podria fer dinàmica. 

## 5. Generar clau pública

Amb tots aquests ingredients ja podem generar la clau pública, es compón del nombre N i l'exponent e. [N,e].

## 6. Exponent clau privada

Per trobar l'exponent de la clau privada únicament s'ha de fer l'invers modular de la l'exponent de la clau pública.


```python
d = invers_modular(e, euler)
print(d)
```

```
76657370226694963309495682747247627505096262265361502734273395648333433573859840542290835931798210405097099047058165075381305540497955463447344373058296857
```



## 7. Clau privada

Amb els ingredients que tenim fins ara ja podem construïr també la clau privada, que consta de, l'exponent d i el nombre N fruit de les multiplicacions dels anteriors de p i q. [N,d]

# Implementació de l'algoritme de xifrat. 

Dona't un missatge m, utiltizem les següents funcions per codificar i descodificar. 


```python

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
    decodedInt = potencia_modular_eficient(toDecode, d, n)
    decoded = str(decodedInt.to_bytes((decodedInt.bit_length() + 7) // 8, 'big'), 'utf-8')
    return decoded
```



La codificació es realitza sobre m, i s'utilitza la propietat c = m^e (mod N). on c és el text codificat. La transformació del text a enter es fa utiltizant les funcions de text -> bytes i tot seguit bytes -> enter. S'aplica la potència modular i tot seguit es transforma el nombre resultant en bytes. El text codificat es desa en bytes. 

Per a la descodificació recollim els bytes que s'han codificat i tot seguit els passem a l'enter. La forma de desar-ho no és important ja que el text ja està codificat i la potència modular ja està aplicada. Un cop tenim els bytes que representen el text codificat utiltizem la propietat m = c^d (mod N) complint amb la manera de fer i desfer. Recordem que m = (m^e)^d. 

Veiem l'exemple amb un text curt. 


```python
t = "pràctica molt llarga complint la correctesa de les claus..."

bytesCodificats = encode(t, e, N)
print("El text codificat en bytes : ")
print(bytesCodificats)

textDescodificat = decode(bytesCodificats, d, N)
print("El text descodificat : ")
print(textDescodificat)
```

```
El text codificat en bytes :
b'\x07\xdf\xe4\x93\x86\x9f?\x14\xac\x9c{;\x03\xd0uJy\x01\xc1U\xde-\xe2\xf3\xa3\x948\xee\x87\x10U\x8c34|v`\x18?xT\xb7\x85\xe9Z\x7f5~x\xab\n\xe7\xf8\xe0\xef\xc9\xfc\xa6\x9b\xf00-\xdb\xde\xf5'
El text descodificat :
pràctica molt llarga complint la correctesa de les claus...
```



# Fem el hacker bruto

El què es pretén en aquest cas és explicar com es s'hauria de fer per poder trobar l'exponent d que s'utilitza dins de la clau privada. La clau privada està composta per dos parts, l'exponent d i el nombre N. La fortalesa de l'algoritme rau en poder trobar la la factorització de N en nombres primers, és a dir, trobar p i q. Aquest problema és exponencial en nombre de bits i té tractament molt llarg. 

En aquest exemple fem l'execució d'un mètode exponencial però amb una clau curta per poder tenir temps que acabi l'execució abans que acabi l'univers. Treballem amb bytes per tant generem dos nombres enters amb llargada 1 i 2 bytes, respectivament seran p i q


```python

def breakKeys(N):
# N > 0. 
# Retorna p i q, els factors primers de N. 
    return utils.factors_primers(N)

p = getSecurePrime(1)
q = getSecurePrime(2)

print(p*q)

print(breakKeys(p*q))
```

```
466687
[13, 35899]
```



Com podem veure ja tenim la p i la q, cosa que s'haurien de desar amb el màxim secret possible o de fet es podrien llençar a les escombreries per què no es requereixen un cop ja tens les claus generades. A partir d'aquí ja podríem trobar la funció phi(n) i conseqüentment la clau d i podriem desxifrar el missatge. **Recordem que l'algoritme és públic!**

Evidenment quan es generen claus s'utilitzen nombres molt llargs. Un exemple d'una possible clau que es podria fer servir seria amb 128 bytes, és a dir, 1024 bits. El mètode següent genera un parell de claus reben una llargada en nombre de **bytes**. 


```python
keys = getKeys(128)
print(keys)
```

```
Pas 1 -> Generem dos nombres aleatoris grans i similars en nombre de
bits pero que difereixin, (que no siguin propers) :
p =
178118345797852065462709324148957190376400984488503590373193990250164600353067885687890646066036725380359430649314066441258336067816321231231922270069808420341681610365873812979723081720317552594061860135653266155923375914118792751843444255031706813787533884144865052962882057807117386489356261559457755407659
q =
4556596576414555137276155416979619035538996119955295502077420840065813765221222688620837714733509577726419472695245072378569976841130347757956946459727267092061121322158116902628472217984025338699347415124469809512884284891153211000759376203423602154935235023382817965589476000027058851096594568629500714479377

Pas 2 -> Calculem n, on n=p*q :
n =
811613444659116584935539445459564691070044202203636694831351644839041678274385405641460990714265284402933529267576403428897950216137229165727130248878460053486340762619760005309711366410849775867007248789777691290501862486929126535209432730873513502790475370452300342107058378673473092513222127746243948355446672218840059234509694028571041526915804123116435947659994719371600123352145868504083541732123821445717691940916416018166016580337992879994728598743293825189619498306637408742709125339871555286192529465021348391139879036371161712601163425919341955530804871657164442860177714067348772819032075858881982583348443

Pas 3 -> Claculem Euler(n) :
euler =
811613444659116584935539445459564691070044202203636694831351644839041678274385405641460990714265284402933529267576403428897950216137229165727130248878460053486340762619760005309711366410849775867007248789777691290501862486929126535209432730873513502790475370452300342107058378673473092513222127746243948355441937503917846827306955163829912950689888726011992148567544104541284144986571577929774813371324275142610913037571856879346188267429046211005539730013496749677216695374113418027100930040167212394899120189761225315471071375565889708848560605460886646562082102749636759841625356009514596581446125028693024113461408

Pas 4 -> Cerquem un e € Naturals i coprimer amb euler(n):
e =
16424436459722425918032656399461273059409553344600160041464537678277161318591

Pas 5 -> Cerquem una d € Naturals i e*d (mod euler(n)) == 1 (mod
euler(n))
d =
604813919099147507935689819263401355240892780277318322587421773757818663436558139846873627394078663698950010184983620138498490598680254407678030065039676872188641891722452542847585011939715481508076205436466757292041713465092206884915366921719235590763046295053242544935613149000604319801312548876170710616096631871796025904207768472661234673539332827263713099188673494854252311702256912674054582023325717447015323485208314785979655631890573438912136244437367020508688066128135994562911507949816354362492024279687120149189755652627443012910597191110503070512420039600456448386792187785397041930147680035300319823414431


([811613444659116584935539445459564691070044202203636694831351644839041678274385405641460990714265284402933529267576403428897950216137229165727130248878460053486340762619760005309711366410849775867007248789777691290501862486929126535209432730873513502790475370452300342107058378673473092513222127746243948355446672218840059234509694028571041526915804123116435947659994719371600123352145868504083541732123821445717691940916416018166016580337992879994728598743293825189619498306637408742709125339871555286192529465021348391139879036371161712601163425919341955530804871657164442860177714067348772819032075858881982583348443,
16424436459722425918032656399461273059409553344600160041464537678277161318591],
[811613444659116584935539445459564691070044202203636694831351644839041678274385405641460990714265284402933529267576403428897950216137229165727130248878460053486340762619760005309711366410849775867007248789777691290501862486929126535209432730873513502790475370452300342107058378673473092513222127746243948355446672218840059234509694028571041526915804123116435947659994719371600123352145868504083541732123821445717691940916416018166016580337992879994728598743293825189619498306637408742709125339871555286192529465021348391139879036371161712601163425919341955530804871657164442860177714067348772819032075858881982583348443,
604813919099147507935689819263401355240892780277318322587421773757818663436558139846873627394078663698950010184983620138498490598680254407678030065039676872188641891722452542847585011939715481508076205436466757292041713465092206884915366921719235590763046295053242544935613149000604319801312548876170710616096631871796025904207768472661234673539332827263713099188673494854252311702256912674054582023325717447015323485208314785979655631890573438912136244437367020508688066128135994562911507949816354362492024279687120149189755652627443012910597191110503070512420039600456448386792187785397041930147680035300319823414431])
```



La generació d'aquests nombres és costosa i realitza cerca per ensaig i error per trobar els possibles primers. Aquesta pràxis és recomenada per què si la generació és totalment aleatòria és més difícil que es pugui interpretar com es realitza el procediment per escollir els nombres primers. Podria induïr a podar branques a l'hora de provar possibilitats per força bruta tal i com hem fet amb la factorització. 

# Conclusions

En aquesta pràctica s'ha treballat un algoritme de clau pública basada en l'exponenciació modular on la força de l'algoritme rau en el desconeixement de la clau privada. Trobar una clau privada a partir de la clau pública és un problema exponencial en nombre de bits i es demostra amb el petit codi que ens permet la factorització en nombres primers (exponencial). 

No s'ha complert exhaustivament amb les característiques que han de tenir els valors enters p, q, N, e i d degut al temps de dedicació i al sobreesforç que representava. Els temps de càlcul podrien ser molt costosos i les proves s'allargaven. 

S'ha entés perfectament les propietats d'un algoritme de clau pública i quines son les seves fortaleses així com s'ha deduït que les seves debilitats rauen en la tria dels nombres anteriorment esmentats.  
