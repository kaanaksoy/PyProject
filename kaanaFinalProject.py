# Code designed and written by: Kaan Aksoy
# Carnegie Mellon University Andrew ID: kaana
# File Created: November 10, 16:00
# Modification History:
# Start               End
# Nov 10 16:00        Nov 10 19:30
# Nov 11 14:00        Nov 12 04:30
# Nov 12 06:00        Nov 12 13:20
# Nov 14 03:30        Nov 14 04:30

import Tkinter
from Tkinter import Label, StringVar, Entry, Button, Menu, Frame, Tk, Canvas
from Tkconstants import LEFT, CENTER, W, SUNKEN, X, Y
from PIL import Image, ImageTk
import urllib2 as urllib
import cStringIO
import math


#\\\\\\\\\\\\\          Helper Functions are defined here        ///////////////////

# This function takes the tile paramaters as inputs and fetches the appropriate tile from the web
def getMarineData(APIkey, Coordinates):

    ageOfData = 1440  # This value is the age of the data recieved in minutes, for more accuracy, it can be reduced to a minimum of 10

    # Here the Coordinates Tuple is put in order of size, in order to find the min and max coordinates
    if Coordinates[0][0] < Coordinates[1][0]:
        lon_min = Coordinates[0][0]
        lon_max = Coordinates[1][0]
    else:
        lon_min = Coordinates[1][0]
        lon_max = Coordinates[0][0]

    if Coordinates[0][1] < Coordinates[1][1]:
        lat_min = Coordinates[0][1]
        lat_max = Coordinates[1][1]
    else:
        lat_min = Coordinates[1][1]
        lat_max = Coordinates[0][1]

    # The url for the request is formed
    url = 'http://services.marinetraffic.com/api/exportvessels/'
    request = url + 'v' + ':8/' + APIkey + '/MINLAT:' + str(lat_min) + '/MAXLAT:' + str(lat_max) + '/MINLON:' + str(
        lon_min) + '/MAXLON:' + str(lon_max) + '/timespan' + ':' + str(ageOfData) + '/protocol:json'
    # print request #Used for debuggung purposes
    mTrafficData = urllib.urlopen(request)  # Request marine data
    data = mTrafficData.read()

    data = [["304010417", "9015462", "359396", "-97.67599", "28.69228", "74", "329", "327", "0", "2017-05-19T09:39:57", "TER", "54"],
            ["215819000", "9034731", "150559", "-94.15851", "29.53593",  "122", "162", "157", "0", "2017-05-19T09:44:27", "TER", "28"],
             ["255925000", "9184433", "300518", "-97.38166", "26.56094", "79", "316", "311", "0", "2017-05-19T09:43:53", "TER", "52"]]
    # data set is replaced by an example set for debugging
    return data


# This function gets the raw data and creates instances of the boat class with the appropriate parameters
def createBoats(data, parent):
    boats = {}  # boats are stored in a dictionary
    for i in range(len(data)):
        boats['boat' + str(i)] = Boat(boatData=data[i], parent=parent)
    return boats


def fromLatLon2Cartesian((Lat1, Lon1), (Lat2, Lon2)):
    centerCoordinate = (((Lat1 - Lat2) / 2), ((Lon1 - Lon2) / 2))
    print centerCoordinate

# This function gets the weather tile from the website


def getTile((xtile, ytile, zoom)):
    # creates the proper URL for the desired tile
    weatherOverlayURL = "https://weather.openportguide.de/tiles/actual/wind_stream/5/" + \
        str(zoom) + "/" + str(xtile) + "/" + str(ytile) + ".png"
    tile = urllib.urlopen(weatherOverlayURL)  # Opens the URL
    # Converts it so it could be read by PIL
    tile = cStringIO.StringIO(tile.read())
    return tile

    # This function uses the top left corner coordinate to calculate the appropriate tile parameters


def convertToTiles((lat, lon), zoom):
    # Derived from the pseudocode available at http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
    latrad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(latrad) +
                                (1 / math.cos(latrad))) / math.pi) / 2.0 * n)
    return (xtile, ytile, zoom)


