#!/bin/bash
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

# ADK Agent Builder Assistant - 커스텀 모델 패치를 적용한 ADK Web 실행 스크립트
#
# 사용법:
#   ./setup_patched_adk_web.sh [agents_directory]
#
# 예시:
#   ./setup_patched_adk_web.sh /path/to/agents
#   ./setup_patched_adk_web.sh .

set -e  # 에러 발생 시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로고 출력
echo -e "${BLUE}"
echo "================================================================"
echo "  ADK Agent Builder Assistant - 커스텀 모델 패치"
echo "  Gemini 2.5 Pro → 커스텀 LiteLlm 모델 오버라이드"
echo "================================================================"
echo -e "${NC}"

# 환경 변수 확인
echo -e "${YELLOW}[1/5] 환경 변수 확인 중...${NC}"

if [ -z "$model" ] || [ -z "$api_base" ]; then
  echo -e "${RED}✗ 오류: 필수 환경 변수가 설정되지 않았습니다.${NC}"
  echo ""
  echo "다음 환경 변수를 설정해주세요:"
  echo ""
  echo "  export model=\"your-model-name\""
  echo "  export api_base=\"https://your-api-base.com/v1\""
  echo "  export api_key=\"your-api-key\""
  echo "  export x-dep-ticket=\"your-ticket\""
  echo "  export Send-System-Name=\"Chain_Reaction\""
  echo "  export User-Id=\"joungwoo.lee\""
  echo "  export User-Type=\"AD_ID\""
  echo ""
  echo "그 후 다시 실행해주세요:"
  echo "  ./setup_patched_adk_web.sh [agents_directory]"
  echo ""
  exit 1
fi

echo -e "${GREEN}✓ 환경 변수 확인 완료${NC}"
echo "  - model: $model"
echo "  - api_base: $api_base"
echo "  - api_key: $(echo $api_key | cut -c1-4)****"
echo "  - x-dep-ticket: ${x_dep_ticket:-api_key (기본값)}"
echo "  - Send-System-Name: ${Send_System_Name:-Chain_Reaction (기본값)}"
echo "  - User-Id: ${User_Id:-joungwoo.lee (기본값)}"
echo "  - User-Type: ${User_Type:-AD_ID (기본값)}"

# google-adk 설치 확인
echo ""
echo -e "${YELLOW}[2/5] google-adk 설치 확인 중...${NC}"

if ! python -c "import google.adk" 2>/dev/null; then
  echo -e "${RED}✗ 오류: google-adk가 설치되어 있지 않습니다.${NC}"
  echo ""
  echo "다음 명령어로 설치해주세요:"
  echo "  pip install --upgrade google-adk"
  echo ""
  exit 1
fi

echo -e "${GREEN}✓ google-adk 설치 확인 완료${NC}"

# 패치 파일 경로 설정
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PATCH_FILE="$SCRIPT_DIR/patch_adk_builder_model.py"

echo ""
echo -e "${YELLOW}[3/5] 패치 파일 확인 중...${NC}"

if [ ! -f "$PATCH_FILE" ]; then
  echo -e "${RED}✗ 오류: 패치 파일을 찾을 수 없습니다: $PATCH_FILE${NC}"
  exit 1
fi

echo -e "${GREEN}✓ 패치 파일 확인 완료: $PATCH_FILE${NC}"

# PYTHONPATH에 패치 디렉토리 추가
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

echo ""
echo -e "${YELLOW}[4/5] PYTHONPATH 설정 완료${NC}"
echo "  PYTHONPATH: $PYTHONPATH"

# 에이전트 디렉토리 설정
AGENTS_DIR="${1:-.}"

if [ ! -d "$AGENTS_DIR" ]; then
  echo -e "${RED}✗ 오류: 에이전트 디렉토리를 찾을 수 없습니다: $AGENTS_DIR${NC}"
  echo ""
  echo "사용법: ./setup_patched_adk_web.sh [agents_directory]"
  echo ""
  exit 1
fi

echo ""
echo -e "${YELLOW}[5/5] ADK Web 실행 중...${NC}"
echo "  에이전트 디렉토리: $AGENTS_DIR"
echo ""

# Python 명령어로 패치를 임포트하고 ADK Web 실행
# -c 옵션으로 먼저 패치를 임포트한 후 adk web 실행
python -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')

# 패치 임포트
import patch_adk_builder_model

# ADK CLI 실행
from google.adk.cli import cli_tools_click

# adk web 명령어 실행
sys.argv = ['adk', 'web', '$AGENTS_DIR']
cli_tools_click.cli()
"

# 스크립트가 여기까지 도달하면 adk web이 종료된 것
echo ""
echo -e "${GREEN}ADK Web이 종료되었습니다.${NC}"
