import cv2
import numpy as np
import math as M

def rotate_point(cx,cy,angle,center):
    s = M.sin(M.degrees(angle))
    c = M.cos(M.degrees(angle))

    #translate point back to origin:
    npx = center[0] - cx
    npy = center[1] - cy

    #rotate point
    xnew = npx * c - npy * s
    ynew = npx * s + npy * c

    #translate point back:
    point = (xnew + cx, ynew + cy)

    return point