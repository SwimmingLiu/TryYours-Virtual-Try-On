import base64
import json
import requests
from PIL import Image
from io import BytesIO

class DataResult():
    def __init__(self, code=200, msg='success', data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def success(self, data=None):
        self.code = 200
        self.msg = 'success'
        self.data = data

    def fail(self, data=None):
        self.code = 500
        self.msg = 'fail'
        if data is None:
            self.data = ''
        else:
            self.data = data

    def toJson(self):
        return json.dumps(self.__dict__)

def get_image_base64(image_path):
    with open(image_path, 'rb') as file:
        binary_content = file.read()
    return base64.b64encode(binary_content).decode('utf-8')



def download_and_save_image(image_url, save_path):
    # 发送请求下载图片
    response = requests.get(image_url)
    if response.status_code == 200:
        # 将内容转换为二进制流
        image_data = BytesIO(response.content)
        # 打开图片
        image = Image.open(image_data)
        # 将图片转换为 JPG 格式（如果需要）
        if image.format != 'JPEG':
            image = image.convert('RGB')
        # 保存图片
        image.save(save_path, format='JPEG')
        return True
    else:
        return False


