from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QGridLayout,
    QLabel,
)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

utils_but = ["C", "DEL", "RES"]

main_buttons = [
    "7",
    "8",
    "9",
    "/",
    "4",
    "5",
    "6",
    "*",
    "1",
    "2",
    "3",
    "-",
    "0",
    ".",
    "=",
    "+",
]
mode_but = ["MODE"]
mode_pos = [(0, 3)]
utils_pos = [(0, 0), (0, 1), (0, 2)]
main_but_pos = [(i, j) for i in range(1, 5) for j in range(4)]


class CalculatorWithUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.font = "Arial"
        self.last_result = None
        self.x_value = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор")
        self.setGeometry(100, 100, 300, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        self.setup_result_display()
        self.setup_last_result_display()
        self.setup_grid_buttons()
        self.setup_x_input()

    def setup_result_display(self):
        # Result Display
        display_layout = QVBoxLayout()  # Layout
        display_header = QLabel("Результат:")
        display_header.setFont(QFont(self.font, 14))
        display_layout.addWidget(display_header)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFont(QFont(self.font, 20))
        self.display.setFixedHeight(40)

        display_layout.addWidget(self.display)

        self.layout.addLayout(display_layout)

    def setup_last_result_display(self):
        # Last Result Display with Header
        last_result_layout = QVBoxLayout()

        # Header for Last Result Display
        last_result_header = QLabel("Последний результат:")
        last_result_header.setFont(QFont(self.font, 14))
        last_result_layout.addWidget(last_result_header)
        # Last Result Display
        self.last_result_display = QLineEdit()
        self.last_result_display.setReadOnly(True)
        self.last_result_display.setFont(QFont(self.font, 14))
        self.last_result_display.setFixedHeight(30)
        last_result_layout.addWidget(self.last_result_display)

        self.layout.addLayout(last_result_layout)

    def setup_grid_buttons(self):
        # Buttons
        self.grid_layout = QGridLayout()

        self.add_buttons(utils_but, utils_pos)
        self.add_buttons(main_buttons, main_but_pos)

        self.layout.addLayout(self.grid_layout)

    def setup_x_input(self):
        # X Input Display with Header
        x_input_layout = QVBoxLayout()

        # Header for X Input Display
        x_input_header = QLabel("Значение x:")
        x_input_header.setFont(QFont(self.font, 14))
        x_input_layout.addWidget(x_input_header)
        # X Input Display
        self.x_input = QLineEdit()
        self.x_input.setFont(QFont(self.font, 14))
        self.x_input.setFixedHeight(30)
        x_input_layout.addWidget(self.x_input)

        # Button to insert x into the expression
        insert_x_button = QPushButton("Вставить x")
        insert_x_button.setFont(QFont(self.font, 14))
        insert_x_button.clicked.connect(self.insert_x)
        x_input_layout.addWidget(insert_x_button)

        self.layout.addLayout(x_input_layout)

    def insert_x(self):
        x_value = self.x_input.text()
        if x_value:
            self.display.setText(self.display.text() + "x")

    def add_buttons(self, buttons: list[str], positions: list[tuple[int]]):
        for position, button_text in zip(positions, buttons):
            button = QPushButton(button_text)
            button.setFixedSize(QSize(60, 60))
            button.setFont(QFont(self.font, 16))
            button.clicked.connect(self.on_button_click)
            self.grid_layout.addWidget(button, *position)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        if text == "=":
            self.calculate()
        elif text == "C":
            self.display.clear()
        elif text == "RES":
            if self.last_result:
                self.last_result_display.setText(self.last_result)
            else:
                self.last_result_display.setText("Пусто")
        elif text == "DEL":
            self.display.setText(self.display.text()[:-1])
        else:
            self.display.setText(self.display.text() + text)

    def calculate(self):
        try:
            expression = self.display.text()
            if "x" in expression:
                x_value = self.x_input.text()
                if x_value:
                    expression = expression.replace("x", x_value)
                else:
                    self.display.setText("Ошибка: x не определено")
                    return

            result = str(eval(expression))
            self.last_result = result
            self.display.setText(result)
        except Exception as e:
            self.display.setText("Ошибка")
            self.last_result = None
