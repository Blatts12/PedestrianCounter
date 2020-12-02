from Project.PedestrianCounter.Tracking.KCFTracker import KCFTracker
from Project.Components.SettingsFormGenerator import SettingsFormGenerator
from Project.Utils.Singleton import Singleton


class Trackers(metaclass=Singleton):
    def __init__(self):
        generator = SettingsFormGenerator()
        self.DICT = {
            "KCF": generator.generate(KCFTracker()),
        }

    def get_first(self):
        return list(self.DICT)[0]