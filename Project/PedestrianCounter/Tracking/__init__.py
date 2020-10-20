import sys
import inspect
from Project.PedestrianCounter.Tracking.ITracker import ITracker
from Project.PedestrianCounter.Tracking.CorrelationTracker import CorrelationTracker
from Project.PedestrianCounter.Tracking.KCFTracker import KCFTracker


TRAKCERS = {}

baseClasses = [ITracker]

for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj):
        for baseClass in baseClasses:
            if issubclass(obj, baseClass) and obj not in baseClasses:
                TRAKCERS[obj.name] = obj