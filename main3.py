import cv2
import tracker
from detector import Detector
import numpy as np
import torch.cuda
from datetime import datetime
from law import colorDetector, midPoint, intersect
from bytetrack.byte_tracker import BYTETracker
import license_process_paddle as lpd
import json
import time
f= open('config.json')
data = json.load(f)
previous = {}
current = {}
t_counter1 = []
t_counter3 = []
t_counter4 = []
t_counter5 = []
v_counter = []
# Functions


lane_left = data["lane_left"]
lane_center = data["lane_center"]
lane_right = data["lane_right"]
derect_left = data["derect_left"]
derect_center = data["derect_center"]
derect_right = data["derect_right"]
#capture = cv2.VideoCapture(data["capture"]) # open one video
capture = cv2.VideoCapture(r"trafic video/vlc-record-2024-05-22-15h12m06s-rtsp___27.72.73.145_8554_uhd-.mp4") # open one video
detector = Detector()
bytetrack = BYTETracker()
while True:
    t = time.time()
    box =[]
    classes =[]
    score =[]
    torch.cuda.empty_cache()
    ret, frame = capture.read()
    # if(frame.shape[0]<2160 and frame.shape[1]<3840):
    #     cv2.resize(frame,(2160,3840))
    boxes = detector.detect(frame)
    #print("boxes", boxes)
    for i in range(len(boxes)):
        box.append([int(boxes[i][0]),int(boxes[i][1]),int(boxes[i][2]),int(boxes[i][3])])
        classes.append(boxes[i][4])
        score.append(boxes[i][5])
    frameToDraw = tracker.draw_bboxes(frame,boxes, None)
    
    #if len(boxes):
        #boxes = tracker.update(boxes, frame)
    #tracker.draw_bboxes(frame2,boxes,2)
    if len(box)>0:
       boxes = bytetrack.update(box,score,classes)
    #print("boxes",boxes[0])
    #print("ok")
    frame2 = frame.copy()
    
    
    
    #cv2.rectangle()
    current_color = colorDetector(frame)
    time_stamp = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    for i in range(len(boxes)):
        box = boxes[i][:4]
        track_id = boxes[i][4]
        cls = boxes[i][4]
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])
        #print("track_id", track_id)
        current[track_id]  = midPoint(x0,y0,x1,y1)
        # if data["detect_license"]:
        #     print("boxes", boxes[i])
        #     license_plate = lpd.detector_lp(frame2, boxes[i])
        if track_id in previous:
            cv2.line(frame, previous[track_id], current[track_id], (0,255,0), 1)
            line_group0 = [lane_left, lane_center, lane_right]
            #print("ok")
            for element in line_group0:
                if len(element):
                    
                    #print(element)
                    start_line = element[0],element[1]
                    end_line = element[2], element[3]
                    frame = cv2.line(frame,start_line,end_line,(255,0,0),2)
                    if intersect(previous[track_id],current[track_id], start_line, end_line):
                        #print(intersect(previous[track_id],current[track_id], start_line, end_line))
                        
                        if line_group0.index(element) == 1:
                            t_counter1.append(track_id)
                            current_color = "green"
                            if current_color != "red":
                                print("Fined")
                                if data["detect_license"]:                  
                                    try:
                                        if boxes[i][5] =="car":
                                            print("boxes", boxes[i])
                                            img_car = frame2[int(box[1]):int(box[3]),int(box[0]):int(box[2])]
                                            license_plate = lpd.process_lp(img_car)
                                            print("text lp",license_plate)
                                    except:
                                        pass
                                
            #print("t_contour1", t_counter1)
            line_group1 = [derect_left, derect_center, derect_right]
            for element in line_group1:
                if len (element):
                    start_line = element[0],element[1]
                    end_line = element[2], element[3]
                    frame = cv2.line(frame,start_line,end_line,(255,0,0),2)
                    if intersect(previous[track_id],current[track_id], start_line, end_line):
                        #print(intersect(previous[track_id],current[track_id], start_line, end_line))
                        if line_group1.index(element) == 1:
                            t_counter3.append(track_id)
                            

        previous[track_id] = current[track_id]

    # print(colorDetector(frame=frame))
    
    frameToShown = cv2.resize(frameToDraw, (int(frameToDraw.shape[1]/3),int(frameToDraw.shape[0]/3)))
    #print("shape frame",frameToShown.shape)
    #frameToShown = frame[0:int(frame.shape)]
    # cv2.imshow("Video Stream", frameToShown)
    duration = time.time() - t
    print("duration",duration)
    print(f"fps: {1/duration}")
    # if cv2.waitKey(1) == ord('q'):
    #     break
    
cv2.destroyAllWindows()