# 🚀 AI & Google Drive Integration Guide

이 문서는 다른 세션(새로운 대화)에서도 쉽게 참조할 수 있도록 **NVIDIA Nemotron API 사용법**과 **Google Drive 자동 업로드 스크립트 사용법**을 정리한 가이드입니다.

---

## 1. NVIDIA Nemotron API 사용법

엔비디아의 API 카탈로그(build.nvidia.com)에서 발급받은 API 키를 활용하여 Nemotron 모델에 요청을 보내는 기본 파이썬 코드입니다.

### 📌 준비 사항
* `openai` 라이브러리 설치: `pip install openai`
* 엔비디아 개발자 계정 및 API 키 발급 (`nvapi-...`)

### 💻 예제 코드 (`nvidia_nemotron_example.py`)
```python
from openai import OpenAI
import os

# 환경 변수에서 키를 불러오는 것을 권장하지만, 테스트용으로는 직접 입력 가능합니다.
API_KEY = "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" 

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = API_KEY
)

completion = client.chat.completions.create(
  model="nvidia/nemotron-3-ultra-550b-a55b",
  messages=[{"role":"user", "content":"Write a limerick about the wonders of GPU computing."}],
  temperature=1,
  top_p=0.95,
  max_tokens=16384,
  stream=True
)

for chunk in completion:
  if not chunk.choices:
    continue
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")
```

---

## 2. Google Drive 파일 자동 업로드 (Python)

기존에 설정된 `C:\Users\exbxda13\gdrive-classifier` 폴더 내의 OAuth 인증 정보(`token.json`, `credentials.json`)와 헬퍼 스크립트를 사용하여 파일을 구글 드라이브에 업로드하는 방법입니다.

### 📌 준비 사항
* 구글 API 클라이언트 라이브러리: `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib`
* 작업 디렉터리가 `C:\Users\exbxda13\gdrive-classifier` 이거나 해당 폴더의 `gdrive_helper.py` 모듈을 import 할 수 있어야 합니다.

### 💻 예제 코드 (드라이브 업로드)
```python
import os
import sys

# gdrive-classifier 폴더를 모듈 경로에 추가
sys.path.append(r"C:\Users\exbxda13\gdrive-classifier")
from gdrive_helper import get_drive_service
from googleapiclient.http import MediaFileUpload

def upload_to_gdrive(file_path):
    # 기존에 저장된 token.json을 통해 인증
    service = get_drive_service()
    
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='text/plain')
    
    # 파일 업로드 실행
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    print(f"✅ 구글 드라이브 업로드 완료!")
    print(f"파일명: {file_name}")
    print(f"파일 ID: {file.get('id')}")

if __name__ == '__main__':
    # 업로드할 파일의 로컬 절대 경로를 입력하세요.
    target_file = r"C:\Users\exbxda13\nvidia_nemotron_example.py"
    upload_to_gdrive(target_file)
```

---

## 3. NVIDIA Flux.1-dev 이미지 생성 API 사용법

엔비디아의 Black Forest Labs Flux 모델을 사용하여 텍스트 프롬프트를 기반으로 이미지를 생성하는 파이썬 코드입니다.

### 📌 준비 사항
* `requests` 라이브러리 설치: `pip install requests`

### 💻 예제 코드 (Flux 이미지 생성)
```python
import requests

invoke_url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"

headers = {
    "Authorization": "Bearer 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",
    "Accept": "application/json",
}

payload = {
    "prompt": "a simple coffee shop interior",
    "mode": "base",
    "cfg_scale": 3.5,
    "width": 1024,
    "height": 1024,
    "seed": 0,
    "steps": 50
}

response = requests.post(invoke_url, headers=headers, json=payload)
response.raise_for_status()

response_body = response.json()
print(response_body)
```

---
💡 **AI (Antigravity) 에게 팁:**
새로운 세션에서 이 기능들이 필요할 경우, 이 파일(`D:\workspace\GEMINI\AI_Cheat_Sheet.md`)을 먼저 읽고(`view_file`) 코드를 작성하면 기존 인증 정보와 코드를 완벽하게 재사용할 수 있습니다!
