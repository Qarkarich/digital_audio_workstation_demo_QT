from Modules import WAVController, MIDIController

# import pathlib

# вынес словарь значений отдельно для возможности замены сторонним файлом, подключением и т.д.
# для теоритического расширения проекта вполне удобно, мне кажется
modules_names = {
    'WAV-файл (*.wav)': WAVController.WAVController,
    'MIDI-файл (*.midi)': MIDIController.MIDIController
}
modules_path = 'Modules'


class ModuleController:
    @staticmethod
    def get_control(fformat):
        return modules_names[fformat]


