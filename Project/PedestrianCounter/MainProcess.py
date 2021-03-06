import datetime
import cv2
import time
import vars
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtGui import QImage
from Project.PedestrianCounter.Detecting import Detectors
from Project.PedestrianCounter.Tracking import Trackers
from Project.PedestrianCounter.Sources import Sources
from Project.PedestrianCounter.Counting.Counter import Counter
from Project.PedestrianCounter.Tracking.CentroidTracker import CentroidTracker


class MainProcess:
    def __init__(self):
        self.sources = Sources().DICT
        self.source = None

        self.detector = None
        self.change_detector = False
        self.new_detector_name = ""

        self.tracker = None
        self.change_tracker = False
        self.new_tracker_name = ""

        self.counter = Counter()
        self.centroid_tracker = CentroidTracker(max_distance=70)

        self.horizontal = False
        self.total_frames = 0
        self.frames_to_skip = 6
        self.margin = 0
        self.vector_len = 16

        self.detector_dict = Detectors().DICT
        self.tracker_dict = Trackers().DICT

        self.set_tracker(Trackers().get_first())
        self.set_detector(Detectors().get_first())

        self.fps = 0
        self.frame_time_start = 0
        self.frame_time_end = 0
        self.frame_time = 0

        self.motion_vector = False

    def set_frames_to_skip(self, frames=6):
        self.frames_to_skip = frames

    def set_margin(self, margin):
        self.margin = margin
        self.counter.set_margin(margin)

    def set_vector_len(self, len):
        self.vector_len = len

    def set_horizontal(self, horizontal):
        self.horizontal = horizontal
        self.counter.set_horizontal(horizontal)

    def set_detector(self, detector_name):
        self.change_detector = True
        self.new_detector_name = detector_name

    def activate_detector(self):
        self.change_detector = False
        self.detector = self.detector_dict[self.new_detector_name][0]
        self.detector.activate()

    def set_tracker(self, tracker_name):
        self.change_tracker = True
        self.new_tracker_name = tracker_name

    def activate_tracker(self):
        self.change_tracker = False
        self.tracker = self.tracker_dict[self.new_tracker_name][0]

    def change_source(self, name):
        self.stop()
        self.counter.reset()
        self.centroid_tracker.reset()
        self.total_frames = 0
        self.sources[name][0].start_cap()
        self.source = self.sources[name][0]
        self.frame_time_start = time.perf_counter()

    def change_motion_vector(self, activate):
        self.motion_vector = activate

    def stop(self):
        if self.source is not None:
            self.source.stop_cap()

    def draw_margin_lines(self, frame, frame_width, frame_height):
        if self.margin > 0:
            if self.horizontal:
                cv2.line(
                    frame,
                    (self.margin, 0),
                    (self.margin, frame_height),
                    (0, 0, 255),
                    2,
                )
                cv2.line(
                    frame,
                    (frame_width - self.margin, 0),
                    (frame_width - self.margin, frame_width),
                    (0, 0, 255),
                    2,
                )
            else:
                cv2.line(
                    frame,
                    (0, self.margin),
                    (frame_width, self.margin),
                    (0, 0, 255),
                    2,
                )
                cv2.line(
                    frame,
                    (0, frame_height - self.margin),
                    (frame_width, frame_height - self.margin),
                    (0, 0, 255),
                    2,
                )

    def draw_counting_line(self, frame, frame_width, frame_height):
        if self.horizontal:
            cv2.line(
                frame,
                (frame_width // 2, 0),
                (frame_width // 2, frame_height),
                (255, 0, 0),
                2,
            )
        else:
            cv2.line(
                frame,
                (0, frame_height // 2),
                (frame_width, frame_height // 2),
                (255, 0, 0),
                2,
            )

    def draw_counter(self, frame, frame_height, frame_width):
        text = "Crossed: {}".format(self.counter.get_crossed())
        cv2.putText(
            frame,
            text,
            (10, frame_height - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
        )

    def draw_fps(self, frame):
        self.frame_time_end = time.perf_counter()
        self.frame_time = self.frame_time_end - self.frame_time_start
        self.fps = 1 / self.frame_time
        cv2.putText(
            frame,
            str(int(self.fps)),
            (10, 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    def draw_motion_vector(self, frame, centroid, person):
        movement_vector = person.get_movement_vector(self.vector_len)

        if self.motion_vector:
            cv2.line(
                frame,
                centroid,
                movement_vector,
                (0, 255, 0),
                2,
            )

            if self.motion_vector and len(person.centroids) > 1:
                centroids = list(person.centroids)
                centroid_old = tuple(centroids.pop(1))
                for c in centroids:
                    centroid_new = tuple(c)
                    cv2.line(
                        frame,
                        centroid_old,
                        centroid_new,
                        (20, 130, 120),
                        2,
                    )
                    centroid_old = centroid_new

    def process_frame(self):
        frame = self.source.read_frame()
        if frame is None:
            return None
        frame_height, frame_width = frame.shape[:2]
        boxes = []
        if self.frames_to_skip == 0:
            if self.change_detector:
                self.activate_detector()

            boxes = self.detector.process_frame(frame, frame_width, frame_height)
        elif self.total_frames % self.frames_to_skip == 0:
            if self.change_detector:
                self.activate_detector()

            if self.change_tracker:
                self.activate_tracker()

            self.tracker.new_tracker()
            boxes = self.detector.process_frame(frame, frame_width, frame_height)

            for box in boxes:
                self.tracker.add_tracker(frame, box)
        else:
            boxes = self.tracker.update_trackers(frame)

        objects = self.centroid_tracker.update(boxes)

        for person in objects:
            centroid = tuple(person.get_centroid())

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
            self.draw_motion_vector(frame, centroid, person)
            self.counter.process_person(person, frame_width, frame_height)

        self.draw_counter(frame, frame_height, frame_width)
        self.draw_counting_line(frame, frame_width, frame_height)
        self.draw_margin_lines(frame, frame_width, frame_height)

        self.draw_fps(frame)

        self.total_frames += 1
        self.frame_time_start = self.frame_time_end
        return frame


class MainProcessThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, *args, **kwargs):
        super(MainProcessThread, self).__init__(*args, **kwargs)
        self.working = True
        self.paused = False
        self.main_process_paused = True
        self.main_process = MainProcess()

    def change_source(self, cap_type):
        if not self.main_process_paused:
            self.stop_source()
        self.main_process.change_source(cap_type)
        self.main_process_paused = False

    def stop(self):
        self.working = False

    def stop_source(self):
        self.main_process_paused = True
        self.main_process.stop()

    def pause(self, pause):
        if not pause:
            self.frame_time_start = time.perf_counter()
        self.paused = pause

    def run(self):
        while self.working:
            if self.paused or self.main_process_paused:
                continue
            frame = self.main_process.process_frame()
            if frame is None:
                self.stop_source()
                self.changePixmap.emit(vars.EMPTY_IMAGE)
                continue
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(
                rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888
            )
            p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
            if self.main_process_paused:
                self.changePixmap.emit(vars.EMPTY_IMAGE)
            else:
                self.changePixmap.emit(p)

        self.main_process.stop()
