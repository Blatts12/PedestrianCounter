import os
import cv2
import vars
import numpy as np
from Project.PedestrianCounter.Detecting.IDetector import IDetector
from Project.Utils.Generator.IGeneratorBase import IGeneratorBase
from Project.Utils.Generator.ValueHolder import ValueHolder as vh
from Project.Components.Generator.GSlider import GSlider


class YoloV4Tiny(IDetector, IGeneratorBase):
    name = "YoloV4-tiny"
    values = {
        "Confidence": vh(GSlider(0, 100, 50, "%"), 0.5, lambda value: value / 100),
        "NMS Threshold": vh(GSlider(0, 100, 40, "%"), 0.4, lambda value: value / 100),
    }

    def __init__(self):
        self.input_width = 416
        self.input_height = 416

        self.net = None
        self.output_layers = None
        self.activated = False

    def activate(self):
        if not self.activated:
            path = os.path.join(vars.RESOURCES_PATH, "YOLOv4-tiny")
            config_path = os.path.join(path, "yolov4-tiny.cfg")
            weights_path = os.path.join(path, "yolov4-tiny.weights")
            self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

            layers = self.net.getLayerNames()
            self.output_layers = [
                layers[i[0] - 1] for i in self.net.getUnconnectedOutLayers()
            ]
            self.activated = True

    def process_frame(self, frame, frame_width, frame_height):
        boxes = []
        return_boxes = []
        confidences = []

        blob = cv2.dnn.blobFromImage(
            frame,
            1 / 255.0,
            (self.input_width, self.input_height),
            swapRB=True,
            crop=False,
        )
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.output_layers)

        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.values["Confidence"].v and class_id == 0:
                    center_x = int(detection[0] * frame_width)
                    center_y = int(detection[1] * frame_height)
                    width = int(detection[2] * frame_width)
                    height = int(detection[3] * frame_height)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        temp = cv2.dnn.NMSBoxes(
            boxes,
            confidences,
            self.values["Confidence"].v,
            self.values["NMS Threshold"].v,
        )
        if type(temp) != tuple:
            indices = temp.flatten().tolist()
            for index in indices:
                return_boxes.append(tuple(boxes[index]))

        return return_boxes
