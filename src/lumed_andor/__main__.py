import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from lumed_andor.andor_widget import AndorCameraWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.show()

    window.setCentralWidget(AndorCameraWidget())

    app.exec_()
