from PyQt5.QtWidgets import QVBoxLayout


class ImageViewerLayout(QVBoxLayout):
    def __init__(self, imageViewer, *args, **kwargs):
        super(ImageViewerLayout, self).__init__(*args, **kwargs)
        self.imageViewer = imageViewer
        self.addWidget(imageViewer)