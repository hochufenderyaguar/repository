import sys
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication


class Window(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('yandex_maps.ui', self)
        self.initUI()

    def initUI(self):
        self.coords = None
        self.scale = None
        self.server = 'http://static-maps.yandex.ru/1.x/'
        self.btn.clicked.connect(self.createMap)

    def createMap(self):
        self.coords = self.width_edit.text(), self.long_edit.text()
        self.scale = self.scale_edit.text()
        params = {
            'll': ','.join([self.coords[0], self.coords[1]]),
            'z': self.scale,
            'l': "map"
        }
        response = requests.get(self.server, params=params)
        self.map_file = 'map.png'
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.map_label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            print(1)
        if event.key() == Qt.Key_Up:
            self.long_edit.setText(str(float(self.long_edit.text()) + 0.1))
            self.createMap()
        if event.key() == Qt.Key_Down:
            pass
        if event.key() == Qt.Key_Left:
            pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

# 37.677751,55.757718
