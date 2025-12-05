#!/bin/bash
# ADK Custom LLM Patch - 도커 내부 설치 스크립트
# 도커 컨테이너 안에서 직접 실행됩니다.

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "================================================================"
echo "  ADK Custom LLM Patch - 도커 내부 설치"
echo "  Gemini 모델 → 커스텀 LiteLlm 자동 교체"
echo "================================================================"
echo -e "${NC}"

# 스크립트 위치 확인
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PATCH_FILE="$SCRIPT_DIR/patch_adk_builder_model.py"
ENV_EXAMPLE_FILE="$SCRIPT_DIR/.env.example"

echo -e "${YELLOW}[1/4] 패치 파일 확인...${NC}"
if [ ! -f "$PATCH_FILE" ]; then
    echo -e "${RED}✗ 패치 파일을 찾을 수 없습니다: $PATCH_FILE${NC}"
    exit 1
fi
if [ ! -f "$ENV_EXAMPLE_FILE" ]; then
    echo -e "${RED}✗ .env.example 파일을 찾을 수 없습니다: $ENV_EXAMPLE_FILE${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 패치 파일 확인: $PATCH_FILE${NC}"
echo -e "${GREEN}✓ .env.example 파일 확인: $ENV_EXAMPLE_FILE${NC}"

# 패치 디렉토리 생성 및 파일 복사
echo ""
echo -e "${YELLOW}[2/4] 패치 파일 설치...${NC}"
mkdir -p /root/adk_patch
cp "$PATCH_FILE" /root/adk_patch/
cp "$ENV_EXAMPLE_FILE" /root/adk_patch/
echo -e "${GREEN}✓ 패치 파일 복사 완료: /root/adk_patch/patch_adk_builder_model.py${NC}"
echo -e "${GREEN}✓ .env.example 파일 복사 완료: /root/adk_patch/.env.example${NC}"

# sitecustomize.py 설치
echo ""
echo -e "${YELLOW}[3/4] sitecustomize.py 설치...${NC}"
cat > /usr/lib/python3.10/sitecustomize.py << 'EOF'
import os
import sys

# 패치를 로드하기 전에 항상 시도 (.env 파일이 자동으로 로드됨)
try:
    sys.path.insert(0, "/root/adk_patch")
    import patch_adk_builder_model
except Exception as e:
    # .env 파일이 없거나 환경 변수가 없으면 조용히 무시
    pass
EOF
echo -e "${GREEN}✓ sitecustomize.py 설치 완료: /usr/lib/python3.10/sitecustomize.py${NC}"

# .env 파일 확인 및 안내
echo ""
echo -e "${YELLOW}[4/4] 환경 변수 설정 확인...${NC}"

ENV_FILE="/root/adk_patch/.env"

# .env 파일이 없으면 .env.example에서 자동 생성될 것임을 안내
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}ℹ .env 파일이 없습니다. 패치 실행 시 .env.example에서 자동 생성됩니다.${NC}"
    echo -e "${GREEN}✓ 환경 변수는 /root/adk_patch/.env.example 기본값을 사용합니다${NC}"
else
    echo -e "${GREEN}✓ 기존 .env 파일 발견: $ENV_FILE${NC}"
fi

# 테스트
echo ""
echo -e "${YELLOW}패치 테스트 중...${NC}"
TEST_RESULT=$(python -c "
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

agent = LlmAgent(name='test', model='gemini-2.5-flash', instruction='test')
print('SUCCESS' if isinstance(agent.model, LiteLlm) else 'FAILED')
" 2>&1 | grep -E "(SUCCESS|FAILED|✓)" || echo "TEST_ERROR")

if echo "$TEST_RESULT" | grep -q "SUCCESS"; then
    echo -e "${GREEN}✓ 패치 테스트 성공!${NC}"
    echo "$TEST_RESULT"
else
    echo -e "${YELLOW}⚠ 패치 테스트를 완료하지 못했습니다${NC}"
    echo "출력: $TEST_RESULT"
fi

# 완료 메시지
echo ""
echo -e "${BLUE}================================================================${NC}"
echo -e "${GREEN}✓✓✓ 설치 완료! ✓✓✓${NC}"
echo -e "${BLUE}================================================================${NC}"
echo ""
echo "패치가 성공적으로 설치되었습니다!"
echo ""
echo "📋 설치된 파일:"
echo "   - /root/adk_patch/patch_adk_builder_model.py"
echo "   - /root/adk_patch/.env.example"
if [ -f "/root/adk_patch/.env" ]; then
    echo "   - /root/adk_patch/.env (기존 파일 사용)"
else
    echo "   - /root/adk_patch/.env (패치 실행 시 자동 생성)"
fi
echo "   - /usr/lib/python3.10/sitecustomize.py"
echo ""
echo "🚀 ADK 실행 방법:"
echo "   cd /root/chainreaction  # 또는 프로젝트 디렉토리"
echo "   adk web . --host 0.0.0.0 --port 38010 --allow_origins=\"*\" --reload --reload_agents"
echo ""
echo "🔧 환경 변수 변경:"
echo "   vi /root/adk_patch/.env"
echo ""
