import logging
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from lumed_andor.andor_widget import AndorCameraWidget

LOG_FORMAT = (
    "%(asctime)s - %(levelname)s"
    "(%(filename)s:%(funcName)s)"
    "(%(filename)s:%(lineno)d) - "
    "%(message)s"
)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
    )
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.show()

    window.setCentralWidget(AndorCameraWidget())

    app.exec_()
