import requests
import json
from pprint import pprint
import os
import pprint


# MY TOKEN = 	7fa3985e0bdfdf47551e0fa58c69a2b2887b1024
BASE_DIR = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(BASE_DIR)
imgname = open(BASE_DIR + "/static/result/upload/4.jpg", 'rb')

files = {
    'image': imgname,
}
x = requests.post('http://127.0.0.1:8000/api/', files=files)
# pprint.pprint(x.json())
y = json.dumps(x.json(),indent=4,separators=(',',':'))
y = json.loads(y)
pprint.pprint(y,indent=2, width=50)