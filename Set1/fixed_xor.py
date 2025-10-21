from hex_to_base64 import *

# Converte una lista di byte (numeri 0–255) in una stringa esadecimale
def bytes_to_hex(byte_list: list) -> str:
    hex_str = ""
    for byte in byte_list:
        # Ogni byte viene formattato come due cifre esadecimali (es. 10 -> "0a")
        hex_str += f"{byte:02x}"
    return hex_str


# Esegue l'operazione di "Fixed XOR" tra due stringhe esadecimali di uguale lunghezza
def fixed_xor(str1, str2):
    # Controlla che le due stringhe abbiano la stessa lunghezza
    if len(str1) != len(str2):
        return "Error string have different length"

    result = []

    # Converte entrambe le stringhe esadecimali in liste di byte
    str1 = hex_to_byte(str1)
    str2 = hex_to_byte(str2)

    # Esegue lo XOR byte per byte tra i due buffer
    for i in range(len(str1)):
        result.append(str1[i] ^ str2[i])  # XOR bit a bit tra i byte corrispondenti

    # Converte il risultato (lista di byte) di nuovo in stringa esadecimale
    result = bytes_to_hex(result)
    return result


# Test della funzione con i valori forniti dal challenge
result = fixed_xor(
    "1c0111001f010100061a024b53535009181c",
    "686974207468652062756c6c277320657965"
)
print(result)  # Output atteso: "746865206b696420646f6e277420706c6179"
