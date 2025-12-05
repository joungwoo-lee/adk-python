# ADK Custom LLM Patch - 자동 설치 패키지

Google ADK의 Gemini 모델을 커스텀 LiteLLM으로 자동 교체하는 패치입니다.

**도커 컨테이너 내부 실행 방식**

## 🎯 교체되는 모델

이 패치는 **Flash와 Pro 둘 다** 바꿉니다!

정확히는 **"gemini"가 들어간 모든 모델**을 다음으로 교체합니다:
```
openai/gpt-oss:20b (http://172.21.137.193:11434/v1)
```

### 감지 로직
세 가지 패치 지점에서 gemini 모델을 감지합니다:

1. `AgentBuilderAssistant.create_agent()` (patch_adk_builder_model.py:210):
   ```python
   if model is None or (isinstance(model, str) and "gemini" in model.lower()):
   ```

2. `LlmAgent.__init__()` (patch_adk_builder_model.py:277):
   ```python
   if isinstance(model, str) and "gemini" in model.lower():
   ```

3. `LLMRegistry.new_llm()` ⭐ (patch_adk_builder_model.py:320):
   ```python
   if isinstance(model, str) and "gemini" in model.lower():
   ```

### 교체되는 모델들
- ✓ `gemini-2.5-flash` (ADK 1.18.0 기본값)
- ✓ `gemini-2.5-pro`
- ✓ `gemini-2.0-flash`
- ✓ `gemini-1.5-pro`
- ✓ 기타 모든 gemini 변형

### 세 가지 경로로 교체

1. **Agent Builder Assistant** (ADK Web UI 빌트인)
   - `AgentBuilderAssistant.create_agent()` 패치
   - UI에서 새 에이전트 생성 시

2. **LlmAgent 초기화** (직접 생성)
   - `LlmAgent.__init__()` 패치
   - 프로그래밍 방식으로 에이전트 생성 시

3. **LLMRegistry 모델 인스턴스화** ⭐ 가장 중요!
   - `LLMRegistry.new_llm()` 패치
   - YAML에서 로드된 `model: gemini-*` 문자열이 실제 모델 인스턴스로 변환될 때
   - 생성된 에이전트와 서브에이전트의 모든 gemini 모델 요청 가로채기

### 교체 결과

**Before:**
```yaml
model: gemini-2.5-flash  # 또는 gemini-2.5-pro
```

**After (자동 교체):**
```python
LiteLlm(
    model="openai/gpt-oss:20b",
    api_base="http://172.21.137.193:11434/v1",
    api_key="api_key"
)
```

환경 변수 `.bashrc`에서 설정한 값으로 교체됩니다.

---

## 📦 포함된 파일

- `install_patch.sh` - 자동 설치 스크립트 (도커 내부 실행)
- `patch_adk_builder_model.py` - 패치 파일
- `README.md` - 이 문서

---

## 🚀 빠른 시작

### 1단계: 도커에 복사

```bash
# 호스트에서 실행
docker cp /home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch 43a7821ec235:/tmp/
```

### 2단계: 도커 안에서 설치

```bash
# 도커 안에서 실행
docker exec -it 43a7821ec235 bash -c "cd /tmp/adk_web_force_patch && chmod +x install_patch.sh && ./install_patch.sh"
```

### 3단계: ADK 실행

```bash
# 도커 안에서 실행
docker exec -it 43a7821ec235 bash -c "source /root/.bashrc && cd /root/chainreaction && adk web . --host 0.0.0.0 --port 38010 --allow_origins='*' --reload --reload_agents"
```

---

## ✅ 설치되는 내용

### 도커 컨테이너 내부:

1. **패치 파일** (`/root/adk_patch/patch_adk_builder_model.py`)
   - Gemini 모델을 자동으로 교체하는 Python 패치

2. **sitecustomize.py** (`/usr/lib/python3.10/sitecustomize.py`)
   - Python 시작 시 자동으로 패치를 로드

3. **환경 변수** (`/root/adk_patch/.env`)
   ```bash
   model=openai/gpt-oss:20b
   api_base=http://172.21.137.193:11434/v1
   api_key=api_key
   ```

   `.env` 파일이 없으면 `.env.example`에서 자동 복사됩니다.

---

## 🔧 설정 변경

### LLM 모델 변경

```bash
# 도커 안에서 .env 파일 편집
docker exec -it 43a7821ec235 bash -c "cat > /root/adk_patch/.env << 'EOF'
# ADK Custom LLM Configuration
model=gpt-4
api_base=https://api.openai.com/v1
api_key=sk-...

# 커스텀 헤더 (선택)
x-dep-ticket=api_key
Send-System-Name=Chain_Reaction
User-Id=joungwoo.lee
User-Type=AD_ID
EOF"

# 변경사항 적용 후 ADK 재시작
```

---

## 🎯 동작 원리

1. **Agent Builder Assistant 패치**
   - `AgentBuilderAssistant.create_agent()` 메서드 교체
   - ADK Web UI의 빌트인 어시스턴트에 적용

2. **LlmAgent 패치**
   - `LlmAgent.__init__()` 메서드 교체
   - 프로그래밍 방식으로 생성되는 에이전트에 적용

3. **LLMRegistry 패치** ⭐ 핵심!
   - `LLMRegistry.new_llm()` 메서드 교체
   - YAML 파일의 `model: gemini-*`가 실제 모델 인스턴스로 변환되는 시점을 가로챔
   - 생성된 에이전트와 모든 서브에이전트의 gemini 모델 요청 처리

