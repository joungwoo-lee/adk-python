# Local LLM Backend Configuration

이 문서는 ADK에서 환경변수를 통해 로컬 LLM 백엔드를 설정하는 방법을 설명합니다.

## 개요

ADK는 이제 환경변수를 통해 로컬 LLM 백엔드를 쉽게 설정할 수 있습니다. 이를 통해 Ollama, LocalAI, LM Studio 등의 로컬 LLM 서버를 사용할 수 있습니다.

## 지원되는 환경변수

### 1. `ADK_DEFAULT_MODEL`
기본 LLM 모델을 지정합니다. Agent를 생성할 때 `model` 파라미터를 생략하면 이 환경변수의 값이 사용됩니다.

```bash
export ADK_DEFAULT_MODEL="ollama/llama3"
```

### 2. `ADK_LLM_API_BASE`
LLM API의 베이스 URL을 지정합니다. 로컬 LLM 서버나 커스텀 엔드포인트를 사용할 때 유용합니다.

```bash
export ADK_LLM_API_BASE="http://localhost:11434"
```

### 3. `ADK_LLM_API_KEY`
API 인증을 위한 키를 지정합니다. (필요한 경우)

```bash
export ADK_LLM_API_KEY="your-api-key"
```

## 사용 예제

### 1. Ollama 사용하기

Ollama는 로컬에서 LLM을 실행할 수 있는 인기 있는 도구입니다.

#### 설치 및 실행

```bash
# Ollama 설치 (macOS/Linux)
curl https://ollama.ai/install.sh | sh

# 모델 다운로드 및 실행
ollama pull llama3
ollama serve  # 기본적으로 http://localhost:11434에서 실행됩니다
```

#### 환경변수 설정

```bash
export ADK_DEFAULT_MODEL="ollama/llama3"
export ADK_LLM_API_BASE="http://localhost:11434"
```

#### Python 코드 예제

```python
from google.adk import Agent, Runner

# 환경변수를 사용하는 경우 - model 파라미터 생략 가능
agent = Agent(
    name="local_assistant",
    instruction="You are a helpful assistant.",
)

# 또는 명시적으로 모델 지정
agent = Agent(
    name="local_assistant",
    model="ollama/llama3",
    instruction="You are a helpful assistant.",
)

# 실행
runner = Runner(agent=agent)
result = await runner.run("Hello, how are you?")
print(result)
```

### 2. LM Studio 사용하기

LM Studio는 GUI를 제공하는 로컬 LLM 실행 도구입니다.

#### 설정

1. LM Studio를 설치하고 실행합니다
2. "Local Server" 탭에서 서버를 시작합니다 (기본: http://localhost:1234)
3. 환경변수를 설정합니다:

```bash
export ADK_DEFAULT_MODEL="openai/local-model"  # LM Studio는 OpenAI 호환 API 제공
export ADK_LLM_API_BASE="http://localhost:1234/v1"
```

#### Python 코드 예제

```python
from google.adk import Agent, Runner

agent = Agent(
    name="lm_studio_assistant",
    model="openai/gpt-3.5-turbo",  # LM Studio에서 실행 중인 모델 이름
    instruction="You are a helpful assistant.",
)

runner = Runner(agent=agent)
result = await runner.run("Tell me a joke")
print(result)
```

### 3. OpenAI 호환 서버 사용하기

많은 로컬 LLM 서버들이 OpenAI 호환 API를 제공합니다.

```bash
export ADK_DEFAULT_MODEL="openai/your-model-name"
export ADK_LLM_API_BASE="http://your-server:port/v1"
export ADK_LLM_API_KEY="your-key-if-needed"  # 필요한 경우
```

```python
from google.adk import Agent, Runner

agent = Agent(
    name="custom_server_assistant",
    instruction="You are a helpful assistant.",
)

runner = Runner(agent=agent)
result = await runner.run("What is the capital of France?")
print(result)
```

## 지원되는 LiteLLM 프로바이더

ADK는 LiteLLM을 통해 다음과 같은 프로바이더를 지원합니다:

- `ollama/*` - Ollama 로컬 모델
- `openai/*` - OpenAI 또는 OpenAI 호환 엔드포인트
- `anthropic/*` - Anthropic Claude 모델
- `together_ai/*` - Together AI 모델
- `huggingface/*` - HuggingFace 모델
- `replicate/*` - Replicate 모델
- `bedrock/*` - AWS Bedrock 모델
- `azure/*` - Azure OpenAI 모델
- `cohere/*` - Cohere 모델
- `vertex_ai/*` - Vertex AI 모델

## 직접 LiteLlm 인스턴스 사용하기

환경변수 대신 코드에서 직접 설정할 수도 있습니다:

```python
from google.adk import Agent, Runner
from google.adk.models import LiteLlm

# LiteLlm 인스턴스 생성
llm = LiteLlm(
    model="ollama/llama3",
    api_base="http://localhost:11434",
    # 기타 LiteLLM 파라미터들...
    timeout=60,
    drop_params=True,  # 지원하지 않는 파라미터 자동 제거
)

# Agent에 전달
agent = Agent(
    name="custom_llm_agent",
    model=llm,
    instruction="You are a helpful assistant.",
)

runner = Runner(agent=agent)
result = await runner.run("Hello!")
print(result)
```

## 문제 해결

### 1. 연결 오류
```
ConnectionError: Failed to connect to http://localhost:11434
```

**해결 방법:**
- 로컬 LLM 서버가 실행 중인지 확인
- 포트 번호가 올바른지 확인
- 방화벽 설정 확인

### 2. 모델을 찾을 수 없음
```
ValueError: Model ollama/llama3 not found.
```

**해결 방법:**
- LiteLlm이 올바르게 등록되었는지 확인
- 모델 이름 패턴이 지원되는 형식인지 확인 (예: `ollama/`, `openai/` 등)

### 3. API 키 오류
```
AuthenticationError: Invalid API key
```

**해결 방법:**
- `ADK_LLM_API_KEY` 환경변수가 올바르게 설정되었는지 확인
- 또는 LiteLlm 생성 시 `api_key` 파라미터 전달

## 추가 정보

- LiteLLM 문서: https://docs.litellm.ai/
- Ollama 문서: https://ollama.ai/
- LM Studio: https://lmstudio.ai/

## 기여

버그 리포트나 기능 요청은 GitHub Issues에 올려주세요.
