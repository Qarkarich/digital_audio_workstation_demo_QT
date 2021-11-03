from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from pathlib import Path


class WAVController(QWidget):
    def __init__(self, window, audiofile):
        super().__init__()
        uic.loadUi(Path('Resources', 'UI', 'wavmodule_design.ui'), self)

        self.audiofile = audiofile
