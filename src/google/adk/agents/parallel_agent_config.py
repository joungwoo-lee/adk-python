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

"""Parallel agent implementation."""

from __future__ import annotations

from typing import Any

from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator

from ..utils.feature_decorator import experimental
from .base_agent_config import BaseAgentConfig


@experimental
class ParallelAgentConfig(BaseAgentConfig):
  """The config for the YAML schema of a ParallelAgent."""

  model_config = ConfigDict(
      extra="ignore",
  )

  agent_class: str = Field(
      default="ParallelAgent",
      description=(
          "The value is used to uniquely identify the ParallelAgent class."
      ),
  )

  @model_validator(mode='before')
  @classmethod
  def strip_workflow_agent_fields(cls, data: Any) -> Any:
    """Remove fields that workflow agents should not have.

    ParallelAgent orchestrates sub-agents and should not define model, tools,
    or instruction fields. This validator automatically removes these fields
    if present in the input data (e.g., from YAML files).

    Args:
      data: The input data dictionary from YAML or other sources.

    Returns:
      The cleaned data dictionary with workflow-incompatible fields removed.
    """
    if isinstance(data, dict):
      # Remove fields that are not applicable to workflow agents
      for field in ('model', 'tools', 'instruction'):
        data.pop(field, None)
    return data
