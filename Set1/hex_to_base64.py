def hex_to_byte(hex_str):
    if(len(hex_str)==0):
        return "Error empty string"
    #ovviamente se è dispari la lunghezza aggiungiamo uno 0 in testa e non alla fine perchè 0F = F mentre invece F0!=F
    if(len(hex_str)%2 != 0) :
        hex_str = "0"+hex_str
    bytes_list = []
    #for su tutta la lunghezza a due a due
    for i in range(0, len(hex_str), 2):
        a = hex_str[i]
        b = hex_str[i+1]

        if a.isnumeric():
            a_val = int(a)
        else:
            # ord restituisce il codice ascii del carattere facendo così con ord otteniamo il valore numerico
            # di quello che abbiamo in input e andiamo a sottrarlo sempre al valore numerico di A
            # es: ord(b) = 66, ord('A') = 65, 66 - 65 + 10 = 11 (valore numerico di B)
            a_val = ord(a.upper()) - ord('A') + 10
        if b.isnumeric():
            b_val = int(b)
        else:
            b_val = ord(b.upper()) - ord('A') + 10
         # Calcoliamo il byte: nibble alto * 16 + nibble basso
        byte_val = a_val * 16 + b_val
        bytes_list.append(byte_val)

    return bytes(bytes_list)

"""
questo accade nel secondo for
byte = 73
→ 73 % 2 = 1 → 36
→ 36 % 2 = 0 → 18
→ 18 % 2 = 0 → 9
→ 9 % 2 = 1 → 4
→ 4 % 2 = 0 → 2
→ 2 % 2 = 0 → 1
→ 1 % 2 = 1 → 0
→ 0 % 2 = 0 → stop
"""

def bytes_to_bin(byte_list):
    bits = []
    for byte in byte_list:
        byte_bits = []
        # Trasformiamo il byte in bit
        for _ in range(8):
            byte_bits.append(byte % 2)
            byte = byte // 2
        byte_bits.reverse()  # perché il bit più significativo va prima
        bits.extend(byte_bits)
    return bits


# ------------------------------------------------------------
# Funzione: bin_to_base64(bits)
# ------------------------------------------------------------
# Converte una sequenza di bit (lista di 0 e 1) in una stringa Base64.
#
# LOGICA GENERALE:
# - Base64 lavora su gruppi di 6 bit → 2⁶ = 64 possibili valori.
# - Ogni gruppo di 6 bit viene convertito in un numero (0–63),
#   che corrisponde a un simbolo dell'alfabeto Base64:
#     A–Z → 0–25
#     a–z → 26–51
#     0–9 → 52–61
#     +   → 62
#     /   → 63
#
# STEP PRINCIPALI:
# 1️ Se la lunghezza dei bit non è multipla di 6, aggiungiamo
#    zeri a destra (padding binario) solo per completare il blocco.
#    → questo padding non altera i dati originali, serve solo per
#      permettere la conversione in gruppi da 6 bit.
#
# 2 Ogni gruppo di 6 bit viene convertito nel corrispondente
#    valore decimale con:
#        value = (value << 1) | bit
#    Significato:
#      - << 1 : shift a sinistra (moltiplica per 2 → sposta i bit)
#      - | bit : aggiunge il nuovo bit in coda (OR logico)
#    In pratica, costruiamo il numero come se "scrivessimo" i bit
#    uno alla volta da sinistra a destra.
#    Esempio:
#        [0,1,0,0,1,0] → 010010₂ = 18 → 'S' nell'alfabeto Base64
#
# 3️ Ogni valore 0–63 viene usato come indice per prendere il
#    carattere corrispondente nella stringa base64_chars.
#
# 4️ Dopo aver convertito tutti i gruppi, controlliamo la lunghezza
#    finale della stringa Base64:
#       - Deve essere multipla di 4 caratteri.
#       - Se non lo è, aggiungiamo padding visivo con "=".
#
#    Padding "=" (visivo) indica che i dati originali non erano
#    multipli di 3 byte:
#       3 byte → 4 simboli → nessun '='
#       2 byte → 3 simboli + '='
#       1 byte → 2 simboli + '=='
#    Serve solo per segnalare al decoder quanti bit finali
#    erano di riempimento.
#
# OUTPUT:
# - Restituisce la stringa codificata in Base64 completa di eventuale '='.
# ------------------------------------------------------------




def bin_to_base64(bits): 
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    base64_str = ""

    # Aggiungiamo padding di zeri se necessario
    while len(bits) % 6 != 0:
        bits.append(0)

    # Ciclo a gruppi di 6 bit
    for i in range(0, len(bits), 6):
        chunk = bits[i:i + 6]
        value = 0
        for bit in chunk:
            value = (value << 1) | bit  # Shift a sinistra e aggiunta del bit
        base64_str += base64_chars[value]

    # Aggiungiamo il padding con '=' se necessario
    while len(base64_str) % 4 != 0:
        base64_str += '='

    return base64_str
         
     
    



a = hex_to_byte("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d")
a = bytes_to_bin(a)
a = bin_to_base64(a)

print(a)
