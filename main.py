import sys
import ctypes
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from Project.Layouts.MainLayout import MainLayout
from Project.Layouts.SettingsLayout import SettingsLayout
from Project.Layouts.DisplayLayout import DisplayLayout
from Project.Layouts.ImageViewerLayout import ImageViewerLayout
from Project.Layouts.InfoLayout import InfoLayout
from Project.Components.OpenCVImageViewer import OpenCVImageViewer
from Project.PedestrianCounter.MainProcess import MainProcessThread

if sys.platform == "win32":
    app_id = u"jakubmelkowski.pedestriancounter"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
WINDOW_NAME = "Pedestrian Counter"


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(WINDOW_NAME)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.settings_layout = SettingsLayout()
        self.display_layout = DisplayLayout()
        self.main_process_thread = MainProcessThread()

        # Settings Layout
        ## Main Tab
        source_layout = self.settings_layout.main_tab_layout.source_layout
        source_layout.changedSource.connect(self.change_source)
        source_layout.changedPause.connect(self.main_process_thread.pause)
        source_layout.resetCounting.connect(
            self.main_process_thread.main_process.counter.reset
        )
        ## Detector Tab
        detector_section = self.settings_layout.detector_tab_layout.first_section
        detector_section.changedDetectorName.connect(
            self.main_process_thread.main_process.set_detector
        )

        ## Tracker Tab
        tracker_section = self.settings_layout.tracker_tab_layout.first_section
        tracker_section.changedTrackerName.connect(
            self.main_process_thread.main_process.set_tracker
        )

        # Display Layout
        self.image_viewer = OpenCVImageViewer()
        self.main_process_thread.changePixmap.connect(self.image_viewer.set_image)

        self.info_layout = InfoLayout()
        self.image_viewer_layout = ImageViewerLayout(self.image_viewer)
        self.display_layout.addLayout(self.image_viewer_layout, 0, 0)
        self.display_layout.addLayout(self.info_layout, 0, 1)

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
