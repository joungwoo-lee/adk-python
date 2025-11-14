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

"""Tool registration system for injecting custom tools into ADK's built-in tools.

This module provides functionality to dynamically register user-defined tools
into the google.adk.tools module, making them available as built-in tools
that can be referenced directly by name in YAML agent configurations.

Usage:
    from example_custom_tools import CUSTOM_TOOLS
    from example_custom_tools.register_tools import register_custom_tools

    # Register all custom tools as built-in tools
    register_custom_tools(CUSTOM_TOOLS)

    # Now you can use them in YAML:
    # tools:
    #   - name: get_weather
    #   - name: calculate
"""

from __future__ import annotations

import importlib
import logging
import sys
from typing import Any
from typing import Callable

logger = logging.getLogger(__name__)


def register_custom_tools(
    tools: list[Callable[..., Any]], package_name: str = "custom_tools"
) -> None:
  """Register custom tools as built-in tools in google.adk.tools.

  This function dynamically injects user-defined tools into the ADK tools
  module, allowing them to be used in YAML agent configurations just like
  native ADK tools.

  Args:
    tools: List of tool functions to register. Each function should have
      proper type hints and docstrings that will be used for tool declaration.
    package_name: Optional name prefix for the tools (default: "custom_tools").
      This helps distinguish custom tools from native ADK tools in logs.

  Example:
    >>> from example_custom_tools import CUSTOM_TOOLS
    >>> register_custom_tools(CUSTOM_TOOLS)
    >>> # Now 'get_weather' can be used in YAML:
    >>> # tools:
    >>> #   - name: get_weather
  """
  try:
    # Import the google.adk.tools module
    adk_tools = importlib.import_module("google.adk.tools")

    registered_count = 0
    for tool in tools:
      tool_name = tool.__name__

      # Inject the tool into the google.adk.tools module namespace
      setattr(adk_tools, tool_name, tool)

      # Update the __all__ list to include the new tool
      if hasattr(adk_tools, "__all__"):
        if tool_name not in adk_tools.__all__:
          adk_tools.__all__.append(tool_name)
      else:
        adk_tools.__all__ = [tool_name]

      logger.info(
          "Registered custom tool '%s' from %s as built-in ADK tool",
          tool_name,
          package_name,
      )
      registered_count += 1

    logger.info(
        "Successfully registered %d custom tools as built-in ADK tools",
        registered_count,
    )

  except ImportError as e:
    logger.error(
        "Failed to import google.adk.tools. Is google-adk installed? Error: %s",
        e,
    )
    raise
  except Exception as e:
    logger.error("Error registering custom tools: %s", e)
    raise


def register_custom_tools_from_module(module_path: str) -> None:
  """Register all tools from a custom module.

  This is a convenience function that automatically finds and registers
  all tool functions from a given module.

  Args:
    module_path: Dotted path to the module containing tools
      (e.g., "example_custom_tools")

  Example:
    >>> register_custom_tools_from_module("example_custom_tools")
  """
  try:
    # Import the custom tools module
    custom_module = importlib.import_module(module_path)

    # Check if the module has a CUSTOM_TOOLS list
    if hasattr(custom_module, "CUSTOM_TOOLS"):
      tools = custom_module.CUSTOM_TOOLS
      register_custom_tools(tools, package_name=module_path)
    else:
      logger.warning(
          "Module '%s' does not have a CUSTOM_TOOLS list. "
          "Please define CUSTOM_TOOLS = [tool1, tool2, ...] in %s/__init__.py",
          module_path,
          module_path,
      )

  except ImportError as e:
    logger.error("Failed to import module '%s': %s", module_path, e)
    raise


def verify_registration() -> dict[str, bool]:
  """Verify that custom tools are properly registered in google.adk.tools.

  Returns:
    A dictionary mapping tool names to their registration status.

  Example:
    >>> register_custom_tools(CUSTOM_TOOLS)
    >>> status = verify_registration()
    >>> print(status)
    {'get_weather': True, 'calculate': True, ...}
  """
  try:
    adk_tools = importlib.import_module("google.adk.tools")
    custom_module = importlib.import_module("example_custom_tools")

    if not hasattr(custom_module, "CUSTOM_TOOLS"):
      logger.warning("No CUSTOM_TOOLS found in example_custom_tools")
      return {}

    status = {}
    for tool in custom_module.CUSTOM_TOOLS:
      tool_name = tool.__name__
      is_registered = (
          hasattr(adk_tools, tool_name)
          and tool_name in getattr(adk_tools, "__all__", [])
      )
      status[tool_name] = is_registered

    return status

  except ImportError as e:
    logger.error("Failed to verify registration: %s", e)
    return {}
