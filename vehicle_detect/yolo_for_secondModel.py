import os
import statistics as st
import numpy as np
import cv2
from PIL import Image
import vehicle_detect.sorttest as srt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIDENCE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
class_names = []
with open(BASE_DIR + "/vehicle_detect/crnet/coco.names", "r")  as f:
    class_names = [cname.strip() for cname in f.readlines()]


def yolo_ocr(original_img):
    net = cv2.dnn.readNet(BASE_DIR + "/vehicle_detect/crnet/cr-net.cfg",
                          BASE_DIR + "/vehicle_detect/crnet/cr-net_last (8).weights", )
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(352, 128), scale=1 / 256)

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
        confidences.append(round(float(score[0]), 4))
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0))
        bboxes.append([x, y, w, h, classid.tolist()])
    cv2.imwrite(BASE_DIR + "/static/result/other img/1.jpg", img)
    # try:
    label, validation, bounds = srt.fetchplate(bboxes, class_names)

    print('plate is', label)

    car_img = cv2.imread(BASE_DIR + "/static/result/other img/sdad.jpg")
    avg_conf = round((st.mean(confidences)) * 100, 4)

    if len(label) > 1:
        label = 'Characters that were detected are ' + ','.join(
            class_names[x[4][0]] for x in sorted(bboxes, key=lambda x: x[0]))
        return label, img

    print('Average confidence is : ', avg_conf)

    cv2.imwrite(BASE_DIR + "/static/result/results/sdad.jpg", car_img)

    return label, img
    # except Exception as e:
    #     print('problem {}'.format(e))
