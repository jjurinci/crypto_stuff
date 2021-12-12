def otp_encode(plaintext, key):
    #y_i = x_i XOR k_i
    return bytes(p^k for p,k in zip(plaintext, key))


def otp_decode(ciphertext, key):
    #x_i = y_i XOR k_i
    return bytes(c^k for c,k in zip(ciphertext, key))


def vulnerability_key_i(plaintext_i, ciphertext_i):
    #k_i = x_i XOR y_i
    return bytes(c^p for c,p in zip(ciphertext_i, plaintext_i))


plaintext = "This is my plaintext yo.".encode(encoding="utf-8")
key = "KEY_YO_RNG_YO_KEY_YO_LOL".encode(encoding="utf-8")
assert len(plaintext) == len(key)

ciphertext = otp_encode(plaintext,key)
plaintext_d = otp_decode(ciphertext, key)

print(plaintext_d)
print(plaintext == otp_decode(otp_encode(plaintext, key), key))

#Full key if I know plaintext and ciphertext
print(vulnerability_key_i(plaintext, ciphertext))

#Partial key if I know the positions of plaintext_i, ciphertext_i
print(vulnerability_key_i(plaintext[3:], ciphertext[3:]))
