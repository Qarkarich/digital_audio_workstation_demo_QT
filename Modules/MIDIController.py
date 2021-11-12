import time

import pygame.midi
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from pathlib import Path
from pygame import midi, mixer


class MIDIController(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(Path('Resources', 'UI', 'design.ui'), self)

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.midi.init()
        self.player = pygame.midi.Output(1)
        self.player.set_instrument(4)

        self.print_checked()

    def print_checked(self):
        # print(self.butttons.checkedButton().objectName())

        self.player.note_on(70, 127, 20)
        self.player.note_off(70, 127, 1)
