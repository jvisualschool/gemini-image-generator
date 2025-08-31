#!/usr/bin/env python3
import os
import requests
import json
import base64

def generate_gemini_image():
    # API 키 확인 - 환경변수에서 가져오거나 파일에서 읽기
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        try:
            # API_key.txt 파일에서 API 키 읽기
            with open('API_key.txt', 'r', encoding='utf-8') as f:
                api_key = f.read().strip()
            print("API_key.txt 파일에서 API 키를 읽었습니다.")
        except FileNotFoundError:
            print("❌ API_key.txt 파일을 찾을 수 없습니다. 환경변수 GEMINI_API_KEY를 설정하거나 API_key.txt 파일을 생성해주세요.")
            return
        except Exception as e:
            print(f"❌ API 키 파일 읽기 오류: {e}")
            return
    
    # PNG 폴더가 없으면 생성
    png_dir = "PNG"
    if not os.path.exists(png_dir):
        os.makedirs(png_dir)
    
    # API 요청 설정
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [
                {"text": "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"}
            ]
        }]
    }
    
    try:
        print("Gemini API로 이미지 생성 중...")
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
                        
                        # PNG 폴더에 저장
                        image_path = os.path.join(png_dir, 'gemini-native-image.png')
                        with open(image_path, 'wb') as f:
                            f.write(decoded_data)
                        
                        print(f"✅ 이미지가 성공적으로 생성되었습니다: {image_path}")
                        return
        
        print("❌ 응답에서 이미지 데이터를 찾을 수 없습니다.")
        print("응답 내용:", json.dumps(response_json, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 실패: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    generate_gemini_image()