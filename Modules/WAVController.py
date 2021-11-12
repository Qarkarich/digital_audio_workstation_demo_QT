import os
import atexit
import shutil
import wave
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic, QtMultimedia
from pathlib import Path
import pyqtgraph
import numpy
from pydub import AudioSegment


class WAVController(QWidget):
    def __init__(self, file):
        super().__init__()
        uic.loadUi(Path('Resources', 'UI', 'wavmodule_design.ui'), self)

        atexit.register(self.clear_data)
        self.permSampleName = 'TestSample.wav'
        self.permSampleFullPath = f"{os.getcwd()}/Modules/{self.permSampleName}"
        shutil.copy2(file, self.permSampleFullPath[:len(file) - 1] + self.permSampleName)

        self.player = QtMultimedia.QMediaPlayer()
        # открытие файла

        with wave.open(file, 'r') as audioFile:
            # получение необходимых данных
            self.channels, self.sampleWidth, self.frameRate, self.framesNumber, self.compType, \
            self.compName = audioFile.getparams()

            # !!! шаг пропуска значений аудио, позволяет не тратить много ресурсов на визуализацию
            # и не рендерить 6e+06 или еще больше точек в секунду, чем больше значение,
            # тем меньше качество и выше производительность
            # значение шага взято на глаз. с математической точки зрения неккоректно, однако
            # для простой визуализации подходит

            step = 100

            # открытие файлов

            self.audio = audioFile.readframes(-1)

            self.audioData = AudioSegment.from_wav(file)

            self.player.setMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile(file)))

            # приведение аудио к графическому виду

            self.displayData = numpy.fromstring(self.audio, "Int32")[::step]

            self.defaultDisplayData = self.displayData.copy()

            # настройки вывода

            self.waveOutput.setMouseEnabled(x=False, y=True)
            self.waveOutput.getAxis('left').hide()
            self.waveOutput.getAxis('bottom').hide()

            self.waveOutput.plot(self.displayData)

        # коннекты событий

        self.playBtn.clicked.connect(self.player.play)
        self.pauseBtn.clicked.connect(self.player.pause)
        self.stopBtn.clicked.connect(self.player.stop)

        self.volumeChanger.sliderReleased.connect(self.change_volume)
        self.speedChanger.sliderReleased.connect(self.change_playback_speed)

    # измение громкости
    def change_volume(self):
        self.displayData = [i * (self.volumeChanger.value() / 100) for i in self.defaultDisplayData]
        self.update_wave()
        if self.volumeChanger.value() > 0:
            volume_value = (self.volumeChanger.value() - 50) / 5
            output_data = self.audioData + volume_value
        else:
            output_data = self.audioData * 0
        self.export_wav_tempor(output_data)
        self.update_player(self.permSampleName)

    # изменение скорости проигрывания
    def change_playback_speed(self):
        playback_speed = (self.speedChanger.value() / 100) * 2
        output_data = self.audioData._spawn(self.audioData.raw_data, overrides={
            "frame_rate": int(self.audioData.frame_rate * playback_speed)
        })
        self.export_wav_tempor(output_data.set_frame_rate(self.frameRate))
        self.update_player(self.permSampleName)

    def update_wave(self):
        self.waveOutput.plot(self.displayData, clear=True)

    def update_player(self, audio):
        media = QUrl.fromLocalFile(f'{os.getcwd()}/Modules/{audio}')
        content = QtMultimedia.QMediaContent(media)
        self.player.setMedia(content)

    def get_audio(self):
        return (self.permSampleName, self.permSampleFullPath)

    def export_wav_tempor(self, data):
        data.export(self.permSampleFullPath, format='wav')

    def clear_data(self):
        if Path(self.permSampleFullPath).exists():
            os.remove(self.permSampleFullPath)
        del self.player
