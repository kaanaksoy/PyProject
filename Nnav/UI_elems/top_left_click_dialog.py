# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qt_D - UIs/top_left_click_dialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
#import resources.click_on_corners_dialog_resources

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

class Ui_top_left_dialog(object):
    def setupUi(self, top_left_dialog):
        top_left_dialog.setObjectName(_fromUtf8("top_left_dialog"))
        top_left_dialog.resize(774, 359)
        self.horizontalLayout = QtGui.QHBoxLayout(top_left_dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.top_left_dialog_layout = QtGui.QVBoxLayout()
        self.top_left_dialog_layout.setObjectName(_fromUtf8("top_left_dialog_layout"))
        self.info_text = QtGui.QLabel(top_left_dialog)
        self.info_text.setObjectName(_fromUtf8("info_text"))
        self.top_left_dialog_layout.addWidget(self.info_text, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.top_left_img = QtGui.QLabel(top_left_dialog)
        self.top_left_img.setText(_fromUtf8(""))
        self.top_left_img.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/top_left.png")))
        self.top_left_img.setScaledContents(False)
        self.top_left_img.setIndent(5)
        self.top_left_img.setObjectName(_fromUtf8("top_left_img"))
        self.top_left_dialog_layout.addWidget(self.top_left_img)
        self.cancelok_btn = QtGui.QDialogButtonBox(top_left_dialog)
        self.cancelok_btn.setOrientation(QtCore.Qt.Horizontal)
        self.cancelok_btn.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelok_btn.setObjectName(_fromUtf8("cancelok_btn"))
        self.top_left_dialog_layout.addWidget(self.cancelok_btn)
        self.horizontalLayout.addLayout(self.top_left_dialog_layout)

        self.retranslateUi(top_left_dialog)
        QtCore.QObject.connect(self.cancelok_btn, QtCore.SIGNAL(_fromUtf8("accepted()")), top_left_dialog.accept)
        QtCore.QObject.connect(self.cancelok_btn, QtCore.SIGNAL(_fromUtf8("rejected()")), top_left_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(top_left_dialog)

    def retranslateUi(self, top_left_dialog):
        top_left_dialog.setWindowTitle(_translate("top_left_dialog", "Click Please", None))
        self.info_text.setText(_translate("top_left_dialog", "Click on the top left corner of the chart", None))

import resources.click_on_corners_dialog_resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    top_left_dialog = QtGui.QDialog()
    ui = Ui_top_left_dialog()
    ui.setupUi(top_left_dialog)
    top_left_dialog.show()
    sys.exit(app.exec_())
