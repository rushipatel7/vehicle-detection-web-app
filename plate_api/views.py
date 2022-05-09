from django.shortcuts import render
# import yolo_for_image4 as yl4
import io
import numpy as np
import cv2
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from PIL import Image
import json
from .model import yolo_for_image4 as yl4
from .model import yolo_main as ym
from collections import OrderedDict

# Create your views here.
# from testuser.models import MyUser

from rest_framework.authtoken.models import Token


# for user in MyUser.objects.all():
#     Token.objects.get_or_create(user=user)

# Create your views here.


# @csrf_exempt
@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication], )
# @permission_classes([IsAuthenticated], )
def plateApi(request):
    result = {}

    if request.method == 'POST':
        name = request.FILES['image'].name
        img = request.FILES['image'].read()
        img = Image.open(io.BytesIO(img))
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plate, _,  avg_confi ,coord_norm, coords_og = ym.yolo_detect_plate(img)
        # plate, cnf = yl4.fetchdetails(img)

        result = {
            'name': name,
            'plate': plate,
            'probability': avg_confi,
            'co-ordinates': {
                'normalized': {
                    'x_min': coord_norm[0],
                    'x_max': coord_norm[1],
                    'y_min': coord_norm[2],
                    'y_max': coord_norm[3],
                },
                'original': {
                    'x': coords_og[0],
                    'y': coords_og[1],
                    'w': coords_og[2],
                    'h': coords_og[3],
                }
            },
        }
        # sort_order = ['name', 'plate', 'probability', 'co-ordinates']
        # result_order = [OrderedDict(sorted(item.iteritems(), key=lambda item: sort_order.index(item[0])))
        #                 for item in result]
        # result['result'] = {'plate': plate, 'probablity': avg_confi}
        # result['name'] = name
        # result['co-ordinates'] = {'normalized': {
        #     'x_min': coord_norm[0],
        #     'x_max': coord_norm[1],
        #     'y_min': coord_norm[2],
        #     'y_max': coord_norm[3],
        # }, 'original': {
        #     'x': coords_og[0],
        #     'y': coords_og[1],
        #     'w': coords_og[2],
        #     'h': coords_og[3],
        # }
        # }
        print('LAVEL', plate)
        print('heell')
    # result = json.dumps(result, indent=2)
    return Response(result)
