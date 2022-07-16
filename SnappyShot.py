import pyautogui
from tkinter import *
from tkinter.filedialog import *
import time
import sys
from pynput import mouse
import os.path

root = Tk()
root.title("SnappyShot")
root.lift()

filePath = "UR FILE PATH"
pathExists = True
i = 1

while pathExists:
    if(not os.path.exists(filePath + ".png")):
        filePath = filePath + ".png"
        pathExists = False
    elif(os.path.exists(filePath + str(i) + ".png")):
        i += 1
    else:
        filePath = filePath + str(i) + ".png"
        pathExists = False

dragCoords = [None, None, None, None]

def onClick(x, y, button, pressed):
    global dragCoords
    if button == button.left:
        if(pressed):
            dragCoords[0] = x
            dragCoords[1] = y
            print(dragCoords)
        else:
            dragCoords[2] = x
            dragCoords[3] = y
            print(dragCoords)
            return False

def screenshot():
    root.withdraw()
    root.update()
    time.sleep(.1)
    capture = pyautogui.screenshot()
    capture.save(r"" + filePath)
    root.destroy()
    sys.exit(0)

def dragScreenshot():
    with mouse.Listener(on_click=onClick) as listener:
        listener.join()

    root.withdraw()
    root.update()
    time.sleep(.1)
    capture = pyautogui.screenshot(region=(dragCoords[0], dragCoords[1], dragCoords[2], dragCoords[3]))
    capture.save(r"" + filePath)
    root.destroy()
    sys.exit(0)

def quit():
    sys.exit(0)

fullScreenCapture = Button(text="Full Screen Capture", command=screenshot, width=15)
dragCapture = Button(text="Drag Capture", command=dragScreenshot, width=15)
quitApp = Button(text='❌', command=quit)
fullScreenCapture.grid(row=1,column=1)
dragCapture.grid(row=2,column=1)
quitApp.grid(row=1 ,column=2, rowspan=2, columnspan=2)

root.mainloop()
