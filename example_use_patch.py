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

"""
Example usage of the ADK Agent Builder Assistant model patch.

This demonstrates how to use the patch to replace the default model
with a custom LiteLlm configuration.
"""

from __future__ import annotations

import os

# Set environment variables BEFORE importing the patch
os.environ["model"] = "gpt-4"  # Your model name
os.environ["api_base"] = "https://api.openai.com/v1"  # Your API base URL
os.environ["api_key"] = "your-api-key-here"  # Your API key
os.environ["x-dep-ticket"] = "your-ticket"  # Optional custom header
os.environ["Send-System-Name"] = "Chain_Reaction"  # Optional custom header
os.environ["User-Id"] = "joungwoo.lee"  # Optional custom header
os.environ["User-Type"] = "AD_ID"  # Optional custom header

# Import the patch - this automatically applies the monkey patch
import patch_adk_builder_model

# Now when you use the Agent Builder Assistant, it will use your custom model
from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import (
    AgentBuilderAssistant,
)

# Create agent - will use your LiteLlm configuration automatically
agent = AgentBuilderAssistant.create_agent()

print(f"Agent created: {agent.name}")
print(f"Agent model: {agent.model}")
print("Model type:", type(agent.model))
