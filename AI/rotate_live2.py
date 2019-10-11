import cv2, sys
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

def crop_minAreaRect(img, rect):

    # rotate img
    angle = rect[2]
    rows, cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    img_rot = cv2.warpAffine(img, M, (cols, rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1],
                       pts[1][0]:pts[2][0]]

    return img_crop

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    black_image = np.zeros(shape=frame.shape, dtype=np.uint8)
    absolute = remove_isolated_pixels(cv2.inRange(frame, np.array([0,83,212]) , np.array([100,242,255])))

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 30))
    threshed = cv2.morphologyEx(absolute, cv2.MORPH_CLOSE, rect_kernel)

    sx = cv2.Sobel(threshed,cv2.CV_32F,1,0)
    sy = cv2.Sobel(threshed,cv2.CV_32F,0,1)
    m = cv2.magnitude(sx,sy)
    m = cv2.normalize(m,None,0.,255.,cv2.NORM_MINMAX,cv2.CV_8U)

    contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if(contours != []):
        rect = cv2.minAreaRect(contours[0]) 
        #box = np.int0(cv2.boxPoints(rect))
        cropImage = crop_minAreaRect(frame, rect)
        ch, cw, _ = cropImage.shape 
        print(ch, cw)
        if(ch > cw):
            tci = cv2.transpose(cropImage, cropImage);
            horImage = cv2.flip(tci, 1);
        else:
            horImage = cropImage

        height, width, _ = horImage.shape

        boundsArray = []
        ssw = 1/8*width

        for i in range(8):
            sliceImage = horImage[0:height,int(ssw*i):int(ssw*(i+1))]
            ix, iy, iw, ih = cv2.boundingRect(sliceImage)

            cx = ssw*i+ix+(iw/2) 
            cy = iy+(ih/2)

            rotation_center = (width/2, height/2)

            p = rotate_point((cx,cy),rect[2],rotation_center)
            p_shift = int(p[0]+rect[0][0]-width/2),int(p[1]+rect[0][1]-height/2)

            cv2.circle(black_image, (p_shift), 2, (0,255,0))
    else:
        cv2.imshow("new", frame)

    cv2.imshow("new", cv2.addWeighted(black_image,0.5,frame,0.5,0))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()