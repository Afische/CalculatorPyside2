from calculatorUI import Calculator
from PySide2.QtWidgets import QApplication
import sys

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    window.setFixedSize(300,400)
    window.setWindowTitle("Adam's Calculator")

    app.exec_()
    sys.exit(0)