try:  
    with open('Mars_Base_Inventory_List.csv', 'r', encoding='utf-8') as file:  
        content = file.read()  
        print(content)  
except FileNotFoundError:  
    print('File not found.')  
except Exception as e:  
    print(f'Unexpected error: {e}') 

lines = content.splitlines()  
inventory_list = []  
for line in lines[1:]:  # 헤더 제외  
    parts = line.split(',')  
    inventory_list.append(parts)  

inventory_list.sort(key=lambda x: float(x[4]), reverse=True)  # 인덱스 4가 flammability  

high_flammability = [item for item in inventory_list if float(item[4]) >= 0.7]  
# ... (이전 코드: high_flammability 리스트 생성 부분)

# 더 정돈된 출력: 테이블 형식으로 헤더와 각 행 출력
print('Substance                  | Weight (g/cm³) | Specific Gravity | Strength     | Flammability')
print('-' * 80)  # 구분선
for item in high_flammability:
    # 각 열을 고정 너비로 포맷팅 (예: Substance 25자, 나머지 15자)
    print(f'{item[0]:<26} | {item[1]:<14} | {item[2]:<16} | {item[3]:<12} | {item[4]:<12}')
try:  
    with open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8') as csv_file:  
        csv_file.write('Substance,Weight (g/cm³),Specific Gravity,Strength,Flammability\n')  # 헤더 작성  
        for item in high_flammability:  
            csv_file.write(','.join(item) + '\n')  
except Exception as e:  
    print(f'Error saving CSV: {e}')  