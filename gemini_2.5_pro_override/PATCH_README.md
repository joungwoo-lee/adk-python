# ADK Agent Builder Assistant - Gemini 2.5 Pro 모델 오버라이드 패치

이 패치는 ADK Agent Builder Assistant가 사용하는 기본 LLM 모델(`gemini-2.5-pro`)을 사용자가 제공한 커스텀 LiteLlm 모델로 자동 교체합니다.

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
os.environ["x-dep-ticket"] = "your-ticket"
os.environ["Send-System-Name"] = "Chain_Reaction"
os.environ["User-Id"] = "joungwoo.lee"
os.environ["User-Type"] = "AD_ID"

# 패치 임포트 - 자동으로 적용됨
import patch_adk_builder_model

# 이제 Agent Builder Assistant를 사용하면 자동으로 커스텀 모델 사용
from google.adk.samples.adk_agent_builder_assistant import root_agent

# 또는 직접 에이전트 생성
from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import (
    AgentBuilderAssistant,
)

agent = AgentBuilderAssistant.create_agent()
print(f"Agent: {agent.name}")
print(f"Model: {agent.model}")
```

### 방법 2: ADK Web UI에서 사용

터미널에서 환경 변수를 설정하고 패치를 자동 로드하도록 설정:

```bash
# 환경 변수 설정
export model="your-model-name"
export api_base="https://your-api-base.com/v1"
export api_key="your-api-key"
export x-dep-ticket="your-ticket"
export Send-System-Name="Chain_Reaction"
export User-Id="joungwoo.lee"
export User-Type="AD_ID"

# 제공된 setup 스크립트 사용 (권장)
./setup_patched_adk_web.sh path/to/agents
```

### 방법 3: sitecustomize.py 사용 (전역 자동 적용)

Python site-packages에 자동 로드되도록 설정하여 모든 Python 실행 시 패치 적용:

```bash
# site-packages 위치 찾기
python -c "import site; print(site.getsitepackages()[0])"

# sitecustomize.py에 패치 추가
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")
cat >> "$SITE_PACKAGES/sitecustomize.py" << 'EOF'

# ADK Agent Builder Assistant 모델 패치 자동 로드
import os
if os.getenv("model") and os.getenv("api_base"):
    try:
        import sys
        from pathlib import Path
        
        # 패치 파일이 있는 디렉토리를 sys.path에 추가
        patch_dir = Path("/workspace/gemini_2.5_pro_override")
        if patch_dir.exists() and str(patch_dir) not in sys.path:
            sys.path.insert(0, str(patch_dir))
        
        import patch_adk_builder_model
    except ImportError:
        pass
EOF

# 이제 일반적인 방법으로 ADK Web 실행
export model="your-model-name"
export api_base="https://your-api-base.com/v1"
adk web path/to/agents
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

## 📝 커스텀 모델 코드

패치에서 사용되는 커스텀 LiteLlm 모델 설정:

```python
from google.adk.models.lite_llm import LiteLlm
import os

MODEL = LiteLlm(
    model=os.getenv("model"),
    api_base=os.getenv("api_base"),
    api_key=os.getenv("api_key", "api_key"),
    extra_headers={
        "x-dep-ticket": os.getenv("x-dep-ticket", "api_key"),
        "Send-System-Name": os.getenv("Send-System-Name", "Chain_Reaction"),
        "User-Id": os.getenv("User-Id", "joungwoo.lee"),
        "User-Type": os.getenv("User-Type", "AD_ID"),
    },
)
```

## 📋 예시 스크립트

전체 예시는 `example_use_patch.py` 파일을 참조하세요.

## 🔍 동작 원리

1. **Monkey Patching**: `AgentBuilderAssistant.create_agent()` 메서드를 런타임에 교체
2. **자동 감지**: `gemini-2.5-pro` 모델이 요청되면 자동으로 커스텀 LiteLlm으로 교체
3. **환경 변수 기반**: 설정이 환경 변수에서 로드되므로 코드 수정 불필요
4. **자동 적용**: 모듈 임포트 시점에 자동으로 패치 적용

## 📂 파일 구조

```
gemini_2.5_pro_override/
├── patch_adk_builder_model.py   # 메인 패치 파일
├── PATCH_README.md              # 이 파일 (한국어 설명서)
├── example_use_patch.py         # 사용 예시 스크립트
├── setup_patched_adk_web.sh     # ADK Web 실행 헬퍼 스크립트
└── test_patch.py                # 패치 동작 테스트 스크립트
```

## ⚠️ 주의사항

1. **환경 변수 우선 설정**: 패치를 임포트하기 **전에** 환경 변수를 설정해야 합니다
2. **필수 변수 누락**: `model`, `api_base`가 설정되지 않으면 에러 발생
3. **설치 위치**: `google-adk`가 pip으로 설치되어 있어야 합니다
4. **다른 모델 사용**: `gemini-2.5-pro`가 아닌 다른 모델을 명시적으로 지정하면 패치가 적용되지 않습니다

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
import sys
sys.path.insert(0, "/workspace/gemini_2.5_pro_override")

import patch_adk_builder_model
print(f"패치 적용 상태: {patch_adk_builder_model._PATCH_APPLIED}")

# False가 출력되면 로그 확인
import logging
logging.basicConfig(level=logging.DEBUG)
```

### ADK Web에서 패치가 적용되지 않는 경우

제공된 `setup_patched_adk_web.sh` 스크립트를 사용하세요:

```bash
./setup_patched_adk_web.sh path/to/agents
```

## 🧪 패치 테스트

패치가 올바르게 동작하는지 테스트:

```bash
# 환경 변수 설정
export model="test-model"
export api_base="https://test-api.example.com/v1"
export api_key="test-key"

# 테스트 실행
cd gemini_2.5_pro_override
python test_patch.py
```

## 📄 라이센스

Apache License 2.0 - 자세한 내용은 LICENSE 파일 참조

## 🤝 기여

버그 리포트나 개선 제안은 이슈로 등록해주세요.

---

## 💡 추가 팁

### VS Code에서 사용하기

VS Code의 Python 설정에서 환경 변수를 설정:

```json
// .vscode/settings.json
{
  "terminal.integrated.env.linux": {
    "model": "your-model-name",
    "api_base": "https://your-api-base.com/v1",
    "api_key": "your-api-key",
    "PYTHONPATH": "${workspaceFolder}/gemini_2.5_pro_override:${env:PYTHONPATH}"
  }
}
```

### Docker 환경에서 사용하기

Dockerfile에 환경 변수 추가:

```dockerfile
ENV model="your-model-name"
ENV api_base="https://your-api-base.com/v1"
ENV api_key="your-api-key"

# 패치 파일 복사
COPY gemini_2.5_pro_override /app/gemini_2.5_pro_override
ENV PYTHONPATH="/app/gemini_2.5_pro_override:${PYTHONPATH}"
```
