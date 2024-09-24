import math
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QGridLayout,
    QLabel,
    QTabWidget,
    QFormLayout,
    QListWidget,
    QListWidgetItem,
)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

# Константы для текста
TEXT_RESULT = "Результат:"
TEXT_LAST_RESULT = "Последний результат:"
TEXT_ERROR_NOT_DEFINED = "Ошибка: переменная не определена"
TEXT_ERROR = "Ошибка"
TEXT_EMPTY = "Пусто"
TEXT_ADD_VARIABLE = "Добавить переменную"
TEXT_VARIABLE_NAME = "Имя переменной:"
TEXT_VARIABLE_VALUE = "Значение переменной:"
TEXT_ADD = "Добавить"
TEXT_AVAILABLE_VARIABLES = "Доступные переменные:"
TEXT_CALCULATOR = "Калькулятор"
TEXT_VARIABLES = "Переменные"

# Константы для кнопок
UTILS_BUTTONS = ["C", "DEL", "RES"]
MAIN_BUTTONS = [
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
MODE_BUTTONS = ["MOD"]
ADD_VARIABLE_BUTTON = ["ADD_VAR"]

# Константы для позиций кнопок
UTILS_POSITIONS = [(0, 0), (0, 1), (0, 2)]
MAIN_POSITIONS = [(i, j) for i in range(1, 5) for j in range(4)]
MODE_POSITIONS = [(0, 3)]
ADD_VARIABLE_POSITIONS = [(0, 4)]

# Константы для шрифтов
FONT_NAME = "Arial"
FONT_SIZE_HEADER = 14
FONT_SIZE_DISPLAY = 20
FONT_SIZE_BUTTON = 16

# Константы для размеров
BUTTON_SIZE = QSize(60, 60)
DISPLAY_HEIGHT = 40
LAST_RESULT_HEIGHT = 30


class DisplayWidget(QWidget):
    def __init__(self, header_text, height, font_size, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.add_header(header_text)
        self.display = self.create_display(height, font_size)
        self.layout.addWidget(self.display)

    def add_header(self, text):
        header = QLabel(text)
        header.setFont(QFont(FONT_NAME, FONT_SIZE_HEADER))
        self.layout.addWidget(header)

    def create_display(self, height, font_size):
        display = QLineEdit()
        display.setFont(QFont(FONT_NAME, font_size))
        display.setFixedHeight(height)
        return display

    def set_text(self, text):
        self.display.setText(text)

    def get_text(self):
        return self.display.text()


class ButtonWidget(QPushButton):
    def __init__(self, text, callback, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(BUTTON_SIZE)
        self.setFont(QFont(FONT_NAME, FONT_SIZE_BUTTON))
        self.clicked.connect(callback)


class VariablesTab(QWidget):
    def __init__(self, variables, parent=None):
        super().__init__(parent)
        self.variables = variables
        self.layout = QVBoxLayout(self)

        # Добавляем список доступных переменных
        self.variables_list = QListWidget()
        self.update_variables_list()
        self.layout.addWidget(QLabel(TEXT_AVAILABLE_VARIABLES))
        self.layout.addWidget(self.variables_list)

        # Добавляем форму для ввода новой переменной
        form_layout = QFormLayout()
        self.variable_name_input = QLineEdit()
        self.variable_value_input = QLineEdit()
        form_layout.addRow(QLabel(TEXT_VARIABLE_NAME), self.variable_name_input)
        form_layout.addRow(QLabel(TEXT_VARIABLE_VALUE), self.variable_value_input)
        self.layout.addLayout(form_layout)

        add_button = QPushButton(TEXT_ADD)
        add_button.clicked.connect(self.add_variable)
        self.layout.addWidget(add_button)

    def update_variables_list(self):
        self.variables_list.clear()
        for var_name, var_value in self.variables.items():
            item_text = f"{var_name} = {var_value}"
            self.variables_list.addItem(QListWidgetItem(item_text))

    def add_variable(self):
        var_name = self.variable_name_input.text()
        var_value = self.variable_value_input.text()
        if var_name and var_value:
            self.variables[var_name] = var_value
            self.update_variables_list()
            self.variable_name_input.clear()
            self.variable_value_input.clear()


class CalculatorWithUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.font = FONT_NAME
        self.last_result = None
        self.variables = {"RES": "0"}  # Добавляем переменную RES по умолчанию
        self.mode_active = False  # Флаг для отслеживания состояния кнопки MOD
        self.additional_buttons = []  # Список для хранения дополнительных кнопок
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор")
        self.setGeometry(100, 100, 300, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        self.setup_tabs()

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.setup_calculator_tab()
        self.setup_variables_tab()

    def setup_calculator_tab(self):
        calculator_tab = QWidget()
        tab_layout = QVBoxLayout(calculator_tab)

        self.setup_result_display(tab_layout)
        self.setup_last_result_display(tab_layout)
        self.setup_grid_buttons(tab_layout)

        self.tabs.addTab(calculator_tab, TEXT_CALCULATOR)

    def setup_variables_tab(self):
        self.variables_tab = VariablesTab(self.variables)
        self.tabs.addTab(self.variables_tab, TEXT_VARIABLES)

    def setup_result_display(self, layout):
        self.result_display = DisplayWidget(
            TEXT_RESULT, DISPLAY_HEIGHT, FONT_SIZE_DISPLAY
        )
        layout.addWidget(self.result_display)

    def setup_last_result_display(self, layout):
        self.last_result_display = DisplayWidget(
            TEXT_LAST_RESULT, LAST_RESULT_HEIGHT, FONT_SIZE_HEADER
        )
        layout.addWidget(self.last_result_display)

    def setup_grid_buttons(self, layout):
        self.grid_layout = QGridLayout()
        self.add_buttons(UTILS_BUTTONS, UTILS_POSITIONS)
        self.add_buttons(MAIN_BUTTONS, MAIN_POSITIONS)
        self.add_buttons(MODE_BUTTONS, MODE_POSITIONS)
        layout.addLayout(self.grid_layout)

    def add_buttons(self, buttons, positions):
        for position, button_text in zip(positions, buttons):
            button = ButtonWidget(button_text, self.on_button_click)
            self.grid_layout.addWidget(button, *position)
            if button_text == "MOD":
                self.mode_button = button  # Сохраняем ссылку на кнопку MOD

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        if text == "=":
            self.calculate()
            self.show_last_result()
        elif text == "C":
            self.result_display.set_text("")
        elif text == "DEL":
            self.delete_last_character()
        elif text == "MOD":
            self.toggle_mode()  # Переключаем состояние кнопки MOD
        else:
            self.append_to_display(text)

    def calculate(self):
        try:
            expression = self.result_display.get_text()
            for var_name, var_value in self.variables.items():
                expression = expression.replace(var_name, var_value)

            if "RES" in expression and self.last_result:
                expression = expression.replace("RES", self.last_result)
            else:
                expression = expression.replace("RES", "")
            # Обработка математических функций
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")

            # Вычисление выражения и округление результата до двух знаков после запятой
            result = round(eval(expression, {"__builtins__": None}, {"math": math}), 2)
            self.last_result = str(result)
            self.variables["RES"] = (
                self.last_result
            )  # Обновляем значение переменной RES
            self.result_display.set_text(self.last_result)
            self.variables_tab.update_variables_list()  # Обновляем список переменных
        except Exception:
            self.result_display.set_text(TEXT_ERROR)
            self.last_result = None

    def show_last_result(self):
        if self.last_result:
            if (
                self.result_display.display.hasFocus()
            ):  # Проверяем, находится ли курсор в поле "Результат"
                self.result_display.set_text(self.last_result)
            else:
                self.last_result_display.set_text(self.last_result)
        else:
            self.last_result_display.set_text(TEXT_EMPTY)

    def delete_last_character(self):
        current_text = self.result_display.get_text()
        self.result_display.set_text(current_text[:-1])

    def append_to_display(self, text):
        current_text = self.result_display.get_text()
        self.result_display.set_text(current_text + text)

    def toggle_mode(self):
        self.mode_active = not self.mode_active  # Переключаем флаг
        if self.mode_active:
            self.add_additional_buttons()
        else:
            self.remove_additional_buttons()

    def add_additional_buttons(self):
        # Добавляем новые кнопки
        additional_buttons = ["sin", "cos", "tan"]
        additional_positions = [(5, 0), (5, 1), (5, 2)]
        for position, button_text in zip(additional_positions, additional_buttons):
            button = ButtonWidget(button_text, self.on_button_click)
            self.grid_layout.addWidget(button, *position)
            self.additional_buttons.append(button)

    def remove_additional_buttons(self):
        # Удаляем добавленные кнопки
        for button in self.additional_buttons:
            self.grid_layout.removeWidget(button)
            button.setParent(None)
        self.additional_buttons.clear()
