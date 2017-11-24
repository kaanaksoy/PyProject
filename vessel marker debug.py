from Tkinter import *
import math

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


def findCoordinates(radius, BoatLatLon, angle):

    center = ((BoatLatLon[0]) / 2, (BoatLatLon[1]) / 2) # Finds the center of the boat polygon

    #Find the location of the individual points to plot an arrow looking shape (All points have to be rotated in order to have the arrow face right, to make it easy when adding rotations)
    A = rotate(center, (center[0], center[1] + radius), -90)
    B = rotate(center, (center[0] + ( (2.1 * radius) / 2.75), center[1] - (radius - (radius / 2.75))), -90)
    C = rotate(center, (center[0], center[1] - (radius - ((2 * radius) / 2.75) ) ), -90)
    D = rotate(center, (center[0] - ((2.1 * radius) / 2.75), center[1] - (radius - (radius / 2.75))), -90)

    polyList = [] #Creates a List to store the point information
    for j in (A, B, C, D): #uses a for loop to enter the point information to the list
        polyList.append(rotate(center, j, angle))
    return polyList

def drawCourse(COURSE, BoatLatLon):
    SPEED = 1
    lenghtofCourse = (SPEED * 50)

    initPoint = BoatLatLon
    finalPoint = (BoatLatLon[0] + lenghtofCourse * sin(COURSE), BoatLatLon[1] - lenghtofCourse(1-cos(COURSE)))

    courseLine = canvas.create_line(initPoint[0], initPoint[1], finalPoint[0], finalPoint[1], fill='Black')
    











polyList = findCoordinates(20, (400,400), 329)
#polyList = findCoordinates(20, 200,200, 0)
wind = Tk()
wind.title('canvas')
canvas = Canvas(wind, width=400, height=400)
boat = canvas.create_polygon(polyList[0][0], polyList[0][1], polyList[1][0], polyList[1][1], polyList[2][0], polyList[2][1], polyList[3][0], polyList[3][1], fill='Black')
#boat = canvas.create_polygon(0,2.75,2.1,-1.75, 0, -0.75, , polyList['D'][1], fill='Black')
canvas.pack()
wind.update()
wind.update_idletasks()
wind.mainloop()
