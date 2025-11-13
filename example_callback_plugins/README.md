# 콜백 플러그인 시스템 - 짧은 이름으로 콜백 사용하기

## 📋 개요

ADK에서 YAML 설정 파일에 콜백을 사용할 때, 기본적으로 전체 모듈 경로를 써야 합니다:

```yaml
# 기존 방식 - 긴 경로
before_model_callbacks:
  - name: my_project.my_package.callbacks.logging_callbacks.log_model_call
```

이 시스템을 사용하면 **짧은 이름**으로 콜백을 사용할 수 있습니다:

```yaml
# 새로운 방식 - 짧은 이름!
before_model_callbacks:
  - name: adk_callbacks.log_model_call
```

## 🎯 동작 원리

1. **가상 모듈 생성**: `adk_callbacks`라는 가상 Python 모듈을 만듭니다
2. **콜백 등록**: 사용자 정의 콜백 함수들을 가상 모듈에 등록합니다
3. **sys.modules 활용**: Python의 `sys.modules`에 가상 모듈을 추가합니다
4. **ADK 호환**: ADK의 `resolve_code_reference`가 자동으로 인식합니다

## 📁 폴더 구조

```
example_callback_plugins/
├── __init__.py                  # CALLBACK_REGISTRY 정의
├── register_callbacks.py        # 자동 등록 시스템 ⭐
│
├── logging_callbacks.py         # 로깅 콜백들
├── security_callbacks.py        # 보안 콜백들
├── state_callbacks.py           # 상태 관리 콜백들
│
├── example_usage.py             # 사용 예시
├── test_registration.py         # 테스트 스크립트
│
├── example_agents/
│   └── callback_agent.yaml      # YAML 예시
│
└── README.md                    # 이 파일
```

## 🚀 빠른 시작 (2단계)

### 1️⃣ 콜백 등록

Python 스크립트나 에이전트 코드 시작 부분에 추가:

```python
from example_callback_plugins import CALLBACK_REGISTRY
from example_callback_plugins.register_callbacks import register_callbacks

# 모든 콜백을 가상 모듈에 등록
register_callbacks(CALLBACK_REGISTRY)
```

### 2️⃣ YAML에서 짧은 이름으로 사용

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

## 📝 제공되는 콜백 예시

### 1. 로깅 콜백 (logging_callbacks.py)

```python
# LLM 호출 로깅
async def log_model_call(callback_context, llm_request):
    """모델 호출 시 로그 출력"""
    print(f"🤖 MODEL CALL: {llm_request.model}")
    return None

# 툴 호출 로깅
def log_tool_call(tool, args, tool_context):
    """툴 호출 시 로그 출력"""
    print(f"🔧 TOOL CALL: {tool.name}")
    return None
```

**YAML 사용:**
```yaml
before_model_callbacks:
  - name: adk_callbacks.log_model_call
before_tool_callbacks:
  - name: adk_callbacks.log_tool_call
```

### 2. 보안 콜백 (security_callbacks.py)

```python
# 툴 권한 검사
def check_tool_permissions(tool, args, tool_context):
    """사용자 권한 확인"""
    permissions = tool_context.state.get("user_permissions", [])
    restricted_tools = {
        "delete_file": "admin",
        "execute_code": "developer",
    }
    
    required = restricted_tools.get(tool.name)
    if required and required not in permissions:
        return {"error": "Permission denied"}
    return None

# 모델 요청 검증
async def validate_model_request(callback_context, llm_request):
    """민감 정보 패턴 체크"""
    sensitive_patterns = ["password", "api_key", "secret"]
    # ... 검증 로직
    return None
```

**YAML 사용:**
```yaml
before_tool_callbacks:
  - name: adk_callbacks.check_tool_permissions
before_model_callbacks:
  - name: adk_callbacks.validate_model_request
```

### 3. 상태 관리 콜백 (state_callbacks.py)

```python
# 모델 정보 저장
async def save_model_info(callback_context, llm_response):
    """응답 정보를 state에 저장"""
    callback_context.state["last_model"] = llm_response.model_version
    callback_context.state["response_count"] = \
        callback_context.state.get("response_count", 0) + 1
    return None

# 툴 사용량 추적
def track_tool_usage(tool, args, tool_context, tool_response):
    """툴 사용 통계 기록"""
    if "tool_usage" not in tool_context.state:
        tool_context.state["tool_usage"] = {}
    
    tool_usage = tool_context.state["tool_usage"]
    if tool.name not in tool_usage:
        tool_usage[tool.name] = {"count": 0}
    
    tool_usage[tool.name]["count"] += 1
    return None
```

**YAML 사용:**
```yaml
after_model_callbacks:
  - name: adk_callbacks.save_model_info
after_tool_callbacks:
  - name: adk_callbacks.track_tool_usage
```

## 🎨 자신만의 콜백 추가하기

### Step 1: 콜백 함수 작성

```python
# my_callbacks.py
async def my_custom_callback(callback_context, llm_request):
    """내 커스텀 콜백"""
    print("My custom callback executed!")
    # state 접근 가능
    callback_context.state['my_data'] = 'value'
    return None
```

### Step 2: CALLBACK_REGISTRY에 추가

