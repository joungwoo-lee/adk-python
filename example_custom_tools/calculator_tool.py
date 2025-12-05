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

"""Example custom calculator tool for ADK.

This demonstrates how to create simple utility tools that can be used
in your agents.
"""

from __future__ import annotations

from typing import Union


def calculate(expression: str) -> Union[float, str]:
  """Evaluate a mathematical expression safely.

  Args:
    expression: A mathematical expression string (e.g., "2 + 3 * 4")

  Returns:
    The result of the calculation, or an error message if invalid.
  """
  try:
    # Safe evaluation with limited namespace
    # Only allow basic math operations
    allowed_names = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "pow": pow,
    }
    result = eval(expression, {"__builtins__": {}}, allowed_names)
    return float(result)
  except Exception as e:
    return f"Error calculating expression: {str(e)}"


def convert_units(
    value: float, from_unit: str, to_unit: str
) -> Union[float, str]:
  """Convert between different units.

  Args:
    value: The numeric value to convert
    from_unit: The source unit (e.g., "km", "miles", "kg", "lbs")
    to_unit: The target unit

  Returns:
    The converted value, or an error message if conversion not supported.
  """
  # Simple conversion table
  conversions = {
      ("km", "miles"): 0.621371,
      ("miles", "km"): 1.60934,
      ("kg", "lbs"): 2.20462,
      ("lbs", "kg"): 0.453592,
      ("celsius", "fahrenheit"): lambda x: x * 9 / 5 + 32,
      ("fahrenheit", "celsius"): lambda x: (x - 32) * 5 / 9,
  }

  key = (from_unit.lower(), to_unit.lower())
  if key in conversions:
    converter = conversions[key]
    if callable(converter):
      return converter(value)
    else:
      return value * converter
  else:
    return f"Conversion from {from_unit} to {to_unit} is not supported."
