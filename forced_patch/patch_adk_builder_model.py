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
Monkey patch for ADK Agent Builder Assistant to use custom LiteLlm model.

Usage:
    Simply import this module before using the Agent Builder Assistant:
    
    ```python
    import patch_adk_builder_model  # This applies the patch automatically
    
    # Now when you use ADK web or create agents, 
    # the builder assistant will use your custom LiteLlm model
    from google.adk.samples.adk_agent_builder_assistant import root_agent
    ```
    
    Or set environment variables before starting:
    
    ```bash
    export model="your-model-name"
    export api_base="https://your-api-base.com/v1"
    export api_key="your-api-key"
    export x-dep-ticket="your-ticket"
    export Send-System-Name="Chain_Reaction"
    export User-Id="joungwoo.lee"
    export User-Type="AD_ID"
    
    adk web path/to/agents
    ```
"""

from __future__ import annotations

import functools
import logging
import os
from typing import Optional
from typing import Union

from google.adk.models.lite_llm import LiteLlm
from google.adk.models.base_llm import BaseLlm

logger = logging.getLogger(__name__)


def create_custom_litelllm_model() -> LiteLlm:
  """Create LiteLlm model with environment variables.
  
  Returns:
    Configured LiteLlm instance
  """
  model_name = os.getenv("model")
  api_base = os.getenv("api_base")
  api_key = os.getenv("api_key", "api_key")
  
  if not model_name or not api_base:
    raise ValueError(
        "Environment variables 'model' and 'api_base' must be set. "
        "Example: export model='gpt-4' and export api_base='https://api.openai.com/v1'"
    )
  
  logger.info(
      "Creating LiteLlm model with model=%s, api_base=%s",
      model_name,
      api_base,
  )
  
  return LiteLlm(
      model=model_name,
      api_base=api_base,
      api_key=api_key,
      extra_headers={
          "x-dep-ticket": os.getenv("x-dep-ticket", "api_key"),
          "Send-System-Name": os.getenv("Send-System-Name", "Chain_Reaction"),
          "User-Id": os.getenv("User-Id", "joungwoo.lee"),
          "User-Type": os.getenv("User-Type", "AD_ID"),
      },
  )


def patch_agent_builder_assistant():
  """Monkey patch AgentBuilderAssistant.create_agent to use custom LiteLlm."""
  try:
    # Try to import from installed package location
    # This works when google-adk is installed via pip
    try:
      from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import (
          AgentBuilderAssistant,
      )
    except ImportError:
      # Fallback to development location (contributing/samples)
      import sys
      from pathlib import Path
      
      # Add contributing/samples to path if not already there
      repo_root = Path(__file__).parent
      samples_path = repo_root / "contributing" / "samples"
      if samples_path.exists():
        sys.path.insert(0, str(samples_path))
      
      from adk_agent_builder_assistant.agent_builder_assistant import (
          AgentBuilderAssistant,
      )
    
    # Store original method
    original_create_agent = AgentBuilderAssistant.create_agent
    
    # Create custom LiteLlm model instance
    custom_model = create_custom_litelllm_model()
    
    @staticmethod
    @functools.wraps(original_create_agent)
    def patched_create_agent(
        model: Union[str, BaseLlm] = None,  # Accept but ignore
        working_directory: Optional[str] = None,
    ):
      """Patched create_agent that always uses custom LiteLlm model.
      
      Args:
        model: Ignored - custom LiteLlm model is used instead
        working_directory: Working directory for path resolution
        
      Returns:
        LlmAgent configured with custom LiteLlm model
      """
      logger.info("Using patched AgentBuilderAssistant with custom LiteLlm model")
      
      # Call original method with our custom model
      return original_create_agent.__func__(
          model=custom_model,
          working_directory=working_directory,
      )
    
    # Apply the patch
    AgentBuilderAssistant.create_agent = patched_create_agent
    
    logger.info(
        "Successfully patched AgentBuilderAssistant.create_agent to use custom LiteLlm model"
    )
    
    return True
    
  except ImportError as e:
    logger.error(
        "Failed to import AgentBuilderAssistant. "
        "Make sure google-adk is installed: %s",
        e,
    )
    return False
  except Exception as e:
    logger.error("Failed to patch AgentBuilderAssistant: %s", e)
    return False


# Automatically apply patch when module is imported
_PATCH_APPLIED = patch_agent_builder_assistant()

if _PATCH_APPLIED:
  print("✓ ADK Agent Builder Assistant patched to use custom LiteLlm model")
else:
  print("✗ Failed to patch ADK Agent Builder Assistant")
