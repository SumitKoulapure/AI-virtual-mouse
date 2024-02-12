import cv2
import time
import HandtrackingModule  as htm
import numpy as np
import pyautogui




wCam, hCam = 640, 480
frameR = 150    #frame reduction
smoothening = 1.8
pTime = 0
plocX, plocY = 0, 0   #previous locations of x and y
clocX, clocY = 0, 0    #current locations of x and y

cap = cv2.VideoCapture(0)
cap.set(3, wCam)#width
cap.set(4, hCam)#height
detector = htm.handDetector(detectionCon=0.60,maxHands=1)
wScr, hScr = pyautogui.size()


while True:
   
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    
    if len(lmList) != 0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
       

        # Check which fingers are up
        fingers = detector.fingersUp()

        #set a region for moving cursor
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)

        #  Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:

           # convirsion of co ordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

        
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            #  Move Mouse
            pyautogui.moveTo(wScr - clocX, clocY)  # for  mirror inversion
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)      # circle for  moving mode
            plocX, plocY = clocX, clocY

        #  Index and middle fingers are up : Clicking Mode 
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length < 30:    
                pyautogui.click()
        

        
                
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            length, img, lineInfo = detector.findDistance(4 ,12 , img)
            if length < 30:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),8, (0, 255, 0), cv2.FILLED)
                    pyautogui.hotkey('Alt','F4')
                    time.sleep(0.30)
                    pyautogui.hotkey('Enter')
                    
           
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 :
            pyautogui.keyDown("right")
            pyautogui.keyUp("left")
            
        if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 :
            pyautogui.keyDown("left")
            pyautogui.keyUp("right")
            
       
            
            
            
            
                    
                
           
    #  Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)

    #  Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)

