import numpy as np
from sympy import Matrix
from string import ascii_uppercase as ALFABET

def matrix_inv_mod (vmnp, mod):
    nr = vmnp.shape[0]
    nc = vmnp.shape[1]
    if (nr!= nc):
        print("Error: Non square matrix! exiting")
        exit()
    vmsym = Matrix(vmnp)
    vmsymInv = vmsym.inv_mod(mod)
    vmnpInv = np.array(vmsymInv)
    k = nr
    vmtest = [[1 for i in range(k)] for j in range(k)]  # just a 2-d list
    vmtestInv = vmsym*vmsymInv
    for i in range(k):
        for j in range(k):
            vmtest[i][j] = vmtestInv[i,j] % mod
    return vmnpInv


ind, slo = {}, {}
for i, slovo in enumerate(ALFABET):
    ind[slovo] = i
    slo[i] = slovo

def dekriptiraj(Y: str, K, m):
    # Y = XK -> X = Y * K_1
    X = ""
    for i in range(0, len(Y), m):
        blok_Y = Y[i:i+m]
        Y_matrix = np.array([ind[i] for i in blok_Y])
        K_1 = matrix_inv_mod(K, 26)
        X_blok = np.dot(Y_matrix, K_1) % 26
        X_blok = X_blok.ravel() #flatterns 2D array to 1D array
        X += "".join([slo[i] for i in X_blok])
    return X


def enkriptiraj(X: str, K, m):
    # Y = XK -> X = Y * K_1
    Y = ""
    for i in range(0, len(X), m):
        blok_X = X[i:i+m]
        X_matrix = np.array([ind[i] for i in blok_X])
        Y_blok = np.dot(X_matrix, K) % 26
        Y_blok = Y_blok.ravel()
        Y += "".join([slo[i] for i in Y_blok])
    return Y


def break_hill(sifrat, plaintext, m):
    #sifrat = plaintext * kljuc ----- Y = XK
    #kljuc = inv(plaintext) * sifrat ---- K = X_1 * Y

    if len(sifrat)%m != 0:
        raise NotImplementedError

    K = None
    blok_sifrat, blok_plaint = [], []
    for i in range(0,len(sifrat), m):
        blok_X = plaintext[i:i+m]
        blok_Y = sifrat[i:i+m]

        blok_sifrat.extend([ind[slovo] for slovo in blok_X])
        blok_plaint.extend([ind[slovo] for slovo in blok_Y])

        if len(blok_sifrat) == m*m:
            try:
                X = np.reshape(blok_sifrat, (m,m))
                Y = np.reshape(blok_plaint, (m,m))
                X_1 = matrix_inv_mod(X,26)
                print(f"{m=}")
                print(f"Plaintext blocks: {blok_plaint} {''.join([slo[i] for i in blok_plaint])}")
                print(f"Ciphertext blocks: {blok_sifrat} {''.join([slo[i] for i in blok_sifrat])}")

                print("Normal X (plain):\n", X)
                print("Inverse X (plain):\n", X_1)
                print("Multiplied by")
                print(f"Ciphertext Y:\n{Y}")
                K = np.dot(X_1, Y) % 26
                print("Found key:\n", K)
            except Exception:
                blok_sifrat, blok_plaint = [], []

    X = dekriptiraj(sifrat, K, m)
    print(f"Found plaintext: {X}\n")


def demo():
    sifrat = "THWJKB"
    odabrani_pt = "ZAGREB"
    m = 2
    break_hill(sifrat, odabrani_pt, m)

    K = [7,19,8,3]
    K = np.reshape(K, (2,2))
    print(enkriptiraj(odabrani_pt, K, m))
    print(odabrani_pt == dekriptiraj(enkriptiraj(odabrani_pt, K, m), K, m))

"""It gets quite messy because given plaintext needs to be invertible in Z_26."""
sifrat = "PMJVKSCBOLANDTYNPGUK"
plaintext = "PRIJESTOLONASLJEDNIK"
m = 2
break_hill(sifrat, plaintext, m)

sifrat = "TCTCAKLGLCBT"
plaintext = "POPOKATEPETL"
m = 2
break_hill(sifrat, plaintext, m)
