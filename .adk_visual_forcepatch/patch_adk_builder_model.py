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
ADK Agent Builder Assistant용 Gemini 모델 강제 패치

이 패치는 모든 Gemini 모델(gemini-2.5-pro, gemini-2.5-flash 등)을
사용자가 제공한 커스텀 LiteLlm 모델로 자동으로 교체합니다.

지원 ADK 버전:
    - ADK 1.18.0+ (google.adk.built_in_agents 경로)
    - 구 버전 (google.adk.samples 경로)
    - 개발 환경 (contributing/samples 경로)

사용 방법:
    패치 모듈을 임포트하기만 하면 자동으로 적용됩니다:

    ```python
    import os
    os.environ["model"] = "openai/gpt-oss:20b"
    os.environ["api_base"] = "http://172.21.137.193:11434/v1"

    import patch_adk_builder_model  # 자동으로 패치 적용

    # 이제 ADK web이나 에이전트를 생성하면,
    # builder assistant가 커스텀 LiteLlm 모델을 사용합니다
    ```

    또는 환경 변수를 설정한 후 시작:

    ```bash
    export model="openai/gpt-oss:20b"
    export api_base="http://172.21.137.193:11434/v1"
    export api_key="api_key"
    export x-dep-ticket="api_key"
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
from pathlib import Path
from typing import Optional
from typing import Union

from google.adk.models.lite_llm import LiteLlm
from google.adk.models.base_llm import BaseLlm

logger = logging.getLogger(__name__)


def load_env_file():
  """패치 파일과 같은 디렉토리에서 .env 파일을 찾아 로드.

  .env 파일이 없으면 .env.example을 복사해서 .env를 생성합니다.

  Returns:
    bool: 환경 변수 로드 성공 여부
  """
  # 패치 파일이 있는 디렉토리 (설치 시 /root/adk_patch/)
  patch_dir = Path(__file__).parent
  env_file = patch_dir / ".env"
  env_example_file = patch_dir / ".env.example"

  # .env 파일이 없으면 .env.example에서 복사
  if not env_file.exists():
    if env_example_file.exists():
      try:
        import shutil
        shutil.copy(env_example_file, env_file)
        logger.info(f".env 파일이 없어서 .env.example을 복사했습니다: {env_file}")
      except Exception as e:
        logger.error(f".env.example 복사 실패: {e}")
        return False
    else:
      logger.error(
          f".env 파일과 .env.example 파일을 찾을 수 없습니다: {patch_dir}"
      )
      return False

  # .env 파일 로드
  if env_file.exists():
    logger.info(f".env 파일 로드 중: {env_file}")
    try:
      with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
          line = line.strip()
          # 주석이나 빈 줄 무시
          if not line or line.startswith('#'):
            continue
          # key=value 형식 파싱
          if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # 환경 변수 설정 (기존 값도 덮어씀)
            os.environ[key] = value
            logger.info(f"환경 변수 등록: {key}={value}")
      return True
    except Exception as e:
      logger.error(f".env 파일 로드 실패: {e}")
      return False

  return False


# .env 파일 자동 로드 시도
load_env_file()


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
  메서드를 교체합니다. gemini 모델이 요청되면 자동으로 커스텀
  LiteLlm 모델로 대체됩니다.

  Returns:
    bool: 패치 성공 여부
  """
  try:
    # pip으로 설치된 패키지 위치에서 임포트 시도 (ADK 1.18.0+)
    try:
      from google.adk.built_in_agents.adk_agent_builder_assistant.agent_builder_assistant import (
          AgentBuilderAssistant,
      )
      logger.info("pip 설치 패키지 (built_in_agents)에서 AgentBuilderAssistant 로드 성공")
    except ImportError:
      # 구 버전 경로 시도
      try:
        from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import (
            AgentBuilderAssistant,
        )
        logger.info("pip 설치 패키지 (samples)에서 AgentBuilderAssistant 로드 성공")
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
      # model이 gemini 계열이거나 None이면 커스텀 모델 사용
      # gemini-2.5-pro, gemini-2.5-flash, gemini-2.0-flash 등 모두 교체
      if model is None or (isinstance(model, str) and "gemini" in model.lower()):
        logger.info(
            "Gemini 모델 감지 (%s) - 커스텀 LiteLlm 모델로 교체합니다", model
        )
        effective_model = custom_model
      else:
        # 다른 모델이 명시적으로 지정된 경우 그대로 사용
        logger.info("명시적으로 지정된 모델 사용: %s", model)
        effective_model = model
      
      # 원본 메서드를 커스텀 모델과 함께 호출
      # staticmethod의 경우 __func__로 접근, 일반 함수는 직접 호출
      if hasattr(original_create_agent, '__func__'):
        return original_create_agent.__func__(
            model=effective_model,
            working_directory=working_directory,
        )
      else:
        return original_create_agent(
            model=effective_model,
            working_directory=working_directory,
        )
    
    # 패치 적용
    AgentBuilderAssistant.create_agent = patched_create_agent
    
    logger.info(
        "AgentBuilderAssistant.create_agent 패치 성공 - "
        "Gemini 모델 → 커스텀 LiteLlm (%s @ %s)",
        os.getenv("model"),
        os.getenv("api_base"),
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


def patch_llm_agent():
  """LlmAgent.__init__를 패치하여 모든 Gemini 모델을 커스텀 LiteLlm으로 교체.

  YAML 파일에서 model: gemini-2.5-flash 등으로 지정된 경우에도 적용됩니다.

  Returns:
    bool: 패치 성공 여부
  """
  try:
    from google.adk.agents import LlmAgent

    # 원본 __init__ 저장
    original_init = LlmAgent.__init__

    # 커스텀 LiteLlm 모델 생성
    custom_model = create_custom_litelllm_model()

    def patched_init(self, *args, model=None, **kwargs):
      """Gemini 모델을 커스텀 LiteLlm으로 교체하는 패치된 __init__."""
      # model이 gemini 계열 문자열이면 커스텀 모델로 교체
      if isinstance(model, str) and "gemini" in model.lower():
        logger.info(
            "LlmAgent: Gemini 모델 (%s) → 커스텀 LiteLlm 모델로 교체", model
        )
        model = custom_model

      # 원본 __init__ 호출
      return original_init(self, *args, model=model, **kwargs)

    # 패치 적용
    LlmAgent.__init__ = patched_init

    logger.info("LlmAgent.__init__ 패치 성공 - YAML 파일의 Gemini 모델도 교체됨")
    return True

  except Exception as e:
    logger.error("LlmAgent 패치 실패: %s", e)
    return False


def patch_llm_registry():
  """LLMRegistry.new_llm을 패치하여 모든 Gemini 모델 요청을 커스텀 LiteLlm으로 교체.

  이것이 가장 중요한 패치입니다! YAML에서 로드된 모든 "gemini-*" 문자열이
  LlmAgent.canonical_model을 통해 LLMRegistry.new_llm()으로 인스턴스화되므로,
  이 메서드를 패치하면 모든 경로의 Gemini 모델을 가로챌 수 있습니다.

  Returns:
    bool: 패치 성공 여부
  """
  try:
    from google.adk.models.registry import LLMRegistry

    # 원본 new_llm 저장
    original_new_llm = LLMRegistry.new_llm

    # 커스텀 LiteLlm 모델 생성
    custom_model = create_custom_litelllm_model()

    @staticmethod
    def patched_new_llm(model: str) -> BaseLlm:
      """Gemini 모델 요청을 커스텀 LiteLlm으로 교체하는 패치된 new_llm."""
      # model이 gemini 계열이면 커스텀 모델로 교체
      if isinstance(model, str) and "gemini" in model.lower():
        logger.info(
            "LLMRegistry.new_llm: Gemini 모델 (%s) → 커스텀 LiteLlm 모델로 교체", model
        )
        return custom_model

      # 다른 모델은 원본 메서드로 처리
      return original_new_llm(model)

    # 패치 적용
    LLMRegistry.new_llm = patched_new_llm

    logger.info(
        "LLMRegistry.new_llm 패치 성공 - "
        "YAML과 프로그래밍 방식의 모든 Gemini 모델 요청이 교체됨"
    )
    return True

  except Exception as e:
    logger.error("LLMRegistry 패치 실패: %s", e)
    return False


# 모듈 임포트 시 자동으로 패치 적용
_PATCH_APPLIED_BUILDER = patch_agent_builder_assistant()
_PATCH_APPLIED_LLM_AGENT = patch_llm_agent()
_PATCH_APPLIED_REGISTRY = patch_llm_registry()

_PATCH_APPLIED = _PATCH_APPLIED_BUILDER or _PATCH_APPLIED_LLM_AGENT or _PATCH_APPLIED_REGISTRY

if _PATCH_APPLIED:
  print(f"✓ ADK Gemini → 커스텀 LiteLlm 모델 패치 완료")
  print(f"  - Agent Builder Assistant: {'✓' if _PATCH_APPLIED_BUILDER else '✗'}")
  print(f"  - LlmAgent (YAML support): {'✓' if _PATCH_APPLIED_LLM_AGENT else '✗'}")
  print(f"  - LLMRegistry (전체 경로): {'✓' if _PATCH_APPLIED_REGISTRY else '✗'}")
  print(f"  Model: {os.getenv('model')}")
  print(f"  API Base: {os.getenv('api_base')}")
else:
  print("✗ ADK 패치 실패")
