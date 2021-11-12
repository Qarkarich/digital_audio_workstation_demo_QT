from Modules import WAVController

# вынес словарь значений отдельно для возможности замены сторонним файлом, подключением и т.д.

modules_names = {
    'WAV-файл (*.wav)': WAVController.WAVController,
}
modules_path = 'Modules'


class ModuleController:
    @staticmethod
    def get_control(fformat):
        return modules_names[fformat]


