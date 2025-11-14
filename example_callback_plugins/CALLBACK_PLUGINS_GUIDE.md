# ADK 콜백 플러그인 시스템 - 완전 가이드

## 📋 문제 정의

ADK에서 YAML 설정 파일에 콜백을 사용할 때, 기본적으로 **전체 모듈 경로**를 써야 합니다:

```yaml
# 😫 기존 방식 - 너무 길다!
before_model_callbacks:
  - name: my_project.my_package.my_module.callbacks.logging.log_model_call
  - name: my_project.my_package.my_module.callbacks.security.validate_request
```

이것은:
- ❌ 경로가 너무 길어서 가독성이 떨어진다
- ❌ 오타가 나기 쉽다
- ❌ 콜백 위치를 변경하면 모든 YAML 수정 필요

## 💡 솔루션

**가상 모듈 시스템**을 사용하여 **짧은 이름**으로 콜백 사용:

```yaml
# 😊 새로운 방식 - 깔끔!
before_model_callbacks:
  - name: adk_callbacks.log_model_call
  - name: adk_callbacks.validate_request
```

마치 `google_search`처럼 내장 툴을 쓰듯이 콜백도 짧은 이름으로!

## 🎯 핵심 아이디어

### 1. 가상 모듈 생성

Python의 `sys.modules`를 활용하여 `adk_callbacks`라는 가상 모듈을 동적으로 생성:

```python
import sys
from types import ModuleType

# 가상 모듈 생성
virtual_module = ModuleType("adk_callbacks")
virtual_module.__file__ = "<virtual>"

# sys.modules에 등록
sys.modules["adk_callbacks"] = virtual_module
```

### 2. 콜백 함수 등록

사용자 정의 콜백 함수들을 가상 모듈의 속성으로 추가:

```python
# 콜백 함수를 가상 모듈에 추가
setattr(virtual_module, "log_model_call", log_model_call)
setattr(virtual_module, "validate_request", validate_request)
```

### 3. ADK 자동 인식

ADK의 `resolve_code_reference` 함수가 자동으로 인식:

```python
# ADK 내부 동작 (src/google/adk/agents/config_agent_utils.py)
module_path, obj_name = "adk_callbacks.log_model_call".rsplit(".", 1)
module = importlib.import_module(module_path)  # adk_callbacks 모듈 로드
obj = getattr(module, obj_name)  # log_model_call 함수 가져오기
```

## 📦 생성된 파일 구조

```
example_callback_plugins/        (총 811줄)
├── __init__.py                  # CALLBACK_REGISTRY 정의
├── register_callbacks.py        # 자동 등록 시스템 ⭐⭐⭐
│
├── logging_callbacks.py         # 로깅 콜백 예시
├── security_callbacks.py        # 보안 콜백 예시
├── state_callbacks.py           # 상태 관리 콜백 예시
│
├── example_usage.py             # 상세 사용 예시
├── test_registration.py         # 테스트 스크립트
│
├── example_agents/
│   └── callback_agent.yaml      # YAML 예시
│
└── README.md                    # 상세 문서
```

## 🚀 사용 방법 (2단계)

### 1단계: 콜백 등록 (Python 코드에서)

```python
# main.py 또는 agent.py 시작 부분
from example_callback_plugins import CALLBACK_REGISTRY
from example_callback_plugins.register_callbacks import register_callbacks

# 모든 콜백을 adk_callbacks 가상 모듈에 등록
register_callbacks(CALLBACK_REGISTRY)
```

### 2단계: YAML에서 짧은 이름 사용

```yaml
# my_agent.yaml
agent_class: LlmAgent
name: my_agent
model: gemini-2.5-flash
instruction: You are a helpful assistant.

tools:
  - name: google_search

# ✨ 짧은 이름으로 콜백 사용!
before_model_callbacks:
  - name: adk_callbacks.log_model_call
  - name: adk_callbacks.validate_model_request

after_model_callbacks:
  - name: adk_callbacks.save_model_info

before_tool_callbacks:
  - name: adk_callbacks.log_tool_call
  - name: adk_callbacks.check_tool_permissions

after_tool_callbacks:
  - name: adk_callbacks.track_tool_usage
```

## 🛠️ 제공되는 콜백 예시 (6개)

### 1️⃣ 로깅 콜백

**`log_model_call`** - LLM 호출 로깅
```python
async def log_model_call(callback_context, llm_request):
    print(f"🤖 MODEL CALL: {llm_request.model}")
    callback_context.state['model_call_count'] += 1
    return None
```

**`log_tool_call`** - 툴 호출 로깅
```python
def log_tool_call(tool, args, tool_context):
    print(f"🔧 TOOL CALL: {tool.name} with {args}")
    return None
```

### 2️⃣ 보안 콜백

**`check_tool_permissions`** - 툴 권한 검사
```python
def check_tool_permissions(tool, args, tool_context):
    permissions = tool_context.state.get("user_permissions", [])
    if tool.name in ["delete_file", "execute_code"]:
        if "admin" not in permissions:
            return {"error": "Permission denied"}
    return None
```

