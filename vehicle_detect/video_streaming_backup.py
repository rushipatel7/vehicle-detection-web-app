import time
import cv2
import numpy as np
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cfg_file = BASE_DIR + '/vehicle_detect/yolo_weight_plate/yolov3-tiny-obj.cfg'
weights_file = BASE_DIR + '/vehicle_detect/yolo_weight_plate/yolov3-tiny-obj_140000.weights'
coco_file = BASE_DIR + '/vehicle_detect/yolo_weight_plate/coco.names'

net = cv2.dnn.readNetFromDarknet(cfg_file, weights_file)

classes = []
with open(coco_file, "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture(0)
        # confidence = 1

        self.video = cv2.VideoCapture(BASE_DIR+ "/static/video/1.mp4")

        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # image = cv2.resize(image, (0, 0), fx=0.3, fy=0.3)
        height, width, channels = image.shape
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)
        for i in range(len(boxes)):
            if i in indexes:
                j = 1
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                # color = colors[class_ids[i]]
                cv2.rectangle(image, (x, y), (x + w + 10, y + h + 10), (255, 255, 255), 2)

                # cv2.rectangle(frame, (x, y), (x + w, y + h), fix_color, 2)
                cv2.rectangle(image, (x, y), (x + w, y), (255, 255, 255), -1)
                # cv2.imwrite('./output/sdad.jpg', image)
                # img = cv2.imread("./output/sdad.jpg")
                # if label == 'plate':
                #     crop_img = img[y:y + h + 10, x:x + w + 20]
                #     # cv2.imshow("cropped", crop_img)
                #     cv2.imwrite("cropped.jpeg", crop_img)
                #     small = cv2.resize(crop_img, (0, 0), fx=0.5, fy=0.5)
                #     cv2.imwrite("cropped.jpeg", small)
                cv2.putText(image, label + " " + str(round(confidence, 2)), (x, y), cv2.FONT_HERSHEY_PLAIN, 1,
                            (255, 255, 255), 2)
                # elapsed_time = time.time() - starting_time
                # fps = frame_id / elapsed_time
                # cv2.putText(image, "FPS: " + str(round(fps, 2)), (10, 50),cv2.FONT_HERSHEY_PLAIN , 3, (0, 0, 0), 3)
                # cv2.imshow("Image", frame)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def index(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")
