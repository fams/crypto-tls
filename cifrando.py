def vigenere_encrypt(plaintext, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    plaintext = ''.join([c for c in plaintext.upper() if c in alphabet])  # remove não letras
    ciphertext = ""

    for i in range(len(plaintext)):
        p = alphabet.index(plaintext[i])
        k = alphabet.index(key[i % len(key)])
        c = (p + k) % 26
        ciphertext += alphabet[c]

    return ciphertext

def vigenere_decrypt(ciphertext, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    ciphertext = ''.join([c for c in ciphertext.upper() if c in alphabet])  # remove não letras
    plaintext = ""

    for i in range(len(ciphertext)):
        c = alphabet.index(ciphertext[i])
        k = alphabet.index(key[i % len(key)])
        p = (c - k + 26) % 26
        plaintext += alphabet[p]

    return plaintext

# Texto original
plaintext = (
    "OMUNDOMUDAQUANDOASPEQUENASACOESSETORNAMHABITOSQUESETRANSFORMAMEMGRANDESMUDANCAS"
    "CONSTANTESERESILIENTESASMENTESQUEPLANTAMOSHOJETRARAMOSAMANTA"
)

# Chave
key = "CRYPTO"

# Cifra
ciphered = vigenere_encrypt(plaintext, key)
print("Texto cifrado:\n", ciphered)

# Decifra
deciphered = vigenere_decrypt(ciphered, key)
print("\nTexto decifrado:\n", deciphered)
