import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def handle_uploaded_file(f):
    with open(BASE_DIR +  '/static/result/upload/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return destination.name
