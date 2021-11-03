import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PathControl.ModuleController import ModuleController
from Modules.WAVController import WAVController


class MainWindow(QMainWindow):
    def __init__(self):
        # инициализация окон, выбор файла, подключение необходимых модулей
        super().__init__()
        uic.loadUi('Resources/Designs/main_window_interface.ui', self)

        filename, file_format = QFileDialog.getOpenFileName(
            self, 'Выбор файла...', '',
            'WAV-файл (*.wav);;MIDI-файл (*.midi)')

        controller = WAVController(self)
        self.horizontalLayout.addWidget(controller)

        # controller = from ModuleController.get_path(file_format)[0] __import__(ModuleController.f)

        # self.horizontalLayout.addWidget(ModuleController.get_path(file_format)[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet('QMainWindow {background-color: #000000}') TODO: наладь коннект стилей потом!!!!
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
