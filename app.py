from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
import os
import uuid

app = Flask(__name__)

# 업로드 및 출력 디렉터리 설정
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# 폴더 없으면 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': '파일이 없습니다.'}), 400

    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'error': '파일명이 없습니다.'}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    # UUID로 고유한 파일 이름 생성
    output_filename = f"{uuid.uuid4().hex}.png"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        # 첫 페이지만 변환
        images = convert_from_path(input_path, dpi=200)
        images[0].save(output_path, 'PNG')

        return jsonify({'download_url': f'/outputs/{output_filename}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 정적 파일 서빙 (변환된 이미지 접근용)
@app.route('/outputs/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

# 정적 리소스 설정 (styles.css, script.js)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
