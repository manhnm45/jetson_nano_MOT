import cv2
import numpy as np

boudary= [[((0,100,95),(0,255,255))],   #Red
          [((20,90,60),(50,200,200))],  #yellow
          [((80,90,110),(90,150,225))]  #Green
          ]

def Average(cl):
    return sum(cl)/len(cl)

def midPoint(x0, y0, x1, y1):
    return int(x0 + (x1 - x0) / 2), int(y0 + (y1 - y0) / 2)

def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def colorDetector(frame, rect= [480, 51, 517, 61]):
    # cv2.imshow("frame", frame)
    color_sum=[0,0,0]
    color=[]
    a=rect[0]
    b=rect[1]
    c=rect[2]
    d= rect[3]
    trafic_light=frame[b:d, a:c]
    # cv2.imshow("img", trafic_light)
    # print(trafic_light)
    trafic_light= cv2.GaussianBlur(trafic_light,(5,5),0)
    hsv = cv2.cvtColor(trafic_light,cv2.COLOR_BGR2HSV)
    for i in range(len(boudary)):
        for (lower,upper) in boudary[i]:
            mask= cv2.inRange(hsv, lower, upper)
            color_sum[i] = np.sum(mask)
    color.append(color_sum.index(np.max(color_sum)))
    color_curent = None
    if len(color) >0 :
        average = Average(color)
        if average == 2:
            color_curent ='green'
        elif average == 0:
            color_curent = 'red'
        else :
            color_curent = 'yellow'
    return color_curent






if __name__ == '__main__':
    img = cv2.imread('150.jpg')
    rect =[480, 51, 517, 61]
    cld = colorDetector(img, rect)
    # cv2.rectangle(img,(rect[0],rect[2]),(rect[1],rect[3]),(0,125,0),2)
    # print(cld)
    # cv2.imshow('img',img)

    cv2.waitKey(0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()