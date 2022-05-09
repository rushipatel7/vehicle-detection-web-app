from PIL import Image
from vehicle_detect import sorttest as srt
from vehicle_detect import font as ft
import cv2
import imutils, sys
import numpy as np
import datetime
import time
import statistics as st
import os

BASE_DIR = os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def fetchdetails(original_img, name, topleft):
    # Loading image
    cfg = BASE_DIR + '/vehicle_detect/crnet/cr-net.cfg'
    whts = BASE_DIR + '/vehicle_detect/crnet/cr-net_last (8).weights'
    net = cv2.dnn.readNetFromDarknet(cfg, whts)
    with open(BASE_DIR + "/vehicle_detect/crnet/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    start = time.time()
    # filename = 'cropped.jpeg'
    global img
    img = original_img
    print(img.size)
    img = np.asarray(img)
    height, width, channels = img.shape
    print('omg shape', img.shape)
    # img = cv2.imread(filename)
    # img = cv2.resize(img, None, fx=0.8 ,fy=0.8)
    # height, width, channels = img.shape

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
    boxestest = []

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
                boxestest.append([x, y, w, h, [class_id]])

                confidences.append(float(confidence))
                class_ids.append(class_id)


    # Co_ordinates for drawing rectangles and putting text
    def getcorners(boxes, validate):
        lastbox = (len(boxes))
        if validate is 'REG_TRUE':  # is probably a two wheeler
            top_from_4 = boxes[:3]
            top_from_4.sort(key=lambda x: x[1])
            staarty = top_from_4[0][1]

            bottom_6 = boxes[4:]
            staartx = bottom_6[0][0]

            bottom_6.sort(key=lambda x: x[1])
            lastbox_bottom_6 = len(bottom_6)
            ytotal = bottom_6[lastbox_bottom_6 - 1][1] + bottom_6[lastbox_bottom_6 - 1][3]
            bottom_6.sort(key=lambda x: x[0])
            xtotal = bottom_6[lastbox_bottom_6 - 1][0] + bottom_6[lastbox_bottom_6 - 1][2]
            text_label_points = (staartx, staarty - 10)

        else:
            boxestest = boxes.copy()
            boxestest = sorted(boxes, key=lambda x: x[0])
            xtotal = boxestest[lastbox - 1][0] + boxestest[lastbox - 1][2]
            ytotal = boxestest[lastbox - 1][1]
            staartx = boxestest[0][0]
            staarty = boxestest[0][1] + boxestest[0][3]
            # text_label_points = (boxestest[0][0], ytotal - 5) #for opecv
            text_label_points = (staartx, ytotal - 20)  # for CUstom font
        print((xtotal, ytotal), (staartx, staarty), text_label_points)
        return (xtotal, ytotal), (staartx, staarty), text_label_points

    # print('\n\n boxees test : ',boxestest)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    class_idstest = [boxestest[x][4][0] for x in range(len(boxestest))]  # ordered class id acc to numb plate

    try:
        label, validation, bounds = srt.fetchplate(boxestest, classes)

        xy1, xy2, labelpts = getcorners(bounds, validation)
        print('xy1', xy1)
        global dhrumin
        dhrumin = label
        print('plate is', dhrumin)
        print('label pts: ', labelpts)
        # car_img = cv2.imread("../static/result/other img/sdad.jpg")
        car_img = cv2.imread(BASE_DIR + "/static/result/other img/sdad.jpg")
        # car_img = cv2.imread("G:/web app/vehicle_system/static/result/other img/sdad.jpg")
        # car_img = Image.open("sdad.jpg")
        # car_img = np.asarray(car_img)
        global avg_conf
        avg_conf = round((st.mean(confidences)) * 100, 4)
        print('Average confidence is : ', avg_conf)
        cv2.rectangle(img, xy1, xy2, (68, 206, 0), 2)
        car_img = ft.drawText(car_img, label, topleft, (255, 255, 255), validation)  # color in BGR Format
        #         # img = ft.drawText(img, label, labelpts, (255, 255, 255), validation)  # color in BGR Format
        # cv2.putText(img,label,labelpts,cv2.FONT_HERSHEY_TRIPLEX,1,(255,255,255))
        # cv2.imwrite("pp.jpg", img)

        # cv2.imwrite("sdad.jpg", car_img)
        # cv2.imwrite("../static/result/other img/sdad.jpg", car_img)
        cv2.imwrite(BASE_DIR + "/static/result/results/sdad.jpg", car_img)
        # cv2.imwrite("G:/web app/vehicle_system/static/result/results/sdad.jpg", car_img)

    except Exception as e:
        print('problem {}'.format(e))

    print('\nexecution time is ;', time.time() - start)
    return dhrumin, car_img, avg_conf
    # cv2 mate
    # cv2.putText(img,label, labelpts,cv2.FONT_ITALIC, 2, (255,255,0), 2)
    # return label,avg_conf
