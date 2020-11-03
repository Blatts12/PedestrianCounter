import os
import cv2
import numpy as np
from Project.PedestrianCounter.Detecting.IDetector import IDetectorWithModel
from Project.Components.Generator.IGeneratorBase import IGeneratorBase


class MobileNetSSD(IDetectorWithModel, IGeneratorBase):
    name = "MobileNet SSD"
    values = {
        "Confidence": [0.5, ("Slider", 0, 100, 50, "%"), lambda value: value / 100],
    }

    def set_value(self, name, value):
        self.values[name][0] = self.values[name][2](value)

    def __init__(self):
        self.net = None
        self.model_active = False

    def set_model_path(
        self,
        path="C:/_Projekty/Inzynierka/MobileNetSDDConfigs",
        name="MobileNetSSD_deploy",
    ):
        if not self.model_active:
            prototxt_path = os.path.sep.join([path, name + ".prototxt.txt"])
            model_path = os.path.sep.join([path, name + ".caffemodel"])
            self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            self.model_active = True

    def process_frame(self, frame, frame_width, frame_height):
        blob = cv2.dnn.blobFromImage(
            frame, 0.007843, (frame_width, frame_height), 127.5
        )
        self.net.setInput(blob)
        detections = self.net.forward()

        return_boxes = []

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.values["Confidence"][0]:
                idx = int(detections[0, 0, i, 1])

                if idx != 15:
                    continue

                box = detections[0, 0, i, 3:7] * np.array(
                    [frame_width, frame_height, frame_width, frame_height]
                )
                return_boxes.append(
                    (
                        int(box[0]),
                        int(box[1]),
                        int(box[2] - box[0]),
                        int(box[3] - box[1]),
                    )
                )

        return return_boxes
