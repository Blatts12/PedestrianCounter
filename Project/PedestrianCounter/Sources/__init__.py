from Project.PedestrianCounter.Sources.FileVideo import FileVideo
from Project.PedestrianCounter.Sources.Webcam import Webcam
from Project.Components.SettingsFormGenerator import SettingsFormGenerator
from Project.Utils.Singleton import Singleton


class Sources(metaclass=Singleton):
    def __init__(self):
        generator = SettingsFormGenerator()
        self.DICT = {
            "Video": generator.generate(FileVideo()),
            "Webcam": generator.generate(Webcam()),
        }
