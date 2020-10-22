import numpy as np
from math import pi, atan2, cos, sin
from collections import OrderedDict, deque
from scipy.spatial import distance as dist


class TrackedObject:
    def __init__(self, _id, centroid, dequeCenLen=36, dequeThetaLen=36):
        self.id = _id
        self.centroids = deque(maxlen=dequeCenLen)
        self.centroids.appendleft(centroid)
        self.counted = False
        self.theta = deque(maxlen=dequeThetaLen)
        self.disappear = 0
        self.updateTime = 0

    def getCentroid(self):
        return self.centroids[0]

    def setNewCentroid(self, centroid):
        self.updateTime += 1
        self.centroids.appendleft(centroid)

    def getDirection(self):
        return self.centroids[0][1] - self.centroids[-1][1]

    def getMovementVector(self, length=18):
        (x1, y1) = self.centroids[0]
        (x2, y2) = self.centroids[-1]
        if x1 == x2 and y1 == y2:
            return (x1, y1)

        theta = atan2(y1 - y2, x1 - x2)

        x = x1 + length * cos(theta)
        y = y1 + length * sin(theta)

        self.theta.appendleft(theta)

        return (int(x), int(y))


class CentroidTracker:
    def __init__(self, maxDistance=35, maxDisappearance=30):
        self.nextObjectId = 0
        self.trackedObjects = OrderedDict()
        self.maxDistance = maxDistance
        self.maxDisappearance = maxDisappearance

    def reset(self):
        self.nextObjectId = 0
        self.trackedObjects = OrderedDict()

    def register(self, centroid):
        self.trackedObjects[self.nextObjectId] = TrackedObject(
            self.nextObjectId, centroid
        )
        self.nextObjectId += 1

    def deregister(self, objectId):
        del self.trackedObjects[objectId]

    def update(self, rects):
        if len(rects) == 0:
            for objectId in list(self.trackedObjects.keys()):
                self.trackedObjects[objectId].disappear += 1
                if self.trackedObjects[objectId].disappear > self.maxDisappearance:
                    self.deregister(objectId)

            return list(self.trackedObjects.values())

        inputCentroids = np.zeros((len(rects), 2), dtype="int")
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int(startX + (endX / 2.0))
            cY = int(startY + (endY / 2.0))
            inputCentroids[i] = (cX, cY)

        if len(self.trackedObjects) == 0:
            for i in range(len(inputCentroids)):
                self.register(inputCentroids[i])

        else:
            objectIds = list(self.trackedObjects.keys())
            objectCentroids = [
                o.getCentroid() for o in list(self.trackedObjects.values())
            ]

            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            usedRows = set()
            usedCols = set()

            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue

                if D[row, col] > self.maxDistance:
                    continue

                objectId = objectIds[row]
                self.trackedObjects[objectId].setNewCentroid(inputCentroids[col])
                self.trackedObjects[objectId].disappear = 0

                usedRows.add(row)
                usedCols.add(col)

            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    objectId = objectIds[row]
                    self.trackedObjects[objectId].disappear += 1

                    if self.trackedObjects[objectId].disappear > self.maxDisappearance:
                        self.deregister(objectId)

            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])

        return list(self.trackedObjects.values())