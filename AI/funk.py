import cv2, funk
import numpy as np
import math as M
from PIL import Image, ImageTk

def cv2tk(img):
    b,g,r = cv2.split(img)
    rgb = cv2.merge((r,g,b))
    im = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image=im)
    return imgtk 

def rotate_point(point,angle,center):
    rad = M.radians(angle)
    
    s = M.sin(rad)
    c = M.cos(rad)

    npx = point[0] - center[0] 
    npy = point[1] - center[1]

    xnew = npx * c - (npy * s)
    ynew = npx * s - (npy * c)

    point_new = (xnew + center[0], ynew + center[1])

    return point_new

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

def findContour(img): #kun en dimension i billedet
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 30))
    threshed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, rect_kernel)

    sx = cv2.Sobel(threshed,cv2.CV_32F,1,0)
    sy = cv2.Sobel(threshed,cv2.CV_32F,0,1)
    m = cv2.magnitude(sx,sy)
    m = cv2.normalize(m,None,0.,255.,cv2.NORM_MINMAX,cv2.CV_8U)

    contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if contours != []:
        return contours[0]
    else:
        return []