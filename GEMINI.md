
# Python API Integration Rules

## 1. Python 3.12 Windows SSL Bug (truststore recursion)
- **현상**: Windows 환경의 Python 3.12에서 `openai` 파이썬 SDK(또는 `httpx`+`truststore`를 사용하는 라이브러리)를 사용할 경우, SSL 컨텍스트 검증 과정에서 `RecursionError: maximum recursion depth exceeded` 오류가 발생하며 스크립트가 뻗는 치명적 버그가 존재함.
- **해결책**: 해당 환경에서는 SDK 라이브러리에 의존하지 말고, 순수 파이썬 내장 `urllib.request` 또는 `requests` 모듈을 사용하여 직접 REST API 엔드포인트로 통신할 것.

## 2. 대규모 LLM 텍스트 생성 스크립트 규칙 (Robust Scripting)
수십~수백 건의 LLM API를 연속 호출하는 자동화 스크립트 작성 시 아래 규칙을 반드시 준수할 것:
- **자동 재시도 (Resiliency)**: 503(Service Unavailable), 429(Rate Limit) 및 일시적 통신 끊김에 대비해 API 호출부를 `try-except`로 감싸고, 최소 5~10회의 재시도(Retry) 및 대기 시간(Backoff) 로직을 필수로 구현할 것.
- **넉넉한 타임아웃**: LLM 텍스트 생성은 응답이 매우 길어질 수 있으므로, 타임아웃을 기본 120초 이상(권장 300초)으로 넉넉하게 설정할 것.
- **이어쓰기(Auto-Resume) 구현**: 스크립트가 중간에 중단되더라도 다시 처음부터 실행되지 않도록, 시작 전 반드시 결과물 파일/디렉토리를 스캔하여 '마지막으로 생성된 인덱스'를 파악하고 그다음 번호부터 이어서(Resume) 작동하도록 상태 추적 로직을 구현할 것.
