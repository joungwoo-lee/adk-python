# Custom Tools for ADK - 사용자 정의 툴 자동 등록 시스템

이 폴더는 `pip install google-adk`로 설치된 라이브러리 환경에서 사용자가 정의한 커스텀 툴을 ADK의 내장 툴로 자동 등록하여 YAML 설정에서 바로 사용할 수 있게 해주는 시스템입니다.

## 📁 폴더 구조

```
example_custom_tools/
├── __init__.py              # 툴 목록 정의 (CUSTOM_TOOLS)
├── register_tools.py        # 자동 등록 시스템
├── weather_tool.py          # 예시 1: 날씨 툴
├── calculator_tool.py       # 예시 2: 계산기 툴
├── text_tool.py             # 예시 3: 텍스트 처리 툴
├── example_usage.py         # 사용 예시 스크립트
├── test_registration.py     # 테스트 스크립트
└── README.md                # 이 파일
```

## 🚀 빠른 시작

### 1단계: 커스텀 툴 등록

Python 스크립트나 에이전트 코드 시작 부분에 다음을 추가하세요:

```python
# 커스텀 툴 자동 등록
from example_custom_tools import CUSTOM_TOOLS
from example_custom_tools.register_tools import register_custom_tools

# 모든 커스텀 툴을 내장 툴로 등록
register_custom_tools(CUSTOM_TOOLS)
```

### 2단계: YAML 설정에서 사용

이제 커스텀 툴을 내장 툴처럼 YAML에서 바로 사용할 수 있습니다:

```yaml
# my_agent.yaml
agent_class: LlmAgent
name: my_assistant
model: gemini-2.5-flash
instruction: |
  You are a helpful assistant with weather, calculator, and text tools.

tools:
  # ADK 기본 내장 툴
  - name: google_search
  
  # 사용자 정의 커스텀 툴 - 이제 내장 툴처럼 사용!
  - name: get_weather
  - name: get_forecast
  - name: calculate
  - name: convert_units
  - name: count_words
  - name: reverse_text
```

### 3단계: ADK Web UI에서 테스트

```bash
# 에이전트 실행
adk web /path/to/agents

# 또는 CLI로 실행
adk run /path/to/my_agent
```

## 📚 제공되는 예시 툴

### 날씨 툴 (weather_tool.py)

- `get_weather(location, unit)`: 현재 날씨 조회
- `get_forecast(location, days)`: 일기예보 조회

```yaml
tools:
  - name: get_weather
  - name: get_forecast
```

### 계산기 툴 (calculator_tool.py)

- `calculate(expression)`: 수식 계산
- `convert_units(value, from_unit, to_unit)`: 단위 변환

```yaml
tools:
  - name: calculate
  - name: convert_units
```

### 텍스트 처리 툴 (text_tool.py)

- `count_words(text)`: 단어 수 세기
- `reverse_text(text)`: 텍스트 뒤집기
- `to_uppercase(text)`: 대문자 변환
- `to_lowercase(text)`: 소문자 변환

```yaml
tools:
  - name: count_words
  - name: reverse_text
  - name: to_uppercase
```

## 🛠️ 자신만의 커스텀 툴 만들기

### 1단계: 새 툴 파일 생성

```python
# my_custom_tool.py
from __future__ import annotations

def my_awesome_tool(param1: str, param2: int = 10) -> str:
    """My awesome tool that does something amazing.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (default: 10)
    
    Returns:
        Result description
    """
    return f"Processed {param1} with {param2}"
```

### 2단계: __init__.py에 추가

```python
# __init__.py
from .my_custom_tool import my_awesome_tool

CUSTOM_TOOLS = [
    # ... 기존 툴들 ...
    my_awesome_tool,  # 새 툴 추가
]

__all__ = [
    # ... 기존 exports ...
    "my_awesome_tool",
]
```

### 3단계: 등록 및 사용

```python
# 등록
from example_custom_tools import CUSTOM_TOOLS
from example_custom_tools.register_tools import register_custom_tools

register_custom_tools(CUSTOM_TOOLS)

# YAML에서 사용
# tools:
#   - name: my_awesome_tool
```

## 🧪 테스트 방법

### 방법 1: 테스트 스크립트 실행

```bash
python -m example_custom_tools.test_registration
```

### 방법 2: 예시 사용 스크립트 실행

```bash
python -m example_custom_tools.example_usage
```

### 방법 3: 직접 테스트

```python
from example_custom_tools import CUSTOM_TOOLS
from example_custom_tools.register_tools import register_custom_tools

# 등록
register_custom_tools(CUSTOM_TOOLS)

# 테스트
from google.adk.tools import get_weather, calculate

print(get_weather("Seoul", "celsius"))
print(calculate("2 + 2 * 5"))
```

## 💡 고급 사용법

### 등록 확인

```python
from example_custom_tools.register_tools import verify_registration

status = verify_registration()
print(status)
# {'get_weather': True, 'calculate': True, ...}
```

### 모듈 경로로 등록

```python
from example_custom_tools.register_tools import register_custom_tools_from_module

# 모듈 경로를 지정하여 자동 등록
register_custom_tools_from_module("example_custom_tools")
```

## 📝 주요 특징

- ✅ **간편한 등록**: 단 2줄의 코드로 커스텀 툴 등록
- ✅ **YAML 호환**: 내장 툴과 동일하게 YAML에서 이름으로 참조
- ✅ **타입 안전**: 함수 시그니처와 docstring 활용
- ✅ **검증 가능**: 등록 상태 확인 기능 제공
- ✅ **확장 가능**: 무제한으로 툴 추가 가능

## ⚠️ 주의사항

1. **등록 타이밍**: 커스텀 툴은 ADK 에이전트를 사용하기 전에 등록해야 합니다.
2. **이름 충돌**: 기존 ADK 내장 툴과 이름이 겹치지 않도록 주의하세요.
3. **타입 힌트**: 툴 함수에는 명확한 타입 힌트와 docstring을 작성하세요.
4. **pure function**: 부작용이 없는 순수 함수로 작성하는 것을 권장합니다.

## 🔧 실전 예시: 에이전트와 함께 사용

```python
# main.py
from google.adk import Agent, Runner
from example_custom_tools import CUSTOM_TOOLS
from example_custom_tools.register_tools import register_custom_tools

# 1. 커스텀 툴 등록
register_custom_tools(CUSTOM_TOOLS)

# 2. YAML에서 에이전트 로드 또는 직접 생성
agent = Agent.from_config("my_agent.yaml")

# 3. 실행
runner = Runner(app=agent)
result = runner.run(
    user_id="user123",
    new_message="서울의 날씨를 알려주고, 2 + 3 * 4를 계산해줘"
)
```

## 📖 추가 리소스

- [ADK 공식 문서](https://google.github.io/adk-docs)
- [ADK GitHub 저장소](https://github.com/google/adk-python)
- [Tool 개발 가이드](https://google.github.io/adk-docs/tools)

## 🤝 기여

이 예시를 개선하고 싶으시다면 Pull Request를 보내주세요!
