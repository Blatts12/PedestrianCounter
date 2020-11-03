from PyQt5.QtWidgets import QVBoxLayout


class ImageViewerLayout(QVBoxLayout):
    def __init__(self, image_viewer, *args, **kwargs):
        super(ImageViewerLayout, self).__init__(*args, **kwargs)
        self.addWidget(image_viewer)