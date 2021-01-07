import sys
import ctypes
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from Project.Layouts.MainLayout import MainLayout
from Project.Layouts.SettingsLayout import SettingsLayout
from Project.Layouts.DisplayLayout import DisplayLayout
from Project.Layouts.ImageViewerLayout import ImageViewerLayout
from Project.Components.OpenCVImageViewer import OpenCVImageViewer
from Project.PedestrianCounter.MainProcess import MainProcessThread

if sys.platform == "win32":
    app_id = u"jakubmelkowski.pedestriancounter"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 700
WINDOW_NAME = "Pedestrian Counter"


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(WINDOW_NAME)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.settings_layout = SettingsLayout()
        self.display_layout = DisplayLayout()
        self.main_process_thread = MainProcessThread()

        # Settings Layout
        ## Main Tab
        source_layout = self.settings_layout.main_tab_layout.source_layout
        source_layout.changedSource.connect(self.change_source)
        source_layout.changedPause.connect(self.main_process_thread.pause)
        source_layout.stopClicked.connect(self.main_process_thread.stop_source)
        source_layout.resetCounting.connect(
            self.main_process_thread.main_process.counter.reset
        )

        ## Detector Tab
        detector_section = self.settings_layout.detector_tab_layout.first_section
        detector_section.changedDetectorName.connect(
            self.main_process_thread.main_process.set_detector
        )
        detector_section.changedSkipFrames.connect(
            self.main_process_thread.main_process.set_frames_to_skip
        )
        detector_section.changedHorizontal.connect(
            self.main_process_thread.main_process.set_horizontal
        )

        ## Tracker Tab
        tracker_section = self.settings_layout.tracker_tab_layout.first_section
        tracker_section.changedTrackerName.connect(
            self.main_process_thread.main_process.set_tracker
        )
        tracker_section.changedMaxDistance.connect(
            self.main_process_thread.main_process.centroid_tracker.set_max_distance
        )
        tracker_section.changedMaxDisappearance.connect(
            self.main_process_thread.main_process.centroid_tracker.set_max_disappearance
        )

        ## Counter Tab
        counter_section = self.settings_layout.counter_tab_layout.first_section
        counter_section.changedMargin.connect(
            self.main_process_thread.main_process.set_margin
        )
        counter_section.changedMinUpdate.connect(
            self.main_process_thread.main_process.counter.set_min_update_time
        )
        counter_section.changedVectorLen.connect(
            self.main_process_thread.main_process.set_vector_len
        )
        counter_section.changedInverted.connect(
            self.main_process_thread.main_process.counter.set_inverted
        )
        counter_section.changedMotion.connect(
            self.main_process_thread.main_process.change_motion_vector
        )

        # Display Layout
        self.image_viewer = OpenCVImageViewer()
        self.main_process_thread.changePixmap.connect(self.image_viewer.set_image)

        self.image_viewer_layout = ImageViewerLayout(self.image_viewer)
        self.display_layout.addStretch()
        self.display_layout.addLayout(self.image_viewer_layout)
        self.display_layout.addStretch()

        main_layout = MainLayout()
        main_layout.addLayout(self.settings_layout, 0, 0)
        main_layout.addLayout(self.display_layout, 1, 0)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.show()

    def change_source(self, cap_type):
        if not self.main_process_thread.isRunning():
            self.main_process_thread.start()
        self.main_process_thread.change_source(cap_type)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
