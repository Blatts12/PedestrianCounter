import cv2
from PyQt5.QtWidgets import QMessageBox
from Project.PedestrianCounter.Sources.ISource import ISource
from Project.Utils.Generator.IGeneratorBase import IGeneratorBase
from Project.Utils.Generator.ValueHolder import ValueHolder as vh
from Project.Components.Generator.GLineEdit import GLineEdit


class IPCam(ISource, IGeneratorBase):
    name = "Video"
    values = {
        "IP": vh(GLineEdit(), ""),
    }

    def __init__(self):
        self.cap = None
        self.working = False

    def ready_for_start(self):
        if self.values["IP"].v == "":
            QMessageBox.warning(None, "IP Cam", "Type ip cam address")
            return False
        return True

    def read_frame(self):
        if not self.working:
            return None
        ret, frame = self.cap.read()
        if not ret:
            self.stop_cap()
            return None
        return frame

    def start_cap(self):
        try:
            self.cap = cv2.VideoCapture(self.values["IP"].v)
            self.working = True
        except Exception as e:
            QMessageBox.warning(None, "IP Cam", "Can't connect to camera")
            self.working = False
            print(e)

    def stop_cap(self):
        self.working = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None