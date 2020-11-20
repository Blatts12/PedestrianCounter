import cv2
import os
from PyQt5.QtWidgets import QMessageBox
from Project.PedestrianCounter.Sources.ISource import ISource
from Project.Utils.Generator.IGeneratorBase import IGeneratorBase
from Project.Utils.Generator.ValueHolder import ValueHolder as vh
from Project.Components.Generator.GCheckBox import GCheckBox
from Project.Components.Generator.GSelectVideoFile import GSelectVideoFile


class FileVideo(ISource, IGeneratorBase):
    name = "Video"
    values = {
        "File": vh(GSelectVideoFile(), ""),
        "Loop": vh(GCheckBox("Loop video"), False),
    }

    def __init__(self):
        self.cap = None
        self.working = False

    def ready_for_start(self):
        if not os.path.exists(self.values["File"].v):
            QMessageBox.warning(None, "Video", "Path isn't valid of file don't exists")
            return False
        return True

    def read_frame(self):
        if not self.working:
            return None
        ret, frame = self.cap.read()
        if not ret:
            if not self.values["Loop"].v:
                self.stop_cap()
                return None
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
                if not ret:
                    self.stop_cap()
                    return None

        return frame

    def start_cap(self):
        try:
            self.cap = cv2.VideoCapture(self.values["File"].v)
            self.working = True
        except Exception as e:
            self.working = False
            QMessageBox.warning(None, "Video", "Can't open video file")
            print(e)

    def stop_cap(self):
        self.working = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None