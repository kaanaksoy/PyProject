# Code designed and written by: Kaan Aksoy
# Carnegie Mellon University Andrew ID: kaana
# File Created: November 10, 16:00

# Modification History:
# Start               End
# Nov 10 16:00        Nov 10 19:30
# Nov 11 14:00        Nov 12 04:30
# Nov 12 06:00        Nov 12 13:20
# Nov 14 03:30        Nov 14 04:30
# Nov 22 16:30        Nov 22 19:30
# Nov 24 13:30        Nov 24 20:20
# Nov 25 15:00        Nov 26 08:30
# Nov 26 19:00        Nov 27 02:00
# Nov 27 09:30        Nov 27 14:10

import ctypes
import cStringIO
import math
from PIL import Image, ImageTk, ImageGrab
from Tkconstants import LEFT, CENTER, W, SUNKEN, X, Y
import Tkinter
from Tkinter import Label, StringVar, Entry, Button, Menu, Frame, Tk, Canvas
import urllib2 as urllib


#\\\\\\\\\\\\\          Helper Functions are defined here        ///////////////////

#This function is used to adjust the main window to the size of the screen
def getScreenSize():
    user32 = ctypes.windll.user32
    return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

#Here we use the size of the chart Window to resize the imported chart
def resizeChart(chart, canvasHeight):
    chartSize = chart.size
    scaleFactor = float(chartSize[1] / canvasHeight)
    chartSize = (int(chartSize[0] / scaleFactor), int(chartSize[1] / scaleFactor))
    return chart.resize(chartSize, Image.BICUBIC)

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
    # #print request #Used for debuggung purposes
    mTrafficData = urllib.urlopen(request)  # Request marine data
    data = mTrafficData.read()

    # The folowing data is used for debugging etc. if you would like to use actual data, comment out this area
    data = [["304010417", "9015462", "359396", "-94", "32.5", "74", "137", "327", "8", "2017-05-19T09:39:57", "TER", "54"],
            ["215819000", "9034731", "150559", "-94", "36",  "122", "162", "157", "7", "2017-05-19T09:44:27", "TER", "28"],
             ["255925000", "9184433", "300518", "-92.5", "32", "79", "253", "311", "6", "2017-05-19T09:43:53", "TER", "52"],
             ["255925000", "9184433", "300518", "-96.5", "35.2", "79", "321", "311", "9", "2017-05-19T09:43:53", "TER", "52"]]


    return data


# This function gets the raw data and creates instances of the boat class with the appropriate parameters
def cleanUpMarineData(data, parent):
    parent = parent
    boats = {}
    for i in range(len(data)):
        boats['boat' + str(i)] = Boat(boatData=data[i], parent=parent)
    return boats

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
def convertToTiles((lon, lat), zoom):
    # Adapted from the pseudocode available at http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
    latrad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(latrad) + (1 / math.cos(latrad))) / math.pi) / 2.0 * n)
    return (xtile, ytile, zoom)


