import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#frame = cv2.imread("color.jpg")
while(True):
    ret, frame = cap.read()

    w, h, ch = frame.shape
    print(frame.shape)
    print(int(w/8))
    print(int(h-1))
    part = frame[0:(h-1),0:int(w/8)]
    cv2.imshow("new", part)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()