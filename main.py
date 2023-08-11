import cv2
import tracker
from detector import Detector
import numpy as np
import time
import torch.cuda
from datetime import datetime
from law import colorDetector, midPoint, intersect
from bytetrack.byte_tracker import BYTETracker

previous = {}
current = {}
t_counter1 = []
v_counter = []
# Functions
def updateCrossLight(img, x0,y0,track_id, time_stamp):
    v_counter.append(track_id)
    cv2.rectangle(img, (x0, y0 - 10), (x0 + 10, y0), (0, 0, 255), -1)
    saveDir = "./law_img"
    file_name = "vuot_den_{}".format(time_stamp)
    cv2.imwrite("{}/{}.jpg".format(saveDir, file_name), img)

lane_left = []
lane_center = [830,420,1200,400] 
lane_right = []
# capture = cv2.VideoCapture("rtsp://admin:Admin@123@27.72.149.50:1554/profile3/media.smp") # open one video
capture = cv2.VideoCapture("/media/jackson/Extra/AI_Camera_CTARG/video_output.mp4") # open one video

detector = Detector()
bytetrack = BYTETracker()
while True:
    box =[]
    classes =[]
    score =[]
    torch.cuda.empty_cache()
    t = time.time()
    _, frame = capture.read()
    boxes = detector.detect(frame)
    for i in range(len(boxes)):
        box.append(int(boxes[i][0]),boxes[i][1],boxes[i][2],boxes[3])
        classes.append(boxes[4])
        score.append(boxes[5])
    #if len(boxes):
        #boxes = tracker.update(boxes, frame)
    
    if len(box)>0:
        boxes = bytetrack.update(box,score,classes)
    cv2.rectangle()
    current_color = colorDetector(frame)
    time_stamp = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    for i in range(len(boxes)):
        box = boxes[i][:4]
        track_id = boxes[i][-1]
        cls = boxes[i][4]
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])
        current[track_id]  = midPoint(x0,y0,x1,y1)

        if track_id in previous:
            cv2.line(frame, previous[track_id], current[track_id], (0,255,0), 1)
            line_group0 = [lane_left, lane_center, lane_right]
            for element in line_group0:
                if len(element):
                    # print(element)
                    start_line = element[0],element[1]
                    end_line = element[2], element[3]
                    if intersect(previous[track_id],current[track_id], start_line, end_line):
                        print(intersect(previous[track_id],current[track_id], start_line, end_line))
                        if line_group0.index(element) == 1:
                            t_counter1.append(track_id)
                            if current_color != "red":
                                print("Fined")
                                updateCrossLight(frame, x0, y0, track_id, time_stamp)
        previous[track_id] = current[track_id]

    # print(colorDetector(frame=frame))
    # frame = tracker.draw_bboxes(frame,boxes, None)
    cv2.imshow("Video Stream", frame)
    duration = time.time() - t
    print(f"fps: {1/duration}")
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()