from hex_to_base64 import *

from collections import Counter
import math
import string

# Funzione di scoring molto semplice:
# somma i pesi delle frequenze attese in inglese per ogni carattere trovato nel testo.
# Più alto è lo score, più il testo "sembra" inglese.
def score_english(text: str) -> float:
    score = 0
    frequency = {
        'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
        'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
        'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
        'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
        'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
        'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
        'y': 0.01974, 'z': 0.00074, ' ': 0.13000
    }
    # Valuta carattere per carattere (minuscolo) e somma il relativo peso
    for char in text.lower():
        if char in frequency:
            score += frequency[char]
    return score


# Brute-force della chiave XOR a 1 byte.
# Input: stringa esadecimale. Output: i migliori 5 candidati (score, chiave, plaintext).
def single_byte_xor(str1):
    # Decodifica da esadecimale a bytes (lista o buffer a seconda della tua hex_to_byte)
    str_bytes = hex_to_byte(str1)

    candidates = []  # raccoglie le tuple (score, chiave, plaintext)

    # Prova tutte le 256 chiavi possibili (0..255)
    for a in range(256):
        result = []  # buffer per il plaintext generato con la chiave 'a'

        # XOR byte-per-byte con la chiave corrente
        for i in range(len(str_bytes)):
            result.append(str_bytes[i] ^ a)

        # Converte la lista di int in bytes e poi in stringa ASCII ignorando byte non validi
        plaintext = bytes(result).decode('ascii', errors='ignore')

        # Calcola lo score di "inglese" del plaintext
        score = score_english(plaintext)

        # Salva candidato: punteggio, chiave usata e testo ottenuto
        candidates.append((score, a, plaintext))

    # Ordina per score decrescente e restituisce i migliori 5
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[:5]


# Test sul ciphertext del challenge
result = single_byte_xor("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
print(result)
