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

"""Example usage of custom tools registration system.

This script demonstrates how to register custom tools and use them in ADK agents.
"""

from __future__ import annotations

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
  """Main function demonstrating custom tool registration."""

  logger.info("=" * 60)
  logger.info("Custom Tools Registration Example")
  logger.info("=" * 60)

  # Step 1: Import the custom tools and registration function
  logger.info("\n[Step 1] Importing custom tools...")
  try:
    from example_custom_tools import CUSTOM_TOOLS
    from example_custom_tools.register_tools import register_custom_tools
    from example_custom_tools.register_tools import verify_registration

    logger.info("✓ Successfully imported custom tools")
    logger.info(f"  Found {len(CUSTOM_TOOLS)} custom tools")
    for tool in CUSTOM_TOOLS:
      logger.info(f"    - {tool.__name__}")
  except ImportError as e:
    logger.error(f"✗ Failed to import custom tools: {e}")
    sys.exit(1)

  # Step 2: Register custom tools as built-in ADK tools
  logger.info("\n[Step 2] Registering custom tools as built-in ADK tools...")
  try:
    register_custom_tools(CUSTOM_TOOLS)
    logger.info("✓ Successfully registered custom tools")
  except Exception as e:
    logger.error(f"✗ Failed to register custom tools: {e}")
    sys.exit(1)

  # Step 3: Verify registration
  logger.info("\n[Step 3] Verifying registration...")
  status = verify_registration()
  if status:
    logger.info("✓ Registration verification results:")
    for tool_name, is_registered in status.items():
      symbol = "✓" if is_registered else "✗"
      logger.info(f"  {symbol} {tool_name}: {'Registered' if is_registered else 'Not registered'}")
  else:
    logger.warning("Could not verify registration status")

  # Step 4: Show how to use in YAML
  logger.info("\n[Step 4] How to use in YAML agent configuration:")
  logger.info("-" * 60)
  yaml_example = """
# Example YAML agent configuration
agent_class: LlmAgent
name: my_custom_agent
model: gemini-2.5-flash
instruction: |
  You are a helpful assistant with access to custom tools.

tools:
  # Built-in ADK tools
  - name: google_search
  
  # Your custom tools - now available as built-in tools!
  - name: get_weather
  - name: get_forecast
  - name: calculate
  - name: convert_units
  - name: count_words
  - name: reverse_text
  - name: to_uppercase
  - name: to_lowercase
"""
  logger.info(yaml_example)
  logger.info("-" * 60)

  # Step 5: Test the tools directly
  logger.info("\n[Step 5] Testing custom tools directly:")
  logger.info("-" * 60)

  # Import and test tools from google.adk.tools namespace
  try:
    from google.adk.tools import get_weather
    from google.adk.tools import calculate
    from google.adk.tools import count_words

    # Test weather tool
    result = get_weather("Seoul", "celsius")
    logger.info(f"✓ get_weather('Seoul', 'celsius')")
    logger.info(f"  Result: {result}")

    # Test calculator tool
    result = calculate("10 + 5 * 2")
    logger.info(f"✓ calculate('10 + 5 * 2')")
    logger.info(f"  Result: {result}")

    # Test text tool
    result = count_words("Hello world from ADK custom tools!")
    logger.info(f"✓ count_words('Hello world from ADK custom tools!')")
    logger.info(f"  Result: {result} words")

  except Exception as e:
    logger.error(f"✗ Error testing tools: {e}")
    import traceback

    traceback.print_exc()

  logger.info("-" * 60)

  # Step 6: Summary
  logger.info("\n[Summary]")
  logger.info("✓ Custom tools are now registered as built-in ADK tools")
  logger.info("✓ You can use them in YAML agent configurations")
  logger.info("✓ They work exactly like native ADK tools (google_search, etc.)")
  logger.info("\nNext steps:")
  logger.info(
      "1. Create your agent YAML file with custom tools (see example above)"
  )
  logger.info("2. Run: adk web /path/to/your/agents")
  logger.info("3. Use the agent builder UI to test your custom tools")
  logger.info("\n" + "=" * 60)


if __name__ == "__main__":
  main()
