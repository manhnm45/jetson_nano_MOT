import cv2
from paddleocr import PaddleOCR
ocr = PaddleOCR(lang="en")
def read_text(img):
    #img = cv2.resize(img, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
    #cv2.imshow("origi",img)
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret1,img2 = cv2.threshold(img1,145,250,cv2.THRESH_BINARY)
    cnts,new = cv2.findContours(img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:1]
    cv2.drawContours(img,cnts,-1,(0,255,0),3)
    cv2.drawContours(img,cnts,-1,(0,255,0),3)
    cv2.imshow("co",img)
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4: 
                screenCnt = approx
    x,y,w,h = cv2.boundingRect(c) 
    img=img[y:y+h,x:x+w]

    #kernel = np.ones((1, 1), np.uint8)
    #img = cv2.dilate(img, kernel, iterations=1)
    #img = cv2.erode(img, kernel, iterations=1)
    # img = cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # img = cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # img = cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    # img = cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    # img = cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    cv2.imshow("crop", img)
    # return " "
    #pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    #elif args["preprocess"] == "blur":
    #gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # Check xem có sử dụng tiền xử lý ảnh không
    # Nếu phân tách đen trắng
    # ret1,gray = cv2.threshold(gray,145,250,cv2.THRESH_BINARY)
    # Nếu làm mờ ảnh
    # kernel = np.zeros((3,3),np.uint8)
    # gray = cv2.erode(gray, kernel, iterations = 1)
    # Ghi tạm ảnh xuống ổ cứng để sau đó apply OCR
    # bfilter = cv2.bilateralFilter(gray, 11, 17,17) # Noise reduction
    # ret1,gray = cv2.threshold(bfilter,145,250,cv2.THRESH_BINARY)
    
    # edged = cv2.Canny(bfilter, 30, 200) # Edge dectection
    # Load ảnh và apply nhận dạng bằng Tesseract OCR
    custom_config = r'--oem 3 --psm 6'
    text = ocr.ocr(img)
    text = text.replace(" ","")
    if text[-1] == "\n":
        text = text.replace("\n", '-')
        text = text[0:-1]
    # print(type(text))
    # print(text)
    text_1 = ""
    for i in range(len(text)):
        if (i ==2 and text[i] == '6'):
            text_1 = text_1 + 'G'
            continue
        if (i == 2 and text[i] == '0'):
            text_1 = text_1 + 'D'
            continue
        if (i == 2 and text[i] == '8'):
            text_1 = text_1 + 'B'
            continue
        if text[i].isalnum() or (i == 3 and text[i] == "-") or (i == 7 and text[i] == '.') :
            text_1 = text_1 + text[i]
    # Xóa ảnh tạm sau khi nhận dạng
    return text