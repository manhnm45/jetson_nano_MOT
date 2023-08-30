import cv2
import numpy
import matplotlib

def detector_lp(img,box):
    img = img.copy()
    
    for i in range(len(box)):
        
        img_crop = img[box[i][1]:box[i][3],box[i][0]:box[i][2]]
    
        #convert to gray image
        gray_img = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
        #canny edge detection
        
        canny_img = cv2.Canny(gray_img, 170 ,200)
        #find countor base on edge
        contours, new  = cv2.findContours(canny_img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours=sorted(contours, key = cv2.contourArea, reverse = True)[:30]
        # Initialize license Plate contour and x,y coordinates
        contour_with_license_plate = None
        license_plate = None
        x = None
        y = None
        w = None
        h = None

         # Find the contour with 4 potential corners and creat ROI around it
        for contour in contours:
                # Find Perimeter of contour and it should be a closed contour
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
                if len(approx) == 4: #see whether it is a Rect
                    contour_with_license_plate = approx
                    x, y, w, h = cv2.boundingRect(contour)
                    license_plate = gray_img[y:y + h, x:x + w]
                    break
            # Removing Noise from the detected image, before sending to Tesseract
        license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)
        (thresh, license_plate) = cv2.threshold(license_plate, 150, 180, cv2.THRESH_BINARY)
        cv2.imshow("frame",img_crop)
        cv2.imshow("test",license_plate)
        #cv2.rectangle(img,(rect[0],rect[2]),(rect[1],rect[3]),(0,125,0),2)
        cv2.waitKey()
        # if cv2.waitKey(5) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()