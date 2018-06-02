import sys
import numpy as np
from PyQt4 import QtCore, QtGui

# Importing Ui files
from UI_elems.ui_mainwindow import Ui_MainWindow
from UI_elems.corner_coors_dialog import Ui_corner_coors_dialog
from UI_elems.top_left_click_dialog import Ui_top_left_dialog
from UI_elems.btm_right_click_dialog import Ui_btm_right_dialog
from UI_elems.please_wait_dialog import Ui_please_wait_dialog
# Importing image cropping script
from img_crop.img_cropper import crop_img
# Importing image conversion script
from assets.toQImage import toQImage
class corner_coors_dialog(QtGui.QDialog, Ui_corner_coors_dialog):
    coors = [None]
    def __init__(self, parent=None):
        super(corner_coors_dialog, self).__init__(parent)
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.accept_click)
        self.cancel_btn.clicked.connect(self.reject_click)

    def accept_click(self):
        # coors format: [(lat, lon), (lat, lon)]
        if not (self.top_left_lat_input.text() and self.top_left_lon_input.text() and self.btm_right_lat_input.text() and self.btm_right_lon_input.text()):
            self.reject_click()
        else:
            corner_coors_dialog.coors[0] = (self.top_left_lat_input.text(), self.top_left_lon_input.text())
            corner_coors_dialog.coors.append((self.btm_right_lat_input.text(), self.btm_right_lon_input.text()))
            NnavMainWindow.set_coors(myapp, corner_coors_dialog.coors)
        return

    def reject_click(self):
        print "None"


class NnavMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(NnavMainWindow, self).__init__(parent)
        self.setupUi(self)
        # connect myaction_logic to myaction.toggled signal
        self.toggl_course.toggled.connect(self.show_course)
        self.toggl_traff.toggled.connect(self.show_boats)
        self.toggl_weather.toggled.connect(self.show_weather)

        self.plot_finish_btn.clicked.connect(self.end_plot)
        self.plot_start_btn.clicked.connect(self.start_plot)
        self.calculate_btn.clicked.connect(self.calculate_route)

        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)

        self.save_action.triggered.connect(self.save_file)
        self.saveAs_action.triggered.connect(self.save_file_as)
        self.import_action.triggered.connect(self.import_file)
        self.quit_action.triggered.connect(self.close_application)
        self.preferences_action.triggered.connect(self.open_preferences)
        self.corner_coors_input_action.triggered.connect(self.set_coors)
        self.import_boats_action.triggered.connect(self.import_boats)
        self.import_weather_action.triggered.connect(self.import_weather)

        self.map_view_scene = QtGui.QGraphicsScene()

    def close_application(self):
        sys.exit()

    def save_file(self):
        print "file saved"
        return

    def save_file_as(self):
        print "file saved as..."

        return

    def import_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File')

        print "opening file"
        OpenCV_img = crop_img(str(filename))
        QT_img = toQImage(OpenCV_img)
        QTimg_pixmap = QtGui.QPixmap(QT_img)
        self.map_view_scene.addPixmap(QTimg_pixmap)
        self.map_view.setScene(self.map_view_scene)
        print "file opened"
        self.open_corner_coors_dialog()
        return


    def set_coors(self, coors):
        print coors
        #self.corner_coors_dialog = QtGui.QDialog()
        #self.corner_coors_dialog_ui = Ui_corner_coors_dialog()
        #self.corner_coors_dialog_ui.setupUi(self.corner_coors_dialog)
        #self.corner_coors_dialog.show()
        return

    def open_corner_coors_dialog(self):
        self.dialog = QtGui.QDialog()
        self.corner_coors_dialog = corner_coors_dialog()
        self.corner_coors_dialog.show()

    def open_top_left_click_popup(self):
        self.top_left_dialog = QtGui.QDialog()
        self.top_left_dialog_ui = Ui_top_left_dialog()
        self.top_left_dialog_ui.setupUi(self.top_left_dialog)
        self.top_left_dialog.show()
        return

    def open_btm_right_click_popup(self):
        self.btm_right_dialog = QtGui.QDialog()
        self.btm_right_dialog_ui = Ui_btm_right_dialog()
        self.btm_right_dialog_ui.setupUi(self.btm_right_dialog)
        self.btm_right_dialog.show()
        return

    def open_waiting_dialog(self):
        self.waiting_dialog = QtGui.QDialog()
        self.waiting_dialog_ui = Ui_please_wait_dialog()
        self.waiting_dialog_ui.setupUi(self.waiting_dialog)
        self.waiting_dialog.show()
        return

    def show_boats(self):
        if self.toggl_traff.isChecked():
            print "Now is On"
        else:
            print "Now is Off"
            return

    def show_weather(self):
        if self.toggl_weather.isChecked():
            print "Now is On"
        else:
            print "Now is Off"
        return

    def show_course(self):
        if self.toggl_course.isChecked():
            print "Now is On"
        else:
            print "Now is Off"
        return

    def zoom_out(self):
        self.map_view.scale(0.9, 0.9)
        self.map_view.show()
        print "zoomed out"
        return

    def zoom_in(self):
        self.map_view.scale(1.1, 1.1)
        self.map_view.show()
        print "zoomed in"
        return

    def start_plot(self):
        print "started plot"
        return

    def end_plot(self):
        print "ended plot"
        return

    def calculate_route(self):
        print "calculated route"
        return

    def open_preferences(self):
        print "opened Preferences"
        return

    def import_boats(self):
        print "imported boats"
        return

    def import_weather(self):
        print "imported weather"
        return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = NnavMainWindow()
    myapp.show()
    sys.exit(app.exec_())
