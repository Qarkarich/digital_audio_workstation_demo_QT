from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from pathlib import Path


class WAVController(QWidget):
    def __init__(self, window):
        super().__init__()
        uic.loadUi(Path('Resources', 'Designs', 'wavmodule_design.ui'), self)