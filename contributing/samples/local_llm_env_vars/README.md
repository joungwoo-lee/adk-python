# Local LLM Configuration with Environment Variables

This example demonstrates how to use environment variables to configure a local LLM backend in ADK, making it easy to switch between different models and endpoints without changing code.

## Prerequisites

1. Install and run a local LLM server (e.g., Ollama)
2. Download a model (e.g., `ollama pull llama3`)

## Configuration

Set the following environment variables:

```bash
# Required: Specify the model to use
export ADK_DEFAULT_MODEL="ollama/llama3"

# Required for local LLMs: Specify the API endpoint
export ADK_LLM_API_BASE="http://localhost:11434"

# Optional: API key if your server requires authentication
# export ADK_LLM_API_KEY="your-key-here"
```

## Running the Example

### Using ADK Web UI

```bash
adk web contributing/samples/local_llm_env_vars
```

Then open your browser to the URL shown (typically http://localhost:8000).

### Using ADK CLI

```bash
adk run contributing/samples/local_llm_env_vars
```

## Example Interactions

Try these prompts:

1. **Weather Query**:
   ```
   What's the weather in San Francisco?
   ```

2. **Calculation**:
   ```
   Calculate 15 * 24 + 100
   ```

3. **Combined Query**:
   ```
   What's the weather in New York and what's 50 + 50?
   ```

## Switching Models

To use a different model, simply change the environment variable:

```bash
# Use a different Ollama model
export ADK_DEFAULT_MODEL="ollama/mistral"

# Or use OpenAI-compatible endpoint
export ADK_DEFAULT_MODEL="openai/gpt-4"
export ADK_LLM_API_BASE="http://localhost:1234/v1"

# Or use a cloud provider
export ADK_DEFAULT_MODEL="anthropic/claude-3-5-sonnet-20241022"
export ADK_LLM_API_KEY="your-anthropic-key"
```

## Supported Providers

ADK's LiteLLM integration supports many providers:

- **Local LLMs**:
  - `ollama/*` - Ollama (requires `OLLAMA_API_BASE` or `ADK_LLM_API_BASE`)
  - `openai/*` - Any OpenAI-compatible server (LM Studio, LocalAI, etc.)

- **Cloud Providers**:
  - `anthropic/*` - Anthropic Claude
  - `together_ai/*` - Together AI
  - `huggingface/*` - HuggingFace
  - `replicate/*` - Replicate
  - `azure/*` - Azure OpenAI
  - `cohere/*` - Cohere
  - And many more...

## Alternative: Direct Model Configuration

If you prefer not to use environment variables, you can specify the model directly in code:

```python
from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm

root_agent = Agent(
    model=LiteLlm(
        model="ollama/llama3",
        api_base="http://localhost:11434",
    ),
    name="local_llm_assistant",
    instruction="You are a helpful assistant.",
    tools=[...],
)
```

## Benefits of Environment Variables

1. **Flexibility**: Easy to switch between models without code changes
2. **Portability**: Same code works in development, testing, and production
3. **Security**: Keep API keys out of source code
4. **Configuration Management**: Works well with Docker, Kubernetes, and CI/CD

## Troubleshooting

### Model not found error
```
ValueError: Model ollama/llama3 not found.
```

**Solution**: Make sure the model name starts with a supported prefix like `ollama/`, `openai/`, `anthropic/`, etc.

### Connection refused
```
ConnectionError: Failed to connect to http://localhost:11434
```

**Solution**:
1. Verify your local LLM server is running
2. Check the port number in `ADK_LLM_API_BASE`
3. For Ollama: `ollama serve`

### Environment variable not applied
```
Agent uses wrong model or fails to connect
```

**Solution**:
1. Verify environment variables are exported in the same terminal session
2. Check variable names are correct (case-sensitive)
3. Restart your Python process after setting variables

## Additional Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Ollama Documentation](https://ollama.ai/)
- [ADK Documentation](https://google.github.io/adk-docs)
