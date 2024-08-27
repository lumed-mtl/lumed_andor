import logging
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from lumed_andor.andor_widget import AndorCameraWidget

logger = logging.getLogger()

LOG_FORMAT = (
    "%(asctime)s - %(levelname)s"
    "(%(filename)s:%(funcName)s)"
    "(%(filename)s:%(lineno)d) - "
    "%(message)s"
)


if __name__ == "__main__":

    formatter = logging.Formatter(LOG_FORMAT)
    terminal_handler = logging.StreamHandler()
    terminal_handler.setFormatter(formatter)
    logger.addHandler(terminal_handler)
    logger.setLevel(logging.INFO)

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.show()

    window.setCentralWidget(AndorCameraWidget())

    app.exec_()
