import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class first(QWidget):
    def __init__(self, parent=None):
        super(first, self).__init__(parent)
        # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))
        self.agree = QPushButton('Agree', self)
        self.agree.move(180, 400)
        self.button2 = QPushButton('Disagree', self)
        self.button2.move(270,400)


class second(QWidget):
    def __init__(self, parent=None):
        super(second, self).__init__(parent)
        self.btn = QPushButton("previous", self)
        self.btn.move(100, 350)
        self.greet = QLabel("second",self)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 400, 450)
        self.setFixedSize(400, 450)
        self.setWindowIcon(QIcon("favicon.png"))
        self.startfirst()

    def startsecond(self):
        self.ToolTab = second(self)
        self.setWindowTitle("second")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.btn.clicked.connect(self.startfirst)
        self.show()

    def startfirst(self):
        self.Window = first(self)
        self.setWindowTitle("first")
        self.setCentralWidget(self.Window)
        self.Window.agree.clicked.connect(self.startsecond)
        self.Window.button2.clicked.connect(QCoreApplication.instance().quit)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
