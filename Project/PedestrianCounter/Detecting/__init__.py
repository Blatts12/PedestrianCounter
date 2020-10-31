import sys
import inspect
from typing import Generator
from Project.PedestrianCounter.Detecting.MobileNetSSD import MobileNetSSD
from Project.PedestrianCounter.Detecting.Yolo import Yolo
from Project.Components.SettingsFormGenerator import SettingsFormGenerator
from Project.Utils.Singleton import Singleton


class Detectors(metaclass=Singleton):
    def __init__(self):
        _generator = SettingsFormGenerator()
        self.DICT = {
            "Yolo": _generator.generate(Yolo()),
            "MobileNet SDD": _generator.generate(MobileNetSSD()),
        }
