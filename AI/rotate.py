import cv2, funk
import numpy as np
import math as M

frame = cv2.imread("nudel.png")
black_image = np.zeros(shape=frame.shape, dtype=np.uint8)
absolute = funk.remove_isolated_pixels(cv2.inRange(frame, np.array([0,83,212]) , np.array([100,242,255])))

contour = funk.findContour(absolute)

rect = cv2.minAreaRect(contour)
box = np.int0(cv2.boxPoints(rect))
cv2.drawContours(black_image, [box], 0, (0,255,0), 2)

cropped = funk.crop_minAreaRect(absolute, rect)

height, width = cropped.shape

boundsArray = []
ssw = 1/8*width

for i in range(8):
    sliceImage = cropped[0:height,int(ssw*i):int(ssw*(i+1))]
    ix, iy, iw, ih = cv2.boundingRect(sliceImage)

    cx = ssw*i+ix+(iw/2) 
    cy = iy+(ih/2)

    rotation_center = (width/2, height/2)

    p = funk.rotate_point((cx,cy),rect[2],rotation_center)
    p_shift = int(p[0]+rect[0][0]-width/2),int(p[1]+rect[0][1]-height/2)

    cv2.circle(black_image, (p_shift), 2, (0,255,0))

while(True):
    #cv2.imshow("n", cropped)
    cv2.imshow("new", cv2.addWeighted(black_image,0.5,frame,0.5,0))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()