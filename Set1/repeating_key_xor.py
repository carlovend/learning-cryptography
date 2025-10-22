from hex_to_base64 import *
from fixed_xor import *

def string_to_bytes(s: str) -> list:
    return [ord(c) for c in s]


def repeating_key_xor(key, to_encode):
    result = []
    byte_key = string_to_bytes(key)
    byte_to_encode = string_to_bytes(to_encode)
    key_lenght = len(byte_key)
    i = 0
    for byte in byte_to_encode:
        result.append(byte ^ byte_key[i])
        if i == key_lenght-1:
            i = 0
        else:
            i = i+1
    result = bytes_to_hex(result)
    return result

res = repeating_key_xor("ICE", "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal")
print(res)
