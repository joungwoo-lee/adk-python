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

"""Example usage of callback plugin registration system."""

from __future__ import annotations

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
  """Main function demonstrating callback registration."""

  logger.info("=" * 70)
  logger.info("Callback Plugin Registration Example")
  logger.info("=" * 70)

  # ========================================================================
  # STEP 1: Import and register callbacks
  # ========================================================================
  logger.info("\n[STEP 1] Registering custom callbacks...")

  from example_callback_plugins import CALLBACK_REGISTRY
  from example_callback_plugins.register_callbacks import register_callbacks
  from example_callback_plugins.register_callbacks import verify_registration

  register_callbacks(CALLBACK_REGISTRY)

  # Verify registration
  status = verify_registration()
  logger.info(f"✓ Registered {len(status)} callbacks:")
  for callback_name, is_registered in status.items():
    symbol = "✓" if is_registered else "✗"
    logger.info(f"  {symbol} {callback_name}")

  # ========================================================================
  # STEP 2: Test that callbacks can be imported from virtual module
  # ========================================================================
  logger.info("\n[STEP 2] Testing virtual module imports...")

  try:
    # Import from the virtual module
    from adk_callbacks import log_model_call
    from adk_callbacks import check_tool_permissions
    from adk_callbacks import save_model_info

    logger.info("✓ Successfully imported callbacks from 'adk_callbacks' module")
    logger.info(f"  - log_model_call: {log_model_call}")
    logger.info(f"  - check_tool_permissions: {check_tool_permissions}")
    logger.info(f"  - save_model_info: {save_model_info}")

  except ImportError as e:
    logger.error(f"✗ Failed to import from virtual module: {e}")
    sys.exit(1)

  # ========================================================================
  # STEP 3: Show how to use in YAML
  # ========================================================================
  logger.info("\n[STEP 3] How to use in YAML agent configuration:")
  logger.info("-" * 70)

  yaml_example = """
# Example YAML agent configuration with short callback names
agent_class: LlmAgent
name: my_agent
model: gemini-2.5-flash
instruction: You are a helpful assistant.

tools:
  - name: google_search

# ✨ Use callbacks with SHORT NAMES!
before_model_callbacks:
  - name: adk_callbacks.log_model_call
  - name: adk_callbacks.validate_model_request

after_model_callbacks:
  - name: adk_callbacks.save_model_info

before_tool_callbacks:
  - name: adk_callbacks.log_tool_call
  - name: adk_callbacks.check_tool_permissions

after_tool_callbacks:
  - name: adk_callbacks.track_tool_usage
"""

  logger.info(yaml_example)
  logger.info("-" * 70)

  # ========================================================================
  # STEP 4: Compare with old way (long module paths)
  # ========================================================================
  logger.info("\n[STEP 4] Comparison with old way:")
  logger.info("-" * 70)

  comparison = """
OLD WAY (Long module paths):
  before_model_callbacks:
    - name: example_callback_plugins.logging_callbacks.log_model_call
    - name: example_callback_plugins.security_callbacks.validate_model_request

NEW WAY (Short names with virtual module):
  before_model_callbacks:
    - name: adk_callbacks.log_model_call
    - name: adk_callbacks.validate_model_request

✅ Much cleaner and easier to use!
"""

  logger.info(comparison)
  logger.info("-" * 70)

  # ========================================================================
  # STEP 5: Test importlib (simulate ADK's resolve_code_reference)
  # ========================================================================
  logger.info("\n[STEP 5] Testing importlib resolution (simulating ADK)...")

  import importlib

  test_references = [
      "adk_callbacks.log_model_call",
      "adk_callbacks.check_tool_permissions",
      "adk_callbacks.save_model_info",
  ]

  for ref in test_references:
    try:
      module_path, obj_name = ref.rsplit(".", 1)
      module = importlib.import_module(module_path)
      obj = getattr(module, obj_name)
      logger.info(f"✓ Resolved '{ref}' successfully")
      logger.info(f"  -> {obj}")
    except Exception as e:
      logger.error(f"✗ Failed to resolve '{ref}': {e}")

  # ========================================================================
  # Summary
  # ========================================================================
  logger.info("\n" + "=" * 70)
  logger.info("Summary")
  logger.info("=" * 70)
  logger.info("✓ Callbacks registered in virtual module 'adk_callbacks'")
  logger.info("✓ Short names work: adk_callbacks.<callback_name>")
  logger.info("✓ Ready to use in YAML configurations")
  logger.info("✓ Compatible with ADK's resolve_code_reference")
  logger.info("\nYour callbacks are now as easy to use as built-in ones!")
  logger.info("=" * 70)


if __name__ == "__main__":
  main()
