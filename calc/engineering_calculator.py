# engineering_calculator.py

import sys
import math
import random
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class EngineeringCalculator(QWidget):
    """
    아이폰 공학용 계산기와 유사한 UI 및 기능을 제공하는 클래스.
    사용자 친화적인 수식을 표시하고, 내부적으로는 파이썬 코드로 변환하여 계산한다.
    특수 연산자(제곱근 등)와 수학적 예외(정의역 오류 등)를 정확하게 처리한다.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()
        
        self.display_expression = ''
        self.eval_expression = ''
        self.is_rad = True
        self.is_2nd = False
        self.memory = 0
        self.reset_display()

    def init_ui(self):
        """공학용 계산기 UI를 초기화하고 설정한다."""
        self.setWindowTitle('공학용 계산기')
        self.setGeometry(100, 100, 850, 450)

        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setMaxLength(50)
        self.result_display.setStyleSheet('border: none; background-color: black; color: white; padding: 10px;')

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.result_display, 0, 0, 1, 10)

        buttons = [
            ('(', 1, 0), (')', 1, 1), ('mc', 1, 2), ('m+', 1, 3), ('m-', 1, 4), ('mr', 1, 5), ('AC', 1, 6), ('+/-', 1, 7), ('%', 1, 8), ('/', 1, 9),
            ('2nd', 2, 0), ('x²', 2, 1), ('x³', 2, 2), ('xʸ', 2, 3), ('eˣ', 2, 4), ('10ˣ', 2, 5), ('7', 2, 6), ('8', 2, 7), ('9', 2, 8), ('*', 2, 9),
            ('1/x', 3, 0), ('√x', 3, 1), ('∛x', 3, 2), ('ʸ√x', 3, 3), ('ln', 3, 4), ('log₁₀', 3, 5), ('4', 3, 6), ('5', 3, 7), ('6', 3, 8), ('-', 3, 9),
            ('x!', 4, 0), ('sin', 4, 1), ('cos', 4, 2), ('tan', 4, 3), ('e', 4, 4), ('EE', 4, 5), ('1', 4, 6), ('2', 4, 7), ('3', 4, 8), ('+', 4, 9),
            ('Rad', 5, 0), ('sinh', 5, 1), ('cosh', 5, 2), ('tanh', 5, 3), ('π', 5, 4), ('Rand', 5, 5), ('0', 5, 6, 1, 2), ('.', 5, 8), ('=', 5, 9)
        ]

        self.button_map = {}
        for btn_def in buttons:
            btn_text, row, col = btn_def[0], btn_def[1], btn_def[2]
            button = QPushButton(btn_text)
            button.clicked.connect(self.button_clicked)
            font = button.font()
            font.setPointSize(16)
            button.setFont(font)
            button.setSizePolicy(button.sizePolicy().horizontalPolicy(), button.sizePolicy().verticalPolicy())
            
            if btn_text.isdigit() or btn_text == '.':
                button.setStyleSheet('background-color: #333; color: white; border-radius: 25px; height: 40px;')
            elif btn_text in ['/', '*', '-', '+', '=']:
                button.setStyleSheet('background-color: #f09a37; color: white; border-radius: 25px; height: 40px;')
            else:
                button.setStyleSheet('background-color: #a5a5a5; color: black; border-radius: 25px; height: 40px;')

            if len(btn_def) > 3:
                grid.addWidget(button, row, col, btn_def[3], btn_def[4])
            else:
                grid.addWidget(button, row, col)
            
            self.button_map[btn_text] = button

        self.setLayout(grid)
        self.reset_display()

    def reset_display(self):
        """화면과 모든 수식을 초기화한다."""
        self.display_expression = ''
        self.eval_expression = ''
        self.result_display.setText('0')
        self.update_font_size()

    def button_clicked(self):
        """버튼 클릭 이벤트를 통합 처리한다."""
        button = self.sender()
        key = button.text()

        if self.result_display.text() == 'Error' and key != 'AC':
            return

        if key.isdigit() or key == '.':
            self.display_expression += key
            self.eval_expression += key
        elif key in ['+', '-', '*', '/']:
            self.display_expression += f' {key} '
            self.eval_expression += f' {key} '
        elif key == '(':
            self.display_expression += '('
            self.eval_expression += '('
        elif key == ')':
            self.display_expression += ')'
            self.eval_expression += ')'
        elif key == 'π':
            self.display_expression += 'π'
            self.eval_expression += 'math.pi'
        elif key == 'e':
            self.display_expression += 'e'
            self.eval_expression += 'math.e'
        elif key == 'Rand':
            rand_val = str(random.random())
            self.display_expression += rand_val
            self.eval_expression += rand_val
        
        elif key == 'AC':
            self.reset_display()
        elif key == '=':
            self.calculate_result()
        elif key == '+/-':
            self.toggle_sign()
        elif key == '%':
            self.display_expression = f'({self.display_expression})%'
            self.eval_expression = f'({self.eval_expression})/100'
        
        elif key == 'x²':
            self.display_expression = f'({self.display_expression})²'
            self.eval_expression = f'({self.eval_expression})**2'
        elif key == 'x³':
            self.display_expression = f'({self.display_expression})³'
            self.eval_expression = f'({self.eval_expression})**3'
        elif key == '1/x':
            self.display_expression = f'1/({self.display_expression})'
            self.eval_expression = f'1/({self.eval_expression})'
        elif key == '√x':
            self.display_expression = f'√({self.display_expression})'
            self.eval_expression = f'math.sqrt({self.eval_expression})'
        elif key == '∛x':
            self.display_expression = f'∛({self.display_expression})'
            self.eval_expression = f'({self.eval_expression})**(1/3)'
        elif key == 'ln':
            self.display_expression = f'ln({self.display_expression})'
            self.eval_expression = f'math.log({self.eval_expression})'
        elif key == 'log₁₀':
            self.display_expression = f'log({self.display_expression})'
            self.eval_expression = f'math.log10({self.eval_expression})'
        elif key == 'x!':
            self.display_expression = f'fact({self.display_expression})'
            self.eval_expression = f'math.factorial(int({self.eval_expression}))'
        elif key == 'eˣ':
            self.display_expression = f'e^({self.display_expression})'
            self.eval_expression = f'math.exp({self.eval_expression})'
        elif key == '10ˣ':
            self.display_expression = f'10^({self.display_expression})'
            self.eval_expression = f'10**({self.eval_expression})'
        
        elif key == 'xʸ':
            self.display_expression += ' ^ '
            self.eval_expression += ' ** '
        elif key == 'ʸ√x':
            self.display_expression += ' ʸ√ '
            self.eval_expression += ' __yth_root__ ' # Placeholder for special processing
        elif key == 'EE':
            self.display_expression += 'E'
            self.eval_expression += '*10**'

        elif key in ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'sinh⁻¹', 'cosh⁻¹', 'tanh⁻¹']:
            func_map_display = {
                'sin': 'sin', 'cos': 'cos', 'tan': 'tan', 'sinh': 'sinh', 'cosh': 'cosh', 'tanh': 'tanh',
                'sin⁻¹': 'asin', 'cos⁻¹': 'acos', 'tan⁻¹': 'atan', 'sinh⁻¹': 'asinh', 'cosh⁻¹': 'acosh', 'tanh⁻¹': 'atanh'
            }
            func_map_eval = {
                'sin': 'math.sin', 'cos': 'math.cos', 'tan': 'math.tan', 'sinh': 'math.sinh', 'cosh': 'math.cosh', 'tanh': 'math.tanh',
                'sin⁻¹': 'math.asin', 'cos⁻¹': 'math.acos', 'tan⁻¹': 'math.atan', 'sinh⁻¹': 'math.asinh', 'cosh⁻¹': 'math.acosh', 'tanh⁻¹': 'math.atanh'
            }
            self.display_expression = f'{func_map_display[key]}({self.display_expression})'
            if not self.is_rad and key in ['sin', 'cos', 'tan']:
                self.eval_expression = f'{func_map_eval[key]}(math.radians({self.eval_expression}))'
            else:
                self.eval_expression = f'{func_map_eval[key]}({self.eval_expression})'

        elif key == '2nd':
            self.toggle_2nd()
        elif key == 'Rad' or key == 'Deg':
            self.is_rad = not self.is_rad
            self.button_map['Rad'].setText('Rad' if self.is_rad else 'Deg')
        
        elif key == 'mc':
            self.memory = 0
        elif key == 'mr':
            mem_str = str(self.memory)
            self.display_expression += mem_str
            self.eval_expression += mem_str
        elif key == 'm+':
            self.calculate_result(update_memory=1)
        elif key == 'm-':
            self.calculate_result(update_memory=-1)

        if key not in ['2nd', 'Rad', 'Deg', 'm+', 'm-']:
            self.update_display()

    def calculate_result(self, update_memory=0):
        """수식을 계산하고 결과를 처리한다. 특수 연산자와 예외를 처리한다."""
        if not self.eval_expression:
            return
        
        expression_to_eval = self.eval_expression
        
        # ʸ√x 플레이스홀더를 올바른 pow() 함수로 변환
        if '__yth_root__' in expression_to_eval:
            parts = expression_to_eval.split('__yth_root__')
            if len(parts) == 2:
                x_part, y_part = parts[0], parts[1]
                expression_to_eval = f"pow({x_part}, 1/({y_part}))"
            else:
                self.show_error()
                return

        try:
            result = eval(expression_to_eval)
            
            if update_memory == 1:
                self.memory += result
                return
            elif update_memory == -1:
                self.memory -= result
                return

            if isinstance(result, float):
                result = round(result, 10)
                if result.is_integer():
                    result = int(result)
            
            result_str = str(result)
            self.display_expression = result_str
            self.eval_expression = result_str
            self.update_display()

        except (ValueError, TypeError): # math domain error (e.g., acos(5), sqrt(-1))
            self.show_error()
        except ZeroDivisionError:
            self.show_error("Error: Division by zero")
        except SyntaxError:
            self.show_error("Error: Invalid syntax")
        except Exception: # Other potential errors
            self.show_error()

    def show_error(self, message="Error"):
        """에러 메시지를 화면에 표시하고 상태를 초기화한다."""
        self.display_expression = ''
        self.eval_expression = ''
        self.result_display.setText(message)
        self.update_font_size()

    def toggle_sign(self):
        """수식의 마지막 숫자의 부호를 변경한다."""
        # 정규표현식을 사용하여 마지막 숫자(정수 또는 실수)를 찾음
        match = re.search(r'([+\-/*\s(]|^)([\d.]+)$', self.eval_expression)
        if match:
            # 마지막 숫자를 (-숫자) 형태로 변경
            start_pos = match.start(2)
            self.eval_expression = f"{self.eval_expression[:start_pos]}(-{match.group(2)})"
            self.display_expression = self.eval_expression # 간단하게 동기화
        self.update_display()

    def toggle_2nd(self):
        """2nd 버튼 상태를 전환하고 관련 버튼의 텍스트를 변경한다."""
        self.is_2nd = not self.is_2nd
        toggle_buttons = {
            'sin': 'sin⁻¹', 'cos': 'cos⁻¹', 'tan': 'tan⁻¹',
            'sinh': 'sinh⁻¹', 'cosh': 'cosh⁻¹', 'tanh': 'tanh⁻¹'
        }
        for base, second in toggle_buttons.items():
            self.button_map[base].setText(second if self.is_2nd else base)

    def update_display(self):
        """결과창의 내용을 현재 수식으로 업데이트하고 폰트 크기를 조절한다."""
        display_text = self.display_expression if self.display_expression else '0'
        self.result_display.setText(display_text)
        self.update_font_size()

    def update_font_size(self):
        """표시되는 텍스트 길이에 따라 폰트 크기를 동적으로 조절한다."""
        length = len(self.result_display.text())
        font_size = 40
        if length > 15: font_size = 32
        if length > 20: font_size = 24
        if length > 30: font_size = 18
        
        font = self.result_display.font()
        font.setPointSize(font_size)
        self.result_display.setFont(font)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = EngineeringCalculator()
    calc.show()
    sys.exit(app.exec_())