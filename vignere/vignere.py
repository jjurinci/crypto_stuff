import string
from collections import Counter
from itertools import product

slovo_to_index = {slovo : i for i, slovo in enumerate(string.ascii_uppercase)}
index_to_slovo = {i : slovo for i, slovo in enumerate(string.ascii_uppercase)}
hrv_freq_premile = {"A":115,"I":98,"O":90,"E":84,"N":66,"S":56,"R":54,"J":51,"T":48,"U":43,"D":37,"K":36,"V":35,"L":33,"M":31,"P":29,"C":28,"Z":23,"G":16,"B":15,"H":8,"F":3}

for slovo,i in slovo_to_index.items():
    if slovo not in hrv_freq_premile:
        hrv_freq_premile[slovo] = 0

HRV_FREQ = {slovo_to_index[k]:v/1000 for k,v in hrv_freq_premile.items()}

def vignere_square():
    alphabet = string.ascii_uppercase
    square = []

    start = alphabet
    for _ in range(26):
        square.append(start)
        start = start[1:] + start[0]
    return square


# Nizovi od z po stupcima, gdje je svaki red sifriran monoalfabetski kao cezar
def get_matrix(cipher, m):
    z = []
    for i in range(0,len(cipher), m):
        z.append(cipher[i:i+m])

    matrix = [[] for _ in range(m)]
    for i in range(m):
        for j in range(len(z)):
            if i < len(z[j]):
                matrix[i].append(z[j][i])
    return matrix


def print_matrix(matrix):
    for row in matrix:
        print("".join(row))
    print("")


def kasiski(cipher):
    trigrams = []
    trig_pos = {}
    for i in range(0,len(cipher)):
        trigram = cipher[i:i+3]
        trigrams.append(trigram)
        if trigram not in trig_pos:
            trig_pos[trigram] = []
        trig_pos[trigram].append(i+1)

    freq = Counter(trigrams)

    for trigram, count in freq.items():
        if count < 2:
            continue

        distances = trig_pos[trigram]
        distance_pairs = list(product(distances, distances))
        for di,dj in distance_pairs:
            if di >= dj:
                continue
            else:
                print(trigram, dj-di)


def Ic(x):
    n = len(x)
    suma = 0
    f = Counter(x)
    for letter in f:
        suma += f[letter] * (f[letter] - 1)
    return suma / (n * (n-1))


def Ic_expected(x):
    n = len(x)
    suma = 0
    f = Counter(x)
    relative_f = {letter : f[letter] / n for letter in f}

    for letter in f:
        suma += (relative_f[letter] * relative_f[letter])

    return suma


def MIc_hrv():
    sol = {}
    for q in range(14):
        sol[q] = 0
        for h in range(26):
            p_h = HRV_FREQ[h]
            p_relative = HRV_FREQ[(h + q) % 26]
            sol[q] += p_h * p_relative
    print(sol)


def MIc(x,y):
    n, n_ = len(x), len(y)
    f, f_ = Counter(x), Counter(y)

    suma = 0
    for i in range(26):
        slovo_i = index_to_slovo[i]
        suma += f[slovo_i] * f_[slovo_i]

    return suma / (n * n_)


def MIc_modified(x,y,g):
    n, n_ = len(x), len(y)
    f, f_ = Counter(x), Counter(y)

    suma = 0
    for i in range(26):
        slovo_i = index_to_slovo[i]
        slovo_j = index_to_slovo[(i-g)%26]
        suma += f[slovo_i] * f_[slovo_j]

    return suma / (n * n_)


def MIc_language(y,g):
    n_ = len(y)
    suma = 0
    f = Counter(y)

    for i in range(26):
        slovo_j = index_to_slovo[(i-g)%26]
        suma += HRV_FREQ[i] * f[slovo_j]

    return suma / n_


def ceasar_encode(plaintext, rot_i):
    alphabet = string.ascii_uppercase
    return [alphabet[(slovo_to_index[char] + rot_i) % 26] for char in plaintext]


def cipher_mic(matrix):
    goods = []
    for i,x in enumerate(matrix): #fiksirani z_i
        for j,y in enumerate(matrix): #mijenjajuci z_j
            if x == y:
                continue
            for g in range(26):
                mic = MIc_modified(x,y,g)

                if mic > 0.062:
                    print(f"MIc(z_{i}, z_{j}^{g}={index_to_slovo[g]}) = {mic}")
                    goods.append((i,j,mic))
        print("")
    print(len(goods))


def cipher_mic_language(matrix):
    key = ""
    for y in matrix:
        M_g = []
        for g in range(26):
            mic = MIc_language(y,g)
            M_g.append((mic, g))

        best = max(M_g, key=lambda x: x[0])
        k_j = -best[1] % 26
        key += index_to_slovo[k_j]

    return key


def fridman_test(matrix):
    for i,z in enumerate(matrix):
        ic = Ic(z)
        print(f"{ic}, z_{i}")


def decipher_vignere(cipher, key):
    plaintext = ""
    alphabet = string.ascii_uppercase

    rot_i = slovo_to_index[key[0]]
    for i, letter in enumerate(cipher):
        index_ltr = slovo_to_index[letter]
        rotated_ltr = alphabet[(index_ltr - rot_i) % 26]
        plaintext += rotated_ltr

        rot_i = key[(i+1) % len(key)]
        rot_i = slovo_to_index[rot_i]

    return plaintext



cipher = "GSIQITUKQIEAOHRVUGLTAZGHXUHLPJMRTTNQRBZIAVBTGQTBYMYAIVOMZTAIXJBTEDEWVQWADVWGOOKNQNTCIPEGPYBOKUSECNWELLCPZUMIVWFUIJMYATUEXISLMZTNPGUJHTMERXJSYSIVWABGVWFDTZILNTIEDEFJMFAMPNQZBRSDIZPRMLGVKFEDZXMVXVQMJXWSLEEQRMAEPRUJXIMFNT"
kasiski(cipher)
m = 5

matrix = get_matrix(cipher, m)
fridman_test(matrix)

key = cipher_mic_language(matrix)
plaintext = decipher_vignere(cipher, key)
print(key, plaintext)

cipher_mic(matrix)
