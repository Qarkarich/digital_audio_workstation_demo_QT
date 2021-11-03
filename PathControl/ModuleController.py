modules_names = {
    'WAV-файл (*.wav)': 'WAVController',
    'MIDI-файл (*.midi)': 'MIDIController'
}
modules_path = 'Modules'


class ModuleController:
    def get_path(format):
        return modules_path, modules_names[format]
