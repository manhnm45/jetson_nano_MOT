import cv2
import numpy
import imutils
import matplotlib
from multiprocessing import Process
#from paddleocr import PaddleOCR
#ocr = PaddleOCR(lang="en")
area_threshold =100
def detector_lp(img):
    img_crop = img.copy()
    
    h, w , c = img_crop.shape
    
    img_crop = img_crop[int(2*h/3):h , int(2*w/3):w]
    #img_crop0 = img_crop.copy()
    
    #cv2.imshow("img_crop",img_crop)
    

    #Remove noise
    gray_img= cv2.bilateralFilter(img_crop, 11, 17, 17)
    cv2.imshow("img_gray",gray_img)
    #cv2.imwrite("gray_img247.jpg",gray_img)
    cv2.waitKey()
    #canny edge detection

    canny_img = cv2.Canny(gray_img,64 ,200)
    #find countor base on edge
    cv2.imshow("canny_edg",canny_img)
    #cv2.imwrite("canny_img247.jpg",canny_img)
    cv2.waitKey()
    contours, new  = cv2.findContours(canny_img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img3 = img_crop.copy()
    #
    #cv2.drawContours(img3, contours, -1, (0,255,0), 2)
    #cv2.imshow("contours_img",img3)
    #cv2.imwrite("contours247.jpg",img3)
    #cv2.waitKey()

    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:2]
    print("len_contours", len(contours))
    img4 = img_crop.copy()
    #cv2.drawContours(img4,contours, -1,(0,255,0),3)
    #cv2.imshow("sort_contour", img4)
    #cv2.waitKey()
    #cv2.imwrite("sort247.jpg",img4)
    # Initialize license Plate contour and x,y coordinates
    license_plate = None
    x = None
    y = None
    w = None
    h = None
        # Find the contour with 4 potential corners and creat ROI around it
    for contour in contours:
            if cv2.contourArea(contour) < area_threshold:
                    
                    continue
            else:
                # Find Perimeter of contour and it should be a closed contour
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
                if len(approx) == 4: #see whether it is a Rect
                    contour_with_license_plate = approx
                    x, y, w, h = cv2.boundingRect(contour)
                    print("tlwh", [x,y,w,h])
                    img6 = img_crop.copy()
                    license_plate = img6[y:y + h , x:x + w ]
    return license_plate
                    
                        
    
        
if __name__ == "__main__":
      img = cv2.imread(r"/home/minhanh/Downloads/jetson_nano_MOT/test_images/data_test/367.ferrari-458-italia111-102433-1368795995_500x0.jpg")
      lp = detector_lp(img)

      cv2.imshow("license_plate",lp)
      cv2.waitKey()
    