```python
# __init__.py
from .my_callbacks import my_custom_callback

CALLBACK_REGISTRY = {
    # ... 기존 콜백들 ...
    "my_custom_callback": my_custom_callback,  # 추가!
}
```

### Step 3: YAML에서 사용

```yaml
before_model_callbacks:
  - name: adk_callbacks.my_custom_callback
```

## 🧪 테스트 방법

### 방법 1: 테스트 스크립트 실행

```bash
python -m example_callback_plugins.test_registration
```

### 방법 2: 예시 스크립트 실행

```bash
python -m example_callback_plugins.example_usage
```

### 방법 3: 직접 테스트

```python
from example_callback_plugins import CALLBACK_REGISTRY
from example_callback_plugins.register_callbacks import register_callbacks

# 등록
register_callbacks(CALLBACK_REGISTRY)

# 테스트: 가상 모듈에서 임포트
from adk_callbacks import log_model_call, check_tool_permissions

print(log_model_call)  # <function log_model_call at 0x...>
print(check_tool_permissions)  # <function check_tool_permissions at 0x...>
```

## 💡 실전 사용 시나리오

### 시나리오 1: CLI 스크립트

```python
# run_agent.py
from example_callback_plugins import CALLBACK_REGISTRY
from example_callback_plugins.register_callbacks import register_callbacks

# 콜백 등록
register_callbacks(CALLBACK_REGISTRY)

# ADK CLI 실행
import subprocess
subprocess.run(["adk", "web", "./agents"])
```

### 시나리오 2: Python 에이전트

```python
# my_agent.py
from google.adk import Agent, Runner
from example_callback_plugins import CALLBACK_REGISTRY
from example_callback_plugins.register_callbacks import register_callbacks

# 1. 콜백 등록
register_callbacks(CALLBACK_REGISTRY)

# 2. YAML에서 에이전트 로드
agent = Agent.from_config("callback_agent.yaml")

# 3. 실행
runner = Runner(app=agent)
result = runner.run(user_id="user123", new_message="Hello")
```

### 시나리오 3: FastAPI 서버

```python
# server.py
from fastapi import FastAPI
from example_callback_plugins import CALLBACK_REGISTRY
from example_callback_plugins.register_callbacks import register_callbacks

# 앱 시작 시 콜백 등록
register_callbacks(CALLBACK_REGISTRY)

# ADK FastAPI 앱
from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(agents_dir="./agents", web=True)
```

## 📊 기존 방식 vs 새로운 방식

### 기존 방식 (긴 경로)

```yaml
before_model_callbacks:
  - name: example_callback_plugins.logging_callbacks.log_model_call
  - name: example_callback_plugins.security_callbacks.validate_model_request
  - name: example_callback_plugins.state_callbacks.save_model_info

# 문제점:
# ❌ 경로가 너무 길다
# ❌ 오타 나기 쉽다
# ❌ 가독성이 떨어진다
```

### 새로운 방식 (짧은 이름)

```yaml
before_model_callbacks:
  - name: adk_callbacks.log_model_call
  - name: adk_callbacks.validate_model_request
  - name: adk_callbacks.save_model_info

# 장점:
# ✅ 짧고 깔끔하다
# ✅ 내장 콜백처럼 보인다
# ✅ 관리하기 쉽다
```

## 🔧 고급 기능

### 1. 커스텀 가상 모듈 이름

```python
# 기본: adk_callbacks
register_callbacks(CALLBACK_REGISTRY)

# 커스텀 이름 사용
register_callbacks(CALLBACK_REGISTRY, module_name="my_callbacks")

# YAML에서:
# before_model_callbacks:
#   - name: my_callbacks.log_model_call
```

### 2. 등록 확인

```python
from example_callback_plugins.register_callbacks import verify_registration

status = verify_registration()
print(status)
# {'log_model_call': True, 'check_tool_permissions': True, ...}
```

### 3. 등록 해제

```python
from example_callback_plugins.register_callbacks import unregister_callbacks

unregister_callbacks()
```

## ⚠️ 주의사항

1. **등록 타이밍**: 에이전트 로드 전에 콜백을 등록해야 합니다
2. **이름 충돌**: 가상 모듈 이름이 기존 모듈과 겹치지 않도록 주의
3. **타입 힌트**: 콜백 함수에 명확한 타입 힌트와 docstring 작성
4. **부작용 최소화**: 콜백은 가볍고 빠르게 실행되어야 합니다

## 🎓 콜백 시그니처 참고

```python
# Before Model Callback
async def before_model_callback(
    callback_context: CallbackContext,
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    pass

# After Model Callback
async def after_model_callback(
    callback_context: CallbackContext,
    llm_response: LlmResponse
) -> Optional[LlmResponse]:
    pass

# Before Tool Callback
def before_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext
) -> Optional[dict]:
    pass

# After Tool Callback
def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict
) -> Optional[dict]:
    pass
```

## 🎉 결론

이제 당신은:
- ✅ 콜백을 짧은 이름으로 사용할 수 있습니다
- ✅ 가상 모듈 시스템을 이해했습니다
- ✅ 자신만의 콜백 플러그인을 만들 수 있습니다
- ✅ YAML 설정이 훨씬 깔끔해집니다

**Happy Coding! 🚀**
