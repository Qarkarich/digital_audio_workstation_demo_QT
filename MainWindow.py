import shutil
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QFileSystemModel
from PathControl import ModuleController


class MainWindow(QMainWindow):
    def __init__(self):
        # инициализация приложения, выбор файла, подключение необходимых модулей
        super().__init__()
        uic.loadUi('Resources/UI/main_window_interface.ui', self)

        self._connectActions()
        self.model = QFileSystemModel()

        self.fname, self.fformat = QFileDialog.getOpenFileName(
            self, 'Выбор файла...', '',
            'WAV-файл (*.wav)')

        self.setWindowTitle(self.fname)

        self.controller = ModuleController.ModuleController.get_control(self.fformat)(self.fname)
        self.horizontalLayout.addWidget(self.controller)

        self.update_file_manager(self.fname)

    def update_file_manager(self, name):
        dir_path = name.split('/')
        dir_path = '/'.join(dir_path[:-1]) + '/'
        self.model.setRootPath(dir_path)
        self.file_manager_widget.setModel(self.model)
        self.file_manager_widget.setRootIndex(self.model.index(dir_path))

    def save_file(self):
        file = QFileDialog.getSaveFileName(self, 'Сохранить...', '', 'WAV-файл (*.wav)')
        shutil.copy2(self.controller.get_audio()[0], file[0])

    def load_file_dialog(self):
        file = QFileDialog.getOpenFileName(self, 'Открыть файл...', '', 'WAV-файл (*.wav)')
        self.load_file(file[0])

    def load_file_widget(self):
        file_path = self.file_manager_widget.currentIndex().data().split('.')
        if file_path[1] == 'wav':
            file_path = f"{'/'.join(self.fname.split('/')[:-1])}/{file_path[0]}.{file_path[1]}"
            self.load_file(file_path)

    def load_file(self, file_path):
        self.horizontalLayout.removeWidget(self.controller)
        del self.controller
        self.controller = ModuleController.ModuleController.get_control(self.fformat)(file_path)
        self.horizontalLayout.addWidget(self.controller)
        self.window().setWindowTitle(file_path)
        self.update_file_manager(file_path)

    def _connectActions(self):
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionOpen_file.triggered.connect(self.load_file_dialog)
        self.actionOpen_file.setShortcut("Ctrl+O")
        self.load_audio_btn.clicked.connect(self.load_file_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
