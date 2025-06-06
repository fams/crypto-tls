import string
from collections import Counter, defaultdict

# Frequência de letras no português
portuguese_freq = {
    'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57,
    'F': 1.02, 'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40,
    'K': 0.02, 'L': 2.78, 'M': 4.74, 'N': 5.05, 'O': 10.73,
    'P': 2.52, 'Q': 1.20, 'R': 6.53, 'S': 7.81, 'T': 4.34,
    'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21, 'Y': 0.01, 'Z': 0.47
}

alphabet = string.ascii_uppercase

def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return set(line.strip().upper() for line in f if line.strip())
# Pequeno dicionário embutido
portuguese_words = load_dictionary('dict.txt')

# Funções auxiliares
def find_repeated_sequences_spacings(ciphertext, seq_len=3):
    positions = defaultdict(list)
    for i in range(len(ciphertext) - seq_len):
        seq = ciphertext[i:i+seq_len]
        positions[seq].append(i)
    spacings = []
    for idxs in positions.values():
        if len(idxs) > 1:
            for i in range(len(idxs)-1):
                spacings.append(idxs[i+1] - idxs[i])
    return spacings

def get_factors(n):
    return [i for i in range(2, 21) if n % i == 0]

def kasiski_estimate_key_lengths(ciphertext):
    spacings = find_repeated_sequences_spacings(ciphertext)
    factors = []
    for space in spacings:
        factors.extend(get_factors(space))
    return [k for k, _ in Counter(factors).most_common()]

def split_by_n(ciphertext, n):
    return [''.join(ciphertext[i::n]) for i in range(n)]

def chi_squared_score(text):
    total = sum(Counter(text).values())
    score = 0
    freqs = Counter(text)
    for letter in alphabet:
        expected = portuguese_freq[letter] / 100 * total
        observed = freqs.get(letter, 0)
        if expected > 0:
            score += (observed - expected) ** 2 / expected
    return score

def best_shift(group):
    min_score = float('inf')
    best = 0
    for shift in range(26):
        shifted = ''.join(
            alphabet[(alphabet.index(c) - shift) % 26]
            for c in group
        )
        score = chi_squared_score(shifted)
        if score < min_score:
            min_score = score
            best = shift
    return best

def find_key(ciphertext, key_len):
    key = ''
    groups = split_by_n(ciphertext, key_len)
    for group in groups:
        shift = best_shift(group)
        key += alphabet[shift]
    return key

def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key = key.upper()
    for i, c in enumerate(ciphertext):
        if c in alphabet:
            c_idx = alphabet.index(c)
            k_idx = alphabet.index(key[i % len(key)])
            p_idx = (c_idx - k_idx + 26) % 26
            plaintext += alphabet[p_idx]
    return plaintext

def count_known_words(text):
    words = [text[i:i+len(w)] for w in portuguese_words for i in range(len(text) - len(w) + 1)]
    return sum(1 for w in words if w in portuguese_words)

# Texto cifrado
ciphertext = (
    "WZNRUWZNHRYHTRUWNLTVYHXRRANVSVAFXXFZATQYIOBXFADNIJMGKEEASHVDIZXQXZNGHVAZNHRVPTWTWALXRVGXWVZRLMCQRGXVANLQVVGXWHCRIPRVGTQFAUHNVBETVRUBLEDIAME"
)
ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))

# Estimar possíveis tamanhos de chave
candidatos = kasiski_estimate_key_lengths(ciphertext)
if not candidatos:
    candidatos = list(range(2, 13))  # fallback

melhor_score = -1
melhor_chave = ""
melhor_texto = ""

for key_len in candidatos[:5]:
    key = find_key(ciphertext, key_len)
    texto = vigenere_decrypt(ciphertext, key)
    score = count_known_words(texto)
    print(f"Tentando chave {key} → {score} palavras conhecidas")
    if score > melhor_score:
        melhor_score = score
        melhor_chave = key
        melhor_texto = texto

print(f"\n🔐 Melhor chave estimada: {melhor_chave}")
print(f"\n📜 Texto decifrado:\n{melhor_texto}")
