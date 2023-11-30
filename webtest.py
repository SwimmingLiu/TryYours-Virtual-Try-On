import json
import time

import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
from PIL import Image
import os

from AnimeGAN.model import  anime_model
from utils import DataResult, get_image_base64, download_and_save_image

app = Flask(__name__)
run_with_ngrok(app)

data_list = []


# @app.route('/', methods=['GET', 'POST'])
# def main():
#     return render_template('main.html')
#
#
# @app.route('/predict', methods=['GET', 'POST'])
# def file_upload():
#     if request.method == 'POST':
#         f = request.files['file']
#         f_src = 'static/origin_web.jpg'
#
#         f.save(f_src)
#         return render_template('fileUpload.html')
#
#
# @app.route('/fileUpload_cloth', methods=['GET', 'POST'])
# def fileUpload_cloth():
#     if request.method == 'POST':
#         f = request.files['file']
#         f_src = 'static/cloth_web.jpg'
#
#         f.save(f_src)
#         return render_template('fileUpload_cloth.html')
#
#
# @app.route('/view', methods=['GET', 'POST'])
# def view():
#     print("inference start")
#
#     terminnal_command = "python main.py"
#     os.system(terminnal_command)
#
#     print("inference end")
#     return render_template('view.html', data_list=data_list)  # html을 렌더하며 DB에서 받아온 값들을 넘김

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')


@app.route('/tryon/predict/', methods=['POST'])
def tryon_predict():
    result = DataResult()
    result.success()
    if request.is_json:
        # 拿到结果
        req_json = request.get_data()
        try:
            req_json = req_json.decode('utf-8')
            req_json = json.loads(req_json)
        except Exception:
            print("fail to load json!!!")
            return result.fail().toJson()

        # 获取衣服图
        cloth = req_json['cloth']
        cloth_path = 'static/cloth_web.jpg'
        if not download_and_save_image(image_url=cloth, save_path=cloth_path):
            result.fail()
            return result.toJson()

        # 获取人物图
        person = req_json['person']
        person_path = 'static/origin_web.jpg'
        if not download_and_save_image(image_url=person, save_path=person_path):
            result.fail()
            return result.toJson()

        terminnal_command = "python main.py"
        os.system(terminnal_command)

        final_image_path = "static/finalimg.png"
        image_value = get_image_base64(final_image_path)
        result.data = {
            'image_value': image_value
        }
        return result.toJson()
    else:
        result.fail()
        return result.toJson()


@app.route('/anime/predict/', methods=['POST'])
def anime_predict():
    result = DataResult()
    result.success()
    if request.is_json:
        # 拿到结果
        req_json = request.get_data()
        try:
            req_json = req_json.decode('utf-8')
            req_json = json.loads(req_json)
        except Exception:
            print("fail to load json!!!")
            return result.fail().toJson()

        # 获取原始图像
        origin_image = req_json['origin_image']
        origin_image_path = 'static/anime_origin.jpg'
        if not download_and_save_image(image_url=origin_image, save_path=origin_image_path):
            result.fail()
            return result.toJson()
        final_image_path = "static/anime_processed.png"
        anime_model(origin_image_path, final_image_path)
        image_value = get_image_base64(final_image_path)
        result.data = {
            'image_value': image_value
        }
        return result.toJson()
    else:
        result.fail()
        return result.toJson()


if __name__ == '__main__':
    app.run()
