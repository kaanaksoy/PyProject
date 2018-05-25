import sys
from PyQt4 import QtGui, QtCore


class PrettyWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.initUI()

    def initUI(self):
        self.resize(1000,600)
        self.center()
        self.setWindowTitle('Browser')

        self.lb = QtGui.QLabel(self)
        pixmap = QtGui.QPixmap("180_original.jpg")
        height_of_label = 100
        self.lb.resize(self.width(), height_of_label)
        self.lb.setPixmap(pixmap.scaled(self.lb.size(), QtCore.Qt.IgnoreAspectRatio))
        self.show()    

    def resizeEvent(self, event):
        self.lb.resize(self.width(), self.lb.height())
        self.lb.setPixmap(self.lb.pixmap().scaled(self.lb.size(), QtCore.Qt.IgnoreAspectRatio))
        QtGui.QWidget.resizeEvent(self, event)


    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QtGui.QApplication(sys.argv)
    w = PrettyWidget()
    app.exec_()

if __name__ == '__main__':
    main()

