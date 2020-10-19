import numpy as np
from math import pi

HALF_PI = pi / 2


class Counter:
    def __init__(self, horizontal=False, margin=0, minUpdateTime=3):
        self.horizontal = horizontal
        self.margin = margin
        self.minUpdateTime = minUpdateTime
        self.up = 0  # or right
        self.down = 0  # or left

    def setMargin(self, margin):
        self.margin = margin

    def setMinUpdateTime(self, minUp):
        self.minUpdateTime = minUp

    def setHorizontal(self, isHor):
        self.horizontal = isHor

    def getInsideUp(self):
        return self.up - self.down

    def getInsideDown(self):
        return self.down - self.up

    def processPerson(self, person, frameWidth, frameHeight):
        if self.horizontal:
            self._processHorizontal(person, frameWidth)
        else:
            self._processVertical(person, frameHeight)

    def _processHorizontal(self, person, frameWidth):
        centroid = tuple(person.getCentroid())
        x = [c[0] for c in person.centroids]
        del x[0]
        direction = centroid[0] - np.mean(x)
        meanTheta = np.mean(person.theta) + HALF_PI
        halfWidth = frameWidth // 2

        if not person.counted and person.updateTime > self.minUpdateTime:
            if (
                direction < 0
                and meanTheta < 0
                and centroid[1] < halfWidth
                and centroid[1] > self.margin
            ):
                print("[{}]UP-MEAN_THETA: {}".format(person.id, meanTheta))
                self.up += 1
                person.counted = True

            elif (
                direction > 0
                and meanTheta > 0
                and centroid[1] > halfWidth
                and centroid[1] < frameWidth - self.margin
            ):
                print("[{}]DOWN-MEAN_THETA: {}".format(person.id, meanTheta))
                self.down += 1
                person.counted = True

    def _processVertical(self, person, frameHeight):
        centroid = tuple(person.getCentroid())
        y = [c[1] for c in person.centroids]
        del y[0]
        direction = centroid[1] - np.mean(y)
        meanTheta = np.mean(person.theta)
        halfHeight = frameHeight // 2

        if not person.counted and person.updateTime > self.minUpdateTime:
            if (
                direction < 0
                and meanTheta < 0
                and centroid[1] < halfHeight
                and centroid[1] > self.margin
            ):
                print("[{}]UP-MEAN_THETA: {}".format(person.id, meanTheta))
                self.up += 1
                person.counted = True

            elif (
                direction > 0
                and meanTheta > 0
                and centroid[1] > halfHeight
                and centroid[1] < frameHeight - self.margin
            ):
                print("[{}]DOWN-MEAN_THETA: {}".format(person.id, meanTheta))
                self.down += 1
                person.counted = True