class Boat():  # This is the Boat class, its instances are displayed on the nautical chart.
    def __init__(self, parent, boatData):
        self.chartCenter = parent.center #Center of the chart
        self.parent = parent #Parent of the instance

        #Read more about maritime data used at https://www.marinetraffic.com/en/ais-api-services/documentation/api-service:ps06#9KOWEslKsTYFuGfl.99
        self.MMSI = int(boatData[0]) #Maritime Mobile Service Identity - a nine-digit number sent in digital form over a radio frequency that identifies the vessel's transmitter station
        self.IMO = int(boatData[1]) #International Maritime Organisation number - a seven-digit number that uniquely identifies vessels
        self.SHIP_ID = int(boatData[2]) #A uniquely assigned ID by MarineTraffic for the subject vessel
        self.LAT = float(boatData[3]) #Latitude
        self.LON = float(boatData[4]) #Longitude
        self.SPEED = int(boatData[5]) #The Speed on knots x10 of the subject vessel
        self.HEADING = int(boatData[6]) #The heading, in degrees of the subject vessel
        self.COURSE = int(boatData[7]) #The course, in degrees of the subject vessel
        self.STATUS = int(boatData[8]) #The AIS Navigational Status of the subject vessel
        self.TIMESTAMP = boatData[9] #The date and time (in UTC) that the subject vessel's position was recorded by MarineTraffic

        self.relativeLocation = None #Location of the vessel relative to the chart
        self.radius = 5 #self.radius of the cirlce, the vessel marker is inscribed in
        self.chartScale = parent.chartScale
        self.statusDict = {0: 'Green', 1: 'Grey', 2: 'Black', 3: 'Orange',
                           4: 'Pink', 5: 'Yellow', 6: 'Blue', 7: 'Red', 8: 'Purple'}

    def determineStatus(self):
        if self.STATUS in self.statusDict:
            return self.statusDict[self.STATUS]
        else:
            return 'White'

    def determineRelativeLocation(self, Center, Lat, Lon):
        self.relativeLocation = (Lat - Center[0], Lon - Center[1])

    #This function is used to rotate the boats about their center
    def rotate(origin, point, angle):
        #Adapted from https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
        #Rotate a point counterclockwise by a given angle around a given origin.

        angle = math.radians(angle)
        ox = origin[0]
        oy = origin[1]

        px = point[0]
        py = point[1]

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return (qx, qy)

    #This function is used to be able to graw an arrow shaped polygon to symbolize the boats
    def findCoordinates(self, self.radius, BoatLatLon, angle):

        center = ((BoatLatLon[0]) / 2, (BoatLatLon[1]) / 2) # Finds the center of the boat polygon

        #Find the location of the individual points to plot an arrow looking shape (All points have to be rotated in order to have the arrow face right, to make it easy when adding rotations)
        A = self.rotate(center, (center[0], center[1] + self.radius), -90)
        B = self.rotate(center, (center[0] + ( (2.1 * self.radius) / 2.75), center[1] - (self.radius - (self.radius / 2.75))), -90)
        C = self.rotate(center, (center[0], center[1] - (self.radius - ((2 * self.radius) / 2.75) ) ), -90)
        D = self.rotate(center, (center[0] - ((2.1 * self.radius) / 2.75), center[1] - (self.radius - (self.radius / 2.75))), -90)

        polyList = [] #Creates a List to store the point information
        for j in (A, B, C, D): #uses a for loop to enter the point information to the list
            polyList.append(rotate(center, j, angle))
        return polyList

    def draw(self):
        parent = self.parent
        location = ((self.relativeLocation[0] * parent.chartScale), (self.relativeLocation[1] * parent.chartScale))
        polyList = self.findCoordinates(self.radius, location, self.HEADING)

        parent.canvas.create_polygon(polyList[0][0], polyList[0][1], polyList[1][0], polyList[1][1], polyList[2][0], polyList[2][1], polyList[3][0], polyList[3][1], fill= determineStatus(self.STATUS))
        parent.window.update()
        parent.window.update_idletasks()