class Boat():  # This is the Boat class, its instances are displayed on the nautical chart.
    def __init__(self, parent, boatData):
        self.chartCenter = parent.center #Center of the chart
        ##print self.chartCenter
        self.parent = parent #Parent of the instance
        self.coordinates = parent.coordinates

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
        self.radius = 22 #self.radius of the cirlce, the vessel marker is inscribed in
        self.chartScale = parent.chartScale
        self.statusDict = {0: 'Green', 1: 'Grey', 2: 'Black', 3: 'Orange',
                           4: 'Pink', 5: 'Yellow', 6: 'Blue', 7: 'Red', 8: 'Purple'}

    # This function is used to connect the status of the boat to a color
    def determineStatus(self, STATUS):
        if STATUS in self.statusDict:
            return self.statusDict[STATUS]
        else:
            return 'White'

    #Finds how far away is a boat from the top left corner of the chart
    def determineRelativeLocation(self, coord, Lat, Lon):
        #print Center
        self.relativeLocation = (coord[0][0]-Lat,coord[0][1]-Lon)
        #self.relativeLocation = (Lat - Center[0], Lon - Center[1])

    #This function is used to rotate the boats about their center
    def rotate(self, origin, point, angle):
        #Adapted from https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
        #Rotate a point counterclockwise by a given angle around a given origin.

        angle = math.radians(-angle)
        Xo = origin[0]
        Yo = origin[1]

        Xp = point[0]
        Yp = point[1]

        Xq = Xo + math.cos(angle) * (Xp - Xo) - math.sin(angle) * (Yp - Yo)
        Yq = Yo + math.sin(angle) * (Xp - Xo) + math.cos(angle) * (Yp - Yo)
        return (Xq, Yq)
    #This function is used to be able to graw an arrow shaped polygon to symbolize the boats
    def findCoordinates(self, radius, BoatLatLon, angle):
        center = ((BoatLatLon[0]) / 2, (BoatLatLon[1]) / 2) # Finds the center of the boat polygon

        #Find the location of the individual points to plot an arrow looking shape (All points have to be rotated in order to have the arrow face right, to make it easy when adding rotations)
        #2.1 and 2.75 are coefficients that are used to form a properly sized arrow point. they keep the sizes standard

        A = self.rotate(center, (center[0], center[1] + radius), 90)
        B = self.rotate(center, (center[0] + ( (2.1 * radius) / 2.75), center[1] - (radius - (radius / 2.75))), 90)
        C = self.rotate(center, (center[0], center[1] - (radius - ((2 * radius) / 2.75) ) ), 90)
        D = self.rotate(center, (center[0] - ((2.1 * radius) / 2.75), center[1] - (radius - (radius / 2.75))), 90)

        polyList = [] #Creates a List to store the point information
        for j in (A, B, C, D): #uses a for loop to enter the point information to the list
            polyList.append(self.rotate(center, j, angle))
        return polyList

    def drawCourse(self, angle, BoatLatLon, speed):
        speed = speed/10 #the service gives us the speed in knots X10 so we divide by 10
        angle = math.radians(angle)
        center = ((BoatLatLon[0]) / 2, (BoatLatLon[1]) / 2) # Finds the center of the boat polygon
        lenghtofCourse = (speed * 25) #to create a distinguishable line
        finalPoint = (center[0] + lenghtofCourse * math.cos(angle), center[1] - lenghtofCourse * math.sin(angle))
        courseList = [(center[0], center[1]), (finalPoint[0], finalPoint[1])]
        return courseList

    #This function draws a boat from the points that were given to it
    def draw(self):
        parent = self.parent
        location = (abs((self.relativeLocation[0] * parent.chartScale) + parent.coordinates[0][0]), abs((self.relativeLocation[1] * parent.chartScale) + parent.coordinates[0][1]))
        polyList = self.findCoordinates(self.radius, location, self.HEADING)
        courseList = self.drawCourse(self.HEADING, location, self.SPEED)

        parent.canvas.create_line(courseList[0][0], courseList[0][1], courseList[1][0], courseList[1][1], fill='Black', width=2)
        parent.canvas.create_polygon(polyList[0][0], polyList[0][1], polyList[1][0], polyList[1][1], polyList[2][0], polyList[2][1], polyList[3][0], polyList[3][1], fill= self.determineStatus(self.STATUS), outline='black')
        parent.window.update()
        parent.window.update_idletasks()


