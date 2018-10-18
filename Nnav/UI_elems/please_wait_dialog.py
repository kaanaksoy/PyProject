# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qt_D - UIs/please_wait_dialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_please_wait_dialog(object):
    def setupUi(self, please_wait_dialog):
        please_wait_dialog.setObjectName(_fromUtf8("please_wait_dialog"))
        please_wait_dialog.resize(542, 188)
        please_wait_dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.verticalLayout_2 = QtGui.QVBoxLayout(please_wait_dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.text_label = QtGui.QLabel(please_wait_dialog)
        self.text_label.setObjectName(_fromUtf8("text_label"))
        self.verticalLayout.addWidget(self.text_label, QtCore.Qt.AlignHCenter)
        self.ships_wheel_gif = QtGui.QLabel(please_wait_dialog)
        self.ships_wheel_gif.setText(_fromUtf8(""))
        self.ships_wheel_gif.setTextFormat(QtCore.Qt.PlainText)
        self.ships_wheel_gif.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../Downloads/2582328 (1).gif")))
        self.ships_wheel_gif.setScaledContents(False)
        self.ships_wheel_gif.setObjectName(_fromUtf8("ships_wheel_gif"))
        self.verticalLayout.addWidget(self.ships_wheel_gif, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(please_wait_dialog)
        QtCore.QMetaObject.connectSlotsByName(please_wait_dialog)

    def retranslateUi(self, please_wait_dialog):
        please_wait_dialog.setWindowTitle(_translate("please_wait_dialog", "Please Wait", None))
        self.text_label.setText(_translate("please_wait_dialog", "Please Wait...", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    please_wait_dialog = QtGui.QDialog()
    ui = Ui_please_wait_dialog()
    ui.setupUi(please_wait_dialog)
    please_wait_dialog.show()
    sys.exit(app.exec_())

