
from itertools import combinations
from statistics import mean
import base64
import sys

from single_byte_xor import single_byte_xor  


# Hamming distance (in bit)
def hammingDist(a: bytes, b: bytes) -> int:
    if len(a) != len(b):
        raise ValueError("Inputs must have same length")
    return sum((x ^ y).bit_count() for x, y in zip(a, b))


def normalized_keysize_score(cipher_bytes: bytes, keysize: int, n_blocks: int = 4) -> float:
    # Prende i primi n_blocks blocchi di lunghezza keysize, calcola le distanze
    # su tutte le coppie, poi fa media e normalizza dividendo per keysize.
    blocks = []
    for i in range(n_blocks):
        start = i * keysize
        end = start + keysize
        if end <= len(cipher_bytes):
            blocks.append(cipher_bytes[start:end])
        else:
            break
    if len(blocks) < 2:
        return float("inf")
    dists = [hammingDist(b1, b2) for (b1, b2) in combinations(blocks, 2)]
    return mean(dists) / keysize


def guess_key_size(cipher_bytes: bytes, ks_min: int = 2, ks_max: int = 40, n_blocks: int = 4, top: int = 3):
    scores = []
    for ks in range(ks_min, ks_max + 1):
        score = normalized_keysize_score(cipher_bytes, ks, n_blocks=n_blocks)
        scores.append((score, ks))
    scores.sort(key=lambda x: x[0])
    return scores[:top] 


#trasposizione
def divide_block(cipher_bytes: bytes, keysize: int):
    result = []
    i = 0
    while i < len(cipher_bytes):
        result.append(cipher_bytes[i:i+keysize])
        i += keysize
    return result


def transpose_blocks(blocks, keysize: int):
    cols = []
    for i in range(keysize):
        col = bytearray()
        for b in blocks:
            if i < len(b):  # ultimo blocco può essere corto
                col.append(b[i])
        cols.append(bytes(col))
    return cols



def best_key_byte_for_column(col_bytes: bytes) -> int:
    col_hex = col_bytes.hex()
    best = single_byte_xor(col_hex)[0]  # (score, key, plaintext)
    return best[1]  # byte di chiave (int 0..255)


def recover_key_bytes(cols) -> bytes:
    return bytes(best_key_byte_for_column(c) for c in cols)



def repeating_key_xor_bytes(key_bytes: bytes, data_bytes: bytes) -> bytes:
    out = bytearray()
    klen = len(key_bytes)
    i = 0
    for b in data_bytes:
        out.append(b ^ key_bytes[i])
        i = 0 if i == (klen - 1) else i + 1
    return bytes(out)


def break_repeating_key_xor(cipher_bytes: bytes):
    # 1) stima KEYSIZE (prendi i migliori 3 candidati)
    candidate_keysizes = guess_key_size(cipher_bytes, ks_min=2, ks_max=40, n_blocks=4, top=3)

    results = []
    for _, keysize in candidate_keysizes:
        # 2) spezza in blocchi e trasponi
        blocks = divide_block(cipher_bytes, keysize)
        cols = transpose_blocks(blocks, keysize)

        # 3) ricava la chiave (byte per byte) con single-byte XOR sulle colonne
        key_bytes = recover_key_bytes(cols)

        # 4) decritta tutto
        plaintext = repeating_key_xor_bytes(key_bytes, cipher_bytes)

        # score semplice: % di caratteri stampabili
        printable = set(range(32, 127)) | {9, 10, 13}
        score = sum(1 for c in plaintext if c in printable) / max(1, len(plaintext))
        results.append((score, key_bytes, plaintext))

    # sceglie il migliore tra i candidati
    results.sort(key=lambda x: x[0], reverse=True)
    best_score, best_key, best_plain = results[0]
    return best_key, best_plain


if __name__ == "__main__":

    with open("prova.txt", "rb") as f:
        data_b64 = f.read()
    cipher_bytes = base64.b64decode(data_b64)

    key, plaintext = break_repeating_key_xor(cipher_bytes)

    try:
        key_str = key.decode("ascii")
    except Exception:
        key_str = repr(key)

    print("=== KEY ===")
    print(key_str)
    print()
    print("=== PLAINTEXT ===")
    print(plaintext.decode("ascii", errors="ignore"))
