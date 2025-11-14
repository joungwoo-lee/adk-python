# 🚀 ADK with Custom LLM - 실행 명령어

## 3가지 실행 방법

### 방법 1: 호스트에서 스크립트 실행 (가장 간단)

```bash
/home/joungwoolee/mysandbox/adk-python/run_adk_with_custom_llm.sh
```

이 스크립트는:
- 환경 변수 자동 로드
- 패치 자동 적용
- ADK Web 서버 시작 (0.0.0.0:38010)

---

### 방법 2: 도커 안에서 직접 실행 (현재 bash 세션에서)

도커 bash에 접속한 상태에서:

```bash
/root/run_adk.sh
```

또는 한 줄로:

```bash
source /root/.bashrc && cd /root/chainreaction && adk web . --host 0.0.0.0 --port 38010 --allow_origins="*" --reload --reload_agents
```

---

### 방법 3: 호스트에서 직접 실행 (스크립트 없이)

```bash
docker exec -it 43a7821ec23580ac2939c3a3c45d567a6d980ad6a8751f60bc343f09169d4870 \
  bash -c 'source /root/.bashrc && cd /root/chainreaction && adk web . --host 0.0.0.0 --port 38010 --allow_origins="*" --reload --reload_agents'
```

---

## 📋 실행 시 출력 예시

```
=== Custom LLM Configuration ===
Model: openai/gpt-oss:20b
API Base: http://172.21.137.193:11434/v1

=== Starting ADK Web Server ===
패치가 자동으로 적용됩니다...

✓ ADK Agent Builder Assistant - Gemini → 커스텀 LiteLlm 모델로 패치 완료
  Model: openai/gpt-oss:20b
  API Base: http://172.21.137.193:11434/v1

INFO:     Started server process [123]
INFO:     Waiting for application startup.

+-----------------------------------------------------------------------------+
| ADK Web Server started                                                      |
|                                                                             |
| For local testing, access at http://127.0.0.1:38010.                        |
+-----------------------------------------------------------------------------+

INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:38010 (Press CTRL+C to quit)
```

---

## 🔧 설정 변경

### 다른 LLM 모델로 변경하려면:

**도커 안의 `/root/.bashrc` 수정:**

```bash
docker exec -it 43a7821ec23580ac2939c3a3c45d567a6d980ad6a8751f60bc343f09169d4870 bash

# .bashrc 편집
vi /root/.bashrc

# 또는 직접 수정
cat > /root/.bashrc << 'EOF'
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# ADK Custom LLM Patch - Auto-load environment variables
export model="다른-모델-이름"
export api_base="http://다른-서버:포트/v1"
export api_key="api_key"
EOF

# 재로드
source /root/.bashrc
```

### 포트 변경하려면:

스크립트에서 `--port 38010` 부분을 원하는 포트로 변경

---

## ✅ 확인 사항

### 1. 패치가 적용되었는지 확인

```bash
docker exec 43a7821ec23580ac2939c3a3c45d567a6d980ad6a8751f60bc343f09169d4870 \
  bash -c 'source /root/.bashrc && python -c "
import sys
print(\"패치 로드됨:\", \"patch_adk_builder_model\" in sys.modules)
"'
```

### 2. 환경 변수 확인

```bash
docker exec 43a7821ec23580ac2939c3a3c45d567a6d980ad6a8751f60bc343f09169d4870 \
  bash -c 'source /root/.bashrc && echo "model=$model" && echo "api_base=$api_base"'
```

**예상 출력:**
```
model=openai/gpt-oss:20b
api_base=http://172.21.137.193:11434/v1
```

### 3. LLM 서버 연결 확인

```bash
curl http://172.21.137.193:11434/v1/models
```

---

## 🐛 트러블슈팅

### 에러: `ValueError: Missing key inputs argument!`

**원인:** 환경 변수가 로드되지 않음

**해결:**
```bash
# 도커 안에서
source /root/.bashrc
env | grep -E "^(model|api_base)="
```

출력이 없으면 `.bashrc` 확인

### 에러: Connection refused

**원인:** LLM 서버가 실행 중이 아니거나 접근 불가

**해결:**
```bash
# LLM 서버 확인
curl http://172.21.137.193:11434/v1/models

# 또는 네트워크 확인
ping 172.21.137.193
```

### 패치 메시지가 안 나옴

**원인:** sitecustomize.py가 로드되지 않음

**해결:**
```bash
docker exec 43a7821ec23580ac2939c3a3c45d567a6d980ad6a8751f60bc343f09169d4870 \
  cat /usr/lib/python3.10/sitecustomize.py
```

---

## 📁 관련 파일 위치

### 호스트
- `/home/joungwoolee/mysandbox/adk-python/run_adk_with_custom_llm.sh` - 실행 스크립트
- `/home/joungwoolee/mysandbox/adk-python/gemini_2.5_pro_override/patch_adk_builder_model.py` - 패치 파일

### 도커
- `/root/run_adk.sh` - 도커 내부 실행 스크립트
- `/root/.bashrc` - 환경 변수 설정
- `/usr/lib/python3.10/sitecustomize.py` - 자동 로드 스크립트

---

## 💡 빠른 시작

**가장 간단한 방법:**

```bash
# 1. 호스트에서 실행
/home/joungwoolee/mysandbox/adk-python/run_adk_with_custom_llm.sh

# 2. 브라우저에서 접속
http://localhost:38010
```

끝! 🎉
