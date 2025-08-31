# 🍌 Gemini Nano Banana 이미지 생성기

Google Gemini API를 사용하여 AI 이미지를 생성하는 Flask 웹 애플리케이션입니다.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ 주요 기능

- 🎨 Google Gemini API를 통한 AI 이미지 생성
- 🇰🇷 한국어 프롬프트 지원
- 🖼️ 생성된 이미지 갤러리 및 관리
- 📊 이미지 메타데이터 CSV 저장
- 🔍 모달을 통한 이미지 원본 보기
- 📱 반응형 웹 디자인

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/jvisualschool/gemini-image-generator.git
cd gemini-image-generator
```

### 2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. API 키 설정

**방법 1: API_key.txt 파일 생성 (권장)**

프로젝트 루트에 `API_key.txt` 파일을 생성하고 API 키를 입력하세요:

```
your_gemini_api_key_here
```

**방법 2: 환경변수 설정**

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 4. Google Gemini API 키 발급

[Google AI Studio](https://aistudio.google.com/apikey)에서 API 키를 발급받으세요.

### 5. 애플리케이션 실행

```bash
python app.py
```

브라우저에서 [http://localhost:5001](http://localhost:5001)로 접속하세요.

## 📁 프로젝트 구조

```
gemini-image-generator/
├── 📄 app.py                    # Flask 메인 애플리케이션
├── 📄 generate_gemini_image.py  # 단독 이미지 생성 스크립트
├── 📁 templates/
│   └── 📄 index.html           # 메인 웹 페이지
├── 📁 static/
│   └── 🖼️ bananas.svg          # 로고 이미지
├── 📁 PNG/                     # 생성된 이미지 저장 폴더 (자동 생성)
├── 📄 image_metadata.csv       # 이미지 메타데이터 (자동 생성)
├── 📄 API_key.txt             # API 키 파일 (수동 생성 필요)
├── 📄 requirements.txt         # Python 의존성
├── 📄 .gitignore              # Git 제외 파일 목록
└── 📄 README.md               # 이 파일
```

## 🔒 보안 주의사항

> ⚠️ **중요**: 다음 파일들은 절대 GitHub에 업로드하지 마세요!

- `API_key.txt` (API 키 포함)
- `PNG/` 폴더 (생성된 이미지들)
- `image_metadata.csv` (메타데이터)
- 가상환경 폴더들 (`venv/`, `flask_venv/`, `gemini_env/`)

이미 `.gitignore` 파일에 설정되어 있습니다.

## 🛠️ API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|------------|------|
| `GET` | `/` | 메인 페이지 |
| `POST` | `/generate` | 이미지 생성 |
| `GET` | `/images` | 이미지 목록 조회 |
| `GET` | `/image/<filename>` | 이미지 파일 서빙 |
| `DELETE` | `/delete/<filename>` | 이미지 삭제 |
| `GET` | `/metadata` | CSV 메타데이터 조회 |
| `GET` | `/get-api-key` | API 키 조회 (개발용) |

## 📖 사용법

1. 웹 페이지에서 API 키를 입력하거나 `API_key.txt` 파일에 저장
2. 프롬프트 입력란에 원하는 이미지 설명 입력
3. 샘플 프롬프트 클릭으로 빠른 입력 가능
4. "이미지 생성하기" 버튼 클릭
5. 생성된 이미지는 갤러리에서 확인 가능
6. 이미지 클릭 시 모달로 원본 크기 보기
7. 삭제 버튼으로 불필요한 이미지 제거

## 💡 샘플 프롬프트

- `"Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"`
- `"A futuristic city with flying cars and neon lights"`
- `"A magical forest with glowing mushrooms and fairy lights"`
- `"서울 경복궁에서 한복을 예쁘게 입고 셀피를 찍는 20대 남여 커플"`
- `"A space station orbiting Earth with astronauts"`
- `"A steampunk robot in Victorian London"`

## 🛠️ 기술 스택

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **AI API**: Google Gemini 2.5 Flash Image Preview
- **이미지 처리**: PIL (Pillow)
- **데이터 저장**: CSV 파일

## 🐛 문제 해결

### API 키 관련 오류
- `API_key.txt` 파일이 존재하는지 확인
- API 키가 올바른지 Google AI Studio에서 확인
- 환경변수 `GEMINI_API_KEY` 설정 확인

### 이미지 생성 실패
- 인터넷 연결 상태 확인
- API 키 할당량 확인
- 프롬프트가 Google 정책에 위반되지 않는지 확인

### 포트 충돌
- 5001 포트가 사용 중인 경우 `app.py`의 포트 번호 변경

## 🤝 기여하기

1. 이 저장소를 포크하세요
2. 새로운 기능 브랜치를 만드세요 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/AmazingFeature`)
5. Pull Request를 열어주세요

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 질문이 있으시면 [Issues](https://github.com/jvisualschool/gemini-image-generator/issues)에 등록해주세요.

## 🙏 감사의 말

- [Google Gemini API](https://ai.google.dev/) - AI 이미지 생성 서비스 제공
- [Flask](https://flask.palletsprojects.com/) - 웹 프레임워크
- [Pillow](https://pillow.readthedocs.io/) - 이미지 처리 라이브러리

---

⭐ 이 프로젝트가 도움이 되셨다면 스타를 눌러주세요!