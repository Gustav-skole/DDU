import math as M

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

print(rotate_point((6,-2),90,(4,-2)))