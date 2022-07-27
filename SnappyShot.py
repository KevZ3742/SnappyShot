import pyautogui
from tkinter import *
import tkinter.filedialog
import time
import sys
from pynput import mouse
import os.path

root = Tk()
root.title("SnappyShot")
root.lift()

currdir = os.getcwd()
filePath = os.getcwd() + "/Capture"
firstCall = True

copyNum = 1

multiplier = 1

class Indicator(Tk):
    pressed = False
    held = False
    width, height= pyautogui.size()
    dragCoords = [None, None, None, None]

    def __init__(self):
        super().__init__()
        self.canvas = Canvas(self, width=self.width, height=self.height, cursor="cross")
        self.canvas.pack(fill="both", expand=1)
        self.canvas.bind("<Button-1>", self.onClick)
        self.canvas.bind("<B1-Motion>", self.onMove)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)

    def onClick(self, event):
        if(not self.pressed):
            self.pressed = True
            self.held = True
            self.dragCoords[0] =  event.x
            self.dragCoords[1] = event.y
            self.start = event.x, event.y
            self.indicator = self.canvas.create_rectangle(*self.start, *self.start, width=3, fill='grey')

    def onMove(self, event):
        if(self.held):
            self.canvas.coords(self.indicator, *self.start, event.x, event.y)

    def onRelease(self, event):
        self.held = False

        self.dragCoords[2] = event.x
        self.dragCoords[3] = event.y

        self.canvas.destroy()

        # right, down 
        if(self.dragCoords[0] <= self.dragCoords[2] and self.dragCoords[1] <= self.dragCoords[3]):
            capture = pyautogui.screenshot(region=(self.dragCoords[0]*multiplier, self.dragCoords[1]*multiplier, (self.dragCoords[2]-self.dragCoords[0])*multiplier, (self.dragCoords[3]-self.dragCoords[1])*multiplier))
        # left, down
        elif(self.dragCoords[0] >= self.dragCoords[2] and self.dragCoords[1] <= self.dragCoords[3]):
            capture = pyautogui.screenshot(region=(self.dragCoords[2]*multiplier, self.dragCoords[1]*multiplier, (self.dragCoords[0]-self.dragCoords[2])*multiplier, (self.dragCoords[3]-self.dragCoords[1])*multiplier))
        # right, up
        elif(self.dragCoords[0] <= self.dragCoords[2] and self.dragCoords[1] >= self.dragCoords[3]):
            capture = pyautogui.screenshot(region=(self.dragCoords[0]*multiplier, self.dragCoords[3]*multiplier, (self.dragCoords[2]-self.dragCoords[0])*multiplier, (self.dragCoords[1]-self.dragCoords[3])*multiplier))
        # left, up
        elif(self.dragCoords[0] >= self.dragCoords[2] and self.dragCoords[1] >= self.dragCoords[3]):
            capture = pyautogui.screenshot(region=(self.dragCoords[2]*multiplier, self.dragCoords[3]*multiplier, (self.dragCoords[0]-self.dragCoords[2])*multiplier, (self.dragCoords[1]-self.dragCoords[3])*multiplier))
        
        
        capture.save(r"" + filePath)

        sys.exit(0)
        
def createFileName():
    global filePath, copyNum, firstCall

    if(not firstCall):
        filePath = filePath[:-4]

    pathExists = True
    
    while pathExists:
        if(not os.path.exists(filePath + ".png")):
            filePath = filePath + ".png"
            pathExists = False
        elif(os.path.exists(filePath + str(copyNum) + ".png")):
            copyNum += 1
        else:
            filePath = filePath + str(copyNum) + ".png"
            pathExists = False

    firstCall = False

createFileName()

def screenshot():
    root.withdraw()
    root.update()
    time.sleep(.3)

    capture = pyautogui.screenshot()
    capture.save(r"" + filePath)

    root.destroy()
    sys.exit(0)

def dragScreenshot():
    root.withdraw()

    width, height = pyautogui.size()
    dragWindow = Indicator()
    dragWindow.title('')
    dragWindow.geometry(str(width) + "x" + str(height) + "-0+0")
    dragWindow.attributes('-alpha',0.1)
     
    root.update()
    time.sleep(.3)

def searchForFilePath():
    global currdir, filePath
    tempdir = tkinter.filedialog.askdirectory(initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
        currdir = tempdir
        filePath = tempdir + "/Capture" + str(copyNum) + ".png"
        createFileName()

def toggle():
    global multiplier

    if(toggleDoubleRetina.config("text")[-1] == "Double Retina: On"):
        toggleDoubleRetina.config(text="Double Retina: Off")
        multiplier = 1
    else:
        toggleDoubleRetina.config(text="Double Retina: On")
        multiplier = 2

def quit():
    sys.exit(0)

fullScreenCapture = Button(text="Full Screen Capture", command=screenshot, width=15)
dragCapture = Button(text="Drag Capture", command=dragScreenshot, width=15)
quitApp = Button(text='❌', command=quit)
filePathButton = Button(master = root, text = 'Choose File Path', width = 15, command=searchForFilePath)
toggleDoubleRetina = Button(text="Double Retina: Off", width=15, command=toggle)

fullScreenCapture.grid(row=0,column=0)
dragCapture.grid(row=1,column=0)
quitApp.grid(row=1,column=1, rowspan=2)
filePathButton.grid(row=2, column=0)
toggleDoubleRetina.grid(row=3, column=0)

root.mainloop()