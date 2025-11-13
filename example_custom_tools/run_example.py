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

"""Complete example: Register custom tools and use them with ADK agents.

This script demonstrates the entire workflow:
1. Register custom tools as built-in tools
2. Load a YAML agent that uses custom tools
3. Run the agent and interact with it
4. Show that custom tools work seamlessly with ADK
"""

from __future__ import annotations

import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
  """Main function demonstrating complete custom tools integration."""

  logger.info("=" * 70)
  logger.info("Complete Custom Tools Integration Example")
  logger.info("=" * 70)

  # ========================================================================
  # STEP 1: Register custom tools as built-in tools
  # ========================================================================
  logger.info("\n[STEP 1] Registering custom tools as built-in ADK tools...")

  from example_custom_tools import CUSTOM_TOOLS
  from example_custom_tools.register_tools import register_custom_tools
  from example_custom_tools.register_tools import verify_registration

  register_custom_tools(CUSTOM_TOOLS)

  # Verify registration
  status = verify_registration()
  registered_count = sum(1 for is_registered in status.values() if is_registered)
  logger.info(
      f"✓ Successfully registered {registered_count}/{len(CUSTOM_TOOLS)} custom tools"
  )

  # ========================================================================
  # STEP 2: Import ADK and create an agent
  # ========================================================================
  logger.info("\n[STEP 2] Creating agent with custom tools...")

  try:
    from google.adk.agents import LlmAgent
    from google.adk.runners import Runner

    # Create an agent that uses custom tools
    agent = LlmAgent(
        name="demo_agent",
        model="gemini-2.5-flash",
        instruction="""You are a helpful assistant with weather and calculation tools.
        
Available tools:
- get_weather(location, unit): Get current weather
- calculate(expression): Perform calculations
- count_words(text): Count words in text

Help users with weather queries, calculations, and text analysis.""",
        tools=[
            # Note: Tools are specified as strings, just like built-in tools
            "get_weather",
            "calculate",
            "count_words",
        ],
    )

    logger.info("✓ Created agent with custom tools")
    logger.info(f"  Agent name: {agent.name}")
    logger.info(f"  Model: {agent.model}")
    logger.info(f"  Tools: {[tool for tool in ['get_weather', 'calculate', 'count_words']]}")

  except ImportError as e:
    logger.error(f"✗ Failed to import ADK: {e}")
    logger.info("\nPlease install ADK first:")
    logger.info("  pip install --upgrade google-adk")
    return

  # ========================================================================
  # STEP 3: Test the agent with custom tools
  # ========================================================================
  logger.info("\n[STEP 3] Testing agent with custom tools...")

  # Create a runner
  try:
    from google.adk.sessions.in_memory_session_service import (
        InMemorySessionService,
    )

    runner = Runner(
        app=agent,
        session_service=InMemorySessionService(),
    )

    # Test 1: Weather query
    logger.info("\n--- Test 1: Weather Query ---")
    logger.info("User: What's the weather in Tokyo?")

    result = await runner.run_async(
        user_id="test_user",
        new_message="What's the weather in Tokyo?",
    )

    logger.info(f"Agent: {result[-1].content}")

    # Test 2: Calculation
    logger.info("\n--- Test 2: Calculation ---")
    logger.info("User: Calculate 15 * 8 + 23")

    result = await runner.run_async(
        user_id="test_user",
        new_message="Calculate 15 * 8 + 23",
    )

    logger.info(f"Agent: {result[-1].content}")

    # Test 3: Text analysis
    logger.info("\n--- Test 3: Text Analysis ---")
    logger.info("User: How many words are in 'Hello world from ADK'?")

    result = await runner.run_async(
        user_id="test_user",
        new_message="How many words are in 'Hello world from ADK'?",
    )

    logger.info(f"Agent: {result[-1].content}")

  except Exception as e:
    logger.error(f"✗ Error during testing: {e}")
    import traceback

    traceback.print_exc()
    return

  # ========================================================================
  # STEP 4: Show YAML usage
  # ========================================================================
  logger.info("\n[STEP 4] Using custom tools in YAML configuration...")
  logger.info("-" * 70)

  yaml_example = """
# weather_assistant.yaml
agent_class: LlmAgent
name: weather_assistant
model: gemini-2.5-flash

instruction: |
  You are a weather and calculation assistant.

tools:
  # ADK built-in tools
  - name: google_search
  
  # Custom tools (after registration)
  - name: get_weather
  - name: get_forecast
  - name: calculate
  - name: convert_units
"""

  logger.info(yaml_example)
  logger.info("-" * 70)
  logger.info("\nTo use with YAML:")
  logger.info("1. Save your agent configuration to a YAML file")
  logger.info("2. Register custom tools before running ADK:")
  logger.info("")
  logger.info("   # your_script.py")
  logger.info("   from example_custom_tools import CUSTOM_TOOLS")
  logger.info(
      "   from example_custom_tools.register_tools import register_custom_tools"
  )
  logger.info("")
  logger.info("   register_custom_tools(CUSTOM_TOOLS)")
  logger.info("")
  logger.info("3. Run: adk web /path/to/agents")

  # ========================================================================
  # Summary
  # ========================================================================
  logger.info("\n" + "=" * 70)
  logger.info("Summary")
  logger.info("=" * 70)
  logger.info("✓ Custom tools registered successfully")
  logger.info("✓ Agent created with custom tools")
  logger.info("✓ Custom tools work seamlessly in ADK")
  logger.info("✓ Ready to use in YAML configurations")
  logger.info("\nYour custom tools are now available as built-in tools!")
  logger.info("=" * 70)


if __name__ == "__main__":
  asyncio.run(main())
