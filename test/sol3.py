# 아래 예시는 임의의 문자 입니다. 문제에 나오는 문자를 사용하세요
CAESAR_PASSWORD_TEXT = 'b ehox Ftkl sdlkf alk sdklfn'

# 함수의 이름을 까먹었습니다. 문제 나오는 함수 형식을 사용해주세요.
def caesar_cipher_decode(text):
    res = []
    for shift in range(26):
        decoded = ''
        for ch in text:
            if ch.isupper():
                decoded += chr((ord(ch) - 65 - shift) % 26 + 65)
            elif ch.islower():
                decoded += chr((ord(ch) - 97 - shift) % 26 + 97)
            else:
                decoded += ch  # 공백 등 비문자 그대로 유지
        res.append(decoded)
    return res
def main():
    try:
        decode_passwords = caesar_cipher_decode(CAESAR_PASSWORD_TEXT)
        
        for i, password in enumerate(decode_passwords):
            # {i}: {password} 형식으로 출력 (반드시 : 다음에 한칸 공백이 있어야 합니다.)
            print(f"{i}: {password}")
        
        # 문제에서 따로 입력 문구는 지정해주지 않습니다.
        # 숫자가 아닌 값이나 0~25 범위인지만 예외처리를 해야 합니다.
        result = int(input())
        
        if not 0 <= result <= 25:
            raise ValueError

        # 사용자가 선택한 결과 출렭
        # 반드시 : 다음에 한칸 공백이 있어야 합니다.
        print(f"Result: {decode_passwords[result]}")
        
    # 4번 문제와 같이 사용자에 입력에 대한 예외처리(ValueError)와 그 외 에러(Exception)로 처리하라고 나옵니다.
    # 에러 문구도 문제를 참고해주세요.
    except ValueError:
        print(f'invalid input.')
        return
    except Exception:
        print(f'error')
        return

if __name__ == '__main__':
    main()