import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Calculator:
    def __init__(self):
        self.reset()

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def reset(self):
        self.current = '0'
        self.operator = None
        self.previous = None
        self.is_new = True

    def negative_positive(self):
        if self.current != '0':
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current

    def percent(self):
        self.current = str(float(self.current) / 100)

    def equal(self):
        if self.operator is None:
            return
        try:
            a = float(self.previous)
            b = float(self.current)
            if self.operator == '+':
                result = self.add(a, b)
            elif self.operator == '-':
                result = self.subtract(a, b)
            elif self.operator == '*':
                result = self.multiply(a, b)
            elif self.operator == '/':
                result = self.divide(a, b)
            self.current = str(result)
            self.previous = None
            self.operator = None
            self.is_new = True
        except ValueError:
            self.current = 'Error'
        except OverflowError:
            self.current = 'Overflow'

    def input_number(self, text):
        if self.is_new:
            self.current = '0'
            self.is_new = False
        if text == '.':
            if '.' in self.current:
                return
            self.current += '.'
        else:
            if self.current == '0':
                self.current = text
            else:
                self.current += text

class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont('Arial', 30))
        grid = QGridLayout()
        grid.addWidget(self.display, 0, 0, 1, 4)
        buttons = [
            'AC', '+/-', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '='
        ]
        positions = [
            (1, 0), (1, 1), (1, 2), (1, 3),
            (2, 0), (2, 1), (2, 2), (2, 3),
            (3, 0), (3, 1), (3, 2), (3, 3),
            (4, 0), (4, 1), (4, 2), (4, 3),
            (5, 0), (5, 2), (5, 3)
        ]
        self.button_map = {}
        for label, pos in zip(buttons, positions):
            button = QPushButton(label)
            button.clicked.connect(self.handle_button)
            if label == '0':
                grid.addWidget(button, pos[0], pos[1], 1, 2)
            else:
                grid.addWidget(button, pos[0], pos[1])
            self.button_map[label] = button
        self.setLayout(grid)
        self.setWindowTitle('Calculator')
        self.resize(300, 400)

    def handle_button(self):
        sender = self.sender()
        text = sender.text()
        if text in '0123456789.':
            self.calculator.input_number(text)
        elif text in '+-*/':
            if self.calculator.operator is not None:
                self.calculator.equal()
            self.calculator.previous = self.calculator.current
            self.calculator.operator = text
            self.calculator.is_new = True
        elif text == '=':
            self.calculator.equal()
        elif text == 'AC':
            self.calculator.reset()
        elif text == '+/-':
            self.calculator.negative_positive()
        elif text == '%':
            self.calculator.percent()
        self.update_display()

    def update_display(self):
        text = self.calculator.current
        length = len(text)
        if length > 10:
            font_size = 30 * 10 / length
        else:
            font_size = 30
        self.display.setFont(QFont('Arial', int(font_size)))
        if '.' in text:
            try:
                f = float(text)
                text = '{:.6f}'.format(f).rstrip('0').rstrip('.')
            except ValueError:
                pass
        self.display.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())