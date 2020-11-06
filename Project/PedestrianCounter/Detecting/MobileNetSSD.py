import os
import cv2
import numpy as np
import vars
from Project.PedestrianCounter.Detecting.IDetector import IDetector
from Project.Utils.Generator.IGeneratorBase import IGeneratorBase
from Project.Utils.Generator.ValueHolder import ValueHolder as vh


class MobileNetSSD(IDetector, IGeneratorBase):
    name = "MobileNet SSD"
    prototxt_path = (
        vars.ROOT_PATH + "/Resources/MobileNetSSD/MobileNetSSD_deploy.prototxt.txt"
    )
    model_path = (
        vars.ROOT_PATH + "/Resources/MobileNetSSD/MobileNetSSD_deploy.caffemodel"
    )
    values = {
        "Confidence": vh("Slider", (0, 100, 50, "%"), 0.5, lambda value: value / 100),
    }

    def __init__(self):
        self.net = None
        self.activated = False

    def activate(self):
        if not self.activated:
            path = "C:/_Projekty/pedestrian-counter-gui-test/Resources/MobileNetSSD"
            name = "MobileNetSSD_deploy"
            prototxt_path = os.path.sep.join([path, name + ".prototxt.txt"])
            model_path = os.path.sep.join([path, name + ".caffemodel"])
            self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            self.activated = True

    def process_frame(self, frame, frame_width, frame_height):
        blob = cv2.dnn.blobFromImage(
            frame, 0.007843, (frame_width, frame_height), 127.5
        )
        self.net.setInput(blob)
        detections = self.net.forward()

        return_boxes = []

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.values["Confidence"].v:
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
