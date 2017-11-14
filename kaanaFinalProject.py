# Code designed and written by: Kaan Aksoy
# Andrew ID: kaana
# File Created: November 10, 16:00
# Modification History:
# Start               End
# Nov 10 16:00        Nov 10 19:30
# Nov 11 14:00        Nov 12 04:30
# Nov 12 06:00        Nov 12 13:20

import Tkinter
from Tkinter import Label, StringVar, Entry, Button, Menu, Frame, Tk, Canvas
from Tkconstants import LEFT, CENTER,W, SUNKEN , X, Y
from PIL import Image, ImageTk
import urllib2 as urllib
import cStringIO
import math

#This function takes the tile paramaters as inputs and fetches the appropriate tile from the web
def getMarineData(APIkey, Coordinates):
    ageOfData = 1440

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

    request = 'http://services.marinetraffic.com/api/exportvessels/' + 'v' + ':8/' + APIkey + '/MINLAT:' + str(lat_min) + '/MAXLAT:' + str(lat_max) + '/MINLON:' + str(lon_min) + '/MAXLON:' + str(lon_max) + '/timespan' + ':' + str(ageOfData) + '/protocol:json'
    print request
    mTrafficData = urllib.urlopen(request)
    data = mTrafficData.read()
    print data
    data = [["304010417","9015462","359396","-97.67599","28.69228","74","329","327","0","2017-05-19T09:39:57","TER","54"], ["215819000","9034731","150559","-94.15851","29.53593","122","162","157","0","2017-05-19T09:44:27","TER","28"], ["255925000","9184433","300518","-97.38166","26.56094","79","316","311","0","2017-05-19T09:43:53","TER","52"]]
    return data

def cleanUpMarineData(data, parent):
    boats = {}
    for i in range(len(data)):
        boats['boat' + str(i)] = Boat(boatData=data[i], parent=parent)
    return boats

def fromLatLon2Cartesian((Lat1,Lon1),(Lat2,Lon2)):
    centerCoordinate = (((Lat1 - Lat2) / 2),((Lon1 - Lon2) / 2))
    print centerCoordinate


def getTile((xtile,ytile,zoom)):
    #creates the proper URL for the desired tile
    weatherOverlayURL = "https://weather.openportguide.de/tiles/actual/wind_stream/5/" + str(zoom) + "/" + str(xtile) + "/" + str(ytile) + ".png"
    tile = urllib.urlopen(weatherOverlayURL) #Opens the URL
    tile = cStringIO.StringIO(tile.read()) #Converts it so it could be read by PIL
    return tile

    #This function uses the top left corner coordinate to calculate the appropriate tile parameters
def convertToTiles((lat, lon), zoom):
    #Derived from the pseudocode available at http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
    latrad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(latrad) + (1 / math.cos(latrad))) / math.pi) / 2.0 * n)
    return (xtile,ytile,zoom)

class Boat():
    def __init__(self, parent, boatData ):
        self.chartCenter = parent.center
        self.parent = parent
        self.SHIP_ID = boatData[2]
        self.LAT = float(boatData[3])
        self.LON = float(boatData[4])
        self.HEADING = int(boatData[6])
        self.STATUS = int(boatData[8])
        self.relativeLocation = None
        self.radius = 25
        self.chartScale = parent.chartScale
        self.statusDict = {0:'Green', 1:'Grey', 2:'Black', 3:'Orange', 4:'Pink', 5:'Yellow', 6:'Blue', 7:'Red', 8:'Purple'}

    def determineStatus(self):
        if self.STATUS in self.statusDict:
            return self.statusDict[self.STATUS]
        else:
            return 'White'

    def determineRelativeLocation(self, Center, Lat, Lon):
        self.relativeLocation = (Lat - Center[0], Lon - Center[1])

    def draw(self):
        parent = self.parent
        location = ((self.relativeLocation[0]) * parent.chartScale), (self.relativeLocation[1] * parent.chartScale)
        parent.canvas.create_oval(location[0], location[1], location[0] + 2*self.radius, location[1] + 2*self.radius, fill=self.determineStatus())
        parent.window.update()
        parent.window.update_idletasks()


