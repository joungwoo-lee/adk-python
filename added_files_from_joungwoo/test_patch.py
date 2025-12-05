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
Test script to verify the ADK Agent Builder Assistant model patch.
"""

from __future__ import annotations

import os
import sys


def test_patch():
  """Test the model patch functionality."""
  print("=" * 60)
  print("Testing ADK Agent Builder Assistant Model Patch")
  print("=" * 60)
  
  # Set up test environment variables
  print("\n1. Setting environment variables...")
  os.environ["model"] = "gpt-4-test"
  os.environ["api_base"] = "https://test-api.example.com/v1"
  os.environ["api_key"] = "test-key-123"
  os.environ["x-dep-ticket"] = "test-ticket"
  os.environ["Send-System-Name"] = "Chain_Reaction"
  os.environ["User-Id"] = "joungwoo.lee"
  os.environ["User-Type"] = "AD_ID"
  print("   ✓ Environment variables set")
  
  # Import the patch
  print("\n2. Importing patch module...")
  try:
    import patch_adk_builder_model
    if patch_adk_builder_model._PATCH_APPLIED:
      print("   ✓ Patch imported and applied successfully")
    else:
      print("   ✗ Patch imported but NOT applied")
      return False
  except Exception as e:
    print(f"   ✗ Failed to import patch: {e}")
    return False
  
  # Try to import AgentBuilderAssistant
  print("\n3. Importing AgentBuilderAssistant...")
  try:
    try:
      from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import (
          AgentBuilderAssistant,
      )
      print("   ✓ Imported from pip-installed location")
    except ImportError:
      # Try development location
      from pathlib import Path
      repo_root = Path(__file__).parent
      samples_path = repo_root / "contributing" / "samples"
      if samples_path.exists():
        sys.path.insert(0, str(samples_path))
      
      from adk_agent_builder_assistant.agent_builder_assistant import (
          AgentBuilderAssistant,
      )
      print("   ✓ Imported from development location")
  except Exception as e:
    print(f"   ✗ Failed to import AgentBuilderAssistant: {e}")
    return False
  
  # Create agent with default settings (should use patched model)
  print("\n4. Creating agent with patched model...")
  try:
    agent = AgentBuilderAssistant.create_agent()
    print("   ✓ Agent created successfully")
  except Exception as e:
    print(f"   ✗ Failed to create agent: {e}")
    return False
  
  # Verify the model is LiteLlm
  print("\n5. Verifying model type...")
  from google.adk.models.lite_llm import LiteLlm
  
  if isinstance(agent.model, LiteLlm):
    print("   ✓ Agent is using LiteLlm model")
  else:
    print(f"   ✗ Agent is using wrong model type: {type(agent.model)}")
    return False
  
  # Verify model configuration
  print("\n6. Verifying model configuration...")
  print(f"   Model: {agent.model.model}")
  print(f"   API Base: {agent.model.api_base}")
  
  if agent.model.model == "gpt-4-test":
    print("   ✓ Model name matches")
  else:
    print(f"   ✗ Model name mismatch: {agent.model.model}")
    return False
  
  if agent.model.api_base == "https://test-api.example.com/v1":
    print("   ✓ API base matches")
  else:
    print(f"   ✗ API base mismatch: {agent.model.api_base}")
    return False
  
  # Check agent properties
  print("\n7. Verifying agent properties...")
  print(f"   Agent name: {agent.name}")
  print(f"   Agent description: {agent.description}")
  print(f"   Number of tools: {len(agent.tools)}")
  
  print("\n" + "=" * 60)
  print("✓ ALL TESTS PASSED!")
  print("=" * 60)
  return True


if __name__ == "__main__":
  success = test_patch()
  sys.exit(0 if success else 1)
