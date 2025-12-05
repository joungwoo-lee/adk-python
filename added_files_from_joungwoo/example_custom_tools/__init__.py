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

"""Custom tools package for ADK.

This package contains user-defined tools that can be automatically registered
as built-in tools in ADK, allowing them to be used in YAML agent configurations
just like native ADK tools.
"""

from __future__ import annotations

# Import all tool functions from submodules
from .calculator_tool import calculate
from .calculator_tool import convert_units
from .text_tool import count_words
from .text_tool import reverse_text
from .text_tool import to_lowercase
from .text_tool import to_uppercase
from .weather_tool import get_forecast
from .weather_tool import get_weather

# List of tools to be registered as built-in tools
# These will be available in YAML agent configs using their function names
CUSTOM_TOOLS = [
    get_weather,
    get_forecast,
    calculate,
    convert_units,
    count_words,
    reverse_text,
    to_uppercase,
    to_lowercase,
]

# Export all tools
__all__ = [
    "get_weather",
    "get_forecast",
    "calculate",
    "convert_units",
    "count_words",
    "reverse_text",
    "to_uppercase",
    "to_lowercase",
    "CUSTOM_TOOLS",
]
