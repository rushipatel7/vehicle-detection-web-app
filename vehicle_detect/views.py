import base64
import cv2
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import render
from vehicle_detect.forms import uploadFileForm, uploadFileSecond
from vehicle_detect.functions import handle_uploaded_file
from vehicle_detect.models import CommercialParking, CommercialHistory, Resident, Visitor
from vehicle_detect import yolo_for_tiny, video_stream
from vehicle_detect import yolo_for_secondModel


@login_required(login_url='login')
def index(request):
    data = CommercialParking.objects.all()
    empty_slot = 0
    total_slot = 10
    for x in data:
        if x.number_plate is None:
            empty_slot += 1
        if x.image is not None:
            x.image = x.image.tobytes()
            x.image = base64.b64encode(x.image)
            x.image = x.image.decode(encoding='utf-8')
        else:
            x.image = None
    content = {
        'data': data,
        'empty_slot': empty_slot,
        'total_slot': total_slot
    }
    print("-dgaqehdhnq-", content['data'])
    return render(request, 'index.html', content)


def landing(request):
    if request.method == 'POST':
        file_ob = uploadFileForm(request.POST, request.FILES)
        file_ob1 = uploadFileSecond(request.POST, request.FILES)
        if file_ob.is_valid() or file_ob1.is_valid():
            print("Under gayu")
            loaded_img = handle_uploaded_file(request.FILES['file'])

            # load yolo model
            plate, result_img = yolo_for_tiny.yolo_detect_plate(loaded_img)

            context = {
                'img': loaded_img,
                'plate_number': plate,
            }
            print("NUMBER PLATE IS:", plate)
            return render(request, "landing.html", context)
            # return render(request, "landing.html")
            # return render_to_response('landing.html', context, context_instance=RequestContext(request))
    else:
        file_ob = uploadFileForm()
        file_ob1 = uploadFileSecond()
    return render(request, "landing.html", {'form': file_ob, 'form1': file_ob1})


def yolo_backend(request):
    if request.method == 'POST':
        file_ob = uploadFileForm(request.POST, request.FILES)
        if file_ob.is_valid():
            print("Under gayu")
            loaded_img = handle_uploaded_file(request.FILES['file'])
            # print("CVFBNHMJDFDGDHFGJGKGFAGSHGDHJ",loaded_img)

            # load yolo model
            # plate, result_img = yolo_main.yolo_detect_plate(loaded_img)
            plate, result_img = yolo_for_tiny.yolo_detect_plate(loaded_img)
            # print("result is ", result_img)
            _, result_img = cv2.imencode('.jpg', result_img)
            # print("string image", result_img)
            result_img = result_img.tobytes()
            result_img = base64.b64encode(result_img)
            result_img = result_img.decode(encoding='utf-8')
            context = {
                'img': loaded_img,
                'plate_number': plate,
                'result_image': result_img
            }

            return render(request, "yolo_backend.html", context)
    else:
        file_ob = uploadFileForm()
        return render(request, "yolo_backend.html", {'form': file_ob})


def btnSecondModel(request):
    if request.method == 'POST':
        file_ob = uploadFileSecond(request.POST, request.FILES)
        if file_ob.is_valid():
            print("===========================================Under gayu")
            loaded_img = handle_uploaded_file(request.FILES['file'])
            print("FILE MALI")
            # print('SGD',type(loaded_img))
            # print("CVFBNHMJDFDGDHFGJGKGFAGSHGDHJ",loaded_img)

            # load yolo model
            # plate, result_img = yolo_main.yolo_detect_plate(loaded_img)
            plate, result_img = yolo_for_secondModel.yolo_ocr(loaded_img)
            # print("result is ", result_img)
            _, result_img = cv2.imencode('.jpg', result_img)
            # print("string image", result_img)
            result_img = result_img.tobytes()
            result_img = base64.b64encode(result_img)
            result_img = result_img.decode(encoding='utf-8')
            context = {
                'img': loaded_img,
                'plate_number': plate,
                'result_image': result_img
            }

            return render(request, "yolo_backend.html", context)
    else:
        file_ob = uploadFileSecond()
        return render(request, "yolo_backend.html", {'form': file_ob})


@login_required(login_url='login')
def commercial_history(request):
    history_data = CommercialHistory.objects.all()
    empty_slot = 0
    total_slot = 10
    for x in history_data:
        if x.number_plate is None:
            empty_slot += 1
        if x.image is not None:
            x.image = x.image.tobytes()
            x.image = base64.b64encode(x.image)

            x.image = x.image.decode(encoding='utf-8')
        else:
            x.image = None
    content = {
        'data': history_data,
        'empty_slot': empty_slot,
        'total_slot': total_slot
    }
    # print("-dgaqehdhnq-", content['data'])

    return render(request, "parking management/park_commercial_history.html", content)


def resident_history(request):
    resident_his = Resident.objects.all()

    visitor_his = Visitor.objects.all()
    for x in visitor_his:
        if x.image is not None:
            x.image = x.image.tobytes()
            x.image = base64.b64encode(x.image)

            x.image = x.image.decode(encoding='utf-8')
        else:
            x.image = None
    content = {
        'data': resident_his,
        'visitor_data': visitor_his,
    }
    return render(request, "parking management/park_resident_history.html", content)


def error_404(request):
    return render(request, "error-404.html")


def error_500(request):
    return render(request, "error-500.html")


def error_validation(request):
    return render(request, "error_verification.html")


def chat(request):
    return render(request, "chat.html")


def streaimg(request):
    vs = StreamingHttpResponse(video_stream.gen(video_stream.VideoCamera()), status=200,
                               content_type="multipart/x-mixed-replace;boundary=frame")
    vs['Cache-Control'] = 'no-cache'
    return vs
