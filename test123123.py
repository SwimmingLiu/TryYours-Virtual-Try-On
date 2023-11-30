import base64
import json
from PIL import Image
import io
import requests

url = "http://6cf8-34-125-125-235.ngrok-free.app/anime/predict/"
header = {
    "Cache-Control": "no-cache",
    "Cookie": "abuse_interstitial=fd74-34-125-125-235.ngrok-free.app",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
data = {
    "userid": 123123,
    "origin_image": "https://i.imgs.ovh/2023/11/30/pzDEm.jpeg",
}
res = requests.post(url=url, headers=header, json=data, timeout=300)
base64_image_data = json.loads(res.content)
base64_image_data = base64_image_data['data']['image_value']
# 解码 base64 数据
decoded_image_data = base64.b64decode(base64_image_data)

# 将二进制数据转换为图像
image = Image.open(io.BytesIO(decoded_image_data))

# 展示图像
image.show()
