import cv2 as cv
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pickle

WIDTH = 800
HEIGHT = 650

camera = cv.VideoCapture(0)
camera.set(3, WIDTH)
camera.set(4, HEIGHT)

handTracker = HandDetector(maxHands=1, detectionCon=0.8)

color = (255, 0, 255)
x, y = 20, 50
BUTTONWIDTH = 150
BUTTONHEIGHT = 100
BUTTONCLICKCOLOR = (12, 255, 12)
BUTTONHOVERCOLOR = (255, 0, 255)

BUTTONTEXTS = [
    '9', '8', '7', 'C', '6', '5', '4', '+', '3', '2', '1', '-', '/', '0', '*', '='
]
LCDX1, LCDX2 = 96, 726
LCDY1, LCDY2 = 10, 90

lcdText = "0"
click = False
error = False
frames = 0
frames1 = 0
loading = True
END = 2000
loadingPercent = 0

with open("CalculatorButtons", "rb") as file:
    calculatorButtons = pickle.load(file)

bg = cv.imread("bg.jpg")
bg = cv.resize(bg,(WIDTH,HEIGHT))

loadingLevel = 0

while True:
    frames += 1
    if frames >= 50:
        error = False
    if loadingLevel >= END:
        loading = False

    _, frame = camera.read()
    frame = cv.resize(frame, (WIDTH, HEIGHT))
    frame = cv.flip(frame, 1)

    if not loading:
        hand = handTracker.findHands(frame, flipType=False, draw=False)

        if hand:
            lmList = hand[0]['lmList']
            fingerDistance, (x1, y1, x2, y2, cx, cy) = handTracker.findDistance(lmList[12], lmList[8])
            cv.circle(frame, (cx, cy), 25, (50, 50, 50), 30)

            cv.rectangle(frame, (LCDX1, LCDY1), (LCDX2, LCDY2), (255, 255, 255), 5)  # Draw lcd display
            cv.putText(frame, lcdText, (LCDX1 + 10, LCDY1 + 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

            if len(lcdText) > 1:
                if lcdText.startswith('0'):
                    lcdText1 = list(lcdText)
                    del lcdText1[0]
                    lcdText = ''.join(lcdText1)

            for button, text in zip(calculatorButtons, BUTTONTEXTS):
                xm, ym = button
                xtext = int(xm + (0.4 * BUTTONWIDTH))
                ytext = int(ym + (0.8 * BUTTONHEIGHT))

                xf, yf = button[0] + BUTTONWIDTH, button[1] + BUTTONHEIGHT

                if button[0] < cx < xf and button[1] < cy < yf:
                    cv.rectangle(frame, button, (xf, yf), BUTTONHOVERCOLOR, 3)

                    if fingerDistance <= 40:
                        if not click:
                            click = True

                            color = (0, 255, 0)
                            buttonColor = (0, 255, 0)
                            cv.rectangle(frame, button, (xf, yf), BUTTONCLICKCOLOR, 3)

                            if text != "=": lcdText += text

                            if text == "C":
                                lcdText = "0"

                            elif text == "=":
                                try:
                                    answer = eval(lcdText)
                                    lcdText = str(answer)
                                    error = False
                                except:
                                    error = True
                                    frames = 0


                    else:
                        click = False
                        color = (255, 0, 255)

                else:
                    cv.rectangle(frame, button, (xf, yf), (255, 255, 255), 3)

                cv.circle(frame, (cx, cy), 15, color, -1)
                cv.putText(frame, text, (xtext, ytext), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                if error:
                    cvzone.putTextRect(frame, "Math Error", (255, 620), 3, colorT=(0, 0, 255), colorR=(255, 255, 255))
        else:
            cv.putText(frame, "No Hand has been detected", (30, HEIGHT // 2), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255),
                       3)
    else:
        frame = bg
        cv.putText(frame,"Virtual Calculator",(120,200),cv.FONT_HERSHEY_PLAIN,4,(255,250,100),3)
        cvzone.putTextRect(frame,"Loading...",(250,400),3,2,colorR=(0,0,0))
        cv.rectangle(frame,(248,439),(500,455),(255,255,255),3)
        loadingLevel+=5
        loadingx = int(np.interp(loadingLevel, (0, END), (250, 500)))
        loadingPercent = int(np.interp(loadingLevel, (0, END), (0, 100)))
        cvzone.putTextRect(frame,f"{loadingPercent}%",(520,455),2,2,colorR=(0,0,0))
        cv.rectangle(frame,(250,439),(loadingx,455),(50,0,0),-1)

    cv.imshow("Virtual Calculator", frame)
    key = cv.waitKey(10)
    if key == ord("d"):
        break
camera.release()
cv.destroyAllWindows()
