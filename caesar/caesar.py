import string
from collections import Counter
from itertools import permutations

alfabet = string.ascii_uppercase
sifrat = "YNCUNAUSQKEUJAUIJXYEEYNNYNUAUUNADUNAKNYNUYADPJAXUVYIJALOEKWIPLXYRRYLXUIYNDXYRXYADPJLIPRAYRPEAXOBWXQPIUEKAOOLUIPAUONHOIUA"
#sifrat = "TQCWTQCKIQRWNOQOBCEWOQVKBUKAPKOQOQBCQPQAJGDUQEQORWTSJGRWEQKYWGTWCJKRBIKZGVOGBQ"

sljedbenici_slova = {slovo:[] for slovo in alfabet}

for i, slovo in enumerate(sifrat):
    if i+1 == len(sifrat):
        break
    sljedbenici_slova[slovo].append(sifrat[i+1])

slova_freq = {slovo:0 for slovo in alfabet}
bigrami_freq = {}
trigrami_freq = {}

for slovo, sljedbenici in sljedbenici_slova.items():
    for i, sljed_slovo in enumerate(sljedbenici):
        slova_freq[sljed_slovo] += 1
        bigram = slovo + sljed_slovo

        if bigram not in bigrami_freq:
            bigrami_freq[bigram] = 1
        else:
            bigrami_freq[bigram] += 1

        if i+1 == len(sljedbenici):
            continue

trigrami = []
quadgrami = []
for i in range(0,len(sifrat)):
    trigram = sifrat[i:i+3]
    quadgram = sifrat[i:i+4]
    if len(trigram) != 3:
        break
    trigrami.append(trigram)
    if len(quadgram) != 4:
        continue
    quadgrami.append(quadgram)


trigrami_freq = Counter(trigrami)
quadgrami_freq = Counter(quadgrami)


for slovo, sljedbenici in sljedbenici_slova.items():
    print(slovo, sljedbenici)

print(sorted(bigrami_freq.items(), key=lambda x:x[1], reverse=True))
print("")
print(sorted(slova_freq.items(), key=lambda x:x[1], reverse=True))

inverzni_bigrami = []
seen = set()
for bigram  in bigrami_freq:
    freq = bigrami_freq[bigram]
    inverz = bigram[1] + bigram[0]

    if inverz in seen or bigram in seen:
        continue
    seen.add(bigram)
    seen.add(inverz)

    if inverz in bigrami_freq:
        inverzni_bigrami.append((bigram, freq, inverz, bigrami_freq[inverz]))

inverzni_bigrami.sort(key=lambda x:(x[1]+x[3]), reverse=True)
print("\n", inverzni_bigrami)

def parcijalno_desifriraj(sifrat, parcijalni_kljuc):
    for i, slovo in enumerate(sifrat):
        print(slovo, end="")
    print("")

    plaintext = ""
    for i,slovo in enumerate(sifrat):
        if slovo in parcijalni_kljuc:
            print(parcijalni_kljuc[slovo],end="")
            plaintext += parcijalni_kljuc[slovo]
        else:
            print("-", end="")
            plaintext += "-"
    print("")
    return plaintext



print(trigrami_freq)
print(quadgrami_freq)
print("")
kljuc = {"U":"E", "A":"T", "Y":"I", "N":"N", "C":"V", "S":"D", "D":"W", "K": "Y", "P":"A", "J":"S", "X":"H", "V": "F", "I":"R", "E":"L", "Q":"B", "L":"P", "O":"O", "W":"G", "R":"C", "B":"U", "H":"M"}

plaintext = parcijalno_desifriraj(sifrat, kljuc)

for i,letter in enumerate(plaintext):
    print(letter, end="")
    if (i+1)%5 == 0:
        print(" ", end="")
print("")

# Print key
print("Kljuc: ")
for letter in string.ascii_uppercase:
    if letter in kljuc:
        print(kljuc[letter], end="")
    else:
        print(letter, end="")
print("")

for letter in string.ascii_uppercase:
    print(letter, end="")
print("")


def decipher(cipher, key):
    for i, letter in enumerate(cipher):
        print(key[letter], end="")
        if (i+1)%5 == 0:
            print(" ", end="")
    print("")

decipher(sifrat, kljuc)
