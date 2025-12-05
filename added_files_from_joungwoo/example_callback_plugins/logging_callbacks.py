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

"""Logging callback functions for ADK agents."""

from __future__ import annotations

import logging
from typing import Any
from typing import Optional

logger = logging.getLogger(__name__)


async def log_model_call(callback_context, llm_request) -> None:
  """Log LLM model calls with details.

  Args:
    callback_context: The callback context
    llm_request: The LLM request being made

  Returns:
    None to allow normal execution
  """
  logger.info("=" * 60)
  logger.info("🤖 MODEL CALL")
  logger.info(f"  Model: {llm_request.model}")
  logger.info(f"  Messages: {len(llm_request.messages)} messages")
  logger.info("=" * 60)

  # Track in state
  if "model_call_count" not in callback_context.state:
    callback_context.state["model_call_count"] = 0
  callback_context.state["model_call_count"] += 1

  return None


def log_tool_call(tool, args: dict[str, Any], tool_context) -> None:
  """Log tool calls with arguments.

  Args:
    tool: The tool being called
    args: Arguments passed to the tool
    tool_context: The tool execution context

  Returns:
    None to allow normal execution
  """
  logger.info("-" * 60)
  logger.info(f"🔧 TOOL CALL: {tool.name}")
  logger.info(f"  Arguments: {args}")
  logger.info("-" * 60)

  # Track in state
  if "tool_calls" not in tool_context.state:
    tool_context.state["tool_calls"] = []
  tool_context.state["tool_calls"].append({
      "tool": tool.name,
      "args": args,
  })

  return None
