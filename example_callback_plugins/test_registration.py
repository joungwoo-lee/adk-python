#!/usr/bin/env python3
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

"""Test script to verify callback registration works correctly."""

from __future__ import annotations

import importlib
import sys


def test_callback_registration():
  """Test that custom callbacks can be registered and used with short names."""
  print("Testing callback registration system...")
  print("=" * 70)

  # Step 1: Register callbacks
  print("\n[1] Registering callbacks...")
  from example_callback_plugins import CALLBACK_REGISTRY
  from example_callback_plugins.register_callbacks import register_callbacks

  register_callbacks(CALLBACK_REGISTRY)
  print(f"✓ Registered {len(CALLBACK_REGISTRY)} callbacks")

  # Step 2: Verify virtual module exists
  print("\n[2] Verifying virtual module 'adk_callbacks' exists...")
  if "adk_callbacks" in sys.modules:
    print("✓ Virtual module 'adk_callbacks' is in sys.modules")
  else:
    print("✗ Virtual module 'adk_callbacks' NOT found")
    return False

  # Step 3: Test imports from virtual module
  print("\n[3] Testing imports from virtual module...")
  try:
    from adk_callbacks import check_tool_permissions
    from adk_callbacks import log_model_call
    from adk_callbacks import save_model_info

    print("✓ Successfully imported:")
    print(f"  - log_model_call: {log_model_call.__name__}")
    print(f"  - check_tool_permissions: {check_tool_permissions.__name__}")
    print(f"  - save_model_info: {save_model_info.__name__}")
  except ImportError as e:
    print(f"✗ Import failed: {e}")
    return False

  # Step 4: Test importlib resolution (simulates ADK's resolve_code_reference)
  print("\n[4] Testing importlib resolution (simulating ADK)...")
  test_cases = [
      "adk_callbacks.log_model_call",
      "adk_callbacks.log_tool_call",
      "adk_callbacks.check_tool_permissions",
      "adk_callbacks.validate_model_request",
      "adk_callbacks.save_model_info",
      "adk_callbacks.track_tool_usage",
  ]

  success_count = 0
  for ref in test_cases:
    try:
      module_path, obj_name = ref.rsplit(".", 1)
      module = importlib.import_module(module_path)
      obj = getattr(module, obj_name)
      print(f"  ✓ {ref}")
      success_count += 1
    except Exception as e:
      print(f"  ✗ {ref}: {e}")

  # Step 5: Verify all callbacks
  print("\n[5] Verifying all registered callbacks...")
  from example_callback_plugins.register_callbacks import verify_registration

  status = verify_registration()
  print(f"✓ Found {len(status)} callbacks:")
  for callback_name, is_registered in sorted(status.items()):
    symbol = "✓" if is_registered else "✗"
    print(f"  {symbol} {callback_name}")

  # Step 6: Summary
  print("\n" + "=" * 70)
  print("Test Summary")
  print("=" * 70)
  print(f"✓ Virtual module created: adk_callbacks")
  print(f"✓ Callbacks registered: {len(CALLBACK_REGISTRY)}")
  print(f"✓ Resolution successful: {success_count}/{len(test_cases)}")
  print("\nYou can now use callbacks in YAML as:")
  print("  before_model_callbacks:")
  print("    - name: adk_callbacks.log_model_call")
  print("=" * 70)

  return success_count == len(test_cases)


if __name__ == "__main__":
  success = test_callback_registration()
  sys.exit(0 if success else 1)
