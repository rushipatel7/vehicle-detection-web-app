import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans
import math


def kmeansdetect(img, bboxes):
    # print('BOXES RECIEVED', bbox)
    # img = cv.imread('img/b23.jpg')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # gray = cv.medianBlur(gray,5)
    edges = cv.Canny(gray, 50, 150, apertureSize=3)
    # cv.imshow('hosd',edges)
    # cv.waitKey(0)
    line_lis = []
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=50)
    #print('total lines', len(lines))
    for line in lines:
        line_lis.append(line[0])
        # print('LINA', line)
        x1, y1, x2, y2 = line[0]
        # cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)

    clusters = 2
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(line_lis)

    y = kmeans.cluster_centers_

    summ_list = y.sum(axis=0) / 2
    # print('SUMMA SUMA',summ_list)

    # print(y)
    hola = y.tolist()

    # print(hola)
    # for x in hola:
    #     x1, y1, x2, y2 = x
    #     cv.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    mid_x1, mid_y1, mid_x2, mid_y2 = summ_list
    # cv.line(img, (int(mid_x1), int(mid_y1)), (int(mid_x2), int(mid_y2)), (0, 255, 0), 2)
    # print('mid line', summ_list)

    return angularsort(summ_list, bboxes)
    # cv.imshow('gsdg',img)
    # cv.imwrite('img/cropres.jpg', img)
    # cv.waitKey(0)


def angularsort(mid, bboxes):
    mid = mid.tolist()
    bbox_result_top = []
    bbox_result_bot = []

    inp_line_m2 = (int(mid[3]) - int(mid[1])) / (int(mid[2]) - int(mid[0]))
    B = math.atan(inp_line_m2) * 180 / 3.14

    for line in bboxes:

        inp_line_m1 = (int(mid[3]) - (line[1] + line[3] // 2)) / (int(mid[2]) - line[0])
        A = math.atan(inp_line_m1) * 180 / 3.14

        resu = round(A - B, 2)
        # print('A - B for class id {0} is {1}'.format(line[4][0], resu))

        if resu > 0 and resu < 100:
            b1 = bbox_result_top.append(line)
        elif resu > 100:
            bbox_result_bot.append(line)
        else:
            bbox_result_bot.append(line)

    bbox_result_top.sort(key=lambda x: x[0])
    bbox_result_bot.sort(key=lambda x: x[0])

    # print('bboxe', bbox_result_top)
    # print('bboxe', bbox_result_bot)

    bbox_final = bbox_result_top + bbox_result_bot

    # print('bboxe', bbox_final)
    return bbox_final
