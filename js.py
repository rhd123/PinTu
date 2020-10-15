from io import BytesIO
from PIL import Image
import base64
import requests


pic_url = requests.get('http://47.102.118.1:8089/api/problem?stuid=031802423')
image_code = base64.b64decode(pic_url.json()['img'])
file_like = BytesIO(image_code)
image = Image.open(file_like)
image.save('image.JPG')
