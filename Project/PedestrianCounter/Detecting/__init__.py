from Project.PedestrianCounter.Detecting.YoloV5m import YoloV5m
from Project.PedestrianCounter.Detecting.MobileNetSSD import MobileNetSSD
from Project.PedestrianCounter.Detecting.YoloV4Tiny import YoloV4Tiny
from Project.Components.SettingsFormGenerator import SettingsFormGenerator
from Project.Utils.Singleton import Singleton


class Detectors(metaclass=Singleton):
    def __init__(self):
        generator = SettingsFormGenerator()
        self.DICT = {
            "MobileNet SDD": generator.generate(MobileNetSSD()),
            "YoloV4-tiny": generator.generate(YoloV4Tiny()),
            "YoloV5m": generator.generate(YoloV5m()),
        }

    def get_first(self):
        return list(self.DICT)[0]
