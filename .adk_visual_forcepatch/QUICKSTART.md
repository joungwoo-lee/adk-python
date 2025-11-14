# 🚀 Quick Start - ADK Custom LLM Patch

**3분 안에 설치하고 실행하기 (도커 내부 실행 방식)**

## 📋 필요한 것

- 실행 중인 ADK 도커 컨테이너
- 도커 컨테이너 접근 권한
- LLM API 서버 (기본: http://172.21.137.193:11434/v1)

## ⚡ 3단계 설치

### 1️⃣ 패치 파일을 도커에 복사 (10초)

```bash
# 호스트에서 실행
docker cp /home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch 43a7821ec235:/tmp/
```

### 2️⃣ 도커 안에서 설치 (30초)

```bash
# 도커 안에서 실행
docker exec -it 43a7821ec235 bash -c "cd /tmp/adk_web_force_patch && chmod +x install_patch.sh && ./install_patch.sh"
```

### 3️⃣ ADK 실행 (5초)

```bash
# 도커 안에서 실행
docker exec -it 43a7821ec235 bash -c "source /root/.bashrc && cd /root/chainreaction && adk web . --host 0.0.0.0 --port 38010 --allow_origins='*' --reload --reload_agents"
```

**끝!** 🎉

---

## 📱 브라우저에서 접속

```
http://localhost:38010
```

---

## 🔧 다른 컨테이너에 설치

```bash
# 컨테이너 ID 확인
docker ps

# 1. 패치 파일 복사
docker cp /home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch <컨테이너_ID>:/tmp/

# 2. 설치
docker exec -it <컨테이너_ID> bash -c "cd /tmp/adk_web_force_patch && chmod +x install_patch.sh && ./install_patch.sh"

# 3. 실행
docker exec -it <컨테이너_ID> bash -c "source /root/.bashrc && cd /root/chainreaction && adk web . --host 0.0.0.0 --port 38010 --allow_origins='*' --reload --reload_agents"
```

---

## 🛠️ 트러블슈팅

### 설치 실패?

```bash
# 도커 컨테이너 실행 확인
docker ps

# 재설치
docker exec -it <컨테이너_ID> bash -c "cd /tmp/adk_web_force_patch && ./install_patch.sh"
```

### 패치 확인

```bash
# 도커 안에서 .env 파일 확인
docker exec -it <컨테이너_ID> cat /root/adk_patch/.env
```

### 패치 테스트

```bash
# 도커 안에서 테스트 1: LLMRegistry (핵심!)
docker exec -it <컨테이너_ID> python -c "
from google.adk.models.registry import LLMRegistry
from google.adk.models.lite_llm import LiteLlm
model = LLMRegistry.new_llm('gemini-2.5-flash')
print('SUCCESS: LLMRegistry 패치 작동' if isinstance(model, LiteLlm) else 'FAILED')
"

# 도커 안에서 테스트 2: LlmAgent
docker exec -it <컨테이너_ID> python -c "
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
agent = LlmAgent(name='test', model='gemini-2.5-flash', instruction='test')
print('SUCCESS: LlmAgent 패치 작동' if isinstance(agent.model, LiteLlm) else 'FAILED')
"
```

---

## 📞 더 자세한 정보

- **전체 문서**: [README.md](README.md)
- **패키지 구조**: [INDEX.md](INDEX.md)
- **패치 코드**: `patch_adk_builder_model.py`

---

## 💡 한 줄 명령어

전체 과정을 한 번에:

```bash
docker cp /home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch 43a7821ec235:/tmp/ && \
docker exec -it 43a7821ec235 bash -c "cd /tmp/adk_web_force_patch && chmod +x install_patch.sh && ./install_patch.sh" && \
docker exec -it 43a7821ec235 bash -c "source /root/.bashrc && cd /root/chainreaction && adk web . --host 0.0.0.0 --port 38010 --allow_origins='*' --reload --reload_agents"
```

---

**설치 시간:** ~1분
**실행 시간:** 즉시

**총 소요 시간:** < 2분 🚀
