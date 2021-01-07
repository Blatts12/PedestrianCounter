import numpy as np
import cv2


class MotionVector:
    def __init__(self, start_frame, points):

        self.lk_params = dict(
            winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
        )
        self.old_frame = start_frame
        self.color = np.random.randint(0, 255, (100, 3))
        self.old_gray = cv2.cvtColor(self.old_frame, cv2.COLOR_BGR2GRAY)
        self.p0 = np.array(points)
        self.mask = np.zeros_like(self.old_frame)

    def process_frame(self, frame, points):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.p0.size == 0:
            self.old_gray = frame_gray.copy()
            if points:
                self.p0 = np.array(points)
                print(self.p0)
            return frame

        p1, st, err = cv2.calcOpticalFlowPyrLK(
            self.old_gray, frame_gray, self.p0, None, **self.lk_params
        )
        good_new = p1[st == 1]
        good_old = self.p0[st == 1]

        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            self.mask = cv2.line(self.mask, (a, b), (c, d), self.color[i].tolist(), 2)
            frame = cv2.circle(frame, (a, b), 5, self.color[i].tolist(), -1)
        img = cv2.add(frame, self.mask)
        self.old_gray = frame_gray.copy()
        self.p0 = good_new.reshape(-1, 1, 2)
        if points:
            np.concatenate(self.p0, np.array(points))

        return img
