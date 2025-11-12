# Local LLM Backend Configuration

This document explains how to configure local LLM backends in ADK using environment variables.

## Overview

ADK now supports easy configuration of local LLM backends through environment variables. This allows you to use local LLM servers like Ollama, LocalAI, LM Studio, and more.

## Supported Environment Variables

### 1. `ADK_DEFAULT_MODEL`
Specifies the default LLM model. When creating an Agent without the `model` parameter, this environment variable will be used.

```bash
export ADK_DEFAULT_MODEL="ollama/llama3"
```

### 2. `ADK_LLM_API_BASE`
Specifies the base URL for the LLM API. Useful when using local LLM servers or custom endpoints.

```bash
export ADK_LLM_API_BASE="http://localhost:11434"
```

### 3. `ADK_LLM_API_KEY`
Specifies the API key for authentication (if required).

```bash
export ADK_LLM_API_KEY="your-api-key"
```

## Usage Examples

### 1. Using Ollama

Ollama is a popular tool for running LLMs locally.

#### Installation and Setup

```bash
# Install Ollama (macOS/Linux)
curl https://ollama.ai/install.sh | sh

# Download and run a model
ollama pull llama3
ollama serve  # Runs on http://localhost:11434 by default
```

#### Environment Variable Configuration

```bash
export ADK_DEFAULT_MODEL="ollama/llama3"
export ADK_LLM_API_BASE="http://localhost:11434"
```

#### Python Code Example

```python
from google.adk import Agent, Runner

# Using environment variables - model parameter can be omitted
agent = Agent(
    name="local_assistant",
    instruction="You are a helpful assistant.",
)

# Or explicitly specify the model
agent = Agent(
    name="local_assistant",
    model="ollama/llama3",
    instruction="You are a helpful assistant.",
)

# Run
runner = Runner(agent=agent)
result = await runner.run("Hello, how are you?")
print(result)
```

### 2. Using LM Studio

LM Studio is a local LLM runtime with a GUI.

#### Setup

1. Install and launch LM Studio
2. Start the server in the "Local Server" tab (default: http://localhost:1234)
3. Set environment variables:

```bash
export ADK_DEFAULT_MODEL="openai/local-model"  # LM Studio provides OpenAI-compatible API
export ADK_LLM_API_BASE="http://localhost:1234/v1"
```

#### Python Code Example

```python
from google.adk import Agent, Runner

agent = Agent(
    name="lm_studio_assistant",
    model="openai/gpt-3.5-turbo",  # Model name running in LM Studio
    instruction="You are a helpful assistant.",
)

runner = Runner(agent=agent)
result = await runner.run("Tell me a joke")
print(result)
```

### 3. Using OpenAI-Compatible Servers

Many local LLM servers provide OpenAI-compatible APIs.

```bash
export ADK_DEFAULT_MODEL="openai/your-model-name"
export ADK_LLM_API_BASE="http://your-server:port/v1"
export ADK_LLM_API_KEY="your-key-if-needed"  # If required
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

## Supported LiteLLM Providers

ADK supports the following providers through LiteLLM:

- `ollama/*` - Ollama local models
- `openai/*` - OpenAI or OpenAI-compatible endpoints
- `anthropic/*` - Anthropic Claude models
- `together_ai/*` - Together AI models
- `huggingface/*` - HuggingFace models
- `replicate/*` - Replicate models
- `bedrock/*` - AWS Bedrock models
- `azure/*` - Azure OpenAI models
- `cohere/*` - Cohere models
- `vertex_ai/*` - Vertex AI models

## Using LiteLlm Instance Directly

You can also configure directly in code instead of using environment variables:

```python
from google.adk import Agent, Runner
from google.adk.models import LiteLlm

# Create LiteLlm instance
llm = LiteLlm(
    model="ollama/llama3",
    api_base="http://localhost:11434",
    # Other LiteLLM parameters...
    timeout=60,
    drop_params=True,  # Automatically drop unsupported parameters
)

# Pass to Agent
agent = Agent(
    name="custom_llm_agent",
    model=llm,
    instruction="You are a helpful assistant.",
)

runner = Runner(agent=agent)
result = await runner.run("Hello!")
print(result)
```

## Troubleshooting

### 1. Connection Error
```
ConnectionError: Failed to connect to http://localhost:11434
```

**Solution:**
- Verify that the local LLM server is running
- Check that the port number is correct
- Check firewall settings

### 2. Model Not Found
```
ValueError: Model ollama/llama3 not found.
```

**Solution:**
- Verify that LiteLlm is properly registered
- Check that the model name pattern is in a supported format (e.g., `ollama/`, `openai/`, etc.)

### 3. API Key Error
```
AuthenticationError: Invalid API key
```

**Solution:**
- Verify that `ADK_LLM_API_KEY` environment variable is set correctly
- Or pass `api_key` parameter when creating LiteLlm

## Additional Resources

- LiteLLM Documentation: https://docs.litellm.ai/
- Ollama Documentation: https://ollama.ai/
- LM Studio: https://lmstudio.ai/

## Contributing

Please submit bug reports or feature requests to GitHub Issues.
