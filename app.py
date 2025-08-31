from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
import json
import base64
from PIL import Image
import io
import glob
import uuid
import csv
from datetime import datetime

app = Flask(__name__)

# PNG 폴더 확인 및 생성
PNG_DIR = "PNG"
if not os.path.exists(PNG_DIR):
    os.makedirs(PNG_DIR)

# CSV 파일 경로
CSV_FILE = "image_metadata.csv"

def load_api_key():
    """API 키를 환경변수 또는 파일에서 로드"""
    # 환경변수에서 먼저 확인
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        return api_key
    
    # API_key.txt 파일에서 읽기
    try:
        with open('API_key.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"API 키 파일 읽기 오류: {e}")
        return None

# 샘플 프롬프트들
SAMPLE_PROMPTS = [
    "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme",
    "A futuristic city with flying cars and neon lights",
    "A magical forest with glowing mushrooms and fairy lights",
    "A space station orbiting Earth with astronauts",
    "A steampunk robot in Victorian London",
    "A cyberpunk street market in Seoul at night",
    "A floating island in the sky with waterfalls",
    "A crystal cave with bioluminescent creatures",
    "서울 경복궁에서 한복을 예쁘게 입고 셀피를 찍는 20대 남여 커플"
]

def generate_gemini_image(prompt, api_key):
    """Gemini API를 사용하여 이미지 생성"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [
                {"text": prompt}
            ]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # 응답에서 이미지 데이터 추출
        response_json = response.json()
        
        # 응답 구조 확인 및 이미지 데이터 찾기
        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            candidate = response_json['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                for part in candidate['content']['parts']:
                    if 'inlineData' in part and 'data' in part['inlineData']:
                        # Base64 디코딩하여 이미지 저장
                        image_data = part['inlineData']['data']
                        decoded_data = base64.b64decode(image_data)
                        
                        # 파일명 생성 (타임스탬프 + UUID)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        unique_id = str(uuid.uuid4())[:8]
                        filename = f"gemini_generated_{timestamp}_{unique_id}.png"
                        
                        # PNG 폴더에 저장
                        image_path = os.path.join(PNG_DIR, filename)
                        with open(image_path, 'wb') as f:
                            f.write(decoded_data)
                        
                        # 이미지 정보 가져오기
                        image_info = get_image_info(image_path)
                        file_stat = os.stat(image_path)
                        
                        # CSV에 메타데이터 저장
                        save_to_csv(
                            filename=filename,
                            prompt=prompt,
                            width=image_info['width'] if image_info else 0,
                            height=image_info['height'] if image_info else 0,
                            file_size=len(decoded_data),
                            created_time=file_stat.st_mtime
                        )
                        
                        return {
                            'success': True,
                            'filename': filename,
                            'path': image_path,
                            'size': len(decoded_data)
                        }
        
        return {
            'success': False,
            'error': '응답에서 이미지 데이터를 찾을 수 없습니다.',
            'response': response_json
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'API 요청 실패: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'오류 발생: {str(e)}'
        }

def get_image_info(image_path):
    """이미지 정보 가져오기"""
    try:
        with Image.open(image_path) as img:
            return {
                'width': img.size[0],
                'height': img.size[1],
                'format': img.format,
                'mode': img.mode
            }
    except Exception:
        return None

def save_to_csv(filename, prompt, width, height, file_size, created_time):
    """CSV 파일에 이미지 메타데이터 저장"""
    file_exists = os.path.exists(CSV_FILE)
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'prompt', 'width', 'height', 'file_size', 'created_time', 'created_timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # 파일이 없으면 헤더 작성
        if not file_exists:
            writer.writeheader()
        
        # 데이터 작성
        writer.writerow({
            'filename': filename,
            'prompt': prompt,
            'width': width,
            'height': height,
            'file_size': file_size,
            'created_time': datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S'),
            'created_timestamp': created_time
        })

def load_prompts_from_csv():
    """CSV 파일에서 프롬프트 정보 로드"""
    prompts_dict = {}
    if os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    prompts_dict[row['filename']] = row['prompt']
        except Exception as e:
            print(f"CSV 파일 읽기 오류: {e}")
    return prompts_dict

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html', sample_prompts=SAMPLE_PROMPTS)

@app.route('/get-api-key')
def get_api_key():
    """개발용 API 키 제공 (배포 시에는 제거하거나 비활성화)"""
    api_key = load_api_key()
    if api_key:
        return jsonify({'success': True, 'api_key': api_key})
    else:
        return jsonify({'success': False, 'error': 'API 키를 찾을 수 없습니다.'})

@app.route('/generate', methods=['POST'])
def generate_image():
    """이미지 생성 API"""
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    api_key = data.get('api_key', '').strip()
    
    if not prompt:
        return jsonify({'success': False, 'error': '프롬프트를 입력해주세요.'})
    
    if not api_key:
        return jsonify({'success': False, 'error': 'API 키를 입력해주세요.'})
    
    result = generate_gemini_image(prompt, api_key)
    return jsonify(result)

@app.route('/images')
def get_images():
    """PNG 폴더의 이미지 목록 가져오기"""
    try:
        image_files = glob.glob(os.path.join(PNG_DIR, "*.png"))
        images = []
        
        # CSV에서 프롬프트 정보 로드
        prompts_dict = load_prompts_from_csv()
        
        for image_file in image_files:
            file_info = os.stat(image_file)
            image_info = get_image_info(image_file)
            filename = os.path.basename(image_file)
            
            images.append({
                'filename': filename,
                'path': f'/image/{filename}',
                'size': file_info.st_size,
                'created': file_info.st_mtime,
                'width': image_info['width'] if image_info else 0,
                'height': image_info['height'] if image_info else 0,
                'prompt': prompts_dict.get(filename, filename)  # 프롬프트가 없으면 파일명 사용
            })
        
        # 생성 시간 역순으로 정렬
        images.sort(key=lambda x: x['created'], reverse=True)
        return jsonify({'success': True, 'images': images})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/image/<filename>')
def serve_image(filename):
    """이미지 파일 서빙"""
    return send_from_directory(PNG_DIR, filename)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_image(filename):
    """이미지 삭제"""
    try:
        file_path = os.path.join(PNG_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
            # CSV에서도 해당 레코드 삭제
            delete_from_csv(filename)
            
            return jsonify({'success': True, 'message': f'{filename} 삭제됨'})
        else:
            return jsonify({'success': False, 'error': '파일을 찾을 수 없습니다.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def delete_from_csv(filename):
    """CSV 파일에서 특정 파일명의 레코드 삭제"""
    if not os.path.exists(CSV_FILE):
        return
    
    try:
        # 기존 데이터 읽기
        rows = []
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = [row for row in reader if row['filename'] != filename]
        
        # 삭제된 데이터로 다시 쓰기
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            if rows:
                fieldnames = ['filename', 'prompt', 'width', 'height', 'file_size', 'created_time', 'created_timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
    except Exception as e:
        print(f"CSV에서 레코드 삭제 오류: {e}")

@app.route('/metadata')
def get_metadata():
    """CSV 파일의 메타데이터 조회"""
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({'success': True, 'data': []})
        
        data = []
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        
        # 생성 시간 역순으로 정렬
        data.sort(key=lambda x: float(x['created_timestamp']), reverse=True)
        return jsonify({'success': True, 'data': data})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
