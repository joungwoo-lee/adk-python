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
ADK Agent Builder Assistant 모델 패치 사용 예시

이 스크립트는 gemini-2.5-pro 모델을 커스텀 LiteLlm 설정으로 
교체하는 방법을 보여줍니다.
"""

from __future__ import annotations

import os
import sys

# 패치 적용 전에 환경 변수 설정
print("=" * 60)
print("ADK Agent Builder Assistant - 모델 패치 예시")
print("=" * 60)

# 환경 변수 설정 (실제 사용 시 여기에 실제 값을 넣으세요)
os.environ["model"] = os.getenv("model", "gpt-4")  # 여기에 실제 모델 이름 설정
os.environ["api_base"] = os.getenv(
    "api_base", "https://api.openai.com/v1"
)  # 여기에 실제 API 베이스 URL 설정
os.environ["api_key"] = os.getenv("api_key", "your-api-key-here")  # API 키
os.environ["x-dep-ticket"] = os.getenv("x-dep-ticket", "your-ticket")  # DEP 티켓
os.environ["Send-System-Name"] = os.getenv(
    "Send-System-Name", "Chain_Reaction"
)  # 시스템 이름
os.environ["User-Id"] = os.getenv("User-Id", "joungwoo.lee")  # 사용자 ID
os.environ["User-Type"] = os.getenv("User-Type", "AD_ID")  # 사용자 타입

print("\n📝 환경 변수 설정:")
print(f"  - model: {os.environ['model']}")
print(f"  - api_base: {os.environ['api_base']}")
print(f"  - api_key: {'*' * 8} (숨김)")
print(f"  - x-dep-ticket: {os.environ['x-dep-ticket']}")
print(f"  - Send-System-Name: {os.environ['Send-System-Name']}")
print(f"  - User-Id: {os.environ['User-Id']}")
print(f"  - User-Type: {os.environ['User-Type']}")

# 패치 임포트 - 자동으로 적용됨
print("\n🔧 패치 임포트 중...")
try:
  import patch_adk_builder_model
  
  print(f"✓ 패치 적용 상태: {patch_adk_builder_model._PATCH_APPLIED}")
except ImportError as e:
  print(f"✗ 패치 임포트 실패: {e}")
  print("\n패치 파일이 현재 디렉토리 또는 PYTHONPATH에 있는지 확인하세요.")
  sys.exit(1)

# 이제 Agent Builder Assistant를 사용하면 커스텀 모델이 적용됩니다
print("\n🤖 Agent Builder Assistant 생성 중...")
try:
  from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import (
      AgentBuilderAssistant,
  )
  
  # 에이전트 생성 - gemini-2.5-pro 대신 커스텀 모델 사용
  agent = AgentBuilderAssistant.create_agent()
  
  print(f"\n✓ 에이전트 생성 완료:")
  print(f"  - 이름: {agent.name}")
  print(f"  - 모델: {agent.model}")
  print(f"  - 모델 타입: {type(agent.model).__name__}")
  
  # 모델이 LiteLlm인지 확인
  from google.adk.models.lite_llm import LiteLlm
  
  if isinstance(agent.model, LiteLlm):
    print(f"\n✓ 성공! 커스텀 LiteLlm 모델이 적용되었습니다.")
    print(f"  - LiteLlm 모델 이름: {agent.model.model_name}")
  else:
    print(f"\n⚠ 경고: 모델이 LiteLlm이 아닙니다.")
    print(f"  - 실제 모델 타입: {type(agent.model)}")
  
  # 도구 목록 출력
  print(f"\n🔧 사용 가능한 도구 ({len(agent.tools)}개):")
  for i, tool in enumerate(agent.tools[:5], 1):
    print(f"  {i}. {tool}")
  if len(agent.tools) > 5:
    print(f"  ... 외 {len(agent.tools) - 5}개")
  
except ImportError as e:
  print(f"\n✗ AgentBuilderAssistant 임포트 실패: {e}")
  print("\ngoogle-adk가 설치되어 있는지 확인하세요:")
  print("  pip install --upgrade google-adk")
  sys.exit(1)
except Exception as e:
  print(f"\n✗ 에이전트 생성 실패: {e}")
  import traceback
  traceback.print_exc()
  sys.exit(1)

print("\n" + "=" * 60)
print("✓ 예시 실행 완료!")
print("=" * 60)
print("\n다음 단계:")
print("1. 실제 API 키와 엔드포인트를 환경 변수에 설정하세요")
print("2. ADK Web UI에서 사용하려면:")
print("   ./setup_patched_adk_web.sh path/to/agents")
print("3. Python 스크립트에서 사용하려면:")
print("   import patch_adk_builder_model")
print("   from google.adk.samples.adk_agent_builder_assistant import root_agent")
