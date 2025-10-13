CIPHER = "gdkkn vnqkc" 

def caesar_cipher_decode(text):
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
def main():
    try:
        decode_text = caesar_cipher_decode(CIPHER)
        for i, text in enumerate(decode_text):
            print(f"{i}: {text}")
        res = int(input())
        if not 0 <= res <= 25:
            raise ValueError
        print(f"Result: {decode_text[res]}")
    except ValueError:
        print(f"invalid input.")
    except Exception:
        print(f"error")
if __name__ == '__main__':
    main()