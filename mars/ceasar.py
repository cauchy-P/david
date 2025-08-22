def caesar_cipher_decode(target_text):
    for shift in range(1, 27):
        decoded = ''
        for char in target_text:
            if char.isupper():
                decoded += chr((ord(char) - 65 - shift) % 26 + 65)
            elif char.islower():
                decoded += chr((ord(char) - 97 - shift) % 26 + 97)
            else:
                decoded += char
        print(f"Shift {shift}: {decoded}")

# 파일 읽기
try:
    with open('./emergency_storage_key/password.txt', 'r') as f:
        text = f.read().strip()
except Exception as e:  
        print(f'Unexpected error: {e}')  
# 모든 shift 결과 출력
caesar_cipher_decode(text)

# 사용자 입력으로 shift 번호 받기
shift = int(input("몇 번째 자리수로 암호가 해독되는지 입력하세요: "))

# 선택된 shift로 해독 결과 계산
decoded = ''
for char in text:
    if char.isupper():
        decoded += chr((ord(char) - 65 - shift) % 26 + 65)
    elif char.islower():
        decoded += chr((ord(char) - 97 - shift) % 26 + 97)
    else:
        decoded += char

# 결과 저장
with open('result.txt', 'w') as f:
    f.write(decoded)

print("해독 결과가 result.txt에 저장되었습니다.")