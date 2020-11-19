import os
from PyQt5.QtGui import QImage

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCES_PATH = os.path.join(PROJECT_PATH, "Resources")

with open(os.path.join(RESOURCES_PATH, "empty.png"), "rb") as f:
    content = f.read()

EMPTY_IMAGE = QImage()
EMPTY_IMAGE.loadFromData(content)