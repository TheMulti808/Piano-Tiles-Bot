import win32gui, win32ui, time
from win32api import GetSystemMetrics

dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0,0))
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))


def draw(coords):
    dcObj.Rectangle((coords[0]-25, coords[1]-25, coords[0]+25, coords[1]+25))
    win32gui.InvalidateRect(hwnd, monitor, False)
    
def drawFast(coords):
    for i in range(0,25):
        time.sleep(0)
        dcObj.Rectangle((coords[0]-i, coords[1]-i, coords[0]+i, coords[1]+i))
        win32gui.InvalidateRect(hwnd, monitor, False)


        
    