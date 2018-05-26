# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qt_D - UIs/btm_right_click_dialog.ui'
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

class Ui_btm_right_dialog(object):
    def setupUi(self, btm_right_dialog):
        btm_right_dialog.setObjectName(_fromUtf8("btm_right_dialog"))
        btm_right_dialog.resize(774, 448)
        self.horizontalLayout = QtGui.QHBoxLayout(btm_right_dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btm_right_dialog_layout = QtGui.QVBoxLayout()
        self.btm_right_dialog_layout.setObjectName(_fromUtf8("btm_right_dialog_layout"))
        self.info_text = QtGui.QLabel(btm_right_dialog)
        self.info_text.setObjectName(_fromUtf8("info_text"))
        self.btm_right_dialog_layout.addWidget(self.info_text, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.btm_right_img = QtGui.QLabel(btm_right_dialog)
        self.btm_right_img.setText(_fromUtf8(""))
        self.btm_right_img.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/btm_right.png")))
        self.btm_right_img.setScaledContents(False)
        self.btm_right_img.setIndent(5)
        self.btm_right_img.setObjectName(_fromUtf8("btm_right_img"))
        self.btm_right_dialog_layout.addWidget(self.btm_right_img)
        self.cancelok_btn = QtGui.QDialogButtonBox(btm_right_dialog)
        self.cancelok_btn.setOrientation(QtCore.Qt.Horizontal)
        self.cancelok_btn.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelok_btn.setObjectName(_fromUtf8("cancelok_btn"))
        self.btm_right_dialog_layout.addWidget(self.cancelok_btn)
        self.horizontalLayout.addLayout(self.btm_right_dialog_layout)

        self.retranslateUi(btm_right_dialog)
        QtCore.QObject.connect(self.cancelok_btn, QtCore.SIGNAL(_fromUtf8("accepted()")), btm_right_dialog.accept)
        QtCore.QObject.connect(self.cancelok_btn, QtCore.SIGNAL(_fromUtf8("rejected()")), btm_right_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(btm_right_dialog)

    def retranslateUi(self, btm_right_dialog):
        btm_right_dialog.setWindowTitle(_translate("btm_right_dialog", "Click Please", None))
        self.info_text.setText(_translate("btm_right_dialog", "Click on the bottom right corner of the chart", None))

import resources.click_on_corners_dialog_resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    btm_right_dialog = QtGui.QDialog()
    ui = Ui_btm_right_dialog()
    ui.setupUi(btm_right_dialog)
    btm_right_dialog.show()
    sys.exit(app.exec_())
