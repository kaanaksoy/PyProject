# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qt_D - UIs/corner_coors_dialog.ui'
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

class Ui_corner_coors_dialog(object):
    def setupUi(self, corner_coors_dialog):
        corner_coors_dialog.setObjectName(_fromUtf8("corner_coors_dialog"))
        corner_coors_dialog.resize(744, 244)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(corner_coors_dialog.sizePolicy().hasHeightForWidth())
        corner_coors_dialog.setSizePolicy(sizePolicy)
        corner_coors_dialog.setMinimumSize(QtCore.QSize(744, 244))
        self.verticalLayout = QtGui.QVBoxLayout(corner_coors_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.title_label = QtGui.QLabel(corner_coors_dialog)
        self.title_label.setObjectName(_fromUtf8("title_label"))
        self.verticalLayout.addWidget(self.title_label, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.title_seperator_line = QtGui.QFrame(corner_coors_dialog)
        self.title_seperator_line.setFrameShape(QtGui.QFrame.HLine)
        self.title_seperator_line.setFrameShadow(QtGui.QFrame.Sunken)
        self.title_seperator_line.setObjectName(_fromUtf8("title_seperator_line"))
        self.verticalLayout.addWidget(self.title_seperator_line)
        self.input_grid = QtGui.QGridLayout()
        self.input_grid.setObjectName(_fromUtf8("input_grid"))
        self.lat_label = QtGui.QLabel(corner_coors_dialog)
        self.lat_label.setObjectName(_fromUtf8("lat_label"))
        self.input_grid.addWidget(self.lat_label, 0, 1, 1, 1)
        self.lon_label = QtGui.QLabel(corner_coors_dialog)
        self.lon_label.setObjectName(_fromUtf8("lon_label"))
        self.input_grid.addWidget(self.lon_label, 0, 2, 1, 1)
        self.top_left_label = QtGui.QLabel(corner_coors_dialog)
        self.top_left_label.setObjectName(_fromUtf8("top_left_label"))
        self.input_grid.addWidget(self.top_left_label, 1, 0, 1, 1)
        self.top_left_lat_input = QtGui.QLineEdit(corner_coors_dialog)
        self.top_left_lat_input.setObjectName(_fromUtf8("top_left_lat_input"))
        self.input_grid.addWidget(self.top_left_lat_input, 1, 1, 1, 1)
        self.btm_right_label = QtGui.QLabel(corner_coors_dialog)
        self.btm_right_label.setObjectName(_fromUtf8("btm_right_label"))
        self.input_grid.addWidget(self.btm_right_label, 2, 0, 1, 1)
        self.top_left_lon_input = QtGui.QLineEdit(corner_coors_dialog)
        self.top_left_lon_input.setObjectName(_fromUtf8("top_left_lon_input"))
        self.input_grid.addWidget(self.top_left_lon_input, 1, 2, 1, 1)
        self.btm_right_lat_input = QtGui.QLineEdit(corner_coors_dialog)
        self.btm_right_lat_input.setObjectName(_fromUtf8("btm_right_lat_input"))
        self.input_grid.addWidget(self.btm_right_lat_input, 2, 1, 1, 1)
        self.btm_right_lon_input = QtGui.QLineEdit(corner_coors_dialog)
        self.btm_right_lon_input.setObjectName(_fromUtf8("btm_right_lon_input"))
        self.input_grid.addWidget(self.btm_right_lon_input, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.input_grid)
        self.cancelok_box = QtGui.QDialogButtonBox(corner_coors_dialog)
        self.cancelok_box.setOrientation(QtCore.Qt.Horizontal)
        self.cancelok_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelok_box.setObjectName(_fromUtf8("cancelok_box"))
        self.verticalLayout.addWidget(self.cancelok_box, QtCore.Qt.AlignBottom)

        self.retranslateUi(corner_coors_dialog)
        QtCore.QObject.connect(self.cancelok_box, QtCore.SIGNAL(_fromUtf8("accepted()")), corner_coors_dialog.accept)
        QtCore.QObject.connect(self.cancelok_box, QtCore.SIGNAL(_fromUtf8("rejected()")), corner_coors_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(corner_coors_dialog)

    def retranslateUi(self, corner_coors_dialog):
        corner_coors_dialog.setWindowTitle(_translate("corner_coors_dialog", "Enter Corner Coordinates", None))
        self.title_label.setText(_translate("corner_coors_dialog", "Please enter the corner coordinates of you chart", None))
        self.lat_label.setText(_translate("corner_coors_dialog", "Latitude", None))
        self.lon_label.setText(_translate("corner_coors_dialog", "Longitude", None))
        self.top_left_label.setText(_translate("corner_coors_dialog", "Top Left", None))
        self.btm_right_label.setText(_translate("corner_coors_dialog", "Bottom Right", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    corner_coors_dialog = QtGui.QDialog()
    ui = Ui_corner_coors_dialog()
    ui.setupUi(corner_coors_dialog)
    corner_coors_dialog.show()
    sys.exit(app.exec_())