class impWnd():  # This class is creates an import window for the user to enter a path to import a file
    def __init__(self, parent):
        self.parent = parent
        self.screenSize = None
        self.window = Tkinter.Tk()  # creates the tkinter window
        self.label = Tkinter.Label(self.window, text='Please enter the path for your desired chart')
        # entry widget where the user types
        self.textBox = Tkinter.Entry(self.window)
        self.enterButton = Tkinter.Button(self.window, text='Enter', command=self.imp)
        self.browseButton = Tkinter.Button(self.window, text='Browse...', command=self.browse)
        self.pathVar = ''  # variable where the path for the file is stored
        self.window.title('  SailNav - Import')

        # here all the widgets in the class are packed
        self.label.grid(row=0, column=0, columnspan=3, padx=4, pady=4)
        self.textBox.grid(row=1, column=0, columnspan=3,sticky='WE', padx=4, pady=4)
        #self.textBox.insert(0, 'C:\Users\kaana\Desktop\Python Final Project\Example1.png')
        self.enterButton.grid(row=2, column=2, sticky='WE',columnspan=2, pady=4, padx=4)
        self.browseButton.grid(row=1, column=3, sticky='WE', columnspan=2, padx=4, pady=4)
        self.enterButton.bind('<Return>', self.imp)
        # starts the main loop
        self.window.mainloop()

    def browse(self):
        self.pathVar = tkFileDialog.askopenfilename(parent=self.window)
        self.textBox.insert(0, self.pathVar)
        ##print self.pathVar

    # this function is called by the enter button in the import window, and it gets the path that was entered by the user
    def imp(self):
        parent = self.parent
        self.pathVar = self.textBox.get()  # stores the path in self.pathVar
        if self.pathVar == None:
            return
        self.chartPIL = Image.open(self.pathVar)
        self.screenSize = getScreenSize()
        self.chartPIL = resizeChart(self.chartPIL, self.screenSize[1]-100)
        self.chart = ImageTk.PhotoImage(self.chartPIL)
        parent.chartSize = self.chartPIL.size
        parent.chart = self.chart
        parent.chartPIL = self.chartPIL

        parent.canvas.create_image(0,0, image=self.chart, anchor='nw')
        parent.canvas.config(scrollregion=(0, 0 , parent.chartSize[0], parent.chartSize[1]), width=parent.chartSize[0], height=parent.chartSize[1])
        self.enterButton.unbind('<Return>')
        parent.window.update()
        parent.window.update_idletasks()
        self.window.destroy()
        coordinateWindow = xyWnd(self.parent)


class xyWnd():  # This class is creates an window for the user to enter a information regarding the chart they are looking at
    def __init__(self, parent):
        self.parent = parent
        self.topLeft = ''
        self.bottomRight = ''
        self.coordinates = ''
        self.window = Tkinter.Tk()  # creates the tkinter window
        self.window.title('  SailNav - Location')

        self.mainLabel = Tkinter.Label(self.window, text='Please enter the corner coordinates of your chart')
        self.topLeftLabel = Tkinter.Label(self.window, text='Top Left')
        self.bottomRightLabel = Tkinter.Label(self.window, text='Bottom Right')
        self.LonLabel = Tkinter.Label(self.window, text='Longitude')
        self.LatLabel = Tkinter.Label(self.window, text='Latitide')

        # entry widget where the user types
        self.topLeftEntryLon = Tkinter.Entry(self.window)
        self.topLeftEntryLat = Tkinter.Entry(self.window)

        # entry widget where the user types
        self.bottomRightEntryLon = Tkinter.Entry(self.window)
        self.bottomRightEntryLat = Tkinter.Entry(self.window)

        self.enterButton = Tkinter.Button(self.window, text='Enter', command=self.store)

        # Here all the widgets in the class are packed
        self.mainLabel.grid(row=0, column=0, columnspan=3, padx=4, pady=4)
        self.LonLabel.grid(row=1, column=2, columnspan=1)
        self.LatLabel.grid(row=1, column=1, columnspan=1)
        self.topLeftLabel.grid(row=2, column=0)
        self.topLeftEntryLon.grid(row=2, column=2, columnspan=1, sticky='WE')
        self.topLeftEntryLat.grid(row=2, column=1, columnspan=1, sticky='WE')
        self.bottomRightLabel.grid(row=3, column=0)
        self.bottomRightEntryLon.grid(row=3, column=2, columnspan=1, sticky='WE')
        self.bottomRightEntryLat.grid(row=3, column=1, columnspan=1, sticky='WE')
        self.topLeftEntryLon.insert(0,'-98')
        self.topLeftEntryLat.insert(0, '30')
        self.bottomRightEntryLon.insert(0,'-94')
        self.bottomRightEntryLat.insert(0, '26.5')
        self.enterButton.grid(row=2, column=3, sticky='NS',rowspan=2)

        # starts the main loop
        self.window.mainloop()

    # this function is called by the enter button in the coordinate window,
    # and it gets the coordinates that was entered by the user
    def store(self):
        parent = self.parent
        self.coordinates = ( (float(self.topLeftEntryLon.get()), float(self.topLeftEntryLat.get())) , (float(self.bottomRightEntryLon.get()), float(self.bottomRightEntryLat.get())) )
        self.parent.coordinates = self.coordinates
        self.window.destroy()

    #This is a basic class, the only reason it exists is to hold its cartesian coordinates
