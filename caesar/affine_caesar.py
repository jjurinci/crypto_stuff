from string import ascii_uppercase as ALFABET
from collections import Counter

ind, slo = {}, {}
for i, slovo in enumerate(ALFABET):
    ind[slovo] = i
    slo[i] = slovo

DOPUSTENI_A_OVI = [1,3,5,7,9,11,15,17,19,21,23,25]
inverz_a = {1:1, 3:9, 5:21, 7:15, 9:3, 11:19, 15:7, 17:23, 19:11, 21:5, 23:17, 25:25}


def e(x,a,b):
    return (a*x+b) % 26


def d(y,a,b):
    return inverz_a[a] * (y-b) % 26


def enkriptaj(plaintext, kljuc):
    a,b = kljuc
    sifrat = ""
    for slovo in plaintext:
        x = ind[slovo]
        enk = e(x,a,b)
        sifrat += slo[enk]
    return sifrat


def dekriptaj(sifrat, kljuc):
    a,b = kljuc
    plaintext = ""
    for slovo in sifrat:
        y = ind[slovo]
        dek = d(y,a,b)
        plaintext += slo[dek]
    return plaintext


def demo():
    K = (7,3)
    plaintext = "ZADAR"

    sifrat = enkriptaj(plaintext, K)
    plain = dekriptaj(sifrat, K)
    print(sifrat, plain)
    print(dekriptaj(enkriptaj(plaintext, K), K) == plaintext)


def pure_brute(sifrat):
    for a in DOPUSTENI_A_OVI:
        for b in range(26):
            K = (a,b)
            print(K, dekriptaj(sifrat, K))


def freq_analysis(sifrat):
    freq = Counter(sifrat)
    print(freq)


sifrat = "OZWHRYEZCVWFCTPCUWRCFPYHWI"
#pure_brute(sifrat)
freq_analysis(sifrat) #A, I, O, E, N

#Postupak:
# 1. Pogodi da je 1 od najfrekventnijih slova A
#    Pogodi da je 1 od najfrekventnijih slova I
#
# 2. Recimo da je e(A) = C, i e(I) = W
#    Znaci da je e(A) = a * 0 + b = b
#    Znaci da je e(I) = a * 8 + b
#
# 3. Razradi da je e(A) = b KONGRUENTNO 2 mod 26 -> b = 2
#    Razradi da je e(I) = a * 8 + b KONGRUENTNO 22 mod 26
#    Razradi da je e(I) = a * 8 + 2 KONKRUENTNO 22 mod 26
#    Mozes brute force-at sve dozvoljene a-ove.
#    Ispada da je a = 9 dobar.
#
#  4. Rezultat: a = 9 i b = 2, odnosno K = (9,2)
#     e(x) = 9x + 2
#     d(y) = 3y - 2
