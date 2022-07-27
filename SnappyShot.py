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
    dragWindow = Toplevel(root)
    dragWindow.title('')
    width, height = pyautogui.size()
    dragWindow.geometry(str(width) + "x" + str(height) + "-0+0")
    dragWindow.attributes('-alpha', .1)

    canvas = Canvas(dragWindow, width=width, height=height, cursor="cross")
    canvas.pack(fill="both", expand=1)
     
    root.update()
    time.sleep(.3)

    dragCoords = [None, None, None, None]
    held = False

    def onClick(x, y, button, pressed):
        global held
        if button == button.left:
            if(pressed):
                dragCoords[0] = x
                dragCoords[1] = y
                held = True
                print(dragCoords)
            else:
                dragCoords[2] = x
                dragCoords[3] = y
                print(dragCoords)
                return False

    def onMove(x, y):
        if(held):
            pass

    with mouse.Listener(on_click=onClick, on_move=onMove) as listener:
        listener.join()

    # right, down 
    if(dragCoords[0] <= dragCoords[2] and dragCoords[1] <= dragCoords[3]):
        capture = pyautogui.screenshot(region=(dragCoords[0]*multiplier, dragCoords[1]*multiplier, (dragCoords[2]-dragCoords[0])*multiplier, (dragCoords[3]-dragCoords[1])*multiplier))
    # left, down
    elif(dragCoords[0] >= dragCoords[2] and dragCoords[1] <= dragCoords[3]):
        capture = pyautogui.screenshot(region=(dragCoords[2]*multiplier, dragCoords[1]*multiplier, (dragCoords[0]-dragCoords[2])*multiplier, (dragCoords[3]-dragCoords[1])*multiplier))
    # right, up
    elif(dragCoords[0] <= dragCoords[2] and dragCoords[1] >= dragCoords[3]):
        capture = pyautogui.screenshot(region=(dragCoords[0]*multiplier, dragCoords[3]*multiplier, (dragCoords[2]-dragCoords[0])*multiplier, (dragCoords[1]-dragCoords[3])*multiplier))
    # left, up
    elif(dragCoords[0] >= dragCoords[2] and dragCoords[1] >= dragCoords[3]):
        capture = pyautogui.screenshot(region=(dragCoords[2]*multiplier, dragCoords[3]*multiplier, (dragCoords[0]-dragCoords[2])*multiplier, (dragCoords[1]-dragCoords[3])*multiplier))
    
    capture.save(r"" + filePath)

    dragWindow.destroy()
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