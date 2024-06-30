import cv2
import numpy
#import imutils
import matplotlib
from multiprocessing import Process
#from paddleocr import PaddleOCR
import time

#ocr = PaddleOCR(lang="en")
area_threshold =500
def detector_lp(img,box):
    print("detect lp success")
    #for i in range(len(box)):
        #confirm = 0
        #box[i].append(confirm)
    #print("box", box)
    if box[5] =="car":

        t = time.time()
        #print("box", box[i])
        img2 = img.copy()
    
    #img_path1 = "/home/minhanh/Downloads/jetson_nano_MOT/test_images/origin_img/10.bien-so-oto-co-co-wurth-1-2.jpg"
    #img_path2 = "/home/minhanh/Downloads/jetson_nano_MOT/test_images/origin_img/100.bien-so-dep-15.jpg"
    #img_path3 = "/home/minhanh/Downloads/jetson_nano_MOT/test_images/origin_img/247.20190722180645-9cd8_wm.jpg"
    #img_path4 = "/home/minhanh/Downloads/jetson_nano_MOT/test_images/origin_img/275.20120615-ha-noi-bien-so-xe-sieu-dep-6688...-sieu-rom-0.jpg"
    #img_path5 = "/home/minhanh/Downloads/jetson_nano_MOT/test_images/origin_img/308.khung-bien-so-o-to-2.jpg"
    #img_path6 = "/home/minhanh/Downloads/jetson_nano_MOT/test_images/origin_img/341.9d421b07a3feaf07c25b2d9d13d2b1c8.jpg"
    #img_path7 = "/home/minhanh/Downloads/jetson_nano_MOT/test_images/origin_img/54.biensocafeauto02-1487586518.jpg"
        img_crop = img2[int(box[1]):int(box[3]),int(box[0]):int(box[2])]

    #img_path = img_path7

    #if img_path == img_path1 or img_path== img_path2 or img_path== img_path6 or img_path== img_path7 or img_path == img_path5:
            #value_thres = 130
    #elif img_path == img_path4:
            #value_thres = 150
    #elif img_path== img_path3:
            #value_thres = 195
    #else:
            #value_thres = 135

        value_thres = 130
    #img_crop = cv2.imread(img_path)
    
        h, w , c = img_crop.shape
    
        cv2.imshow("img car", img_crop)
        cv2.waitKey()