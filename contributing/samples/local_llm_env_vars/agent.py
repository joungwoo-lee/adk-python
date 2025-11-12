# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example agent using environment variables for local LLM configuration.

This example demonstrates how to use environment variables to configure
a local LLM backend without hardcoding the model and API endpoint in the code.

Environment Variables:
  ADK_DEFAULT_MODEL: The model to use (e.g., "ollama/llama3")
  ADK_LLM_API_BASE: The base URL for the LLM API (e.g., "http://localhost:11434")
  ADK_LLM_API_KEY: API key if required (optional)

Usage:
  export ADK_DEFAULT_MODEL="ollama/llama3"
  export ADK_LLM_API_BASE="http://localhost:11434"
  adk web contributing/samples/local_llm_env_vars
"""

from google.adk.agents.llm_agent import Agent


def get_weather(location: str) -> str:
  """Get the current weather for a location.

  Args:
    location: The city and state, e.g. "San Francisco, CA"

  Returns:
    A description of the current weather.
  """
  # This is a mock implementation
  return f"The weather in {location} is sunny and 72°F."


def calculate(expression: str) -> str:
  """Calculate a mathematical expression.

  Args:
    expression: The mathematical expression to evaluate (e.g., "2 + 2 * 3")

  Returns:
    The result of the calculation.
  """
  try:
    # Safe evaluation of simple mathematical expressions
    result = eval(expression, {"__builtins__": {}}, {})
    return f"The result is: {result}"
  except Exception as e:
    return f"Error calculating: {e}"


# Agent uses ADK_DEFAULT_MODEL environment variable
# No need to specify the model parameter if ADK_DEFAULT_MODEL is set
root_agent = Agent(
    name="local_llm_assistant",
    description="A helpful assistant using a local LLM backend",
    instruction="""
You are a helpful assistant that can help with various tasks.
You have access to weather information and can perform calculations.
Be friendly and concise in your responses.
""",
    tools=[
        get_weather,
        calculate,
    ],
)