4. **자동 로드**
   - `sitecustomize.py`가 Python 시작 시 자동 실행
   - 환경 변수 확인 후 패치 적용

---

## 📋 확인 방법

### 패치 설치 확인

```bash
# 도커 안에서 확인
docker exec 43a7821ec235 cat /usr/lib/python3.10/sitecustomize.py
docker exec 43a7821ec235 cat /root/adk_patch/.env
docker exec 43a7821ec235 ls -la /root/adk_patch/
```

### 패치 작동 확인

```bash
# 도커 안에서 테스트
docker exec 43a7821ec235 python -c "
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

agent = LlmAgent(name='test', model='gemini-2.5-flash', instruction='test')
print(f'Model type: {type(agent.model).__name__}')
print(f'Is LiteLlm: {isinstance(agent.model, LiteLlm)}')
"
```

**예상 출력:**
```
✓ ADK Gemini → 커스텀 LiteLlm 모델 패치 완료
  - Agent Builder Assistant: ✓
  - LlmAgent (YAML support): ✓
  - LLMRegistry (전체 경로): ✓
  Model: openai/gpt-oss:20b
  API Base: http://172.21.137.193:11434/v1
Model type: LiteLlm
Is LiteLlm: True
```

---

## 🐛 트러블슈팅

### 에러: `ValueError: Missing key inputs argument!` 또는 환경 변수 오류

**원인:** .env 파일이 없거나 잘못된 형식

**해결:**
```bash
# .env 파일 확인
docker exec 43a7821ec235 cat /root/adk_patch/.env

# .env 파일이 없으면 .env.example에서 복사
docker exec 43a7821ec235 cp /root/adk_patch/.env.example /root/adk_patch/.env

# 또는 직접 생성
docker exec 43a7821ec235 bash -c "cat > /root/adk_patch/.env << 'EOF'
model=openai/gpt-oss:20b
api_base=http://172.21.137.193:11434/v1
api_key=api_key
EOF"
```

### 패치가 적용되지 않음

**원인:** sitecustomize.py가 올바르게 설치되지 않음

**해결:**
```bash
# 재설치
docker exec -it 43a7821ec235 bash -c "cd /tmp/adk_web_force_patch && ./install_patch.sh"

# 또는 수동 확인
docker exec 43a7821ec235 python -v -c "print('test')" 2>&1 | grep sitecustomize
```

### LLM 서버 연결 실패

**원인:** LLM 서버가 실행되지 않거나 네트워크 문제

**해결:**
```bash
# LLM 서버 확인
curl http://172.21.137.193:11434/v1/models

# 도커 내부에서 확인
docker exec 43a7821ec235 curl http://172.21.137.193:11434/v1/models
```

---

## 🔄 재설치

패치를 재설치하려면:

```bash
docker exec -it 43a7821ec235 bash -c "cd /tmp/adk_web_force_patch && ./install_patch.sh"
```

기존 설정을 덮어씁니다.

---

## 📁 설치 위치

### 호스트 머신
- `/home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch/` - 이 패키지
  - `install_patch.sh` - 설치 스크립트
  - `patch_adk_builder_model.py` - 패치 파일
  - `README.md` - 문서

### 도커 컨테이너
- `/tmp/adk_web_force_patch/` - 복사된 패치 파일들
- `/root/adk_patch/` - 설치된 패치 파일
  - `patch_adk_builder_model.py`
  - `.env.example` (기본 설정 템플릿)
  - `.env` (실제 환경 변수 - 자동 생성됨)
- `/usr/lib/python3.10/sitecustomize.py` - 자동 로드

---

## 💡 사용 예시

### 기본 사용
```bash
# 1. 도커에 복사
docker cp /home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch 43a7821ec235:/tmp/

# 2. 설치
docker exec -it 43a7821ec235 bash -c "cd /tmp/adk_web_force_patch && chmod +x install_patch.sh && ./install_patch.sh"

# 3. 실행
docker exec -it 43a7821ec235 bash -c "source /root/.bashrc && cd /root/chainreaction && adk web . --host 0.0.0.0 --port 38010 --allow_origins='*' --reload --reload_agents"
```

### 다른 컨테이너에 설치
```bash
# 컨테이너 ID 확인
docker ps

# 복사 및 설치
docker cp /home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch <다른_컨테이너_ID>:/tmp/
docker exec -it <다른_컨테이너_ID> bash -c "cd /tmp/adk_web_force_patch && chmod +x install_patch.sh && ./install_patch.sh"
```

### 다른 LLM 서버 사용
```bash
# .env 파일 수정
docker exec -it 43a7821ec235 bash -c "cat > /root/adk_patch/.env << 'EOF'
model=gpt-4
api_base=https://api.openai.com/v1
api_key=sk-...
EOF"

# ADK 재시작
docker exec -it 43a7821ec235 bash -c "cd /root/chainreaction && adk web . --host 0.0.0.0 --port 38010 --allow_origins='*' --reload --reload_agents"
```

---

## 📞 지원

문제가 발생하면:
1. 트러블슈팅 섹션 확인
2. 패치 작동 확인 명령어 실행
3. 로그 확인

---

**버전:** 1.0
**최종 업데이트:** 2025-11-13
**호환 ADK 버전:** 1.18.0+
