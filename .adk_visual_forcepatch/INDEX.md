# 📦 ADK Custom LLM Patch - 설치 패키지

**Google ADK의 Gemini 모델을 커스텀 LiteLLM으로 자동 교체 (도커 내부 실행 방식)**

---

## 🚀 빠른 시작

```bash
# 1. 도커에 복사
docker cp /home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch 43a7821ec235:/tmp/

# 2. 도커 안에서 설치
docker exec -it 43a7821ec235 bash -c "cd /tmp/adk_web_force_patch && chmod +x install_patch.sh && ./install_patch.sh"
```

**상세 가이드**: [QUICKSTART.md](QUICKSTART.md)

---

## 📁 패키지 내용

### 실행 파일

| 파일 | 설명 |
|------|------|
| `install_patch.sh` | 🔧 패치 자동 설치 스크립트 (도커 내부 실행) |
| `patch_adk_builder_model.py` | 🐍 Python 패치 파일 |

### 문서

| 파일 | 설명 |
|------|------|
| `QUICKSTART.md` | ⚡ 빠른 시작 가이드 (3분) |
| `README.md` | 📖 전체 문서 |
| `INDEX.md` | 📋 이 파일 |

---

## 📖 문서 가이드

### 처음 사용하는 경우
👉 [QUICKSTART.md](QUICKSTART.md) - 3분 안에 설치하고 실행

### 상세 정보가 필요한 경우
👉 [README.md](README.md) - 전체 문서, 트러블슈팅, 고급 설정

---

## ⚡ 사용 방법

### 1. 도커에 복사
```bash
docker cp /home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch <컨테이너_ID>:/tmp/
```

### 2. 도커 안에서 설치
```bash
docker exec -it <컨테이너_ID> bash -c "cd /tmp/adk_web_force_patch && chmod +x install_patch.sh && ./install_patch.sh"
```

### 3. 실행
```bash
docker exec -it <컨테이너_ID> bash -c "source /root/.bashrc && cd /root/chainreaction && adk web . --host 0.0.0.0 --port 38010 --allow_origins='*' --reload --reload_agents"
```

---

## 🎯 주요 기능

✅ **Agent Builder Assistant 패치**
- ADK Web UI의 빌트인 어시스턴트 자동 교체

✅ **LlmAgent 패치**
- 프로그래밍 방식으로 생성되는 에이전트 자동 교체

✅ **LLMRegistry 패치** ⭐ 가장 중요!
- YAML 파일의 `model: gemini-*`가 실제 모델 인스턴스로 변환되는 시점 가로채기
- 생성된 에이전트와 모든 서브에이전트의 gemini 모델 요청 처리

✅ **자동 로드**
- Python 시작 시 자동으로 패치 적용

✅ **환경 변수 기반**
- 코드 수정 없이 설정 변경 가능

---

## 🔧 지원 환경

- **ADK 버전**: 1.18.0+
- **Python 버전**: 3.10+
- **플랫폼**: 도커 컨테이너

---

## 📊 설치 결과

### 도커 컨테이너에 생성되는 파일:

```
/root/adk_patch/
└── patch_adk_builder_model.py

/usr/lib/python3.10/
└── sitecustomize.py

/root/
└── .bashrc (환경 변수)
```

---

## 💡 한 줄 설치 & 실행

```bash
docker cp /home/joungwoolee/mysandbox/jw-sandbox/sandbox/adk_web_force_patch 43a7821ec235:/tmp/ && docker exec -it 43a7821ec235 bash -c "cd /tmp/adk_web_force_patch && chmod +x install_patch.sh && ./install_patch.sh"
```

---

## 📞 트러블슈팅

문제 발생 시:
1. [QUICKSTART.md](QUICKSTART.md) - 빠른 해결
2. [README.md](README.md) - 상세 트러블슈팅
3. 패치 테스트 실행하여 진단

---

## 🔄 업데이트

패치 재설치:
```bash
docker exec -it <컨테이너_ID> bash -c "cd /tmp/adk_web_force_patch && ./install_patch.sh"
```

---

**버전**: 1.0
**최종 업데이트**: 2025-11-13
**라이센스**: Apache 2.0
