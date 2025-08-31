# Gemini Nano Banana 이미지 생성기

Google Gemini API를 사용하여 AI 이미지를 생성하는 Flask 웹 애플리케이션입니다.

## 주요 기능

- Google Gemini API를 통한 AI 이미지 생성
- 한국어 프롬프트 지원
- 생성된 이미지 갤러리 및 관리
- 이미지 메타데이터 CSV 저장
- 모달을 통한 이미지 원본 보기
- 반응형 웹 디자인

## 설치 및 실행

### 1. 필요한 패키지 설치

```bash
pip install flask requests pillow
```

### 2. API 키 설정

다음 중 하나의 방법으로 Google Gemini API 키를 설정하세요:

**방법 1: API_key.txt 파일 생성 (권장)**
```
프로젝트 루트에 API_key.txt 파일을 생성하고 API 키를 입력하세요.
```

**방법 2: 환경변수 설정**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Google Gemini API 키 발급

https://aistudio.google.com/apikey 에서 API 키를 발급받으세요.

### 4. 애플리케이션 실행

```bash
python app.py
```

브라우저에서 http://localhost:5001 로 접속하세요.

## 파일 구조

```
├── app.py                 # Flask 메인 애플리케이션
├── generate_gemini_image.py # 단독 이미지 생성 스크립트
├── templates/
│   └── index.html        # 메인 웹 페이지
├── static/
│   └── bananas.svg       # 로고 이미지
├── PNG/                  # 생성된 이미지 저장 폴더 (자동 생성)
├── image_metadata.csv    # 이미지 메타데이터 (자동 생성)
└── API_key.txt          # API 키 파일 (수동 생성 필요)
```

## 보안 주의사항

⚠️ **중요**: 다음 파일들은 절대 GitHub에 업로드하지 마세요:

- API_key.txt (API 키 포함)
- PNG/ 폴더 (생성된 이미지들)
- image_metadata.csv (메타데이터)
- 가상환경 폴더들 (venv/, flask_venv/, gemini_env/)

이미 .gitignore 파일에 설정되어 있습니다.

## API 엔드포인트

- `GET /` - 메인 페이지
- `POST /generate` - 이미지 생성
- `GET /images` - 이미지 목록 조회
- `GET /image/<filename>` - 이미지 파일 서빙
- `DELETE /delete/<filename>` - 이미지 삭제
- `GET /metadata` - CSV 메타데이터 조회
- `GET /get-api-key` - API 키 조회 (개발용)

## 사용법

1. 웹 페이지에서 API 키를 입력하거나 API_key.txt 파일에 저장
2. 프롬프트 입력란에 원하는 이미지 설명 입력
3. 샘플 프롬프트 클릭으로 빠른 입력 가능
4. "이미지 생성하기" 버튼 클릭
5. 생성된 이미지는 갤러리에서 확인 가능
6. 이미지 클릭 시 모달로 원본 크기 보기
7. 삭제 버튼으로 불필요한 이미지 제거

## 샘플 프롬프트

- "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
- "A futuristic city with flying cars and neon lights"
- "A magical forest with glowing mushrooms and fairy lights"
- "서울 경복궁에서 한복을 예쁘게 입고 셀피를 찍는 20대 남여 커플"
- 기타 다양한 창의적 프롬프트들

## 기술 스택

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **AI API**: Google Gemini 2.5 Flash Image Preview
- **이미지 처리**: PIL (Pillow)
- **데이터 저장**: CSV 파일

## 라이선스

이 프로젝트는 개인 및 교육 목적으로 자유롭게 사용할 수 있습니다.

## 문제 해결

### API 키 관련 오류
- API_key.txt 파일이 존재하는지 확인
- API 키가 올바른지 Google AI Studio에서 확인
- 환경변수 GEMINI_API_KEY 설정 확인

### 이미지 생성 실패
- 인터넷 연결 상태 확인
- API 키 할당량 확인
- 프롬프트가 Google 정책에 위반되지 않는지 확인

### 포트 충돌
- 5001 포트가 사용 중인 경우 app.py의 포트 번호 변경

## 개발자 정보

이 프로젝트는 Google Gemini API를 활용한 이미지 생성 데모 애플리케이션입니다.