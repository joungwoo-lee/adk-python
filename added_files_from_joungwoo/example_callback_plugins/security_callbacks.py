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

"""Security callback functions for ADK agents."""

from __future__ import annotations

import logging
from typing import Any
from typing import Optional

logger = logging.getLogger(__name__)


def check_tool_permissions(
    tool, args: dict[str, Any], tool_context
) -> Optional[dict]:
  """Check if user has permission to use the tool.

  Args:
    tool: The tool being called
    args: Arguments passed to the tool
    tool_context: The tool execution context

  Returns:
    Error dict if permission denied, None otherwise
  """
  # Get user permissions from state
  permissions = tool_context.state.get("user_permissions", [])

  # Define restricted tools
  restricted_tools = {
      "delete_file": "admin",
      "execute_code": "developer",
      "access_database": "admin",
  }

  # Check if tool is restricted
  required_permission = restricted_tools.get(tool.name)
  if required_permission:
    if required_permission not in permissions:
      logger.warning(
          f"🚫 SECURITY: User lacks '{required_permission}' permission for"
          f" {tool.name}"
      )
      return {
          "error": "Permission denied",
          "required_permission": required_permission,
          "tool": tool.name,
      }

  # Allow execution
  return None


async def validate_model_request(callback_context, llm_request) -> None:
  """Validate model requests for security issues.

  Args:
    callback_context: The callback context
    llm_request: The LLM request being made

  Returns:
    None to allow normal execution
  """
  # Check for sensitive patterns in messages
  sensitive_patterns = ["password", "api_key", "secret", "token"]

  for message in llm_request.messages:
    for part in message.parts:
      if hasattr(part, "text") and part.text:
        text_lower = part.text.lower()
        for pattern in sensitive_patterns:
          if pattern in text_lower:
            logger.warning(
                f"⚠️  SECURITY: Detected sensitive pattern '{pattern}' in"
                " request"
            )
            # Could modify or block the request here
            break

  return None
