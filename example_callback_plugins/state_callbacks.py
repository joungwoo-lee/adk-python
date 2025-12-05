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

"""State management callback functions for ADK agents."""

from __future__ import annotations

from typing import Any


async def save_model_info(callback_context, llm_response) -> None:
  """Save model response information to state.

  Args:
    callback_context: The callback context
    llm_response: The LLM response received

  Returns:
    None to allow normal execution
  """
  # Save model information
  callback_context.state["last_model"] = llm_response.model_version
  callback_context.state["last_response_length"] = len(
      llm_response.text or ""
  )

  # Track response count
  if "response_count" not in callback_context.state:
    callback_context.state["response_count"] = 0
  callback_context.state["response_count"] += 1

  return None


def track_tool_usage(
    tool, args: dict[str, Any], tool_context, tool_response: dict
) -> None:
  """Track tool usage statistics in state.

  Args:
    tool: The tool that was called
    args: Arguments passed to the tool
    tool_context: The tool execution context
    tool_response: The response from the tool

  Returns:
    None to allow normal execution
  """
  # Initialize usage tracking
  if "tool_usage" not in tool_context.state:
    tool_context.state["tool_usage"] = {}

  tool_usage = tool_context.state["tool_usage"]

  # Track per-tool usage
  if tool.name not in tool_usage:
    tool_usage[tool.name] = {
        "count": 0,
        "last_used": None,
    }

  tool_usage[tool.name]["count"] += 1
  tool_usage[tool.name]["last_used"] = "now"  # Could use actual timestamp

  return None