class impWnd(): #This class is creates an import window for the user to enter a path to import a file
    def __init__(self, parent):
        self.parent = parent
        self.window = Tkinter.Tk() #creates the tkinter window
        self.label = Tkinter.Label(self.window, text='Please enter the path for your desired chart')
        self.textBox = Tkinter.Entry(self.window) #entry widget where the user types
        self.enterButton = Tkinter.Button(self.window, text='Enter', command=self.imp)
        self.pathVar = '' #variable where the path for the file is stored

        #here all the widgets in the class are packed
        self.label.grid(row=0, column=0,columnspan=3, padx=4, pady=4)
        self.textBox.grid(row=1, column=0,columnspan=3, sticky ='WE', padx=4, pady=4)
        self.textBox.insert(0,'C:\Users\kaana\Desktop\Python Final Project\Example1.png')
        self.enterButton.grid(row=2, column=2, sticky='WE', columnspan=2, pady=4, padx=4)

        #starts the main loop
        self.window.mainloop()

    #this function is called by the enter button in the import window,
    #and it gets the path that was entered by the user
    def imp(self):
        parent = self.parent
        self.pathVar = self.textBox.get() #stores the path in self.pathVar
        self.chartPIL = Image.open(self.pathVar)
        self.chart = ImageTk.PhotoImage(self.chartPIL)
        parent.chartSize = self.chartPIL.size
        parent.chart = self.chart
        parent.chartPIL = self.chartPIL
        parent.canvas.create_image(0,0, image=self.chart, anchor='nw')
        parent.canvas.config(scrollregion=(0,0,parent.chartSize[0], parent.chartSize[1]))
        parent.window.update()
        parent.window.update_idletasks()
        #chart = Image.open(self.pathVar)
        #chart.show()
        self.window.destroy()

class xyWnd(): #This class is creates an import window for the user to enter a path to import a file
    def __init__(self, parent):
        self.parent = parent
        self.topLeft = ''
        self.bottomRight = ''
        self.coordinates = ''
        self.window = Tkinter.Tk() #creates the tkinter window
        self.mainLabel = Tkinter.Label(self.window, text='Please enter the corner coordinates of your chart')
        self.topLeftLabel = Tkinter.Label(self.window, text='Top Left')
        self.bottomRightLabel = Tkinter.Label(self.window, text='Bottom Right')
        self.topLeftEntry = Tkinter.Entry(self.window) #entry widget where the user types
        self.bottomRightEntry = Tkinter.Entry(self.window) #entry widget where the user types
        self.enterButton = Tkinter.Button(self.window, text='Enter', command=self.store)

        #here all the widgets in the class are packed
        self.mainLabel.grid(row=0, column=0,columnspan=3, padx=4, pady=4)
        self.topLeftLabel.grid(row=1, column=0)
        self.topLeftEntry.grid(row=1, column=1,columnspan=1, sticky ='WE')
        self.bottomRightLabel.grid(row=2,column=0)
        self.bottomRightEntry.grid(row=2, column=1,columnspan=2, sticky ='WE')
        self.topLeftEntry.insert(0,'(-98,30)')
        self.bottomRightEntry.insert(0,'(-94,26.5)')
        self.enterButton.grid(row=2, column=2, sticky='WE', columnspan=2, pady=4, padx=4)

        #starts the main loop
        self.window.mainloop()

    #this function is called by the enter button in the coordinate window,
    #and it gets the coordinates that was entered by the user
    def store(self):
        parent = self.parent
        self.topLeft = self.topLeftEntry.get() #stores the corner in self.topLeft
        self.bottomRight = self.bottomRightEntry.get() #stores the corner in self.bottomRight

        self.coordintes = (self.topLeftEntry.get(),self.bottomRightEntry.get())
        print self.coordinates

        self.window.destroy()

