import shutil
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PathControl import ModuleController, SampleController


class MainWindow(QMainWindow):
    def __init__(self):
        # инициализация приложения, выбор файла, подключение необходимых модулей
        super().__init__()
        uic.loadUi('Resources/UI/main_window_interface.ui', self)

        self._connectActions()

        fname, fformat = QFileDialog.getOpenFileName(
            self, 'Выбор файла...', '',
            'WAV-файл (*.wav);;MIDI-файл (*.midi)')

        self.setWindowTitle(fname)

        self.sample_manager = SampleController.SampleController()

        self.controller = ModuleController.ModuleController.get_control(fformat)(fname)
        self.horizontalLayout.addWidget(self.controller)

        self.update_file_manager()

    def update_file_manager(self):
        for i in self.sample_manager.index_samples():
            self.file_manager_widget.addItem(i[0])

    def save_file(self):
        file = QFileDialog.getSaveFileName(self, 'Сохранить...', '', 'WAV-файл (*.wav)')
        shutil.copy2(self.controller.get_audio(), file[0])

    def load_file(self):
        file = QFileDialog.getOpenFileName(self, 'Открыть файл...', '', 'WAV-файл (*.wav)')
        self.horizontalLayout.removeWidget(self.controller)
        del self.controller
        self.controller = ModuleController.ModuleController.get_control('WAV-файл (*.wav)')(file[0])
        self.horizontalLayout.addWidget(self.controller)
        self.window().setWindowTitle(file[0])

    def create_sample(self):
        sample = QFileDialog.getSaveFileName(self, 'Сохранить...')


    def _connectActions(self):
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionOpen_file.triggered.connect(self.load_file)
        self.actionOpen_file.setShortcut("Ctrl+O")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet('QMainWindow {background-color: #000000}') TODO: наладь коннект стилей потом!!!!
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
