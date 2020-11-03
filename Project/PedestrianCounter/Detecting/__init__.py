from typing import Set
from Project.PedestrianCounter.Detecting.MobileNetSSD import MobileNetSSD
from Project.PedestrianCounter.Detecting.Yolo import Yolo
from Project.Components.SettingsFormGenerator import SettingsFormGenerator
from Project.Utils.Singleton import Singleton


class Detectors(metaclass=Singleton):
    def __init__(self):
        generator = SettingsFormGenerator()
        self.DICT = {
            "Yolo": generator.generate(Yolo()),
            "MobileNet SDD": generator.generate(MobileNetSSD()),
        }
