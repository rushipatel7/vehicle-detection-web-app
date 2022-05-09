import time
import cv2
import numpy as np
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
with open(BASE_DIR + '/vehicle_detect/only plates first model/coco.names', "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

cfg_file =  BASE_DIR + '/vehicle_detect/only plates first model/yolov3-tiny-obj.cfg'
weight_file =  BASE_DIR + '/vehicle_detect/only plates first model/yolov3-tiny-obj_last (17).weights'
net = cv2.dnn.readNet(cfg_file, weight_file)

# if gpu is available
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1 / 256)


class VideoCamera(object):
    def __init__(self):

        # self.video = cv2.VideoCapture(BASE_DIR + "/static/video/1.mp4")
        self.video = cv2.VideoCapture("https://192.168.0.101:8080/video")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        (grabbed, frame) = self.video.read()
        if not grabbed:
            exit()

        start = time.time()
        classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        end = time.time()

        start_drawing = time.time()
        for (classid, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classid) % len(COLORS)]
            label = "%s : %s" % (class_names[classid[0]], round(float(score[0]), 2))
            label1 = class_names[classid[0]]
            cv2.rectangle(frame, box, color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


        end_drawing = time.time()

        fps_label = "FPS: %.2f (excluding drawing time of %.2fms)" % (
            1 / (end - start), (end_drawing - start_drawing) * 1000)
        cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        # cv2.imshow("detections", frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n' )


@gzip.gzip_page
def index(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")
