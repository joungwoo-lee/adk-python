# ADK Agent Builder Assistant - Custom Model Patch

이 패치는 ADK Agent Builder Assistant가 사용하는 기본 LLM 모델(`gemini-2.5-pro`)을 커스텀 LiteLlm 모델로 교체합니다.

## 🎯 목적

`pip install --upgrade google-adk`로 설치된 환경에서 Agent Builder Assistant의 모델을 런타임에 교체하여 커스텀 LLM API를 사용할 수 있게 합니다.

## 📦 설치 환경

```bash
pip install --upgrade google-adk
```

## 🚀 사용 방법

### 방법 1: Python 스크립트에서 사용

```python
import os

# 환경 변수 설정 (패치 임포트 전에 설정해야 함)
os.environ["model"] = "your-model-name"
os.environ["api_base"] = "https://your-api-base.com/v1"
os.environ["api_key"] = "your-api-key"

# 패치 임포트 - 자동으로 적용됨
import patch_adk_builder_model

# 이제 Agent Builder Assistant를 사용하면 자동으로 커스텀 모델 사용
from google.adk.samples.adk_agent_builder_assistant import root_agent
```

### 방법 2: ADK Web UI에서 사용

```bash
# 환경 변수 설정
export model="your-model-name"
export api_base="https://your-api-base.com/v1"
export api_key="your-api-key"
export x-dep-ticket="your-ticket"
export Send-System-Name="Chain_Reaction"
export User-Id="joungwoo.lee"
export User-Type="AD_ID"

# Python 시작 시 패치 자동 로드하도록 설정
export PYTHONSTARTUP=/path/to/patch_adk_builder_model.py

# ADK Web 실행
adk web path/to/agents
```

### 방법 3: sitecustomize.py 사용 (전역 적용)

Python site-packages에 자동 로드되도록 설정:

```bash
# site-packages 위치 찾기
python -c "import site; print(site.getsitepackages()[0])"

# sitecustomize.py 생성 또는 수정
cat >> $(python -c "import site; print(site.getsitepackages()[0])")/sitecustomize.py << 'EOF'
import os
# 환경 변수가 설정되어 있으면 자동으로 패치 적용
if os.getenv("model") and os.getenv("api_base"):
    try:
        import patch_adk_builder_model
    except ImportError:
        pass
EOF
```

## 🔧 환경 변수 설정

### 필수 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `model` | LiteLlm 모델 이름 | `gpt-4`, `claude-3-opus` |
| `api_base` | API 베이스 URL | `https://api.openai.com/v1` |

### 선택적 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `api_key` | `"api_key"` | API 인증 키 |
| `x-dep-ticket` | `"api_key"` | 커스텀 헤더: DEP 티켓 |
| `Send-System-Name` | `"Chain_Reaction"` | 커스텀 헤더: 시스템 이름 |
| `User-Id` | `"joungwoo.lee"` | 커스텀 헤더: 사용자 ID |
| `User-Type` | `"AD_ID"` | 커스텀 헤더: 사용자 타입 |

## 📝 예시 스크립트

전체 예시는 `example_use_patch.py` 파일을 참조하세요:

```python
import os
import patch_adk_builder_model

from google.adk.samples.adk_agent_builder_assistant import root_agent

# root_agent는 이제 LiteLlm 모델을 사용합니다
```

## 🔍 동작 원리

1. **Monkey Patching**: `AgentBuilderAssistant.create_agent()` 메서드를 런타임에 교체
2. **환경 변수 기반**: 설정이 환경 변수에서 로드되므로 코드 수정 불필요
3. **자동 적용**: 모듈 임포트 시점에 자동으로 패치 적용

## ⚠️ 주의사항

1. **환경 변수 우선 설정**: 패치를 임포트하기 **전에** 환경 변수를 설정해야 합니다
2. **필수 변수 누락**: `model`, `api_base`가 설정되지 않으면 에러 발생
3. **설치 위치**: `google-adk`가 pip으로 설치되어 있어야 합니다

## 🐛 트러블슈팅

### "Failed to import AgentBuilderAssistant" 에러

```bash
# google-adk가 설치되어 있는지 확인
pip show google-adk

# 없으면 설치
pip install --upgrade google-adk
```

### "Environment variables 'model' and 'api_base' must be set" 에러

```bash
# 환경 변수 설정 확인
echo $model
echo $api_base

# 설정되지 않았으면 export
export model="your-model"
export api_base="https://your-api-base.com/v1"
```

### 패치가 적용되지 않는 경우

```python
# 패치 적용 상태 확인
import patch_adk_builder_model
print(patch_adk_builder_model._PATCH_APPLIED)

# True가 아니면 로그 확인
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📄 라이센스

Apache License 2.0 - 자세한 내용은 LICENSE 파일 참조

## 🤝 기여

버그 리포트나 개선 제안은 이슈로 등록해주세요.
