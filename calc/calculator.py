# calculator.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QSizePolicy
from PyQt5.QtCore import Qt
import math

class CalculatorLogic:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_input = '0'
        self.previous_input = ''
        self.operation = None
        self.has_decimal = False
        self.result_shown = False
        return self.current_input

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

    def negative_positive(self):
        try:
            value = float(self.current_input)
            self.current_input = str(-value) if value != 0 else '0'
            return self.current_input
        except ValueError:
            return self.current_input

    def percent(self):
        try:
            value = float(self.current_input) / 100
            self.current_input = str(value)
            return self.current_input
        except ValueError:
            return self.current_input

    def equal(self):
        if self.operation is None or self.previous_input == '':
            return self.current_input

        try:
            a = float(self.previous_input)
            b = float(self.current_input)
            if self.operation == '+':
                result = self.add(a, b)
            elif self.operation == '-':
                result = self.subtract(a, b)
            elif self.operation == '*':
                result = self.multiply(a, b)
            elif self.operation == '/':
                result = self.divide(a, b)
            else:
                return 'Error'

            # Handle overflow
            if math.isinf(result) or math.isnan(result):
                return 'Error'

            # Bonus: Round to 6 decimal places if necessary
            if abs(result) - abs(int(result)) > 0:
                result = round(result, 6)
                if result == int(result):
                    result = int(result)

            return str(result)
        except ValueError:
            return 'Error'

class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = CalculatorLogic()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(300, 400)

        layout = QGridLayout()
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 40px;")
        layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ('AC', 1, 0), ('+/-', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 1, 2), ('.', 5, 2), ('=', 5, 3)
        ]

        self.button_map = {}
        for btn_text, row, col, *span in buttons:
            button = QPushButton(btn_text)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if len(span) == 2:
                layout.addWidget(button, row, col, span[0], span[1])
            else:
                layout.addWidget(button, row, col)
            button.clicked.connect(self.button_clicked)
            self.button_map[btn_text] = button

        self.setLayout(layout)

    def button_clicked(self):
        sender = self.sender()
        text = sender.text()

        if text in '0123456789':
            self.handle_number(text)
        elif text == '.':
            self.handle_decimal()
        elif text in '+-*/':
            self.handle_operation(text)
        elif text == '=':
            self.handle_equal()
        elif text == 'AC':
            result = self.logic.reset()
            self.update_display(result)
        elif text == '+/-':
            result = self.logic.negative_positive()
            self.update_display(result)
        elif text == '%':
            result = self.logic.percent()
            self.update_display(result)

    def handle_number(self, num):
        if self.logic.result_shown:
            self.logic.current_input = num
            self.logic.result_shown = False
        elif self.logic.current_input == '0':
            self.logic.current_input = num
        else:
            self.logic.current_input += num
        self.update_display()

    def handle_decimal(self):
        if self.logic.result_shown:
            self.logic.current_input = '0.'
            self.logic.has_decimal = True
            self.logic.result_shown = False
        elif not self.logic.has_decimal:
            self.logic.current_input += '.'
            self.logic.has_decimal = True
        self.update_display()

    def handle_operation(self, op):
        if self.logic.operation is not None:
            self.handle_equal()
        self.logic.previous_input = self.logic.current_input
        self.logic.operation = op
        self.logic.current_input = '0'
        self.logic.has_decimal = False
        self.logic.result_shown = False

    def handle_equal(self):
        result = self.logic.equal()
        self.logic.current_input = result
        self.logic.operation = None
        self.logic.previous_input = ''
        self.logic.has_decimal = '.' in result
        self.logic.result_shown = True
        self.update_display(result)

    def update_display(self, text=None):
        if text is None:
            display_text = self.logic.current_input
        else:
            display_text = text
        # Bonus: Adjust font size based on length
        length = len(str(display_text))  # Ensure str
        if length > 10:
            font_size = max(20, 40 - (length - 10) * 2)
        else:
            font_size = 40
        self.display.setStyleSheet(f"font-size: {font_size}px;")
        self.display.setText(str(display_text))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())