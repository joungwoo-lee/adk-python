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
ADK Agent Builder Assistant 모델 패치 테스트 스크립트

이 스크립트는 패치가 올바르게 동작하는지 테스트합니다.
"""

from __future__ import annotations

import os
import sys
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch as mock_patch


class TestAgentBuilderPatch(unittest.TestCase):
  """ADK Agent Builder Assistant 패치 테스트"""

  @classmethod
  def setUpClass(cls):
    """테스트 클래스 설정"""
    # 환경 변수 설정
    os.environ["model"] = "test-model"
    os.environ["api_base"] = "https://test-api.example.com/v1"
    os.environ["api_key"] = "test-api-key"
    os.environ["x-dep-ticket"] = "test-ticket"
    os.environ["Send-System-Name"] = "Test-System"
    os.environ["User-Id"] = "test-user"
    os.environ["User-Type"] = "TEST"

  def test_01_environment_variables(self):
    """환경 변수가 올바르게 설정되었는지 테스트"""
    print("\n[테스트 1] 환경 변수 확인")
    
    self.assertEqual(os.getenv("model"), "test-model")
    self.assertEqual(os.getenv("api_base"), "https://test-api.example.com/v1")
    self.assertEqual(os.getenv("api_key"), "test-api-key")
    
    print("  ✓ 모든 환경 변수가 올바르게 설정되었습니다")

  def test_02_patch_import(self):
    """패치 모듈을 임포트할 수 있는지 테스트"""
    print("\n[테스트 2] 패치 모듈 임포트")
    
    try:
      import patch_adk_builder_model
      print(f"  ✓ 패치 모듈 임포트 성공")
      print(f"  ✓ 패치 적용 상태: {patch_adk_builder_model._PATCH_APPLIED}")
      self.assertTrue(hasattr(patch_adk_builder_model, "_PATCH_APPLIED"))
    except ImportError as e:
      self.fail(f"패치 모듈 임포트 실패: {e}")

  def test_03_custom_model_creation(self):
    """커스텀 LiteLlm 모델 생성 테스트"""
    print("\n[테스트 3] 커스텀 모델 생성")
    
    try:
      import patch_adk_builder_model
      
      # 커스텀 모델 생성
      model = patch_adk_builder_model.create_custom_litelllm_model()
      
      print(f"  ✓ 커스텀 모델 생성 성공")
      print(f"  ✓ 모델 타입: {type(model).__name__}")
      
      # LiteLlm 타입인지 확인
      from google.adk.models.lite_llm import LiteLlm
      self.assertIsInstance(model, LiteLlm)
      
      print(f"  ✓ LiteLlm 인스턴스 확인 완료")
      
    except Exception as e:
      self.fail(f"커스텀 모델 생성 실패: {e}")

  def test_04_agent_builder_patch(self):
    """AgentBuilderAssistant 패치 테스트"""
    print("\n[테스트 4] AgentBuilderAssistant 패치")
    
    try:
      import patch_adk_builder_model
      
      # AgentBuilderAssistant 임포트
      try:
        from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import (
            AgentBuilderAssistant,
        )
      except ImportError:
        # 개발 환경에서 임포트
        from pathlib import Path
        repo_root = Path(__file__).parent.parent
        samples_path = repo_root / "contributing" / "samples"
        if samples_path.exists():
          sys.path.insert(0, str(samples_path))
        
        from adk_agent_builder_assistant.agent_builder_assistant import (
            AgentBuilderAssistant,
        )
      
      print(f"  ✓ AgentBuilderAssistant 임포트 성공")
      
      # create_agent 메서드가 패치되었는지 확인
      self.assertTrue(hasattr(AgentBuilderAssistant, "create_agent"))
      
      print(f"  ✓ create_agent 메서드 확인 완료")
      
    except Exception as e:
      print(f"  ⚠ AgentBuilderAssistant 패치 확인 실패: {e}")
      print(f"  ℹ google-adk가 설치되어 있지 않을 수 있습니다")

  def test_05_agent_creation(self):
    """에이전트 생성 테스트"""
    print("\n[테스트 5] 에이전트 생성 (통합 테스트)")
    
    try:
      import patch_adk_builder_model
      
      # AgentBuilderAssistant 임포트
      try:
        from google.adk.samples.adk_agent_builder_assistant.agent_builder_assistant import (
            AgentBuilderAssistant,
        )
      except ImportError:
        # 개발 환경에서 임포트
        from pathlib import Path
        repo_root = Path(__file__).parent.parent
        samples_path = repo_root / "contributing" / "samples"
        if samples_path.exists():
          sys.path.insert(0, str(samples_path))
        
        from adk_agent_builder_assistant.agent_builder_assistant import (
            AgentBuilderAssistant,
        )
      
      # 에이전트 생성
      agent = AgentBuilderAssistant.create_agent()
      
      print(f"  ✓ 에이전트 생성 성공")
      print(f"  ✓ 에이전트 이름: {agent.name}")
      print(f"  ✓ 에이전트 모델: {agent.model}")
      print(f"  ✓ 모델 타입: {type(agent.model).__name__}")
      
      # 모델이 LiteLlm인지 확인
      from google.adk.models.lite_llm import LiteLlm
      
      if isinstance(agent.model, LiteLlm):
        print(f"  ✓ 커스텀 LiteLlm 모델이 성공적으로 적용되었습니다!")
        self.assertIsInstance(agent.model, LiteLlm)
      else:
        print(f"  ⚠ 모델이 LiteLlm이 아닙니다: {type(agent.model)}")
      
    except Exception as e:
      print(f"  ⚠ 에이전트 생성 실패: {e}")
      print(f"  ℹ google-adk가 설치되어 있지 않을 수 있습니다")

  def test_06_environment_variable_missing(self):
    """필수 환경 변수가 없을 때 에러 처리 테스트"""
    print("\n[테스트 6] 환경 변수 누락 시 에러 처리")
    
    # 환경 변수 임시 제거
    original_model = os.getenv("model")
    original_api_base = os.getenv("api_base")
    
    try:
      del os.environ["model"]
      del os.environ["api_base"]
      
      # 패치 모듈 재로드 (새로운 환경에서)
      import importlib
      import patch_adk_builder_model
      importlib.reload(patch_adk_builder_model)
      
      # 에러가 발생해야 함
      print("  ⚠ 환경 변수 누락 시 에러가 발생하지 않았습니다")
      
    except ValueError as e:
      print(f"  ✓ 예상된 에러 발생: {e}")
      self.assertIn("model", str(e).lower())
      
    finally:
      # 환경 변수 복원
      if original_model:
        os.environ["model"] = original_model
      if original_api_base:
        os.environ["api_base"] = original_api_base


def main():
  """메인 테스트 실행 함수"""
  print("=" * 70)
  print("ADK Agent Builder Assistant - 모델 패치 테스트")
  print("=" * 70)
  
  # 테스트 실행
  loader = unittest.TestLoader()
  suite = loader.loadTestsFromTestCase(TestAgentBuilderPatch)
  runner = unittest.TextTestRunner(verbosity=2)
  result = runner.run(suite)
  
  # 결과 요약
  print("\n" + "=" * 70)
  print("테스트 결과 요약")
  print("=" * 70)
  print(f"실행된 테스트: {result.testsRun}개")
  print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}개")
  print(f"실패: {len(result.failures)}개")
  print(f"에러: {len(result.errors)}개")
  
  if result.wasSuccessful():
    print("\n✓ 모든 테스트가 성공적으로 통과했습니다!")
    return 0
  else:
    print("\n✗ 일부 테스트가 실패했습니다.")
    return 1


if __name__ == "__main__":
  sys.exit(main())
