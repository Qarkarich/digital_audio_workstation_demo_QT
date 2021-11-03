import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PathControl.ModuleController import ModuleController


class MainWindow(QMainWindow):
    def __init__(self):
        # инициализация приложения, выбор файла, подключение необходимых модулей
        super().__init__()
        uic.loadUi('Resources/UI/main_window_interface.ui', self)

        fname, fformat = QFileDialog.getOpenFileName(
            self, 'Выбор файла...', '',
            'WAV-файл (*.wav);;MIDI-файл (*.midi)')

        controller = ModuleController.get_path(fformat)
        self.horizontalLayout.addWidget(controller(self, fname))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet('QMainWindow {background-color: #000000}') TODO: наладь коннект стилей потом!!!!
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
