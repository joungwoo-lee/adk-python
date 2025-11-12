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
ADK Agent Builder Assistant용 Gemini 2.5 Pro 모델 강제 패치

이 패치는 gemini-2.5-pro 모델을 사용자가 제공한 커스텀 LiteLlm 모델로 
자동으로 교체합니다.

사용 방법:
    패치 모듈을 임포트하기만 하면 자동으로 적용됩니다:
    
    ```python
    import patch_adk_builder_model  # 자동으로 패치 적용
    
    # 이제 ADK web이나 에이전트를 생성하면,
    # builder assistant가 커스텀 LiteLlm 모델을 사용합니다
    from google.adk.samples.adk_agent_builder_assistant import root_agent
    ```
    
    또는 환경 변수를 설정한 후 시작:
    
    ```bash
    export model="your-model-name"
    export api_base="https://your-api-base.com/v1"
    export api_key="your-api-key"
    export x-dep-ticket="your-ticket"
    export Send-System-Name="Chain_Reaction"
    export User-Id="joungwoo.lee"
    export User-Type="AD_ID"
    
    python -c "import patch_adk_builder_model; from google.adk.cli import cli_tools_click; cli_tools_click.cli()"
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
  """환경 변수를 사용하여 커스텀 LiteLlm 모델 생성.
  
  Returns:
    설정된 LiteLlm 인스턴스
    
  Raises:
    ValueError: 필수 환경 변수가 설정되지 않은 경우
  """
  model_name = os.getenv("model")
  api_base = os.getenv("api_base")
  api_key = os.getenv("api_key", "api_key")
  
  if not model_name or not api_base:
    raise ValueError(
        "환경 변수 'model'과 'api_base'는 필수입니다. "
        "예시: export model='gpt-4' && export api_base='https://api.openai.com/v1'"
    )
  
  logger.info(
      "커스텀 LiteLlm 모델 생성 중: model=%s, api_base=%s",
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
  """AgentBuilderAssistant.create_agent를 패치하여 커스텀 LiteLlm 사용.
  
  이 함수는 monkey patching을 사용하여 AgentBuilderAssistant의 create_agent 
  메서드를 교체합니다. gemini-2.5-pro 모델이 요청되면 자동으로 커스텀 
  LiteLlm 모델로 대체됩니다.
  
  Returns:
    bool: 패치 성공 여부
  """
  try:
    # pip으로 설치된 패키지 위치에서 임포트 시도
    try:
      from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import (
          AgentBuilderAssistant,
      )
      logger.info("pip 설치 패키지에서 AgentBuilderAssistant 로드 성공")
    except ImportError:
      # 개발 환경 위치에서 임포트 (contributing/samples)
      import sys
      from pathlib import Path
      
      # contributing/samples를 path에 추가
      repo_root = Path(__file__).parent.parent
      samples_path = repo_root / "contributing" / "samples"
      if samples_path.exists():
        sys.path.insert(0, str(samples_path))
        logger.info("개발 환경 samples 경로 추가: %s", samples_path)
      
      from adk_agent_builder_assistant.agent_builder_assistant import (
          AgentBuilderAssistant,
      )
      logger.info("개발 환경에서 AgentBuilderAssistant 로드 성공")
    
    # 원본 메서드 저장
    original_create_agent = AgentBuilderAssistant.create_agent
    
    # 커스텀 LiteLlm 모델 인스턴스 생성
    custom_model = create_custom_litelllm_model()
    
    @staticmethod
    @functools.wraps(original_create_agent)
    def patched_create_agent(
        model: Union[str, BaseLlm] = None,  # 무시됨
        working_directory: Optional[str] = None,
    ):
      """gemini-2.5-pro를 커스텀 LiteLlm 모델로 교체하는 패치된 create_agent.
      
      Args:
        model: 무시됨 - 대신 커스텀 LiteLlm 모델이 사용됩니다
        working_directory: 경로 해석을 위한 작업 디렉토리
        
      Returns:
        커스텀 LiteLlm 모델로 설정된 LlmAgent
      """
      # model이 gemini-2.5-pro 문자열이거나 None이면 커스텀 모델 사용
      if model is None or (isinstance(model, str) and "gemini-2.5-pro" in model):
        logger.info(
            "gemini-2.5-pro 감지 - 커스텀 LiteLlm 모델로 교체합니다"
        )
        effective_model = custom_model
      else:
        # 다른 모델이 명시적으로 지정된 경우 그대로 사용
        logger.info("명시적으로 지정된 모델 사용: %s", model)
        effective_model = model
      
      # 원본 메서드를 커스텀 모델과 함께 호출
      return original_create_agent.__func__(
          model=effective_model,
          working_directory=working_directory,
      )
    
    # 패치 적용
    AgentBuilderAssistant.create_agent = patched_create_agent
    
    logger.info(
        "AgentBuilderAssistant.create_agent 패치 성공 - "
        "gemini-2.5-pro → 커스텀 LiteLlm"
    )
    
    return True
    
  except ImportError as e:
    logger.error(
        "AgentBuilderAssistant 임포트 실패. "
        "google-adk가 설치되어 있는지 확인하세요: %s",
        e,
    )
    return False
  except Exception as e:
    logger.error("AgentBuilderAssistant 패치 실패: %s", e)
    return False


# 모듈 임포트 시 자동으로 패치 적용
_PATCH_APPLIED = patch_agent_builder_assistant()

if _PATCH_APPLIED:
  print("✓ ADK Agent Builder Assistant - gemini-2.5-pro → 커스텀 LiteLlm 모델로 패치 완료")
else:
  print("✗ ADK Agent Builder Assistant 패치 실패")
