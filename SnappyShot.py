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

def searchForFilePath():
    global currdir, filePath
    tempdir = tkinter.filedialog.askdirectory(initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
        currdir = tempdir
        filePath = tempdir + "/Capture" + str(copyNum) + ".png"
        createFileName()

def quit():
    sys.exit(0)

fullScreenCapture = Button(text="Full Screen Capture", command=screenshot, width=15)
dragCapture = Button(text="Drag Capture", command=dragScreenshot, width=15)
quitApp = Button(text='❌', command=quit)
filePathButton = Button(master = root, text = 'Choose File Path', width = 15, command=searchForFilePath)
fullScreenCapture.grid(row=0,column=0)
dragCapture.grid(row=1,column=0)
quitApp.grid(row=1,column=1)
filePathButton.grid(row=2, column=0)

root.mainloop()
