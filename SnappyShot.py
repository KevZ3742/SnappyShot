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

filePath = "/Users/kevz3742/Desktop/Capture"
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
    root.withdraw()
    root.update()
    time.sleep(.1)

    with mouse.Listener(on_click=onClick) as listener:
        listener.join()

    # right, down 
    if(dragCoords[0] <= dragCoords[2] and dragCoords[1] <= dragCoords[3]):
        print('1')
        capture = pyautogui.screenshot(region=(dragCoords[0]*2, dragCoords[1]*2, (dragCoords[2]-dragCoords[0])*2, (dragCoords[3]-dragCoords[1])*2))
    # left, down
    elif(dragCoords[0] >= dragCoords[2] and dragCoords[1] <= dragCoords[3]):
        print('2')
        capture = pyautogui.screenshot(region=(dragCoords[2]*2, dragCoords[1]*2, (dragCoords[0]-dragCoords[2])*2, (dragCoords[3]-dragCoords[1])*2))
    # right, up
    elif(dragCoords[0] <= dragCoords[2] and dragCoords[1] >= dragCoords[3]):
        print('3')
        capture = pyautogui.screenshot(region=(dragCoords[0]*2, dragCoords[3]*2, (dragCoords[2]-dragCoords[0])*2, (dragCoords[1]-dragCoords[3])*2))
    # left, up
    elif(dragCoords[0] >= dragCoords[2] and dragCoords[1] >= dragCoords[3]):
        print('4')
        capture = pyautogui.screenshot(region=(dragCoords[2]*2, dragCoords[3]*2, (dragCoords[0]-dragCoords[2])*2, (dragCoords[1]-dragCoords[3])*2))
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
