import cv2, funk
import numpy as np

#cap = cv2.VideoCapture(0)
frame = cv2.imread("nudel.png")
while(True):

    #ret, frame = cap.read()
    flip = cv2.flip(frame,1)

    black_image = np.zeros(shape=frame.shape, dtype=np.uint8)

    absolute = funk.remove_isolated_pixels(cv2.inRange(frame, np.array([0,83,212]) , np.array([100,242,255])))
    contour = funk.findContours(absolute)
    if str(contour) != "[]":
        vx,vy,x,y = cv2.fitLine(contour[0],cv2.DIST_L2,0,0.01,0.01)

        rect = cv2.minAreaRect(contour[0])
        box = np.int0(cv2.boxPoints(rect))

        cv2.drawContours(black_image, [box], 0, (0,255,0), 2)

        for i in range(8):
            pass
        print(box)

        lefty = int((-x*vy/vx) + y)
        righty = int(((frame.shape[1]-x)*vy/vx)+y)

        #print(vx,vy,x,y)

        cv2.line(black_image,(frame.shape[1]-1,righty),(0,lefty),255,2)

    cv2.imshow("new", cv2.addWeighted(black_image,0.5,frame,0.5,0))
    #cv2.imshow('Frame', cv2.add(cv2.cvtColor(mask_rg,cv2.COLOR_GRAY2RGB), flip))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()