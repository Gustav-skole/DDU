import cv2
import numpy as np

#Eksempel taget fra OpenCV-python tutorials

def RGBBGR(r,g,b):
    return np.array([b,g,r])

#funktion taget fra Alexander på stackoverflow (han havde ikke et handle)
def remove_isolated_pixels(image):
    connectivity = 8

    output = cv2.connectedComponentsWithStats(image, connectivity, cv2.CV_32S)

    num_stats = output[0]
    labels = output[1]
    stats = output[2]

    new_image = image.copy()

    for label in range(num_stats):
        if stats[label,cv2.CC_STAT_AREA] == 1:
            new_image[labels == label] = 0

    return new_image

cap = cv2.VideoCapture(0)
#frame = cv2.imread("color.jpg")
while(True):

    ret, frame = cap.read()
    flip = cv2.flip(frame,1)
    mask_rg = remove_isolated_pixels(cv2.inRange(flip, np.array([0,83,212]) , np.array([100,242,255])))

    center, radius = cv2.minEnclosingCircle(mask_rg)

    cv2.imshow("new", mask_rg)
    #cv2.imshow('Frame', cv2.add(cv2.cvtColor(mask_rg,cv2.COLOR_GRAY2RGB), flip))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()