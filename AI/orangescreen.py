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
#frame = cv2.imread("nudel.png")
while(True):

    ret, frame = cap.read()
    black_image = np.zeros(shape=frame.shape, dtype=np.uint8)
    flip = cv2.flip(frame,1)
    mask_rg = remove_isolated_pixels(cv2.inRange(flip, np.array([0,83,212]) , np.array([100,242,255])))

    absolute = mask_rg
    x, y, w, h = cv2.boundingRect(absolute)
    if h >= 15:
        rect = (x, y, w, h)
        #cv2.rectangle(black_image, (x, y), (x+w, y+h), (0, 255, 0), 1)

    boundsArray = []

    boxImage = absolute[y:(y+h),x:(x+w)]
    ssw = 1/8*w

    for i in range(8):
        sliceImage = boxImage[0:h,int(ssw*i):int(ssw*(i+1))]
        print(sliceImage.shape,x,y,w,h)
        ix, iy, iw, ih = cv2.boundingRect(sliceImage)
        #cv2.rectangle(black_image, (ix+x+int(ssw*i), iy+y), (x+ix+iw+int(ssw*i), y+iy+ih), (0, 255, 0), 1)
        pointY = int(iy+y+ih/2)
        pointX = int(x+ix+i*ssw+iw/2)

        boundsArray.append((int(pointX),int(pointY)))

    for i in range(7):
        #print(boundsArray[i],boundsArray[1+i])
        cv2.line(black_image,boundsArray[i],boundsArray[1+i],(0,255,0),1)

    width, height, channels = flip.shape
    # (((width - height)/2)+height)
    #
    cropped = flip[80:480,0:400]
    scaled = cv2.resize(cropped,(72,72))
    cv2.imshow("new", cv2.addWeighted(black_image,0.5,cv2.cvtColor(absolute, cv2.COLOR_GRAY2RGB),0.5,0))
    #cv2.imshow("new", cv2.add(black_image, cv2.cvtColor(absolute, cv2.COLOR_GRAY2RGB)))
    #cv2.imshow('Frame', cv2.add(cv2.cvtColor(mask_rg,cv2.COLOR_GRAY2RGB), flip))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()