import re
import cv2
import numpy as np
import time
from vehicle_detect import houghsort as ht
from vehicle_detect import affinedetect as aff


# print('hola', np.subtract(max((staartx,staarty),(xtotal,ytotal)), min((staartx,staarty),(xtotal,ytotal))))
plate_regex = '^[A-Z]{2}[0-9]{1,3}[A-Z]{1,3}[0-9]{4}$'


# classes = []
# with open("coco.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]


def findplatestr(bounds, classes):
    try:
        plate = []
        for i in range(len(bounds)):
            label = str(classes[bounds[i][4][0]])
            plate.append(label)
        plate_to_str = ''.join(plate)
        return plate_to_str
    except:
        return None


def fetchplate(boxes, classes, img=None):
    print("length of biox",len(boxes))
    # boxes.sort(key= lambda x : x[1])
    # print('BOXES TEST', boxes)
    boxes_temp = boxes.copy()
    # IF Conditon sorts by height mostly 2 whlrs are taken into account

    if len(boxes) < 9:
        return boxes,None,None

    # return getplate,'REG_pehle',boxes_temp
    # print('\n\nboxes',boxes)
    else:
        # return 'No 10 digit plate to work with!'
        # print('LENGTH ELSA MA gayu (CAR MATE)')
        boxes_temp.sort(key=lambda x: x[0])
        getplate = findplatestr(boxes_temp, classes)
        # print('REEEEEEEEEE', (re.match(plate_regex, getplate)))
        getplate = findplatestr(boxes_temp, classes)
    # print('get plate regex1 ', getplate)

    if (re.match(plate_regex, getplate)) is not None:
        # print('1ST if regex ma')
        # print('get plate ', getplate)
        return getplate, 'REG_baad', boxes
    else:
        # print('1ST ELSE MA GAYUA')
        boxes.sort(key=lambda x: x[1])
        # print("\n\n:boxes", boxes)
        # boxes_extra = boxes[3:5]
        # boxes_extra.sort(key= lambda x : x[0])
        # print('\n\nboxes_Extra',boxes_extra)
        boxestop = boxes[:4]
        # boxestop += boxes_extra
        boxesbot = boxes[4:]
        boxestop.sort(key=lambda x: x[0])
        boxesbot.sort(key=lambda x: x[0])
        # print('boxestop',boxestop)
        # print('\n\nboxesbot',boxesbot)
        boxes1 = []
        boxes1 = boxestop + boxesbot
        getplate = findplatestr(boxes1, classes)
    # print('get plate regex2 ', getplate)

    if (re.match(plate_regex, getplate)) is not None:
        # print('get plate ', getplate)
        # print('2ND IF REGEX CHECK')
        return getplate, 'REG_baad', boxes
    else:
        # print('2ND ELSA MA GAYUA')
        # 3 values x thi sort

        if img is not None:
            start = time.time()
            try:
                boxes = aff.affineDetect(img)
                # print('\n\nbobxgesn', boxes)\
                if len(boxes) > 8:
                    getplate = findplatestr(boxes, classes)
            except:
                pass
            # print('TOTAL TIME fafafsa ;;;;', time.time() - start)
        # print('get plate 2nd else vadu ', getplate)
        else:
            pass

    if (re.match(plate_regex, getplate)) is not None:
        # print('get plate ', getplate)
        # print('3RD IF REGEX CHECK')
        return getplate, 'REG_baad', boxes
    else:
        try:
            # print("3RD ELSE MA GYU")
            origin = np.array((0, 0))
            distances = [[x, np.linalg.norm(np.array(tuple(x[0:2])) - origin)] for x in boxes]
            distances.sort(key=lambda x: x[1])
            # print('DISSSTACNECEN', distances)
            temp_eucli1 = distances[0:4]
            temp_eucli1.sort(key=lambda x: x[0])
            temp_eucli2 = distances[4:]
            temp_eucli2.sort(key=lambda x: x[0])

            tempeucli = temp_eucli1 + temp_eucli2
            tempeucli = [x[0] for x in tempeucli]
            getplate = findplatestr(tempeucli, classes)
        except:
            pass
    # print('get plate 3nd else vadu ', getplate)
    if (re.match(plate_regex, getplate)) is not None:
        # print('4TH IF REGEX CHECK')
        return getplate, 'REG_baad', tempeucli
    else:
        # print('4TH IF REGEX CHECK')
        if img is not None:
            try:
                start = time.time()

                ht_boxes = ht.kmeansdetect(img, boxes)
                getplate = findplatestr(ht_boxes, classes)
            except:
                pass
        if (re.match(plate_regex, getplate)) is not None:
            return getplate, 'REG_baad', ht_boxes

# print(fetchplate(test))