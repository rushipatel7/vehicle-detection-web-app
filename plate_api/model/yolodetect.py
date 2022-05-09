import cv2
import numpy as np
import time
import datetime
import json
import pandas as pd
import threading
import os

BASE_DIR = os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))



def yolo_ocr(original_img, name):
    # print('ocr og image', type(original_img))
    # cfg_file = 'G:/Web Application Development/Rushi/trying_hard/hard_working/yolo_weights_ocr/yolov3-tiny-obj.cfg'
    # weight_file = 'G:/Web Application Development/Rushi/trying_hard/hard_working/yolo_weights_ocr/yolov3-tiny-obj_45000.weights'

    cfg_file = BASE_DIR + '/vehicle_detect/crnet/cr-net.cfg'

    weight_file = BASE_DIR +  '/vehicle_detect/crnet/cr-net_last.weights'
    confidence = 1
    net = cv2.dnn.readNetFromDarknet(cfg_file, weight_file)
    print("loading Yolo ocr Model")

    # checks if cuda is available,if available then deploy it on cuda
    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    classes = []
    # with open("G:/Web Application Development/Rushi/trying_hard/hard_working/yolo_weights_ocr/coco.names", "r") as f:
    with open(BASE_DIR + "/vehicle_detect/crnet/coco.names", "r") as f:
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

    # original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    # original_img = Image.fromarray(original_img)

    # img = Image.open(original_img)

    img = original_img
    # img = cv2.imread(original_img)
    # cv2.imshow("img",img)
    # img = cv2.resize(img, None, fx=1, fy=1)
    # img = cv2.resize(img, None, fx=0.1, fy=0.1)

    print(img.size)
    img = np.asarray(img)
    height, width, channels = img.shape
    print(img.shape)

    # 320×320 it’s small so less accuracy but better speed
    # 609×609 it’s bigger so high accuracy and slow speed
    # 416×416 it’s in the middle and you get a bit of both.

    # Detecting objects
    # blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    blob = cv2.dnn.blobFromImage(img, 0.00392, (352, 128), (0, 0, 0), True, crop=False)
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
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
        print(confidences)
        # date_format = datetime.datetime.now()
        # local_format = date_format.strftime("%c")
        # day_format = date_format.strftime("%A")
        # month_format = date_format.strftime("%B")
        # Write  Json Data
        # data = {
        #     "X_min": x,
        #     "Y_min": y,
        #     "Weight": w,
        #     "Height": h,
        #     "File_Name": name,
        #     "Date and Time": local_format,
        #     "Confidence": confidences
        # }
        # print(json.dumps(data, indent=2))
        #
        # fetch_data = open("Fetch_Data.json", "w")
        # json.dump(data, fetch_data, indent=2)
        # fetch_data.close()
        #
        # with open("Fetch_Data.json") as fd:
        #     data1 = json.load(fd)
        # print("Fetch Data from JSON File-->  X_MiN : ", data1["X_min"])

        # json End

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            # cv2.imwrite("42.png",img)

            # img = cv2.imread("42.png")
            # crop_img = img[y:y + h, x:x + w]
            # cv2.imshow("cropped", crop_img)
            # cv2.imwrite("cropped.jpeg",crop_img)
            # cv2.waitKey(0)
            print(label, end='')

            cv2.putText(img, label, (x, y - 5), font, 2, color, 2)
    # cv2.imshow("Image", img)
    cv2.imwrite( BASE_DIR + "/static/result/other img/pp.jpg", img)

    # json_to_csv = pd.read_json(r'G:/Web Application Development/Rushi/trying_hard/Fetch_Data.json')
    # export_csv = json_to_csv.to_csv(r'G:/Web Application Development/Rushi/trying_hard/data.csv', index=None)
    # print(json_to_csv)

    # text = pytesseract.image_to_string(crop_img , lang='eng')
    # print("plate is "+text)
    # cv2.waitKey(0)

# rushi patel kem che
