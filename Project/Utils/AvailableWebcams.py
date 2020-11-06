import cv2
from Project.Utils.Singleton import Singleton


class AvailableWebcams(metaclass=Singleton):
    def __init__(self):
        self.webcams = self._get_avalible_webcams_ids(20)

    def _get_avalible_webcams_ids(self, max):
        webcams = []
        for i in range(max):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            if cap is not None and cap.isOpened():
                webcams.append(str(i))
            cap.release()

        return webcams
