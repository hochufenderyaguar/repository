import sys
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QButtonGroup


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
        self.vid = "map"
        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.radioButton)
        self.btn_group.addButton(self.radioButton_2)
        self.btn_group.addButton(self.radioButton_3)
        self.btn_group.buttonClicked.connect(self.click_radio_btn)
        self.width_edit.setText('37.677751')
        self.long_edit.setText('55.757718')

    def createMap(self):
        print(self.vid)
        self.coords = self.width_edit.text(), self.long_edit.text()
        self.scale = self.scale_edit.text()
        params = {
            'll': ','.join([self.coords[0], self.coords[1]]),
            'z': self.scale,
            'l': self.vid
        }
        response = requests.get(self.server, params=params)
        self.map_file = 'map.png'
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.map_label.setPixmap(self.pixmap)
        self.map_label.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            scale = int(self.scale_edit.text()) + 1
            self.scale_edit.setText(str(scale) if scale < 18 else '17')
        if event.key() == Qt.Key_PageDown:
            scale = int(self.scale_edit.text()) - 1
            self.scale_edit.setText(str(scale) if scale > -1 else '0')
        if event.key() == Qt.Key_Right:
            print(1)
        if event.key() == Qt.Key_Up:
            self.long_edit.setText(str(float(self.long_edit.text()) + 0.1))
        if event.key() == Qt.Key_Down:
            pass
        if event.key() == Qt.Key_Left:
            pass
        self.createMap()

    def click_radio_btn(self, btn):
        # там потому что sat - jpg, то не отображается
        text = btn.text()
        if text == 'схема':
            self.vid = "map"
        elif text == 'спутник':
            self.vid = "sat"
        else:
            self.vid = "sat,skl"
        self.createMap()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

# 37.677751,55.757718
