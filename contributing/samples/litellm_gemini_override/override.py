"""LiteLLM 기반 커스텀 모델로 `gemini-2.5-flash`를 오버라이드합니다."""

from __future__ import annotations

import os

from google.adk.models import LLMRegistry
from google.adk.models.lite_llm import LiteLlm


class LiteLlmGemini25Override(LiteLlm):
  """환경 변수 기반 LiteLLM 설정으로 `gemini-2.5-flash`를 대체합니다."""

  @classmethod
  def supported_models(cls) -> list[str]:
    # 정확히 gemini-2.5-flash 문자열과 매칭해 기존 Gemini 클래스를 덮어씁니다.
    return [r'gemini-2\.5-flash']

  def __init__(self, model: str, **kwargs):
    """환경 변수 값을 LiteLLM 초기화 인자로 주입합니다."""
    resolved_model = os.getenv('model', model)
    resolved_api_base = os.getenv('api_base', kwargs.pop('api_base', None))
    resolved_api_key = os.getenv('api_key', kwargs.pop('api_key', 'api_key'))

    extra_headers = kwargs.pop('extra_headers', {}) or {}
    env_headers = {
        'x-dep-ticket': os.getenv('x-dep-ticket', 'api_key'),
        'Send-System-Name': os.getenv('Send-System-Name', 'Chain_Reaction'),
        'User-Id': os.getenv('User-Id', 'joungwoo.lee'),
        'User-Type': os.getenv('User-Type', 'AD_ID'),
    }
    # 환경 변수 우선, 코드에서 직접 넘긴 값이 있다면 병합합니다.
    merged_headers = {**extra_headers, **env_headers}

    super().__init__(
        model=resolved_model,
        api_base=resolved_api_base,
        api_key=resolved_api_key,
        extra_headers=merged_headers,
        **kwargs,
    )


# 모듈이 임포트되는 즉시 레지스트리에 등록해 기본 Gemini 클래스를 대체합니다.
LLMRegistry.register(LiteLlmGemini25Override)