class Point():
    # \ Class Description ////
    def __init__(self, xcord, ycord):
        self.coordinates = (xcord,ycord)

# This class defines the main window the user uses to work with the program, all commands could be used from here
class mainWnd():
    def __init__(self):
        self.chartSize = (900, 730)
        self.displaySize = getScreenSize()
        self.coordinates = None  # ((-98,30),(-94,26.5))
        self.center = (-96, 28.25)
        self.chartScale = None
        self.image = None #This image of the chart is displayed in the canvas, and is not editable
        self.chart = None #Opened chart file
        self.updatedChart = None #Used while updating the canvas image
        self.chartPIL = None #This is the editable, PIL based image of the chart
        self.window = Tkinter.Tk()
        self.window.title('  SailNav')
        self.APIkey = '11eeca74a8b2f9b1f39efc06abcc590863a76aa3'

        self.pointList = []
        self.lineWidth = 5
        self.lineColor = 'black'
        self.plotState = False

        # defining the frames
        self.sideBarFrame = Tkinter.Frame(self.window, height=751, width=120)
        self.sideBarBox1 = Tkinter.Frame(self.sideBarFrame, height=150, width=120, bd=2)
        self.sideBarBox2 = Tkinter.Frame(self.sideBarFrame, height=150, width=120, bd=2)
        self.mapSideFrame = Tkinter.Frame(self.window, height=751, width=900, bg='Blue')
        self.mapFrame = Tkinter.Frame(self.mapSideFrame, height=735, width=900, bg='Red')
        self.scrollFrame = Tkinter.Frame(self.mapSideFrame, height=15, width=900, bg='Green')

        #\\\\    Defining the widgets in the frames    ////

        self.menuBar = Tkinter.Menu(self.window)  # Creates the Menubar
        # File button on the menubar
        self.fileDropdown = Tkinter.Menu(self.menuBar, tearoff=0)  # Creates the File dropdown
        # fills the dropdown with commands
        self.fileDropdown.add_command(label='Import', command=self.importChart)
        self.fileDropdown.add_command(label='Save', command=self.save)
        self.fileDropdown.add_command(label='Coordinates', command=self.getCoordinates)
        # makes the file menu cascade
        self.menuBar.add_cascade(label='File', menu=self.fileDropdown)

        # Toggle button on the menubar
        # Creates the viewing options menu
        self.toggleDropdown = Tkinter.Menu(self.menuBar, tearoff=0)
        self.toggleDropdown.add_command(label='Boats', command=self.getBoats)
        self.toggleDropdown.add_checkbutton(label='Weather', command=self.getWeather)
        self.menuBar.add_cascade(label='Display', menu=self.toggleDropdown)

        self.window.config(menu=self.menuBar)  # displays the menubar

        # \\\\   Defining widgets in the sidebar   ////
        self.plotButton = Tkinter.Button(self.sideBarBox1, text='Plot Course', command=self.plotToggle)

        #\\\\    PACKING OF THE SIDEBAR AND THE CHART DISPLAY    ////
        self.mapSideFrame.pack(side='left', expand=1, fill='both')
        self.sideBarFrame.pack(side='left', expand=0, fill='both')
        self.sideBarBox1.pack(fill=X)
        self.sideBarBox2.pack(fill=X)

        self.scrollFrame.pack(expand=1, fill='both')
        self.mapFrame.pack(expand=1, fill='both')

        #\\\\    PACKING OF THE PLOT BUTTON    ////
        self.plotButton.pack(fill=X, expand=1)

        #\\\\    PACKING OF THE SCROLL BARS     ////
        self.verticalScroll = Tkinter.Scrollbar(self.mapFrame)
        self.horizontalScroll = Tkinter.Scrollbar(self.scrollFrame)

        #\\\\    THE CANVAS IS CONFIGURED   ////
        self.canvas = Tkinter.Canvas(self.mapFrame, bg='Pink', yscrollcommand=self.verticalScroll.set,xscrollcommand=self.horizontalScroll.set, width=self.chartSize[0], height=self.displaySize[1]-100)
        self.canvas.config(scrollregion=(0, 0, self.displaySize[0], self.displaySize[1]))

        self.canvas.pack(side='left', fill='both', expand=1)
        self.horizontalScroll.pack(fill='both', expand=1)
        self.verticalScroll.pack(side='left',fill='both', expand=0)

        self.verticalScroll.config(command=self.canvas.yview)
        self.horizontalScroll.config(command=self.canvas.xview, orient='horizontal')

        self.window.mainloop()

    #\\\\    Definition of class functions    ////
    def save(self):
        savename = 'im_{0:0>6}'.format(0)
        ImageGrab.grab((0,0,self.chartSize[0],self.chartSize[1])).save(savename + '.jpg')

    def plotToggle(self):
        if self.plotState == False:
            self.canvas.bind('<Button-1>', self.addPoint)
            self.plotButton.config(bg='dark grey')
            self.plotState = True
        else:
            self.canvas.unbind('<Button-1>')
            self.plotButton.config(bg='white')
            self.plotState = False

    def addPoint(self, event):
        self.plotPoint(event)

    def plotPoint(self, event):
        y_offset = self.verticalScroll.get()
        x_offset = self.horizontalScroll.get()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        Chart = self.chartSize
        Diff_x = Chart[0] - canvas_width
        Diff_y = Chart[1] - canvas_height

        x = event.x
        y = event.y + int(Diff_y * y_offset[0] * 12.5)#[]+ self.canvas.yview
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='Black')
        self.pointList.append(Point(x, y))
        if len(self.pointList) > 1:
            self.connectTheDots(self.pointList[-2], self.pointList[-1])

        AllPoints = self.canvas.find_all()
        self.window.update()
        self.window.update_idletasks()

    def moveUnder(self, thing):
        overlap = self.canvas.find_overlapping(0,0,self.chartSize[0], self.chartSize[1])
        for object in overlap:
            self.canvas.tag_lower(thing)

    def connectTheDots(self, oldcoord, newcoord):
        self.canvas.create_line(oldcoord.coordinates[0], oldcoord.coordinates[1], newcoord.coordinates[0], newcoord.coordinates[1], width=self.lineWidth, fill=self.lineColor, capstyle=Tkinter.ROUND, smooth=Tkinter.TRUE, splinesteps=36)
        self.window.update()
        self.window.update_idletasks()

    # This function is used to calculate the chart scale in order to lay out the boats
    def findChartScale(self):
        if self.coordinates[0][0] < self.coordinates[1][0]:
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

        lat_min = float(lat_min)
        lat_max = float(lat_max)
        lon_min = float(lon_min)
        lon_max = float(lon_max)

        self.chartScale = (((self.chartSize[0] / (lon_max - lon_min)) + (self.chartSize[1] / (lat_max - lat_min))) / 2)

    # This function creates an instance of the xyWnd class which is used to get the coordinate information of the chart
    def getCoordinates(self):
        coordinateWindow = xyWnd(self)

    # This function finds the centerpoint of the chart
    def fromLatLon2Cartesian(self, ((Lat1, Lon1), (Lat2, Lon2))):
        centerCoordinate = (((Lat1 + Lat2) / 2), ((Lon1 + Lon2) / 2))
        self.center = centerCoordinate
        #print self.center, 'Line 520'

    # This function imports the chart
    def importChart(self):
        importWindow = impWnd(self)


    # This function gets weather information of the area displayed in the chart
    def getWeather(self):
        zoom = 5  # seems to work best with nautical charts
        if self.coordinates == None:
            self.getCoordinates()
        else:
            #print self.coordinates
            Coordinates = (self.coordinates[0][0], self.coordinates[0][1])
            # gets the tile for a given area and zoom
            weatherOverlay = Image.open(getTile(convertToTiles(Coordinates, zoom)))
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
        boatdata = getMarineData(self.APIkey, self.coordinates)  # Gets the boat data
        # created boats and stores them in a dictionary
        boatDict = cleanUpMarineData(boatdata, parent=self)
        for i in boatDict.keys():  # Calls the determineRelativeLocation function of the boat class to find the location of the boats realtive to the chart
            boatDict[i].determineRelativeLocation(
                coord=self.coordinates, Lat=boatDict[i].LAT, Lon=boatDict[i].LON)
        for i in boatDict.keys():  # calls the draw function of the boat class to draw the boats on the canvas
            boatDict[i].draw()

mainWindow = mainWnd()  # Run the whole thing
