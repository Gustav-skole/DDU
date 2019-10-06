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

frame = cv2.imread("nudel.png")
while(True):
    black_image = np.zeros(shape=frame.shape, dtype=np.uint8)

    flip = cv2.flip(frame,1)
    absolute = remove_isolated_pixels(cv2.inRange(flip, np.array([0,83,212]) , np.array([100,242,255])))

    
    rotrect = cv2.minAreaRect(absolute)
    box = cv2.cv.BoxPoints(rotrect)
    box = numpy.int0(box)
    cv2.drawContours(black_image, [box], 0, (0,0,255), 2)

    width, height, channels = flip.shape
    cropped = flip[80:480,0:400]
    scaled = cv2.resize(cropped,(72,72))
    cv2.imshow("new", cv2.addWeighted(black_image,0.5,cv2.cvtColor(absolute, cv2.COLOR_GRAY2RGB),0.5,0))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()