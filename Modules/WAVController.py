import wave

from PyQt5.QtWidgets import QWidget
from PyQt5 import uic, QtMultimedia
from pathlib import Path
import pyqtgraph
import numpy


class WAVController(QWidget):
    def __init__(self, audioFile):
        super().__init__()
        uic.loadUi(Path('Resources', 'UI', 'wavmodule_design.ui'), self)

        # открытие файла

        with wave.open(audioFile) as audioFile:
            # получение необходимых данных
            self.channels = audioFile.getnchannels()
            self.frameRate = audioFile.getframerate()
            self.sampleWidth = audioFile.getsampwidth()
            self.framesNumber = audioFile.getnframes()
            self.duration = self.framesNumber / self.frameRate

            # !!! шаг пропуска значений аудио, позволяет не тратить много ресурсов на визуализацию
            # и не рендерить 6e+06 точек в секунду, чем больше значение, тем меньше качество и выше
            # производительность
            # значение шага взято на глаз. с математической точки зрения неккоректно, однако
            # для визуализации волны подходит

            step = 100

            # приведение аудио к графическому виду

            self.audioData = audioFile.readframes(-1)
            self.audioData = numpy.fromstring(self.audioData, "Int32")[::step]
            self.defaultData = self.audioData.copy()

            # настройки вывода

            self.waveOutput.setMouseEnabled(x=False, y=True)
            self.waveOutput.getAxis('left').hide()
            self.waveOutput.getAxis('bottom').hide()

            # self.waveOutput.plot(self.audioData
            # playbackFile = self.update_wave()
            # playbackFile.setnchannels(self.channels)

            # коннекты событий

            self.volumeChanger.sliderReleased.connect(self.change_volume)
            self.pitchChanger.sliderReleased.connect(self.change_pitch)
            self.speedChanger.sliderReleased.connect(self.change_playback_speed)
            self.playBtn.clicked.connect(self.player.play)
            self.pauseBtn.clicked.connect(self.player.pause)
            self.stopBtn.clicked.connect(self.player.stop)

    # измение громкости
    def change_volume(self):
        self.audioData = [i * (self.volumeChanger.value() / 100) for i in self.defaultData]
        self.update_wave()

    # изменение тона
    def change_pitch(self):
        pass

    # изменение скорости проигрывания
    def change_playback_speed(self):
        pass

    def update_wave(self):
        self.waveOutput.plot(self.audioData, clear=True)
