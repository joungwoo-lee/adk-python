# ADK Agent Builder Assistant 패치 분석 및 수정 완료

## 🔍 문제 원인 분석

### 1. **잘못된 Import 경로**
- **문제**: 패치가 `google.adk.samples.adk_agent_builder_assistant`를 찾으려 시도
- **실제**: ADK 1.18.0에서는 `google.adk.built_in_agents.adk_agent_builder_assistant` 사용
- **결과**: ImportError로 인해 패치가 적용되지 않거나 잘못된 클래스 패치

### 2. **모델 이름 불일치**  
- **문제**: 패치가 `gemini-2.5-pro`만 감지
- **실제**: ADK 1.18.0의 기본 모델은 `gemini-2.5-flash`
- **결과**: 기본값으로 에이전트 생성 시 패치가 적용되지 않음

### 3. **StaticMethod 처리 오류**
- **문제**: `original_create_agent.__func__()` 호출
- **실제**: 일반 함수로 저장되어 `__func__` 속성이 없음
- **결과**: AttributeError 발생

## ✅ 수정 사항

### 1. Import 경로 수정 (Lines 111-138)

```python
# 수정 전
from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import AgentBuilderAssistant

# 수정 후 (다중 경로 지원)
try:
    # ADK 1.18.0+
    from google.adk.built_in_agents.adk_agent_builder_assistant.agent_builder_assistant import AgentBuilderAssistant
except ImportError:
    try:
        # 구 버전
        from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import AgentBuilderAssistant
    except ImportError:
        # 개발 환경
        from adk_agent_builder_assistant.agent_builder_assistant import AgentBuilderAssistant
```

### 2. 모델 감지 로직 확장 (Line 163)

```python
# 수정 전
if model is None or (isinstance(model, str) and "gemini-2.5-pro" in model):

# 수정 후 (모든 Gemini 모델 감지)
if model is None or (isinstance(model, str) and "gemini" in model.lower()):
```

**이제 감지하는 모델:**
- `gemini-2.5-pro`
- `gemini-2.5-flash` ✓ (기본값)
- `gemini-2.0-flash`
- `gemini-1.5-pro`
- 기타 모든 gemini 계열

### 3. StaticMethod 호출 수정 (Lines 183-192)

```python
# 수정 전
return original_create_agent.__func__(model=effective_model, ...)

# 수정 후 (안전한 호출)
if hasattr(original_create_agent, '__func__'):
    return original_create_agent.__func__(model=effective_model, ...)
else:
    return original_create_agent(model=effective_model, ...)
```

## 🎯 패치 동작 원리

### 실행 흐름

```
1. 환경 변수 설정
   model="openai/gpt-oss:20b"
   api_base="http://172.21.137.193:11434/v1"
   
2. patch_adk_builder_model 임포트
   ↓
3. AgentBuilderAssistant.create_agent 찾기
   - google.adk.built_in_agents 경로에서 성공 ✓
   
4. 원본 메서드 저장
   original_create_agent = AgentBuilderAssistant.create_agent
   
5. 커스텀 LiteLlm 모델 생성
   LiteLlm(
     model="openai/gpt-oss:20b",
     api_base="http://172.21.137.193:11434/v1",
     extra_headers={...}
   )
   
6. 래퍼 함수로 메서드 교체
   AgentBuilderAssistant.create_agent = patched_create_agent
   
7. 사용자가 create_agent() 호출
   ↓
8. patched_create_agent 실행
   - model 파라미터 확인: "gemini-2.5-flash" (기본값)
   - "gemini" 감지 ✓
   - effective_model = custom_model (LiteLlm 인스턴스)
   
9. 원본 함수 호출 (교체된 모델로)
   original_create_agent(model=LiteLlm(...))
   
10. 결과: 사내 LLM 서버를 사용하는 에이전트 생성 ✓
```

## 📊 테스트 결과

### 도커 환경 (ADK 1.18.0)

```bash
$ docker exec <container> python -c "..."

✓ ADK Agent Builder Assistant - Gemini → 커스텀 LiteLlm 모델로 패치 완료
  Model: openai/gpt-oss:20b
  API Base: http://172.21.137.193:11434/v1

=== VERIFICATION ===
✓ Agent name: agent_builder_assistant
✓ Model type: LiteLlm
✓ Is LiteLlm: True
✓ Model details: model='openai/gpt-oss:20b' ...

🎉 PATCH WORKING SUCCESSFULLY!
```

## 🚀 사용 방법

### 도커 환경에서 자동 적용

#### 방법 1: sitecustomize.py (권장)

```bash
# 도커 컨테이너 안에서
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")

cat > "$SITE_PACKAGES/sitecustomize.py" << 'PYTHON_EOF'
import os
if os.getenv("model") and os.getenv("api_base"):
    try:
        import sys
        sys.path.insert(0, "/root/ext_volume/mysandbox/adk-python/gemini_2.5_pro_override")
        import patch_adk_builder_model
    except Exception as e:
        print(f"Failed to load ADK patch: {e}")
PYTHON_EOF
```

#### 방법 2: 환경 변수 PYTHONPATH

```bash
# docker-compose.yml 또는 Dockerfile
ENV PYTHONPATH="/root/ext_volume/mysandbox/adk-python/gemini_2.5_pro_override:${PYTHONPATH}"
ENV model="openai/gpt-oss:20b"
ENV api_base="http://172.21.137.193:11434/v1"
```

#### 방법 3: Python 시작 스크립트

```python
# entrypoint.py 또는 main.py 맨 위에
import os
import sys

sys.path.insert(0, "/root/ext_volume/mysandbox/adk-python/gemini_2.5_pro_override")
import patch_adk_builder_model

# 나머지 코드...
from google.adk.cli import cli_tools_click
cli_tools_click.cli()
```

## 🔧 환경 변수

### 필수
- `model`: LiteLLM 모델 이름 (예: `openai/gpt-oss:20b`)
- `api_base`: API 엔드포인트 URL (예: `http://172.21.137.193:11434/v1`)

### 선택
- `api_key`: API 키 (기본값: `"api_key"`)
- `x-dep-ticket`: 커스텀 헤더
- `Send-System-Name`: 시스템 이름 (기본값: `"Chain_Reaction"`)
- `User-Id`: 사용자 ID (기본값: `"joungwoo.lee"`)
- `User-Type`: 사용자 타입 (기본값: `"AD_ID"`)

## 📁 수정된 파일

- `/home/joungwoolee/mysandbox/adk-python/gemini_2.5_pro_override/patch_adk_builder_model.py`
- `/home/joungwoolee/mysandbox/adk-python/forced_patch/patch_adk_builder_model.py`

## 🎉 결론

패치가 성공적으로 작동합니다!

- ✅ 모든 Gemini 모델 자동 감지
- ✅ ADK 1.18.0+ 지원
- ✅ 구 버전 호환성 유지
- ✅ 개발 환경 지원
- ✅ 도커 환경에서 테스트 완료

사내 LLM 서버(`http://172.21.137.193:11434/v1`)를 사용하여
ADK Agent Builder Assistant를 실행할 수 있습니다.
