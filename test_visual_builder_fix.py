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

"""Test script for visual builder model field fix."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import yaml


def test_remove_model_field():
  """Test the model field removal logic."""
  
  # Test YAML with ParallelAgent containing model field
  test_yaml_content = """
agent_class: ParallelAgent
name: test_parallel
model: gemini-2.5-flash
description: Test parallel agent
sub_agents:
  - agent_class: LlmAgent
    name: sub_agent_1
    model: gemini-2.5-flash
    instruction: Test instruction 1
  - agent_class: LoopAgent
    name: sub_agent_2
    model: gemini-2.5-flash
    max_iterations: 3
    sub_agents:
      - agent_class: LlmAgent
        name: nested_agent
        model: gemini-2.5-flash
        instruction: Nested instruction
  - agent_class: SequentialAgent
    name: sub_agent_3
    model: gemini-2.5-pro
    sub_agents:
      - agent_class: LlmAgent
        name: seq_sub_1
        model: gemini-2.5-flash
        instruction: Sequential sub instruction
"""
  
  # Agent types that should not have model field
  agent_types_without_model = {
      'ParallelAgent', 
      'LoopAgent', 
      'SequentialAgent'
  }
  
  def remove_model_recursive(obj):
    """Recursively remove model field from agent configs."""
    if not isinstance(obj, dict):
      return
    
    # Check if this is an agent config with agent_class
    agent_class = obj.get('agent_class', '')
    if agent_class in agent_types_without_model and 'model' in obj:
      print(f"Removing 'model' field from {agent_class}")
      del obj['model']
    
    # Recursively process sub_agents
    if 'sub_agents' in obj and isinstance(obj['sub_agents'], list):
      for sub_agent in obj['sub_agents']:
        remove_model_recursive(sub_agent)
  
  # Create a temp file for testing
  with tempfile.NamedTemporaryFile(
      mode='w', 
      suffix='.yaml', 
      delete=False
  ) as f:
    f.write(test_yaml_content)
    temp_file = f.name
  
  try:
    # Load and process the YAML
    with open(temp_file, 'r', encoding='utf-8') as f:
      data = yaml.safe_load(f)
    
    print("\n=== Original YAML ===")
    print(yaml.dump(data, default_flow_style=False))
    
    # Remove model fields
    remove_model_recursive(data)
    
    print("\n=== Processed YAML ===")
    print(yaml.dump(data, default_flow_style=False))
    
    # Verify results
    assert 'model' not in data, "ParallelAgent should not have model field"
    
    # Check sub_agents
    for sub_agent in data.get('sub_agents', []):
      agent_class = sub_agent.get('agent_class', '')
      if agent_class == 'LlmAgent':
        assert 'model' in sub_agent, f"LlmAgent should keep model field"
      elif agent_class in agent_types_without_model:
        assert 'model' not in sub_agent, (
            f"{agent_class} should not have model field"
        )
        
        # Check nested sub_agents
        for nested in sub_agent.get('sub_agents', []):
          nested_class = nested.get('agent_class', '')
          if nested_class in agent_types_without_model:
            assert 'model' not in nested, (
                f"Nested {nested_class} should not have model field"
            )
    
    print("\n✅ All tests passed!")
    return True
    
  finally:
    # Clean up
    if os.path.exists(temp_file):
      os.remove(temp_file)


def test_patch_loading():
  """Test if the visual builder patch can be loaded."""
  workspace_root = Path.cwd()
  patch_dir = workspace_root / ".adk_visual_forcepatch"
  patch_file = patch_dir / "patch_adk_builder_model.py"
  
  print("\n=== Checking Visual Builder Patch ===")
  print(f"Workspace root: {workspace_root}")
  print(f"Patch directory: {patch_dir}")
  print(f"Patch file: {patch_file}")
  
  if patch_file.exists():
    print("✅ Visual builder patch file found")
    
    # Check if .env or .env.example exists
    env_file = patch_dir / ".env"
    env_example = patch_dir / ".env.example"
    
    if env_file.exists():
      print(f"✅ .env file found: {env_file}")
    elif env_example.exists():
      print(f"✅ .env.example file found: {env_example}")
      print("   (Will be copied to .env on first use)")
    else:
      print("⚠️  No .env or .env.example file found")
    
    return True
  else:
    print(f"ℹ️  Visual builder patch not found at {patch_file}")
    print("   This is optional and only needed for custom LLM integration")
    return False


if __name__ == '__main__':
  print("=" * 60)
  print("Visual Builder Model Field Fix - Test Suite")
  print("=" * 60)
  
  # Test 1: Model field removal
  print("\n[Test 1] Testing model field removal logic")
  test_remove_model_field()
  
  # Test 2: Patch loading
  print("\n[Test 2] Testing patch file detection")
  test_patch_loading()
  
  print("\n" + "=" * 60)
  print("All tests completed successfully!")
  print("=" * 60)
