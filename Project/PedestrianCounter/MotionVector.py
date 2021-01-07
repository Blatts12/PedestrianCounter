import numpy as np
import cv2


class MotionVector:
    def __init__(self, start_frame):
        self.old_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
        self.hsv = np.zeros_like(start_frame)
        self.hsv[..., 1] = 255

    def process_frame(self, frame):
        new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(
            self.old_frame, new_frame, None, 0.5, 1, 3, 15, 3, 5, 1
        )
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        self.hsv[..., 0] = ang * 180 / np.pi / 2
        self.hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        bgr = cv2.cvtColor(self.hsv, cv2.COLOR_HSV2BGR)
        self.old_frame = new_frame

        return bgr
