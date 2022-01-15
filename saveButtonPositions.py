import cv2 as cv
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pickle

WIDTH = 800
HEIGHT = 650

camera = cv.VideoCapture(0)

BUTTONWIDTH = 150
BUTTONHEIGHT = 100
BUTTONSPERROW = 4

try:
    with open("CalculatorButtons","rb") as b:
        buttons = pickle.load(b)
except:
    buttons = []


def callback(event, xpos, ypos, flags, params):
    global buttons
    if event == cv.EVENT_LBUTTONUP:
        print(f"X:{xpos},Y:{ypos}")
        for x in range(BUTTONSPERROW):
            buttons.append((xpos, ypos))
            xpos += BUTTONWIDTH+10

    with open("CalculatorButtons","wb") as b:
        pickle.dump(buttons,b)


while True:
    _, frame = camera.read()
    frame = cv.resize(frame,(WIDTH,HEIGHT))
    frame = cv.flip(frame, 1)

    for button in buttons:
        cv.rectangle(frame,button,(button[0]+BUTTONWIDTH,button[1]+BUTTONHEIGHT),(255,0,255),-1)

    cv.imshow("Settings", frame)
    cv.setMouseCallback("Settings", callback)
    key = cv.waitKey(1)
    if key == ord("d"):
        break
    elif key == ord("c"):
        buttons = []
camera.release()
cv.destroyAllWindows()
with open("CalculatorButtons","wb") as b:
        pickle.dump(buttons,b)

