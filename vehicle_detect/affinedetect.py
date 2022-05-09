import cv2
import numpy as np
import time
from vehicle_detect import yolo_for_affine as yaff

start = time.time()


def affineDetect(img):
    try:
        rows, cols, ch = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv.medianBlur(gray,5)
        edges = cv2.Canny(gray, 50, 250, apertureSize=3)
        # cv2.imshow('hosd',edges)
        # cv2.waitKey(0)
        line_lis = []
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=50)
        # print('total lines', len(lines))
        for line in lines:
            line_lis.append(line[0])
            x1, y1, x2, y2 = line[0]
            # cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

        # print(line_lis)
        line_1 = line_lis[0]

        if line_1[1] < rows // 2:
            # print('if vadu')
            pts1 = np.float32([[line_1[0], line_1[1]], [line_1[2], line_1[3]	] ,[ 0, cols ]])
            pts2 = np.float32([ [	50 ,0		],					[cols ,0				] ,[0, cols 	]])
        else:
            # print('else vadu')
            pts1 = np.float32([ [	line_1[0],	line_1[1]	],	[	line_1[2] ,line_1[3]		] ,[ rows ,0]])
            pts2 = np.float32([[0, cols - 60], [cols, rows], [line_1[2], 20]])

        M = cv2.getAffineTransform(pts1, pts2)

        dst = cv2.warpAffine(img, M, (int(cols * 1.1), int(rows * 1.1)))

        boxes = yaff.affine_boxes_detect(dst)
        # print('BOBOXBDSN', bboxes)
        boxes.sort(key=lambda x: x[1])
        boxestop = boxes[:4]
        # boxestop += boxes_extra
        boxesbot = boxes[4:]
        boxestop.sort(key=lambda x: x[0])
        boxesbot.sort(key=lambda x: x[0])
        boxes1 = []
        boxes1 = boxestop + boxesbot
        return boxes1

    except:
        return None
