import cv2
from paddleocr import PaddleOCR
import os
import numpy as np
list_text = []
# Khởi tạo mô hình OCR
ocr = PaddleOCR(lang="en")  # Thay đổi "vi" sang ngôn ngữ mong muốn (tiếng Anh: "en", v.v.)

def paddele_ocr(img):
    h,w,c = img.shape 
    out_line = np.array([[[[1,1]], [[w-1,1]],[[w-1, h-1]],[[1,h-1]]]])
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold_image = cv2.threshold(cv2.bilateralFilter(gray_image, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((2, 2), np.uint8)
    dilat_img = cv2.dilate(threshold_image, kernel, iterations=2)   
    erode_img = cv2.erode(dilat_img, kernel, iterations=2)   
    threshold_image = cv2.drawContours(erode_img, out_line, -1, (0, 0, 0), 1)
    blur = cv2.GaussianBlur(threshold_image, (5, 5), 1)

    # find max contour that contain number
    edges = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key = cv2.contourArea)
    #approx max contour become rectangle
    if img.shape[1]> 2*img.shape[0]:
        eps = 0.03                      #bien ngang N = 20
    else:
        eps = 0.09                      
    peri = cv2.arcLength(max_contour, True)
    max_contour = cv2.approxPolyDP(max_contour, int(eps*peri), True)    

    # create mask number area    
    mask = np.zeros_like(blur)
    mask1 = cv2.fillPoly(mask, [max_contour], 255)
    cv2.imshow("mask1", mask1)
    cv2.waitKey(0)
    #delete edge of licenseplate
    mask = cv2.bitwise_and(blur, blur, mask=mask1)     #logic and
    cv2.imshow("mask", mask)
    cv2.waitKey(0)
    result0 = cv2.bitwise_not(cv2.bitwise_xor(mask1, mask, mask=mask1))  #logic exor
    dilat_img2 = cv2.dilate(result0, kernel, iterations=2)        #delete noise
    result = cv2.erode(dilat_img2, kernel, iterations=2)           #restore number
    cv2.imshow("result", result)
    cv2.waitKey(0)

    try:
        if img.shape[1]> 2*img.shape[0]:
            text = ocr.ocr(result)[0][0][1][0]
        else:
            img1 = result[0:int(img.shape[0]/2),:]
            img2 = result[int(img.shape[0]/2):img.shape[0],:]

            text1 = ocr.ocr(img1)[0][0][1][0]
            text2 = ocr.ocr(img2)[0][0][1][0]
            text = text1+"-"+text2
    except:
        text = 'none'
    return text
    # In ra kết quả
if __name__== '__main__':
    img = cv2.imread('results/esr_img.png')
    text = paddele_ocr(img)
    print("text",text)