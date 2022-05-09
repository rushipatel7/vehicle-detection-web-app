import os
import cv2
import time
from PIL import Image
import numpy as np
# import yolo_for_crnet as yc
# from . import
from . import yolo_for_crnet as yc
from vehicle_detect import font as ft

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def yolo_detect_plate(original_img):
    CONFIDENCE_THRESHOLD = 0.2
    NMS_THRESHOLD = 0.4
    COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

    with open(BASE_DIR + "/vehicle_detect/only plates first model/coco.names", "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]

    cfg_file = BASE_DIR + "/vehicle_detect/only plates first model/yolov3-tiny-obj.cfg"
    weight_file = BASE_DIR + "/vehicle_detect/only plates first model/yolov3-tiny-obj_last (17).weights"
    net = cv2.dnn.readNet(cfg_file, weight_file)
    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1 / 256)

    img = Image.open(original_img)
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    classes, scores, boxes = model.detect(img, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    bboxes = []
    confidences = []
    for (classid, score, box) in zip(classes, scores, boxes):
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        cv2.rectangle(img, (x, y), (x + w, y + h), (68, 206, 0), 3)
        confidences.append(round(float(score[0]), 4))
        bboxes.append([x, y, w, h, classid.tolist()])
        label = class_names[classid[0]]

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
            # pratik = Image.open("G:/web app/vehicle_system/static/result/other img/cropped.jpg")
            crop_img = Image.open(BASE_DIR + "/static/result/other img/cropped.jpg")

            global top_coords
            top_coords = (x, y - 20)

    plate, img = yc.yolo_ocr(crop_img, top_coords)
    if plate is not None and len(plate) > 8:
        img = ft.drawText(img, plate, top_coords, (255, 255, 255), 'REG_TRUE')  # color in BGR Format
    else:
        pass

    return plate, img
