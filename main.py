import cv2 as cv
import cvzone
import mediapipe as mp
import numpy as np
import math

math.hypot()

WIDTH = 640
HEIGHT = 780

cam = cv.VideoCapture("videos/Blinking Morse Code _ Hello(720P_HD).mp4")
cam.set(3, WIDTH)
cam.set(4, HEIGHT)

faceMesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
irisColor = (0, 0, 255)

blinks = 0
eyeOpen = True
lastN = 0

while True:
    _, frame = cam.read()
    totalFrames = cam.get(cv.CAP_PROP_FRAME_COUNT)
    currentFrame = cam.get(cv.CAP_PROP_POS_FRAMES)
    if currentFrame == totalFrames:
        cam.set(cv.CAP_PROP_POS_FRAMES,0)
    if not _:
        break
    #frame = cv.flip(frame, 1)
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = faceMesh.process(frameRGB).multi_face_landmarks
    facePoints = []
    if results:
        ih, iw, ic = frame.shape
        facePoints = [[int(lm.x * iw), int(lm.y * ih)] for lm in results[0].landmark]

        upperLidPt1 = facePoints[158]
        upperLidPt2 = facePoints[159]

        lowerLidPt1 = facePoints[144]
        lowerLidPt2 = facePoints[145]
        lowerLidPt3 = facePoints[153]

        avgUpperLidX = (upperLidPt1[0] + upperLidPt2[0]) // 2
        upperLidY = upperLidPt1[1]

        avgLowerLidX = (lowerLidPt1[0] + lowerLidPt2[0] + lowerLidPt3[0]) // 3
        lowerLidY = lowerLidPt1[1]

        lidCenterY = (upperLidY + lowerLidY) // 2
        lidCenterX = lowerLidPt2[0]
        print(lidCenterX, lidCenterY)

        A = (upperLidY - lowerLidY)
        B = lowerLidPt1[1] - lowerLidPt3[1]

        N = ((A ** 2) + (B ** 2))
        N = 0.5*N + 0.5*lastN
        lastN = N
        C = math.sqrt(N)
        print("Distance between two lids ::: ",N)
        if N <= 500:
            print(f"Your left eye is closed ::: Hypo = {N}")
            irisColor = (0, 255, 0)
            if not eyeOpen:
                blinks += 1
                eyeOpen = True

        else:
            irisColor = (0, 0, 255)
            eyeOpen = False

        cv.rectangle(frame,(10,30),(150,80),(0,0,0),-1)
        cv.putText(frame,"Blinks:",(15,70),cv.FONT_HERSHEY_PLAIN,2.3,(255,255,255),2)

        cv.rectangle(frame,(160,30),(250,80),(0,0,0),-1)
        cv.putText(frame,str(blinks),(165,75),cv.FONT_HERSHEY_PLAIN,3,(255,255,255),3)

        cv.circle(frame, upperLidPt1, 1, (0, 255, 0), -1)
        cv.circle(frame, upperLidPt2, 1, (0, 255, 0), -1)
        cv.circle(frame, lowerLidPt1, 1, (0, 255, 0), -1)
        cv.circle(frame, lowerLidPt2, 1, (0, 255, 0), -1)
        cv.circle(frame, lowerLidPt3, 1, (0, 255, 0), -1)

        cv.circle(frame, (lidCenterX, lidCenterY), 10, irisColor, 5)
        cv.putText(frame,str(N),(50,400),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),3)

    cv.rectangle(frame,(380,20),(630,45),(0,0,0),-1)
    cv.putText(frame,"Eye Blink Counter",(390,40),cv.FONT_HERSHEY_PLAIN,1.5,(255,255,255),1)

    cv.imshow("Camera", frame)
    key = cv.waitKey(1)
    if key == ord('d'):
        break
cam.release()
cv.destroyAllWindows()