class impWnd():  # This class is creates an import window for the user to enter a path to import a file
    def __init__(self, parent):
        self.parent = parent
        self.window = Tkinter.Tk()  # creates the tkinter window
        self.label = Tkinter.Label(
            self.window, text='Please enter the path for your desired chart')
        # entry widget where the user types
        self.textBox = Tkinter.Entry(self.window)
        self.enterButton = Tkinter.Button(
            self.window, text='Enter', command=self.imp)
        self.pathVar = ''  # variable where the path for the file is stored
        self.window.title('  SailNav - Import')

        # here all the widgets in the class are packed
        self.label.grid(row=0, column=0, columnspan=3, padx=4, pady=4)
        self.textBox.grid(row=1, column=0, columnspan=3,
                          sticky='WE', padx=4, pady=4)
        self.textBox.insert(0, 'C:\Users\kaana\Desktop\Python Final Project\Example1.png')
        self.enterButton.grid(row=2, column=2, sticky='WE',
                              columnspan=2, pady=4, padx=4)

        # starts the main loop
        self.window.mainloop()

    # this function is called by the enter button in the import window, and it gets the path that was entered by the user
    def imp(self):
        parent = self.parent
        self.pathVar = self.textBox.get()  # stores the path in self.pathVar
        self.chartPIL = Image.open(self.pathVar)
        self.chart = ImageTk.PhotoImage(self.chartPIL)
        parent.chartSize = self.chartPIL.size
        parent.chart = self.chart
        parent.chartPIL = self.chartPIL
        parent.canvas.create_image(0, 0, image=self.chart, anchor='nw')
        parent.canvas.config(scrollregion=(
            0, 0, parent.chartSize[0], parent.chartSize[1]))
        parent.window.update()
        parent.window.update_idletasks()
        self.window.destroy()


class xyWnd():  # This class is creates an window for the user to enter a information regarding the chart they are looking at
    def __init__(self, parent):
        self.parent = parent
        self.topLeft = ''
        self.bottomRight = ''
        self.coordinates = ''
        self.window.title('  SailNav - Location')

        self.window = Tkinter.Tk()  # creates the tkinter window
        self.mainLabel = Tkinter.Label(
            self.window, text='Please enter the corner coordinates of your chart')
        self.topLeftLabel = Tkinter.Label(self.window, text='Top Left')
        self.bottomRightLabel = Tkinter.Label(self.window, text='Bottom Right')
        # entry widget where the user types
        self.topLeftEntry = Tkinter.Entry(self.window)
        # entry widget where the user types
        self.bottomRightEntry = Tkinter.Entry(self.window)
        self.enterButton = Tkinter.Button(
            self.window, text='Enter', command=self.store)

        # Here all the widgets in the class are packed
        self.mainLabel.grid(row=0, column=0, columnspan=3, padx=4, pady=4)
        self.topLeftLabel.grid(row=1, column=0)
        self.topLeftEntry.grid(row=1, column=1, columnspan=1, sticky='WE')
        self.bottomRightLabel.grid(row=2, column=0)
        self.bottomRightEntry.grid(row=2, column=1, columnspan=2, sticky='WE')
        self.topLeftEntry.insert(0, '(-98,30)')
        self.bottomRightEntry.insert(0, '(-94,26.5)')
        self.enterButton.grid(row=2, column=2, sticky='WE',
                              columnspan=2, pady=4, padx=4)

        # starts the main loop
        self.window.mainloop()

    # this function is called by the enter button in the coordinate window,
    # and it gets the coordinates that was entered by the user
    def store(self):
        parent = self.parent
        self.topLeft = self.topLeftEntry.get()  # stores the corner in self.topLeft
        # stores the corner in self.bottomRight
        self.bottomRight = self.bottomRightEntry.get()

        self.coordintes = (self.topLeftEntry.get(),
                           self.bottomRightEntry.get())
        # print self.coordinates

        self.window.destroy()

# This class defines the main window the user uses to work with the program, all commands could be used from here


