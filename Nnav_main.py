import sys
from PyQt4 import QtGui, QtCore

class main_window(QtGui.QMainWindow):

    def __init__(self):
        super(main_window, self).__init__()
        self.setGeometry(600, 400, 1200, 800)
        self.setWindowTitle("N-nav ")
        #self.setWindowIcon(QtGui.QIcon("main_icon.jpg"))

        ## MENU BAR ##

        #File Menu Actions
        quit_action = QtGui.QAction("&Quit N-nav", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit N-nav and close all corresponding windows")
        quit_action.triggered.connect(self.close_application)

        save_action = QtGui.QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip('Save Current File')
        save_action.triggered.connect(self.save_file)

        saveAs_action = QtGui.QAction("&Save As...", self)
        saveAs_action.setShortcut("Ctrl+Shift+S")
        saveAs_action.setStatusTip('Save As...')
        saveAs_action.triggered.connect(self.save_file_as)

        import_action = QtGui.QAction("&Import...", self)
        import_action.setShortcut("Ctrl+I")
        import_action.setStatusTip('Import')
        import_action.triggered.connect(self.import_file)


        #Edit Menu Actions
        changeCoors_action = QtGui.QAction("&Change Coordinates", self)
        changeCoors_action.setStatusTip('Change the corner coordinates')
        changeCoors_action.triggered.connect(self.set_coors)


        #Display Menu Actions
        displayBoats_action = QtGui.QAction("&Marine Traffic",
                                            self, checkable=True)
        displayBoats_action.triggered.connect(self.show_boats)

        displayWind_action = QtGui.QAction("&Windspeed",
                                            self, checkable=True)
        displayWind_action.triggered.connect(self.show_wind)

        displayTemps_action = QtGui.QAction("&Tempreture",
                                            self, checkable=True)
        displayTemps_action.triggered.connect(self.show_temps)

        displayWave_action = QtGui.QAction("&Wave Information",
                                            self, checkable=True)
        displayWave_action.triggered.connect(self.show_waves)

        displayCourse_action = QtGui.QAction("&Toggle Course",
                                            self, checkable=True)
        displayCourse_action.triggered.connect(self.show_course)


        #Adding Actions to Menu Bar
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("&File")
        edit_menu = main_menu.addMenu("&Edit")
        display_menu = main_menu.addMenu("&Display")

        file_menu.addAction(save_action)
        file_menu.addAction(saveAs_action)
        file_menu.addAction(import_action)
        file_menu.addAction(quit_action)

        edit_menu.addAction(changeCoors_action)

        display_menu.addAction(displayBoats_action)
        display_menu.addAction(displayWind_action)
        display_menu.addAction(displayTemps_action)
        display_menu.addAction(displayWave_action)
        display_menu.addAction(displayCourse_action)
        self.statusBar()


        self.home()

    def home(self):
        self.show()

    def close_application(self):
        sys.exit()

    def save_file(self):
        return

    def save_file_as(self):
        return

    def import_file(self):
        return

    def set_coors(self):
        return

    def show_boats(self):
        return
    def show_wind(self):
        return
    def show_waves(self):
        return
    def show_temps(self):
        return
    def show_course(self):
        return


def main():
    app = QtGui.QApplication(sys.argv)
    main = main_window()
    sys.exit(app.exec_())


main()
