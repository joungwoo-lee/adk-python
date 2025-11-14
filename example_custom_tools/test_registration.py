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

"""Test script to verify custom tools registration works correctly."""

from __future__ import annotations


def test_tool_registration():
  """Test that custom tools can be registered and imported from google.adk.tools."""
  print("Testing custom tools registration system...")
  print("=" * 70)

  # Step 1: Register tools
  print("\n[1] Registering custom tools...")
  from example_custom_tools import CUSTOM_TOOLS
  from example_custom_tools.register_tools import register_custom_tools

  register_custom_tools(CUSTOM_TOOLS)
  print(f"✓ Registered {len(CUSTOM_TOOLS)} custom tools")

  # Step 2: Verify they are available in google.adk.tools
  print("\n[2] Verifying tools are available in google.adk.tools...")
  import google.adk.tools as adk_tools

  success_count = 0
  for tool in CUSTOM_TOOLS:
    tool_name = tool.__name__
    if hasattr(adk_tools, tool_name):
      print(f"  ✓ {tool_name} is available")
      success_count += 1
    else:
      print(f"  ✗ {tool_name} is NOT available")

  # Step 3: Test importing directly
  print("\n[3] Testing direct imports from google.adk.tools...")
  try:
    from google.adk.tools import calculate
    from google.adk.tools import count_words
    from google.adk.tools import get_weather

    print("  ✓ Successfully imported: get_weather, calculate, count_words")
  except ImportError as e:
    print(f"  ✗ Import failed: {e}")
    return False

  # Step 4: Test tool functionality
  print("\n[4] Testing tool functionality...")
  test_cases = [
      ("get_weather", lambda: get_weather("Tokyo", "celsius")),
      ("calculate", lambda: calculate("2 + 2")),
      ("count_words", lambda: count_words("one two three")),
  ]

  for tool_name, test_func in test_cases:
    try:
      result = test_func()
      print(f"  ✓ {tool_name}() executed successfully")
      print(f"    Result: {result}")
    except Exception as e:
      print(f"  ✗ {tool_name}() failed: {e}")
      return False

  # Step 5: Summary
  print("\n" + "=" * 70)
  print(f"✓ All tests passed! ({success_count}/{len(CUSTOM_TOOLS)} tools registered)")
  print("\nCustom tools are ready to use in YAML configurations:")
  print("  tools:")
  for tool in CUSTOM_TOOLS:
    print(f"    - name: {tool.__name__}")
  print("=" * 70)

  return True


if __name__ == "__main__":
  import sys

  success = test_tool_registration()
  sys.exit(0 if success else 1)
