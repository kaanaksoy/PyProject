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
