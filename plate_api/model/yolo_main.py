import datetime
import cv2
import io
import numpy as np
from PIL import Image
from pytictoc import TicToc
from vehicle_detect import font as ft
from plate_api.model import yolo_for_image as yt
import os

BASE_DIR = os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def yolo_detect_plate(original_img):
    t = TicToc()
    t.tic()
    # print('og imae', original_img)
    cfg_file = BASE_DIR + '/vehicle_detect/yolo_weight_plate/yolov3-tiny-obj.cfg'
    weight_file = BASE_DIR + '/vehicle_detect/yolo_weight_plate/yolov3-tiny-obj_140000.weights'
    confidence = 1
    net = cv2.dnn.readNetFromDarknet(cfg_file, weight_file)
    print("loading Yolo plate Model")

    # checks if cuda is available,if available then deploy it on cuda
    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    classes = []
    with open(BASE_DIR + "/vehicle_detect/yolo_weight_plate/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
    # file_name = "015.jpg"

    # filename = secure_filename(original_img)
    # file_data = original_img.stream.read()
    # nparr = np.fromstring(file_data, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # image_request = request.FILES["file"]
    # image_bytes = image_request.read()
    # img = Image.open(io.BytesIO(image_bytes))

    # img = Image.open(original_img)
    img = original_img

    # img = cv2.imread(original_img)
    # cv2.imshow("img",img)
    # img = cv2.resize(img, None, fx=1, fy=1)
    # img = cv2.resize(img, None, fx=0.1, fy=0.1)

    print(img.size)
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # cv2.imwrite('dhrumin.jpg', img)
    height, width, channels = img.shape
    print(img.shape)
    # 320×320 it’s small so less accuracy but better speed
    # 609×609 it’s bigger so high accuracy and slow speed
    # 416×416 it’s in the middle and you get a bit of both.

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
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
            if confidence > 0.4:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                global x, y, w, h
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                global xmin, xmax, ymin, ymax
                xmin = x - (w / 2)
                xmax = x + (w / 2)
                ymin = y - (h / 2)
                ymax = y + (h / 2)
        print(confidences)
        date_format = datetime.datetime.now()
        local_format = date_format.strftime("%c")
        # jn.fetch_json_data(x_min, x_max, y_min, y_max, local_format, original_img)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (68, 206, 0), 5)
            # cv2.putText(img, label, (x, y - 5), font, 3, color, 5)

            # cv2.imwrite("G:/web app/vehicle_system/static/result/other img/sdad.jpg", img)
            cv2.imwrite(BASE_DIR + "/static/result/other img/sdad.jpg", img)

            # img = Image.open("G:/web app/vehicle_system/static/result/other img/sdad.jpg")
            img = Image.open(BASE_DIR + "/static/result/other img/sdad.jpg")
            img = np.asarray(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            if label == 'plate':
                global crop_img
                crop_img = img[y:y + h, x:x + w]
                # cv2.imshow("cropped", crop_img)
                cv2.imwrite(BASE_DIR + "/static/result/other img/cropped.jpg", crop_img)
                # cv2.imwrite("G:/web app/vehicle_system/static/result/other img/cropped.jpg", crop_img)
                global pratik
                # pratik = Image.open("G:/web app/vehicle_system/static/result/other img/cropped.jpg")
                pratik = Image.open(BASE_DIR + "/static/result/other img/cropped.jpg")
                global top_coords
                top_coords = (x, y - 50)

    # yolodetect1.yolo_ocr(pratik, original_img)
    plate, img, avg_confidence = yt.fetchdetails(pratik, original_img, top_coords)
    # print('===CORDS===', cord)

    return plate, img, avg_confidence, (xmin, xmax, ymin, ymax), (x, y, w, h)
    t.toc()
