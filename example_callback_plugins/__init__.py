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

"""Custom callback plugins package for ADK.

This package contains user-defined callback functions that can be automatically
registered to allow short-name references in YAML agent configurations.
"""

from __future__ import annotations

# Import all callback functions from submodules
from .logging_callbacks import log_model_call
from .logging_callbacks import log_tool_call
from .security_callbacks import check_tool_permissions
from .security_callbacks import validate_model_request
from .state_callbacks import save_model_info
from .state_callbacks import track_tool_usage

# List of callbacks to be registered for short-name access
CALLBACK_REGISTRY = {
    # Logging callbacks
    "log_model_call": log_model_call,
    "log_tool_call": log_tool_call,
    # Security callbacks
    "check_tool_permissions": check_tool_permissions,
    "validate_model_request": validate_model_request,
    # State management callbacks
    "save_model_info": save_model_info,
    "track_tool_usage": track_tool_usage,
}

# Export all callbacks
__all__ = [
    "log_model_call",
    "log_tool_call",
    "check_tool_permissions",
    "validate_model_request",
    "save_model_info",
    "track_tool_usage",
    "CALLBACK_REGISTRY",
]
