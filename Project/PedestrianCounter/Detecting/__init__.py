import sys
import inspect
from Project.PedestrianCounter.Detecting.IDetector import IDetectorWithModel
from Project.PedestrianCounter.Detecting.MobileNetSSD import MobileNetSSD
from Project.PedestrianCounter.Detecting.Yolo import Yolo


DETECTORS = {}

baseClasses = [IDetectorWithModel]

for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj):
        for baseClass in baseClasses:
            if issubclass(obj, baseClass) and obj not in baseClasses:
                DETECTORS[obj.name] = obj