class mainWnd():
    def __init__(self):
        self.chartSize = (900, 730)
        self.coordinates = None  # ((-98,30),(-94,26.5))
        self.center = None  # (-96, 28.25)
        self.chartScale = None
        self.image = None
        self.chart = None
        self.updatedChart = None
        self.chartPIL = None
        self.window = Tkinter.Tk()
        self.window.title('  SailNav')
        self.APIkey = '11eeca74a8b2f9b1f39efc06abcc590863a76aa3'

        # defining the frames
        self.sideBarFrame = Tkinter.Frame(self.window, height=751, width=120)
        self.sideBarBox1 = Tkinter.Frame(
            self.sideBarFrame, height=150, width=120, bd=2)
        self.sideBarBox2 = Tkinter.Frame(
            self.sideBarFrame, height=150, width=120, bd=2)
        self.mapFrame = Tkinter.Frame(
            self.window, height=735, width=900, bg='Red')

        #\\\\    Defining the widgets in the frames    ////

        self.menuBar = Tkinter.Menu(self.window)  # Creates the Menubar

        # File button on the menubar
        self.fileDropdown = Tkinter.Menu(
            self.menuBar, tearoff=0)  # Creates the File dropdown
        # fills the dropdown with commands
        self.fileDropdown.add_command(label='Import', command=self.importChart)
        self.fileDropdown.add_command(label='Save')
        self.fileDropdown.add_command(
            label='Coordinates', command=self.getCoordinates)
        # makes the file menu cascade
        self.menuBar.add_cascade(label='File', menu=self.fileDropdown)

        # Toggle button on the menubar
        # Creates the viewing options menu
        self.toggleDropdown = Tkinter.Menu(self.menuBar, tearoff=0)
        self.toggleDropdown.add_command(label='Boats', command=self.getBoats)
        self.toggleDropdown.add_checkbutton(
            label='Weather', command=self.getWeather)
        self.toggleDropdown.add_checkbutton(label='Waves')
        self.toggleDropdown.add_checkbutton(label='Plotted Course')
        # makes the toggleDropdown
        self.menuBar.add_cascade(label='Toggle', menu=self.toggleDropdown)

        self.window.config(menu=self.menuBar)  # displays the menubar

        # \\\\   Defining widgets in the sidebar   ////
        self.weatherCoordinateLabel = Tkinter.Label(
            self.sideBarBox1, text='Enter the coordintes \n of the top left corner \n of the chart')
        self.lonLabel = Tkinter.Label(self.sideBarBox1, text='Longitude')
        self.lonEntry = Tkinter.Entry(self.sideBarBox1)
        self.latLabel = Tkinter.Label(self.sideBarBox1, text='Latitude')
        self.latEntry = Tkinter.Entry(self.sideBarBox1)
        self.enterCoordinates = Tkinter.Button(
            self.sideBarBox1, text='Enter', command=self.getWeather)

        #\\\\    Defining the zoom functionality    ////
        self.zoominButton = Tkinter.Button(
            self.sideBarBox2, text='Zoom In', command=self.zoomin)
        self.zoomoutButton = Tkinter.Button(
            self.sideBarBox2, text='Zoom Out', command=self.zoomout)

        #\\\\    PACKING OF THE SIDEBAR AND THE CHART DISPLAY    ////
        self.sideBarFrame.grid(row=1, column=4, sticky='N', padx=0, pady=0)
        self.sideBarBox1.grid(row=0, column=0, sticky='N')
        self.sideBarBox2.grid(row=1, column=0, sticky='N')
        self.mapFrame.grid(row=1, column=0, sticky='NSEW', padx=0, pady=0)

        #\\\\    PACKING OF THE ZOOM FUNCTIONALITY   ////
        self.zoominButton.grid(row=0, column=0, sticky='WE')
        self.zoomoutButton.grid(row=1, column=0, sticky='WE')

        #\\\\    PACKING OF THE COORDINATE ENTRY FOR WEATHER    ////
        self.weatherCoordinateLabel.grid(row=0, column=0, columnspan=2)
        self.lonLabel.grid(row=1, column=0)
        self.lonEntry.grid(row=1, column=1)
        self.latLabel.grid(row=2, column=0)
        self.latEntry.grid(row=2, column=1)
        self.enterCoordinates.grid(row=3, column=0, columnspan=2, sticky='WE')

        #\\\\    PACKING OF THE SCROLL BARS     ////
        self.verticalScroll = Tkinter.Scrollbar(self.mapFrame)
        self.horizontalScroll = Tkinter.Scrollbar(self.mapFrame)

        #\\\\    THE CANVAS IS CONFIGURED   ////
        self.canvas = Tkinter.Canvas(self.mapFrame, bg='Pink', yscrollcommand=self.verticalScroll.set,
                                     xscrollcommand=self.horizontalScroll.set, width=self.chartSize[0], height=self.chartSize[1])
        self.canvas.config(scrollregion=(
            0, 0, self.chartSize[0], self.chartSize[1]))

        self.canvas.grid(row=0, column=0)
        self.verticalScroll.grid(row=0, column=1, sticky='ns')
        self.horizontalScroll.grid(row=1, column=0, rowspan=4, sticky='we')

        self.verticalScroll.config(command=self.canvas.yview)
        self.horizontalScroll.config(
            command=self.canvas.xview, orient='horizontal')

        self.window.mainloop()

    #\\\\    Definition of class functions    ////
    def zoomin(self):  # Pretty self explanatory but this is the zoom in function
        self.canvas.scale('all', 1.5, 1.1, 1, 1)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def zoomout(self):  # Zoom out function
        self.canvas.scale('all', 0.9, 0.9, 1, 1)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    # This function is used to calculate the chart scale in order to lay out the boats
    def findChartScale(self):
        if self.coordinates[0][0] < self.coordinates[1][0]:
            #
            lon_min = self.coordinates[0][0]
            lon_max = self.coordinates[1][0]
        else:
            lon_min = self.coordinates[1][0]
            lon_max = self.coordinates[0][0]

        if self.coordinates[0][1] < self.coordinates[1][1]:
            lat_min = self.coordinates[0][1]
            lat_max = self.coordinates[1][1]
        else:
            lat_min = self.coordinates[1][1]
            lat_max = self.coordinates[0][1]

        self.chartScale = (((1000 / (lon_max - lon_min)) +
                            (1000 / (lat_max - lat_min))) / 2)

    # This function creates an instance of the xyWnd class which is used to get the coordinate information of the chart
    def getCoordinates(self):
        coordinateWindow = xyWnd(self)

    # This function finds the centerpoint of the chart
    def fromLatLon2Cartesian(self, ((Lat1, Lon1), (Lat2, Lon2))):
        centerCoordinate = (((Lat1 + Lat2) / 2), ((Lon1 + Lon2) / 2))
        self.center = centerCoordinate

    # This function imports the chart
    def importChart(self):
        importWindow = impWnd(self)

    # This function gets weather information of the area displayed in the chart
    def getWeather(self):
        zoom = 5  # seems to work best with nautical charts
        if self.latEntry.get() == '' or self.lonEntry.get() == '':
            print 'No coordinate given'
            return
        else:
            Coordinates = (float(self.latEntry.get()),
                           float(self.lonEntry.get()))
            # gets the tile for a given area and zoom
            weatherOverlay = Image.open(
                getTile(convertToTiles(Coordinates, zoom)))
            # gets the size of the chart to calcualte the amount of resizing she needs
            chartSize = self.chartPIL.size
            weatherOverlay = weatherOverlay.resize(
                chartSize)  # resizez the wather Overlay

            # merges the overlay with the original image
            self.chartPIL.paste(weatherOverlay, (0, 0), weatherOverlay)
            # Passes the image created by PIL to Tkinter for display
            self.updatedChart = ImageTk.PhotoImage(self.chartPIL)
            self.canvas.delete('all')  # Clears the canvas
            # Displays the new chart image on the canvas
            self.canvas.create_image(
                0, 0, image=self.updatedChart, anchor='nw')
            self.window.update()  # updates the windows
            self.window.update_idletasks()

    # This function is used to get boat information
    def getBoats(self):
        self.findChartScale()  # Finds the scale of the chart
        boatdata = getMarineData(
            self.APIkey, self.coordinates)  # Gets the boat data
        # created boats and stores them in a dictionary
        boatDict = createBoats(boatdata, parent=self)

        for i in boatDict.keys():  # Calls the determineRelativeLocation function of the boat class to find the location of the boats realtive to the chart
            boatDict[i].determineRelativeLocation(
                Center=boatDict[i].chartCenter, Lat=boatDict[i].LAT, Lon=boatDict[i].LON)
        for i in boatDict.keys():  # calls the draw function of the boat class to draw the boats on the canvas
            boatDict[i].draw()
            # print i, 'drawn'


mainWindow = mainWnd()  # Run the whole thing
