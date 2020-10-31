import os
import cv2
import numpy as np
from Project.PedestrianCounter.Detecting.IDetector import IDetectorWithModel
from Project.Components.Generator.IGeneratorBase import IGeneratorBase


class Yolo(IDetectorWithModel, IGeneratorBase):
    name = "YOLO"
    values = {
        "Confidence": [0.5, ("Slider", 0, 100, 50, "%"), lambda value: value / 100],
        "NMS Threshold": [0.4, ("Slider", 0, 100, 40, "%"), lambda value: value / 100],
    }

    def setValue(self, name, value):
        self.values[name][0] = self.values[name][2](value)

    def getValue(self, name):
        return self.values[name][0]

    def __init__(self):
        self.inputWidth = 416
        self.inputHeight = 416

        self.net = None
        self.outputLayers = None

    def setModelPath(
        self, path="C:/_Projekty/Inzynierka/YoloConfigs", name="yolov4-tiny"
    ):
        weightsPath = os.path.sep.join([path, name + ".weights"])
        configPath = os.path.sep.join([path, name + ".cfg"])
        self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        layers = self.net.getLayerNames()
        self.outputLayers = [
            layers[i[0] - 1] for i in self.net.getUnconnectedOutLayers()
        ]

    def processFrame(self, frame, frameWidth, frameHeight):
        boxes = []
        returnBoxes = []
        confidences = []

        blob = cv2.dnn.blobFromImage(
            frame,
            1 / 255.0,
            (self.inputWidth, self.inputHeight),
            swapRB=True,
            crop=False,
        )
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.outputLayers)

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if (
                    confidence > self.values["Confidence"][0] and classId == 0
                ):  # 0 = person
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        temp = cv2.dnn.NMSBoxes(
            boxes,
            confidences,
            self.values["Confidence"][0],
            self.values["NMS Threshold"][0],
        )
        if type(temp) != tuple:
            indices = temp.flatten().tolist()
            for index in indices:
                returnBoxes.append(tuple(boxes[index]))

        return returnBoxes
