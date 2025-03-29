

# from flask import Flask, request, jsonify, send_from_directory, render_template
# from werkzeug.utils import secure_filename
# from pdf2image import convert_from_path
# import os
# import uuid

# app = Flask(__name__)

# # 업로드/출력 디렉터리 설정
# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'outputs'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# # 폴더가 없으면 생성
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/convert', methods=['POST'])
# def convert_pdf():
#     if 'pdf_file' not in request.files:
#         return jsonify({'error': '파일이 없습니다.'}), 400

#     file = request.files['pdf_file']
#     if file.filename == '':
#         return jsonify({'error': '파일명이 없습니다.'}), 400

#     filename = secure_filename(file.filename)
#     input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(input_path)

#     # 출력 파일명 생성
#     output_filename = f"{uuid.uuid4().hex}.png"
#     output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

#     try:
#         # poppler_path가 필요한 경우 여기 명시
#         # 예: poppler_path=r'C:\Poppler\poppler-xx\bin' (Windows 사용자용)
#         images = convert_from_path(input_path, dpi=200)
#         images[0].save(output_path, 'PNG')

#         return jsonify({'download_url': f'/outputs/{output_filename}'})
#     except Exception as e:
#         print("PDF 변환 중 오류:", e)  # 콘솔 로그
#         return jsonify({'error': str(e)}), 500

# # 변환된 이미지 제공
# @app.route('/outputs/<filename>')
# def serve_image(filename):
#     return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

# # 정적 리소스 제공 (JS, CSS 등)
# @app.route('/static/<path:filename>')
# def static_files(filename):
#     return send_from_directory('static', filename)

# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
import os
import uuid

app = Flask(__name__)

# 업로드 및 출력 폴더 설정
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# 폴더 없으면 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 홈 페이지
@app.route('/')
def index():
    return render_template('index.html')

# PDF 변환 엔드포인트
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

    try:
        # 모든 페이지를 이미지로 변환
        images = convert_from_path(input_path, dpi=200)

        image_urls = []

        for idx, image in enumerate(images):
            output_filename = f"{uuid.uuid4().hex}_p{idx+1}.png"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            image.save(output_path, 'PNG')
            image_urls.append(f"/outputs/{output_filename}")

        return jsonify({'download_urls': image_urls})

    except Exception as e:
        print("PDF 변환 중 오류:", e)
        return jsonify({'error': str(e)}), 500

# 변환된 이미지 제공
@app.route('/outputs/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

# 정적 파일 제공 (JS, CSS 등)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# 로컬 테스트용 실행
if __name__ == '__main__':
    app.run(debug=True)
