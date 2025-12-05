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

"""Callback registration system for enabling short-name references in YAML.

This module provides functionality to register custom callbacks so they can be
referenced by short names in YAML agent configurations, similar to built-in
ADK callbacks.

Usage:
    from example_callback_plugins import CALLBACK_REGISTRY
    from example_callback_plugins.register_callbacks import register_callbacks

    # Register all callbacks with short names
    register_callbacks(CALLBACK_REGISTRY)

    # Now you can use them in YAML:
    # before_model_callbacks:
    #   - name: adk_callbacks.log_model_call
    #   - name: adk_callbacks.validate_model_request
"""

from __future__ import annotations

import logging
import sys
from types import ModuleType
from typing import Any
from typing import Callable
from typing import Dict

logger = logging.getLogger(__name__)

# Virtual module name for short callback references
VIRTUAL_MODULE_NAME = "adk_callbacks"


def register_callbacks(
    callback_registry: Dict[str, Callable], module_name: str = VIRTUAL_MODULE_NAME
) -> None:
  """Register custom callbacks for short-name access in YAML configurations.

  This function creates a virtual Python module and registers all callback
  functions in it, allowing them to be referenced by short names in YAML
  agent configurations.

  Args:
    callback_registry: Dictionary mapping callback names to callback functions
    module_name: Name of the virtual module (default: "adk_callbacks")

  Example:
    >>> from example_callback_plugins import CALLBACK_REGISTRY
    >>> register_callbacks(CALLBACK_REGISTRY)
    >>> # Now in YAML you can use:
    >>> # before_model_callbacks:
    >>> #   - name: adk_callbacks.log_model_call
  """
  # Create or get existing virtual module
  if module_name in sys.modules:
    virtual_module = sys.modules[module_name]
    logger.info(
        "Virtual module '%s' already exists, updating...", module_name
    )
  else:
    virtual_module = ModuleType(module_name)
    virtual_module.__doc__ = (
        "Virtual module containing registered callback functions"
    )
    virtual_module.__file__ = "<virtual>"
    sys.modules[module_name] = virtual_module
    logger.info("Created virtual module '%s'", module_name)

  # Register all callbacks in the virtual module
  registered_count = 0
  for callback_name, callback_func in callback_registry.items():
    setattr(virtual_module, callback_name, callback_func)
    logger.info(
        "Registered callback '%s.%s'", module_name, callback_name
    )
    registered_count += 1

  logger.info(
      "Successfully registered %d callbacks in module '%s'",
      registered_count,
      module_name,
  )
  logger.info(
      "Callbacks can now be used in YAML as '%s.<callback_name>'",
      module_name,
  )


def register_callbacks_from_module(
    module_path: str, module_name: str = VIRTUAL_MODULE_NAME
) -> None:
  """Register all callbacks from a custom module.

  This is a convenience function that automatically finds and registers
  all callback functions from a given module.

  Args:
    module_path: Dotted path to the module containing callbacks
      (e.g., "example_callback_plugins")
    module_name: Name of the virtual module (default: "adk_callbacks")

  Example:
    >>> register_callbacks_from_module("example_callback_plugins")
  """
  import importlib

  try:
    # Import the custom callbacks module
    custom_module = importlib.import_module(module_path)

    # Check if the module has a CALLBACK_REGISTRY
    if hasattr(custom_module, "CALLBACK_REGISTRY"):
      callback_registry = custom_module.CALLBACK_REGISTRY
      register_callbacks(callback_registry, module_name)
    else:
      logger.warning(
          "Module '%s' does not have a CALLBACK_REGISTRY. "
          "Please define CALLBACK_REGISTRY = {...} in %s/__init__.py",
          module_path,
          module_path,
      )

  except ImportError as e:
    logger.error("Failed to import module '%s': %s", module_path, e)
    raise


def verify_registration(
    module_name: str = VIRTUAL_MODULE_NAME,
) -> Dict[str, bool]:
  """Verify that callbacks are properly registered in the virtual module.

  Args:
    module_name: Name of the virtual module to verify

  Returns:
    A dictionary mapping callback names to their registration status.

  Example:
    >>> register_callbacks(CALLBACK_REGISTRY)
    >>> status = verify_registration()
    >>> print(status)
    {'log_model_call': True, 'check_permissions': True, ...}
  """
  if module_name not in sys.modules:
    logger.warning("Virtual module '%s' not found in sys.modules", module_name)
    return {}

  virtual_module = sys.modules[module_name]
  status = {}

  # Check all registered callbacks
  for attr_name in dir(virtual_module):
    if not attr_name.startswith("_"):
      attr = getattr(virtual_module, attr_name)
      if callable(attr):
        status[attr_name] = True

  return status


def unregister_callbacks(module_name: str = VIRTUAL_MODULE_NAME) -> None:
  """Unregister callbacks by removing the virtual module.

  Args:
    module_name: Name of the virtual module to remove

  Example:
    >>> unregister_callbacks()
  """
  if module_name in sys.modules:
    del sys.modules[module_name]
    logger.info("Unregistered virtual module '%s'", module_name)
  else:
    logger.warning(
        "Virtual module '%s' not found, nothing to unregister", module_name
    )
