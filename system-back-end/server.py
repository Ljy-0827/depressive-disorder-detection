import flask
import sys
from pathlib import Path
from flask_cors import CORS
import json
import zipfile
import os

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    exec_dir = Path(sys.executable).parent.resolve()
else:
    exec_dir = Path(__file__).parent.resolve()

server = flask.Flask(__name__,
                     static_url_path='',
                     static_folder=str(exec_dir/'web'),
                     template_folder=str(exec_dir/'web'))

server.jinja_env.variable_start_string = '{['
server.jinja_env.variable_end_string = ']}'
CORS(server)


@server.route('/')
def index():
    return flask.render_template('index.html')


# 上传量表作答结果
@server.route('/upload-questionnaire-answer', methods = ['POST'])
def upload_questionnaire_answer():
    try:
        json_data = flask.request.get_json()
        print(json_data)
        with open('./user-result/questionnaire/questionnaire_answer.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False)
        return 'questionnaire answer JSON data saved successfully', 200
    except Exception as e:
        return 500


# 上传视频（情绪图片观看、视频
@server.route('/upload-video', methods=['POST'])
def upload_video():
    try:
        # 检查请求中是否包含名为video的文件
        if 'video' not in flask.request.files:
            return 'No file part', 400

        # 获取前端发送的文件对象
        video_file = flask.request.files['video']

        # 检查是否选择了文件
        if video_file.filename == '':
            return 'No selected file', 400

        # 确定保存的文件名和路径
        save_path = './user-result/video/' + video_file.filename

        # 保存文件到本地
        video_file.save(save_path)
        return 'Video data saved successfully', 200

    except Exception as e:
        return 500


# 上传音频（文本朗读）
@server.route('/upload-audio', methods=['POST'])
def upload_audio():
    try:
        if 'audio' not in flask.request.files:
            return 'No file part', 400

        audio_file = flask.request.files['audio']

        if audio_file.filename == '':
            return 'No selected file', 400

        save_path = './user-result/audio/' + audio_file.filename

        audio_file.save(save_path)
        return 'Audio data saved successfully', 200

    except Exception as e:
        return 500


if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=False, port=8080)



