import time, win32api, win32con, sys, mouse, keyboard, pyautogui
import numpy as np
import drawer as drawer
from PIL import ImageGrab
debug = True
ErrorsToSkip = [SystemExit]
def dbg(txt):
    if debug: print(txt)

class clickingBot:
    def __init__(self):
        self.pointsToClick = []
        self.initialPoint = None
        self.drawPoints = True
        self.neededPoints = 4
        self.gameStatus = 0 # 0 - Creating, 1 - Paused, 2 - Started, 3 - (exit app)
        self.mouse = [False, False, (0,0)]
        self.keyboard = {"esc": False, "enter": False}
        dbg('Main bot instance initialized')
        self.createInitialPoint()
        time.sleep(0.5)
        while len(self.pointsToClick) < 4:
            self.addPoint()
            time.sleep(0.5)
        dbg("Points successfully added at positions: {}".format(self.pointsToClick))
        self.drawPoints = False
        self.gameStatus = 1
        while True:
            self.proceedKeyControl()
            if self.gameStatus == 2:
                for point in self.pointsToClick:
                    time.sleep(0)
                    if self.shouldClickAtPoint(point): self.clickAtPoint(point)
    def __call__(self, value):
       pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if (exc_type != None) and not exc_type in ErrorsToSkip:
            print('Error occured, details:')
            print('Error type: {},\nError Value: {},\nError Table: {}'.format(exc_type, exc_val, exc_tb))
            return True
    def proceedKeyControl(self):
        self.mouse[0] = mouse.is_pressed(button='left') 
        self.mouse[1] = mouse.is_pressed(button='right') 
        self.mouse[2] = mouse.get_position()
        self.keyboard["esc"] = keyboard.is_pressed('esc')
        self.keyboard["enter"] = keyboard.is_pressed('enter')
        if self.keyboard["esc"]: self.gameStatus = 3
        if self.keyboard["enter"]:
            if self.gameStatus == 1: self.gameStatus = 2
            elif self.gameStatus == 2: self.gameStatus = 1
            dbg('Current game status: {}'.format(self.gameStatus == 0 and "Creating" or (self.gameStatus == 1 and "Paused" or "Started")))
            time.sleep(0.7)
        if self.gameStatus == 3: # Here because its gonna be called every frame
            dbg('Exiting App')
            sys.exit()
    def shouldClickAtPoint(self, point):
        im2 = ImageGrab.grab(bbox =(point[0],point[1],point[0]+1,point[1]+1), include_layered_windows=False, all_screens=True).getpixel((0,0))
        if im2 == self.initialPoint:
            return True
        return False
    def clickAtPoint(self, point):
        win32api.SetCursorPos((point[0], point[1]))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,point[0], point[1],0,0)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,point[0], point[1],0,0)
        time.sleep(0.00)
    def drawPointsAtThisFrame(self):
        if self.drawPoints:
            for point in self.pointsToClick:
                drawer.draw(point)
    def addPoint(self):
        dbg("Adding point number {}".format(len(self.pointsToClick)+1))
        while True:
            self.proceedKeyControl()
            self.drawPointsAtThisFrame()
            if self.mouse[0]:
                self.pointsToClick.append(self.mouse[2])
                dbg("Point {} added at position {}!".format(len(self.pointsToClick), self.mouse[2]))
                break

    def createInitialPoint(self):
        dbg('Click LPM at initial point (1 pixel)')
        while True:
            time.sleep(0.01)
            self.proceedKeyControl()
            if self.mouse[0]:
                tempImg = ImageGrab.grab(bbox =(self.mouse[2][0],self.mouse[2][1],self.mouse[2][0]+1,self.mouse[2][1]+1), include_layered_windows=False, all_screens=True)
                self.initialPoint = tempImg.getpixel((0,0))
                dbg("Setted initial pixel with value of {}".format(self.initialPoint))
                break



            



def main():
    with clickingBot() as newBot:
       pass
        




if __name__ == "__main__":
    main()
    
    