import cv2, sys, funk
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

#definer video input
cap = cv2.VideoCapture(0)
#definer grundstruktur til bruger fladen
root = Tk()
alive = True

def on_closing():
    alive = 0
    root.destroy()

color_A = np.array([0,83,212]) 
color_B = np.array([100,242,255])

#definer bruger input til forste farve
r1 = Scale(root, from_=0, to=255, orient=HORIZONTAL, length=300)
r1.set(color_A[2])
r1.pack()
g1 = Scale(root, from_=0, to=255, orient=HORIZONTAL, length=300)
g1.set(color_A[1])
g1.pack()
b1 = Scale(root, from_=0, to=255, orient=HORIZONTAL, length=300)
b1.set(color_A[0])
b1.pack()

#definer bruger input til anden farve
r2 = Scale(root, from_=0, to=255, orient=HORIZONTAL, length=300)
r2.set(color_B[2])
r2.pack()
g2 = Scale(root, from_=0, to=255, orient=HORIZONTAL, length=300)
g2.set(color_B[1])
g2.pack()
b2 = Scale(root, from_=0, to=255, orient=HORIZONTAL, length=300)
b2.set(color_B[0])
b2.pack()

frame = cv2.imread("nudel.png")
imgtk = funk.cv2tk(frame)
imgShow = Label(root, image=imgtk)
imgShow.pack()

vinkel = Label(root, text="Vinkel")
vinkel.pack()

rect = [0,0,0]

while(alive):
    ret, frame = cap.read()
    black_image = np.zeros(shape=frame.shape, dtype=np.uint8)

    try:
        color_H = np.array([b1.get(),g1.get(),r1.get()])
        color_L = np.array([b2.get(),g2.get(),r2.get()])
    except:
        break

    absolute = funk.remove_isolated_pixels(cv2.inRange(frame, color_H, color_L))

    contour = funk.findContour(absolute)
    if str(contour) != "[]":
        rect = cv2.minAreaRect(contour)
        box = np.int0(cv2.boxPoints(rect))
        cv2.drawContours(black_image, [box], 0, (0,255,0), 2)
        cropped = funk.crop_minAreaRect(absolute, rect)

        height, width = cropped.shape
        rotate_compensate = 0

        if height > width:
            cropped = funk.rotate_image(cropped, 90)
            rotate_compensate = 90

        boundsArray = []
        ssw = 1/8*width

        for i in range(8):
            sliceImage = cropped[0:height,int(ssw*i):int(ssw*(i+1))]
            ix, iy, iw, ih = cv2.boundingRect(sliceImage)

            cx = ssw*i+ix+(iw/2) 
            cy = iy+(ih/2)

            rotation_center = (width/2, height/2)

            p = funk.rotate_point((cx,cy),rect[2]+rotate_compensate,rotation_center)
            p_shift = int(p[0]+rect[0][0]-width/2),int(p[1]+rect[0][1]-height/2)

            cv2.circle(black_image, (p_shift), 2, (0,255,0))

    img2 = funk.cv2tk(cv2.addWeighted(black_image,0.5,frame,0.5,0))
    imgShow.configure(image=img2)
    imgShow.image = img2
    vinkel.configure(text=str(rect[2]))
    vinkel.text = str(rect[2])
    root.update()

root.protocol("WM_DELETE_WINDOW", on_closing)