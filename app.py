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
    try:
        if 'pdf_file' not in request.files:
            print("❌ 업로드된 파일이 없습니다.")
            return jsonify({'error': '파일이 없습니다.'}), 400

        file = request.files['pdf_file']
        if file.filename == '':
            print("❌ 파일명이 비어있습니다.")
            return jsonify({'error': '파일명이 없습니다.'}), 400

        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        print(f"📥 저장된 파일 경로: {input_path}")

        # 고유한 출력 파일 이름 생성
        output_filename = f"{uuid.uuid4().hex}.png"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        # Windows인 경우 poppler_path 꼭 지정
        images = convert_from_path(
            input_path,
            dpi=200,
            poppler_path=r"C:\poppler\Library\bin"  # 여기 실제 경로로 바꿔야 함!
        )

        print("🖼️ PDF → 이미지 변환 성공")

        images[0].save(output_path, 'PNG')
        print(f"✅ PNG 저장 완료: {output_path}")

        return jsonify({'download_url': f'/outputs/{output_filename}'})
    
    except Exception as e:
        print("🚨 서버 에러 발생:", str(e))
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
