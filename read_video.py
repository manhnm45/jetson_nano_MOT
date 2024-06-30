
import cv2

cam = cv2.VideoCapture("rtsp://admin:Admin@123@27.72.149.50:1554/profile3/media.smp")
while True:
    _, frame = cam.read()
    h, w,c   = frame.shape
    #cv2.resize(frame, (int(w/4), int(h/4)))
    cv2.imshow("cam", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cv2.cv2.destroyAllWindows()
cam.release()