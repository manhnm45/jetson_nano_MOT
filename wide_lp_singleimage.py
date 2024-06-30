import matplotlib.pyplot as plt
import cv2
import numpy as np
from ultralytics import YOLO
import glob
import os
model = YOLO('yolov8_License_plate_obb.pt')
def wide_img_lp(image):

    results = model(image)  # results list
    bb=[]
    # View results
    for r in results:
        bb.append(r.obb.xyxyxyxy.squeeze().tolist())
    
    # plt.imshow(image)
    # plt.show()
    bb=np.array(bb)
    bb=np.squeeze(bb)
    print("bb",bb)
    if bb[0][0]<bb[2][0]:
      bb[[0,2]]=bb[[2,0]]
    if bb[1][0]<bb[3][0]:
      bb[[1,3]]=bb[[3,1]]
    if bb[0][1]<bb[1][1]:
      bb[[0,1]]=bb[[1,0]]
    if bb[2][1]>bb[3][1]:
      bb[[2,3]]=bb[[3,2]]
    bb[[0,2]]=bb[[2,0]]
    bb[[2,3]]=bb[[3,2]]
    coner=bb
    xmin = bb[1][0] if bb[0][0]>bb[1][0] else bb[0][0]
    xmax = bb[2][0] if bb[2][0]>bb[3][0] else bb[3][0]
    ymin = bb[0][1] if bb[3][1]>bb[0][1] else bb[3][1]

    ymax = bb[2][1] if bb[2][1]>bb[1][1] else bb[1][1]
    wmax = int(xmax - xmin)
    hmax = int(ymax - ymin) 
    src_p=np.float32(coner)
    des_p=np.float32([[0,0],[image.shape[1],0],[0,image.shape[0]],[image.shape[1],image.shape[0]]])
    matrix=cv2.getPerspectiveTransform( src_p,des_p)
    warp=cv2.warpPerspective(image,matrix,(image.shape[1],image.shape[0]))
    warp2 = cv2.resize(warp,(int(wmax*1.1),int(hmax*1.1)))
    cv2.imshow("lpimg",warp2)
    cv2.waitKey(0)
    return warp2
  