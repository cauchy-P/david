import os
import json
from datetime import datetime  # 추가: datetime import

try:
    # 파일 경로를 명확히 지정
    #file_path = os.path.join('mars', 'mission_computer_main.log')
    with open("./mission_computer_main.log", 'r', encoding='utf-8') as file:
        content = file.read()
        print("Log file content:")
        print(content)

    # 로그 데이터를 리스트로 변환 (event는 무시하고 timestamp와 message만)
    lines = content.splitlines()[1:]  # 헤더 제외
    log_list = [[line.split(',', 2)[0], line.split(',', 2)[2]] for line in lines]
    print("\nLog list (before sort):")
    print(log_list)

    # 시간 역순 정렬 (datetime으로 변환하여 안전하게 정렬)
    log_list.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'), reverse=True)
    print("\nSorted log list (reverse chronological):")
    print(log_list)

    # 사전 객체로 변환
    log_dict = {item[0]: item[1] for item in log_list}
    
    # JSON 파일로 저장
    try:
        with open('./mission_computer_main.json', 'w', encoding='utf-8') as json_file:
            json.dump(log_dict, json_file, ensure_ascii=False, indent=4)
        print("\nJSON file saved successfully.")
    except Exception as e:
        print(f'Error saving JSON: {e}')

except FileNotFoundError:
    print('File not found. Ensure mission_computer_main.log exists in the mars directory.')
except UnicodeDecodeError:
    print('Decoding error. Check the file encoding.')
except Exception as e:
    print(f'Unexpected error: {e}')