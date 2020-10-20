import os
import cv2
import numpy as np
from .IDetector import IDetectorWithModel


class MobileNetSSD(IDetectorWithModel):
    name = "MobileNet SSD"

    def __init__(self, confidenceThreshold=0.55):
        self.confidenceThreshold = confidenceThreshold
        self.net = None

    def setModelPath(
        self,
        path="C:/_Projekty/Inzynierka/MobileNetSDDConfigs",
        name="MobileNetSSD_deploy",
    ):
        prototxtPath = os.path.sep.join([path, name + ".prototxt.txt"])
        modelPath = os.path.sep.join([path, name + ".caffemodel"])

        self.net = cv2.dnn.readNetFromCaffe(prototxtPath, modelPath)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def setConfidenceThreshold(self, conf):
        self.confidenceThreshold = conf

    def processFrame(self, frame, frameWidth, frameHeight):
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (frameWidth, frameHeight), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        returnBoxes = []

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > self.confidenceThreshold:
                idx = int(detections[0, 0, i, 1])

                if idx != 15:  # 15 = person
                    continue

                box = detections[0, 0, i, 3:7] * np.array(
                    [frameWidth, frameHeight, frameWidth, frameHeight]
                )
                returnBoxes.append(
                    (
                        int(box[0]),
                        int(box[1]),
                        int(box[2] - box[0]),
                        int(box[3] - box[1]),
                    )
                )

        return returnBoxes