class mainWnd():
    def __init__(self):
        self.chartSize = (900,730)
        self.coordinates = ((-98,30),(-94,26.5))
        self.center = (-96, 28.25)
        self.chartScale = None
        self.image = None
        self.chart = None
        self.updatedChart = None
        self.chartPIL = None
        self.window = Tkinter.Tk()
        self.window.title('  SailNav')
        self.APIkey = '11eeca74a8b2f9b1f39efc06abcc590863a76aa3'


        #defining the frames
        self.sideBarFrame = Tkinter.Frame(self.window,height=751, width=120)
        self.sideBarBox1 = Tkinter.Frame(self.sideBarFrame,height=150, width=120, bd=2)
        self.sideBarBox2 = Tkinter.Frame(self.sideBarFrame,height=150, width=120, bd=2)
        self.mapFrame = Tkinter.Frame(self.window,height=735, width=900, bg='Red')

        #Defining the widgets in the frames
        self.menuBar = Tkinter.Menu(self.window) #Creates the Menubar

        self.fileMenu = Tkinter.Menu(self.menuBar, tearoff=0) #Creates the File dropdown
        self.fileMenu.add_command(label='Import', command=self.importChart) #fills the dropdown with commands
        self.fileMenu.add_command(label='Save')
        self.fileMenu.add_command(label='Coordinates', command = self.getCoordinates)

        self.toggleMenu = Tkinter.Menu(self.menuBar, tearoff=0) #Creates the viewing options menu
        self.toggleMenu.add_command(label='Boats', command=self.getBoats)
        self.toggleMenu.add_checkbutton(label='Weather', command=self.getWeather)
        self.toggleMenu.add_checkbutton(label='Waves')
        self.toggleMenu.add_checkbutton(label='Plotted Course')

        self.menuBar.add_cascade(label='File', menu=self.fileMenu) #makes the file menu cascade
        self.menuBar.add_cascade(label='Toggle', menu=self.toggleMenu) #makes the toggleMenu
        self.window.config(menu=self.menuBar) #displays the menubar


        self.weatherCoordinateLabel = Tkinter.Label(self.sideBarBox1, text='Enter the coordintes \n of the top left corner \n of the chart')
        self.lonLabel = Tkinter.Label(self.sideBarBox1, text='Longitude')
        self.lonEntry = Tkinter.Entry(self.sideBarBox1)
        self.latLabel = Tkinter.Label(self.sideBarBox1, text='Latitude')
        self.latEntry = Tkinter.Entry(self.sideBarBox1)
        self.enterCoordinates = Tkinter.Button(self.sideBarBox1, text='Enter', command=self.getWeather)

        self.zoominButton = Tkinter.Button(self.sideBarBox2, text='Zoom In', command=self.zoomin)
        self.zoomoutButton = Tkinter.Button(self.sideBarBox2, text='Zoom Out', command=self.zoomout)

        #here we pack the two frames
        self.sideBarFrame.grid(row=1, column=4, sticky='N', padx=0, pady=0)
        self.sideBarBox1.grid(row=0,column=0,sticky='N')
        self.sideBarBox2.grid(row=1,column=0,sticky='N')
        self.mapFrame.grid(row=1, column=0, sticky='NSEW', padx=0, pady=0)

        self.zoominButton.grid(row=0, column=0, sticky='WE')
        self.zoomoutButton.grid(row=1, column=0, sticky='WE')

        self.weatherCoordinateLabel.grid(row=0,column=0, columnspan=2)
        self.lonLabel.grid(row=1, column=0)
        self.lonEntry.grid(row=1, column=1)
        self.latLabel.grid(row=2, column=0)
        self.latEntry.grid(row=2, column=1)
        self.enterCoordinates.grid(row=3,column=0, columnspan=2, sticky='WE')

        self.verticalScroll = Tkinter.Scrollbar(self.mapFrame)
        self.horizontalScroll = Tkinter.Scrollbar(self.mapFrame)
        self.canvas = Tkinter.Canvas(self.mapFrame, bg='Pink', yscrollcommand=self.verticalScroll.set, xscrollcommand=self.horizontalScroll.set, width=self.chartSize[0],height=self.chartSize[1])
        self.canvas.config(scrollregion=(0,0,self.chartSize[0],self.chartSize[1]))

        self.canvas.grid(row=0, column=0)
        self.verticalScroll.grid(row=0, column=1, sticky='ns')
        self.horizontalScroll.grid(row=1,column=0, rowspan=4, sticky='we')

        self.verticalScroll.config(command=self.canvas.yview)
        self.horizontalScroll.config(command=self.canvas.xview, orient='horizontal')

        self.window.mainloop()
    def zoomin(self):
        self.canvas.scale('all', 1.5, 1.1, 1, 1)
        self.canvas.configure(scrollregion = self.canvas.bbox('all'))
    def zoomout(self):
        self.canvas.scale('all', 0.9, 0.9, 1, 1)
        self.canvas.configure(scrollregion = self.canvas.bbox('all'))
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

        self.chartScale = (((1000/(lon_max - lon_min)) + (1000/(lat_max - lat_min))) / 2)


    def getCoordinates(self):
        coordinateWindow = xyWnd(self)

    def fromLatLon2Cartesian(self, ((Lat1,Lon1),(Lat2,Lon2))):
        centerCoordinate = (((Lat1 + Lat2) / 2),((Lon1 + Lon2) / 2))
        self.center = centerCoordinate

    def importChart(self):
        importWindow = impWnd(self)

    def getWeather(self):
        zoom = 5 #seems to work best with nautical charts
        Coordinates = (float(self.latEntry.get()),float(self.lonEntry.get()))
        weatherOverlay = Image.open(getTile(convertToTiles(Coordinates, zoom))) #gets the tile for a given area and zoom
        chartSize = self.chartPIL.size #gets the size of the chart to calcualte the amount of resizing she needs
        weatherOverlay = weatherOverlay.resize(chartSize) #resizez the wather Overlay


        self.chartPIL.paste(weatherOverlay, (0, 0), weatherOverlay) #merges the overlay with the original image
        self.updatedChart = ImageTk.PhotoImage(self.chartPIL)
        self.canvas.delete('all')
        self.canvas.create_image(0,0, image = self.updatedChart, anchor = 'nw')
        self.window.update()
        self.window.update_idletasks()

    def getBoats(self):
        self.findChartScale()
        boatdata = getMarineData(self.APIkey, self.coordinates)
        boatDict = cleanUpMarineData(boatdata, parent=self)
        for i in boatDict.keys():
            boatDict[i].determineRelativeLocation(Center=boatDict[i].chartCenter,Lat=boatDict[i].LAT, Lon=boatDict[i].LON)
        for i in boatDict.keys():
            boatDict[i].draw()
            print i, 'drawn'

mainWindow = mainWnd()


#chart = Image.open('C:\Users\kaana\Desktop\Python Final Project\Example1.png')
#chart.show()
