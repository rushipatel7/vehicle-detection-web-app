import cv2
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("JGF",BASE_DIR)
CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
with open(BASE_DIR + "/vehicle_detect/crnet/coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]


def affine_boxes_detect(img):
    bboxes = []
    cfg =  BASE_DIR + "/vehicle_detect/crnet/cr-net.cfg"
    whts = BASE_DIR +"/vehicle_detect/crnet/cr-net_last.weights"
    net = cv2.dnn.readNet(cfg, whts)

    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(352, 128), scale=1 / 256)

    classes, scores, boxes = model.detect(img, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

    for (classid, score, box) in zip(classes, scores, boxes):
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        bboxes.append([x, y, w, h, classid.tolist()])

    return bboxes


