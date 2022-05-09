from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def drawText(im_o, label, co_ords, color, validation):
    # Make into PIL Image
    co_ords_list = list(co_ords)
    im_p = Image.fromarray(im_o)

    path = BASE_DIR + "/static/font/sansbolditalic.ttf"
    # Get a drawing context
    draw = ImageDraw.Draw(im_p)
    if validation is 'REG_TRUE' and im_p.width < 1000:  # mostly 2 wheeler
        monospace = ImageFont.truetype(path,20)
        size = list(draw.textsize(label, font=monospace))
        size[0] = size[0] + co_ords_list[0]
        size[1] = size[1] + co_ords_list[1] + 5
    else:
        monospace = ImageFont.truetype(path, 50)
        size = list(draw.textsize(label, font=monospace))
        size[0] = size[0] + co_ords_list[0]
        size[1] = size[1] + co_ords_list[1] + 2
    size = tuple(size)
    draw.rectangle([(co_ords), (size)], fill=(68, 206, 0))
    # print('text size is ' ,size)
    draw.text(co_ords, label, color, font=monospace)

    # Convert back to OpenCV image and save
    result_o = np.array(im_p)
    return result_o