**`validate_model_request`** - 민감 정보 검증
```python
async def validate_model_request(callback_context, llm_request):
    # 비밀번호, API 키 등 민감 패턴 감지
    for message in llm_request.messages:
        # ... 검증 로직
    return None
```

### 3️⃣ 상태 관리 콜백

**`save_model_info`** - 모델 정보 저장
```python
async def save_model_info(callback_context, llm_response):
    callback_context.state["last_model"] = llm_response.model_version
    callback_context.state["response_count"] += 1
    return None
```

**`track_tool_usage`** - 툴 사용량 추적
```python
def track_tool_usage(tool, args, tool_context, tool_response):
    if "tool_usage" not in tool_context.state:
        tool_context.state["tool_usage"] = {}
    tool_context.state["tool_usage"][tool.name] = \
        tool_context.state["tool_usage"].get(tool.name, 0) + 1
    return None
```

## 🎨 자신만의 콜백 추가하기

### Step 1: 콜백 함수 파일 생성

```python
# my_custom_callbacks.py
from __future__ import annotations

async def monitor_response_time(callback_context, llm_request):
    """응답 시간 모니터링"""
    import time
    callback_context.state['request_start_time'] = time.time()
    return None

async def calculate_response_time(callback_context, llm_response):
    """응답 시간 계산"""
    import time
    if 'request_start_time' in callback_context.state:
        elapsed = time.time() - callback_context.state['request_start_time']
        print(f"⏱️  Response time: {elapsed:.2f}s")
    return None
```

### Step 2: CALLBACK_REGISTRY에 추가

```python
# __init__.py
from .my_custom_callbacks import monitor_response_time
from .my_custom_callbacks import calculate_response_time

CALLBACK_REGISTRY = {
    # ... 기존 콜백들 ...
    "monitor_response_time": monitor_response_time,
    "calculate_response_time": calculate_response_time,
}
```

### Step 3: YAML에서 사용

```yaml
before_model_callbacks:
  - name: adk_callbacks.monitor_response_time

after_model_callbacks:
  - name: adk_callbacks.calculate_response_time
```

## 🧪 테스트

### 빠른 테스트

```bash
cd /workspace
python -m example_callback_plugins.test_registration
```

**예상 출력:**
```
Testing callback registration system...
======================================================================

[1] Registering callbacks...
✓ Registered 6 callbacks

[2] Verifying virtual module 'adk_callbacks' exists...
✓ Virtual module 'adk_callbacks' is in sys.modules

[3] Testing imports from virtual module...
✓ Successfully imported:
  - log_model_call: log_model_call
  - check_tool_permissions: check_tool_permissions
  - save_model_info: save_model_info

[4] Testing importlib resolution (simulating ADK)...
  ✓ adk_callbacks.log_model_call
  ✓ adk_callbacks.log_tool_call
  ✓ adk_callbacks.check_tool_permissions
  ✓ adk_callbacks.validate_model_request
  ✓ adk_callbacks.save_model_info
  ✓ adk_callbacks.track_tool_usage

Test Summary
======================================================================
✓ Virtual module created: adk_callbacks
✓ Callbacks registered: 6
✓ Resolution successful: 6/6
```

### 상세 예시 실행

```bash
python -m example_callback_plugins.example_usage
```

## 💻 실전 사용 예시

### 예시 1: CLI 스크립트

```python
# run_my_agent.py
from example_callback_plugins import CALLBACK_REGISTRY
from example_callback_plugins.register_callbacks import register_callbacks

# 1. 콜백 등록
register_callbacks(CALLBACK_REGISTRY)

# 2. ADK CLI 실행
import subprocess
subprocess.run(["adk", "web", "./my_agents"])
```

### 예시 2: Python 코드에서 에이전트 실행

```python
# agent_runner.py
from google.adk import Agent, Runner
from example_callback_plugins import CALLBACK_REGISTRY
from example_callback_plugins.register_callbacks import register_callbacks

# 1. 콜백 등록
register_callbacks(CALLBACK_REGISTRY)

# 2. YAML에서 에이전트 로드
agent = Agent.from_config("my_agents/callback_agent.yaml")

# 3. 실행
runner = Runner(app=agent)
result = runner.run(
    user_id="user123",
    new_message="서울의 날씨를 알려줘"
)
```

### 예시 3: FastAPI 서버

```python
# server.py
from fastapi import FastAPI
from example_callback_plugins import CALLBACK_REGISTRY
from example_callback_plugins.register_callbacks import register_callbacks

# 앱 시작 시 콜백 등록
register_callbacks(CALLBACK_REGISTRY)

# ADK Web 서버 실행
from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(
    agents_dir="./agents",
    web=True
)
```

## 📊 비교: 기존 방식 vs 새로운 방식

### 기존 방식 (긴 경로)

