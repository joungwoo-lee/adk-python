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

"""Example custom weather tool for ADK.

This is an example of how to create a custom tool that can be automatically
registered as a built-in tool in ADK.
"""

from __future__ import annotations


def get_weather(location: str, unit: str = "celsius") -> str:
  """Get current weather for a location.

  Args:
    location: The city or location to get weather for (e.g., "Seoul", "Tokyo")
    unit: Temperature unit, either "celsius" or "fahrenheit" (default: celsius)

  Returns:
    A string describing the current weather conditions.
  """
  # This is a mock implementation for demonstration
  # In a real implementation, you would call a weather API
  temp = 22 if unit == "celsius" else 72
  return (
      f"The current weather in {location} is sunny with a temperature "
      f"of {temp}°{unit[0].upper()}."
  )


def get_forecast(location: str, days: int = 3) -> str:
  """Get weather forecast for upcoming days.

  Args:
    location: The city or location to get forecast for
    days: Number of days to forecast (1-7, default: 3)

  Returns:
    A string with the weather forecast.
  """
  # Mock implementation
  if days < 1 or days > 7:
    return "Please specify a number of days between 1 and 7."

  forecast_text = f"{days}-day forecast for {location}:\n"
  for day in range(1, days + 1):
    forecast_text += f"Day {day}: Partly cloudy, 20-25°C\n"

  return forecast_text
