import sys
import cv2 
import imutils
from yoloDet import YoloTRT
import torch
import tracker
from datetime import datetime
from law import colorDetector, midPoint, intersect
from bytetrack.byte_tracker import BYTETracker
import csv
import json
import license_placedetect as lpd

f= open('config.json')
data = json.load(f)
current = {}
previous = {}
t_counter1 = []
lane_left = data["lane_left"]
lane_center = data["lane_center"]
lane_right = data["lane_right"]
v_counter = []



tracker2 = BYTETracker()
def updateCrossLight(img, x0,y0,track_id, time_stamp):
    v_counter.append(track_id)
    cv2.rectangle(img, (x0, y0 - 10), (x0 + 10, y0), (0, 0, 255), -1)
    saveDir = "./law_img"
    file_name = "vuot_den_{}".format(time_stamp)
    cv2.imwrite("{}/{}.jpg".format(saveDir, file_name), img)


# use path for library and engine file
model = YoloTRT(library="yolov5/build/libmyplugins.so", engine="yolov5/build/yolov5s.engine", conf=0.5, yolo_ver="v5")
cap = cv2.VideoCapture("/home/ctarg_lab_1/Desktop/video_output.mp4")
#cap = cv2.VideoCapture(data["cature"]) # open one video
torch.cuda.empty_cache()
'''
time_list =[]
stt = 0
while True:
    box=[]
    classes = []
    score = []
    ret, frame = cap.read()
    if ret:
        pass
    else:
        break
    boxes, t = model.Inference(frame)
    t_track = datetime.now()


    if len(boxes):
        boxes = tracker.update(boxes,frame)
       
    t_track = datetime.now() - t_track
    frame = tracker.draw_bboxes(frame, boxes, None)
    t_error = datetime.now()
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
    #t_error = datetime.now() - t_error
    #print("FPS: {} sec".format(1/t))
    
    #time_list.append([stt,t, t_track, t_error])
    #stt = stt + 1
    torch.cuda.empty_cache()
    cv2.imshow("Output", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
       break
#    if stt > 50000:
#       break
#with open('yolov5_deepsort.csv','w',newline='') as f:
#    write = csv.writer(f)
#    write.writerow(['stt','detection time', 'track time', 'error time'])
#    write.writerows(time_list)
'''
time_list =[]
stt = 0
cap = cv2.VideoCapture(data["capture"])
while True:
    box=[]
    classes = []
    score = []
    ret, frame = cap.read()
    if ret:
        pass
    else:
        break
    boxes, t = model.Inference(frame)
    frame2 = frame.copy()
    if data["detect_license"] :
        lpd.detector_lp(frame2, boxes)
    for i in range(len(boxes)):
        box.append([int(boxes[i][0]),int(boxes[i][1]),int(boxes[i][2]),int(boxes[i][3])])
        classes.append(boxes[i][4])
        score.append(boxes[i][5])
    t_track = datetime.now()
    if len(boxes):
        #boxes = tracker.update(boxes,frame)
        boxes = tracker2.update(box, score, classes)
    t_track = datetime.now()-t_track
    frame = tracker.draw_bboxes(frame, boxes, None)
    t_error = datetime.now()
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
 
    t_error = datetime.now() - t_error
    time_list.append([stt,t, t_track, t_error])
    stt = stt + 1
    torch.cuda.empty_cache()
    cv2.imshow("Output", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
       break
#    if stt > 50000:
#       break
with open('yolov5_bytetrack.csv','w',newline='') as f:
    write = csv.writer(f)
    write.writerow(['stt','detection time', 'track time', 'error time'])
    write.writerows(time_list)
cap.release()
cv2.destroyAllWindows()

