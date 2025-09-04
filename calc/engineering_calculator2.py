import sys
import math
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
        self.expression = ''

    def negative_positive(self):
        if self.current != '0':
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.expression = self.current

    def percent(self):
        self.current = str(float(self.current) / 100)
        self.expression = self.current

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
            self.expression = self.current
            self.previous = None
            self.operator = None
            self.is_new = True
        except ValueError:
            self.current = 'Error'
            self.expression = 'Error'
        except OverflowError:
            self.current = 'Overflow'
            self.expression = 'Overflow'

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
        self.expression += text


class EngineeringCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.memory = 0
        self.deg = True  # True for degrees, False for radians

    # 공학용 계산기에서 추가된 30가지 기능 정리 (추가 버튼/기능 목록):
    # 1. 2nd (secondary function toggle)
    # 2. ( (open parenthesis)
    # 3. ) (close parenthesis)
    # 4. mc (memory clear)
    # 5. m+ (memory add)
    # 6. m- (memory subtract)
    # 7. mr (memory recall)
    # 8. EE (scientific notation)
    # 9. x² (square)
    # 10. x³ (cube)
    # 11. x^y (power)
    # 12. e^x (exponential e)
    # 13. 10^x (exponential 10)
    # 14. √ (square root)
    # 15. ∛ (cube root)
    # 16. ln (natural log)
    # 17. log (log base 10)
    # 18. sin (sine)
    # 19. cos (cosine)
    # 20. tan (tangent)
    # 21. sinh (hyperbolic sine)
    # 22. cosh (hyperbolic cosine)
    # 23. tanh (hyperbolic tangent)
    # 24. Rad/Deg (toggle radians/degrees)
    # 25. Rand (random number)
    # 26. 1/x (reciprocal)
    # 27. pi (pi constant)
    # 28. e (e constant)
    # 29. ! (factorial)
    # 30. inverse functions (via 2nd, e.g., arcsin)

    def sin(self):
        try:
            f = float(self.current)
            if self.deg:
                f = math.radians(f)
            return math.sin(f)
        except (ValueError, OverflowError):
            raise ValueError("Invalid input for sin")

    def cos(self):
        try:
            f = float(self.current)
            if self.deg:
                f = math.radians(f)
            return math.cos(f)
        except (ValueError, OverflowError):
            raise ValueError("Invalid input for cos")

    def tan(self):
        try:
            f = float(self.current)
            if self.deg:
                f = math.radians(f)
                if math.cos(f) == 0:
                    raise ValueError("Tan undefined at this angle")
            return math.tan(f)
        except (ValueError, OverflowError):
            raise ValueError("Invalid input for tan")

    def sinh(self):
        try:
            return math.sinh(float(self.current))
        except (ValueError, OverflowError):
            raise ValueError("Invalid input for sinh")

    def cosh(self):
        try:
            return math.cosh(float(self.current))
        except (ValueError, OverflowError):
            raise ValueError("Invalid input for cosh")

    def tanh(self):
        try:
            return math.tanh(float(self.current))
        except (ValueError, OverflowError):
            raise ValueError("Invalid input for tanh")

    def pi(self):
        return math.pi

    def square(self):
        try:
            return float(self.current) ** 2
        except (ValueError, OverflowError):
            raise ValueError("Invalid input for square")

    def cube(self):
        try:
            return float(self.current) ** 3
        except (ValueError, OverflowError):
            raise ValueError("Invalid input for cube")

    def memory_clear(self):
        self.memory = 0

    def memory_add(self):
        try:
            self.memory += float(self.current)
        except (ValueError, OverflowError):
            raise ValueError("Invalid memory operation")

    def memory_subtract(self):
        try:
            self.memory -= float(self.current)
        except (ValueError, OverflowError):
            raise ValueError("Invalid memory operation")

    def memory_recall(self):
        return self.memory


class EngineeringCalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = EngineeringCalculator()
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont('Arial', 30))
        grid = QGridLayout()
        grid.addWidget(self.display, 0, 0, 1, 9)
        left_buttons = [
            ['2nd', '(', ')', 'mc', 'mr'],
            ['m+', 'm-', 'EE', 'x²', 'x³'],
            ['x^y', 'e^x', '10^x', '√', '∛'],
            ['ln', 'log', 'sin', 'cos', 'tan'],
            ['sinh', 'cosh', 'tanh', 'Rad', 'Rand']
        ]
        self.button_map = {}
        for r, row_buttons in enumerate(left_buttons, start=1):
            for c, label in enumerate(row_buttons):
                button = QPushButton(label)
                button.clicked.connect(self.handle_button)
                grid.addWidget(button, r, c)
                self.button_map[label] = button
        right_buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        for r, row_buttons in enumerate(right_buttons, start=1):
            for c, label in enumerate(row_buttons):
                button = QPushButton(label)
                button.clicked.connect(self.handle_button)
                if r == 5 and c == 0:
                    grid.addWidget(button, r, 5, 1, 2)
                elif r == 5 and c == 1:
                    grid.addWidget(button, r, 7)
                elif r == 5 and c == 2:
                    grid.addWidget(button, r, 8)
                else:
                    grid.addWidget(button, r, c + 5)
                self.button_map[label] = button
        self.setLayout(grid)
        self.setWindowTitle('Engineering Calculator')
        self.resize(600, 400)
        self.update_rad_deg_button()

    def update_rad_deg_button(self):
        button = self.button_map.get('Rad')
        if button:
            button.setText('Deg' if self.calculator.deg else 'Rad')

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
            self.calculator.expression += f' {text} '
        elif text == '=':
            self.calculator.equal()
        elif text == 'AC':
            self.calculator.reset()
            self.calculator.expression = ''
        elif text == '+/-':
            self.calculator.negative_positive()
        elif text == '%':
            self.calculator.percent()
        elif text == 'sin':
            try:
                self.calculator.expression = f'sin({self.calculator.current})'
                self.calculator.current = str(self.calculator.sin())
            except ValueError:
                self.calculator.current = 'Error'
                self.calculator.expression = 'Error'
        elif text == 'cos':
            try:
                self.calculator.expression = f'cos({self.calculator.current})'
                self.calculator.current = str(self.calculator.cos())
            except ValueError:
                self.calculator.current = 'Error'
                self.calculator.expression = 'Error'
        elif text == 'tan':
            try:
                self.calculator.expression = f'tan({self.calculator.current})'
                self.calculator.current = str(self.calculator.tan())
            except ValueError:
                self.calculator.current = 'Error'
                self.calculator.expression = 'Error'
        elif text == 'sinh':
            try:
                self.calculator.expression = f'sinh({self.calculator.current})'
                self.calculator.current = str(self.calculator.sinh())
            except ValueError:
                self.calculator.current = 'Error'
                self.calculator.expression = 'Error'
        elif text == 'cosh':
            try:
                self.calculator.expression = f'cosh({self.calculator.current})'
                self.calculator.current = str(self.calculator.cosh())
            except ValueError:
                self.calculator.current = 'Error'
                self.calculator.expression = 'Error'
        elif text == 'tanh':
            try:
                self.calculator.expression = f'tanh({self.calculator.current})'
                self.calculator.current = str(self.calculator.tanh())
            except ValueError:
                self.calculator.current = 'Error'
                self.calculator.expression = 'Error'
        elif text == 'x²':
            try:
                self.calculator.expression = f'({self.calculator.current})²'
                self.calculator.current = str(self.calculator.square())
            except ValueError:
                self.calculator.current = 'Error'
                self.calculator.expression = 'Error'
        elif text == 'x³':
            try:
                self.calculator.expression = f'({self.calculator.current})³'
                self.calculator.current = str(self.calculator.cube())
            except ValueError:
                self.calculator.current = 'Error'
                self.calculator.expression = 'Error'
        elif text == 'pi':
            self.calculator.current = str(self.calculator.pi())
            self.calculator.expression = 'π'
        elif text == 'mc':
            self.calculator.memory_clear()
            self.calculator.expression = ''
        elif text == 'm+':
            try:
                self.calculator.memory_add()
                self.calculator.expression = f'M+({self.calculator.current})'
            except ValueError:
                self.calculator.expression = 'Error'
        elif text == 'm-':
            try:
                self.calculator.memory_subtract()
                self.calculator.expression = f'M-({self.calculator.current})'
            except ValueError:
                self.calculator.expression = 'Error'
        elif text == 'mr':
            self.calculator.current = str(self.calculator.memory_recall())
            self.calculator.expression = 'MR'
        elif text == 'Rad':
            self.calculator.deg = not self.calculator.deg
            self.update_rad_deg_button()
        # Other buttons (e.g., 2nd, EE, x^y) are not implemented per requirements
        self.update_display()

    def update_display(self):
        text = self.calculator.expression or self.calculator.current
        length = len(text)
        if length > 10:
            font_size = 30 * 10 / length
        else:
            font_size = 30
        self.display.setFont(QFont('Arial', int(font_size)))
        if '.' in text and text not in ('Error', 'Overflow'):
            try:
                f = float(text)
                text = '{:.6f}'.format(f).rstrip('0').rstrip('.')
            except ValueError:
                pass
        self.display.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = EngineeringCalculatorUI()
    calc.show()
    sys.exit(app.exec_())