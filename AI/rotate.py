import cv2
import numpy as np

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

frame = cv2.imread("nudel2.png")
black_image = np.zeros(shape=frame.shape, dtype=np.uint8)
absolute = remove_isolated_pixels(cv2.inRange(frame, np.array([0,83,212]) , np.array([100,242,255])))

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 30))
threshed = cv2.morphologyEx(absolute, cv2.MORPH_CLOSE, rect_kernel)

sx = cv2.Sobel(threshed,cv2.CV_32F,1,0)
sy = cv2.Sobel(threshed,cv2.CV_32F,0,1)
m = cv2.magnitude(sx,sy)
m = cv2.normalize(m,None,0.,255.,cv2.NORM_MINMAX,cv2.CV_8U)

contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

rect = cv2.minAreaRect(contours[0])
box = np.int0(cv2.boxPoints(rect))
cv2.drawContours(black_image, [box], 0, (0,255,0), 2)

while(True):
    cv2.imshow("new", cv2.addWeighted(black_image,0.5,frame,0.5,0))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()