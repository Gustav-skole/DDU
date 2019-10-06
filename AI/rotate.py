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

frame = cv2.imread("nudel.png")
black_image = np.zeros(shape=frame.shape, dtype=np.uint8)
absolute = remove_isolated_pixels(cv2.inRange(frame, np.array([0,83,212]) , np.array([100,242,255])))

contours, _ = cv2.findContours(absolute, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cont = []
for contour in contours:
	cont.append(contour[0][0])

cnt = cv2.convexHull(np.float32(cont))
rect = cv2.minAreaRect(cnt)

print(rect[-1])

box = np.int0(cv2.boxPoints(rect))
cv2.drawContours(black_image, [box], 0, (0,255,0), 2)


x, y, w, h = cv2.boundingRect(absolute)
cv2.rectangle(black_image, (x, y), (x+w, y+h), (0, 255, 0), 1)

while(True):
	cv2.imshow("new", cv2.addWeighted(black_image,0.5,cv2.cvtColor(absolute, cv2.COLOR_GRAY2RGB),0.5,0))
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

cv2.destroyAllWindows()