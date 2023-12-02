import json
import time

import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
from PIL import Image
import os
import sys
from AnimeGAN.model import anime_model
from utils import DataResult, get_image_base64, download_and_save_image
from pyngrok import ngrok

app = Flask(__name__)
app.config.from_mapping(
    BASE_URL="http://localhost:5000",
    USE_NGROK=True
)

if app.config["USE_NGROK"]:
    # pyngrok will only be installed, and should only ever be initialized, in a dev environment

    # Get the dev server port (defaults to 5000 for Flask, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "5000"

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port,domain="certain-ideally-foal.ngrok-free.app").public_url
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    app.config["BASE_URL"] = public_url

data_list = []


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
        except Exception:
            result.fail()
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
        except Exception:
            result.fail()
            return result.toJson()
    else:
        result.fail()
        return result.toJson()


if __name__ == '__main__':
    app.run()
