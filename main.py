from PyQt5.QtWidgets import QApplication
import sys
from calc_ui import CalculatorWithUI


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = CalculatorWithUI()

    ui.show()
    sys.exit(app.exec_())
