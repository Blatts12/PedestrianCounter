import cv2
import dlib
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QThreadPool
from PyQt5.QtGui import QImage
import Project.PedestrianCounter.Detecting as Detecting
import Project.PedestrianCounter.Tracking as Tracking
from Project.PedestrianCounter.Counting.Counter import Counter
from Project.PedestrianCounter.Tracking.CentroidTracker import CentroidTracker


class MainProcess:
    def __init__(self):
        self.cap = None
        self.detector = None
        self.tracker = None
        self.counter = Counter()
        self.centroidTracker = CentroidTracker(maxDistance=70)

        self.horizontal = False
        self.totalFrames = 0
        self.framesToSkip = 6
        self.margin = 0

        self.detectorDict = Detecting.DETECTORS
        self.trackerDict = Tracking.TRAKCERS
        # "boosting": cv2.TrackerBoosting_create,
        # "mil": cv2.TrackerMIL_create,
        # "kcf": KCFTracker,
        # "correlation": CorrelationTracker,
        # "tld": cv2.TrackerTLD_create,
        # "medianFlow": cv2.TrackerMedianFlow_create,
        # "goTurn": cv2.TrackerGOTURN_create,
        # "mosse": cv2.TrackerMOSSE_create,
        # "csrt": cv2.TrackerCSRT_create,

    def setFramesToSkip(self, frames=6):
        self.framesToSkip = frames

    def setMargin(self, margin):
        self.margin = margin
        self.counter.setMargin(margin)

    def setDetector(self, detectorName="YOLO"):
        self.detector = self.detectorDict[detectorName]()
        self.detector.setModelPath()

    def setTracker(self, trackerName="kcf"):
        self.tracker = self.trackerDict[trackerName]()

    def setCapVideo(self, filePath):
        self.cap = cv2.VideoCapture(filePath)

    def setCapWebcam(self, index=0):
        pass

    def setCapIpcam(self, ip):
        pass

    def _startCap(self):
        threadPool = QThreadPool.globalInstance()
        threadPool.start(self.cap)

    def stop(self):
        if self.cap is not None:
            self.cap.release()

    def processFrame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        frameHeight, frameWidth = frame.shape[:2]
        boxes = []

        if self.totalFrames % self.framesToSkip == 0:
            self.tracker.newTracker()
            boxes = self.detector.processFrame(frame, frameWidth, frameHeight)

            for box in boxes:
                self.tracker.addTracker(frame, box)
        else:
            boxes = self.tracker.updateTrackers(frame)

        objects = self.centroidTracker.update(boxes)

        for person in objects:
            centroid = tuple(person.getCentroid())

            cv2.circle(frame, centroid, 4, (0, 255, 0), -1)
            cv2.putText(
                frame,
                str(person.id),
                (centroid[0] - 9, centroid[1] - 9),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

            cv2.line(
                frame,
                centroid,
                person.getMovementVector(),
                (0, 255, 0),
                2,
            )

            self.counter.processPerson(person, frameWidth, frameHeight)

        text = "UP: {}, DOWN: {}".format(self.counter.up, self.counter.down)
        cv2.putText(
            frame,
            text,
            (10, frameHeight - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
        )

        # Draw counting line
        if self.horizontal:
            cv2.line(
                frame,
                (frameWidth // 2, 0),
                (frameWidth // 2, frameHeight),
                (255, 0, 0),
                2,
            )
        else:
            cv2.line(
                frame,
                (0, frameHeight // 2),
                (frameWidth, frameHeight // 2),
                (255, 0, 0),
                2,
            )

        # Draw margin lines
        if self.margin > 0:
            if self.horizontal:
                cv2.line(
                    frame,
                    (self.margin, 0),
                    (self.margin, frameHeight),
                    (0, 0, 255),
                    2,
                )
                cv2.line(
                    frame,
                    (frameWidth - self.margin, 0),
                    (frameWidth - self.margin, frameWidth),
                    (0, 0, 255),
                    2,
                )
            else:
                cv2.line(
                    frame,
                    (0, self.margin),
                    (frameWidth, self.margin),
                    (0, 0, 255),
                    2,
                )
                cv2.line(
                    frame,
                    (0, frameHeight - self.margin),
                    (frameWidth, frameHeight - self.margin),
                    (0, 0, 255),
                    2,
                )

        self.totalFrames += 1

        return frame


class MainProcessThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, *args, **kwargs):
        super(MainProcessThread, self).__init__(*args, **kwargs)
        self.working = True
        self.paused = True
        self.mainProcess = MainProcess()

    def stop(self):
        self.working = False

    def unpause(self):
        self.paused = False

    def pause(self):
        self.paused = True

    def run(self):
        while self.working:
            if self.paused:
                continue
            frame = self.mainProcess.processFrame()
            if frame is None:
                continue
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(
                rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888
            )
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

        self.mainProcess.stop()
