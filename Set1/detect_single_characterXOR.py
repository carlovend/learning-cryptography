from single_byte_xor import *


def resolve():
    best = None
    with open("prova.txt", "r") as f:
        for line_no, line in enumerate(f, start=1):
            hx = line.strip()
            if not hx:
                continue
            result = hex_to_byte(hx)
            candidate = (result[0], result[1], result[2], line_no, hx)
            if best is None or candidate[0] > best[0]:
                best = candidate
    print(f"Best line #{best[3]} key={best[1]} -> {best[2]}")