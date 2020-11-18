import cv2
from PyQt5.QtWidgets import QMessageBox
from Project.PedestrianCounter.Sources.ISource import ISource
from Project.Utils.Generator.IGeneratorBase import IGeneratorBase
from Project.Utils.Generator.ValueHolder import ValueHolder as vh
from Project.Utils.AvailableWebcams import AvailableWebcams
from Project.Components.Generator.GComboBox import GComboBox


class Webcam(ISource, IGeneratorBase):
    name = "Video"
    values = {
        "Webcam": vh(GComboBox(AvailableWebcams().webcams, "Select webcam id"), ""),
    }

    def __init__(self):
        self.cap = None

    def ready_for_start(self):
        if self.values["Webcam"].v == "":
            QMessageBox.warning(None, "Webcam", "Select webcam")
            return False
        return True

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.stop_cap()
            return None
        return frame

    def start_cap(self):
        self.cap = cv2.VideoCapture(int(self.values["Webcam"].v), cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def stop_cap(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None