def ceasar_cipher_decode(text):
    res = []
    for shift in range(26):
        tmp = ""
        for ch in text:
            if ch.islower():
                tmp += chr((ord(ch) - 97 - shift) % 26 + 97)
            else:
                tmp += ch
        res.append(tmp)
    return res
print(ceasar_cipher_decode("b ehox Ftkl"))