```yaml
before_model_callbacks:
  - name: example_callback_plugins.logging_callbacks.log_model_call
  - name: example_callback_plugins.security_callbacks.validate_model_request
  - name: example_callback_plugins.security_callbacks.check_tool_permissions
  - name: example_callback_plugins.state_callbacks.save_model_info
  - name: example_callback_plugins.state_callbacks.track_tool_usage

# 문제점:
# ❌ 경로가 너무 길다 (50+ 문자)
# ❌ 오타 나기 쉽다
# ❌ 파일 구조 변경 시 모든 YAML 수정 필요
# ❌ 가독성이 매우 떨어진다
```

### 새로운 방식 (짧은 이름)

```yaml
before_model_callbacks:
  - name: adk_callbacks.log_model_call
  - name: adk_callbacks.validate_model_request
  - name: adk_callbacks.check_tool_permissions
  - name: adk_callbacks.save_model_info
  - name: adk_callbacks.track_tool_usage

# 장점:
# ✅ 짧고 깔끔하다 (30자 이내)
# ✅ 내장 기능처럼 보인다
# ✅ 관리가 쉽다
# ✅ 가독성이 우수하다
```

**라인 수 비교:**
- 기존: 평균 60-70자/줄
- 새로운: 평균 30-35자/줄
- **절반 이상 단축!**

## 🔧 고급 기능

### 1. 커스텀 가상 모듈 이름

```python
# 기본 이름: adk_callbacks
register_callbacks(CALLBACK_REGISTRY)

# 커스텀 이름 사용
register_callbacks(CALLBACK_REGISTRY, module_name="my_callbacks")

# YAML에서:
# before_model_callbacks:
#   - name: my_callbacks.log_model_call
```

### 2. 등록 상태 확인

```python
from example_callback_plugins.register_callbacks import verify_registration

status = verify_registration()
print(status)
# {
#   'log_model_call': True,
#   'check_tool_permissions': True,
#   'save_model_info': True,
#   ...
# }
```

### 3. 등록 해제

```python
from example_callback_plugins.register_callbacks import unregister_callbacks

unregister_callbacks()  # adk_callbacks 모듈 제거
```

### 4. 모듈 경로로 자동 등록

```python
from example_callback_plugins.register_callbacks import register_callbacks_from_module

# CALLBACK_REGISTRY를 자동으로 찾아서 등록
register_callbacks_from_module("example_callback_plugins")
```

## 🎓 콜백 타입별 시그니처

### Before Model Callback

```python
async def before_model_callback(
    callback_context: CallbackContext,
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """LLM 호출 전에 실행
    
    Returns:
        None: 정상 진행
        LlmResponse: LLM 호출 스킵하고 이 응답 사용
    """
    pass
```

### After Model Callback

```python
async def after_model_callback(
    callback_context: CallbackContext,
    llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """LLM 호출 후에 실행
    
    Returns:
        None: 원본 응답 사용
        LlmResponse: 수정된 응답 사용
    """
    pass
```

### Before Tool Callback

```python
def before_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext
) -> Optional[dict]:
    """툴 실행 전에 실행
    
    Returns:
        None: 정상 진행
        dict: 툴 실행 스킵하고 이 응답 사용
    """
    pass
```

### After Tool Callback

```python
def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict
) -> Optional[dict]:
    """툴 실행 후에 실행
    
    Returns:
        None: 원본 응답 사용
        dict: 수정된 응답 사용
    """
    pass
```

## ⚠️ 주의사항 및 Best Practices

### ✅ 해야 할 것

1. **등록 타이밍**: 에이전트 로드 **전에** 콜백 등록
2. **명확한 이름**: 콜백 이름은 동작을 명확히 설명
3. **타입 힌트**: 모든 매개변수에 타입 힌트 추가
4. **Docstring**: 콜백의 목적과 반환값 문서화
5. **가벼운 로직**: 콜백은 빠르게 실행되어야 함

### ❌ 하지 말아야 할 것

1. **이름 충돌**: 기존 Python 모듈과 이름 충돌 피하기
2. **무거운 작업**: 콜백에서 오래 걸리는 작업 지양
3. **에러 무시**: 콜백 에러는 적절히 처리
4. **상태 남용**: state를 과도하게 사용하지 않기

## 🎉 결론

이제 당신은:
- ✅ 콜백을 짧은 이름으로 사용할 수 있습니다
- ✅ 가상 모듈 시스템의 원리를 이해했습니다
- ✅ YAML 설정이 훨씬 깔끔해집니다
- ✅ 자신만의 콜백 플러그인을 만들 수 있습니다
- ✅ 마치 내장 기능처럼 콜백을 사용할 수 있습니다

**예:**
```yaml
# 이전
- name: my_very_long_project_name.callbacks.my_very_long_callback_name

# 이후
- name: adk_callbacks.my_callback
```

**50자 → 25자로 단축!** 🎊

**Happy Coding! 🚀**
