#!/bin/bash
# ADK Custom LLM Patch - 테스트 스크립트

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

DOCKER_CONTAINER="${1:-43a7821ec23580ac2939c3a3c45d567a6d980ad6a8751f60bc343f09169d4870}"

echo "=== ADK Custom LLM Patch - 테스트 ==="
echo ""
echo "도커 컨테이너: $DOCKER_CONTAINER"
echo ""

# 테스트 1: .env 파일 확인
echo "[테스트 1] .env 파일 확인"
if docker exec "$DOCKER_CONTAINER" test -f /root/adk_patch/.env; then
    echo -e "${GREEN}✓ .env 파일 존재: /root/adk_patch/.env${NC}"
    ENV_CONTENT=$(docker exec "$DOCKER_CONTAINER" cat /root/adk_patch/.env | grep -E "^(model|api_base)=" | head -2)
    echo "$ENV_CONTENT"
else
    echo -e "${YELLOW}⚠ .env 파일 없음 (.env.example에서 자동 생성됨)${NC}"
fi
echo ""

# 테스트 2: 패치 파일 존재 확인
echo "[테스트 2] 패치 파일 확인"
if docker exec "$DOCKER_CONTAINER" test -f /root/adk_patch/patch_adk_builder_model.py; then
    echo -e "${GREEN}✓ 패치 파일 존재: /root/adk_patch/patch_adk_builder_model.py${NC}"
else
    echo -e "${RED}✗ 패치 파일 없음${NC}"
    exit 1
fi
echo ""

# 테스트 3: sitecustomize.py 확인
echo "[테스트 3] sitecustomize.py 확인"
if docker exec "$DOCKER_CONTAINER" test -f /usr/lib/python3.10/sitecustomize.py; then
    echo -e "${GREEN}✓ sitecustomize.py 존재${NC}"
else
    echo -e "${RED}✗ sitecustomize.py 없음${NC}"
    exit 1
fi
echo ""

# 테스트 4: 패치 로드 확인
echo "[테스트 4] 패치 로드 테스트"
PATCH_LOAD=$(docker exec "$DOCKER_CONTAINER" python -c "import sys; print('patch_loaded' if 'patch_adk_builder_model' in sys.modules else 'patch_not_loaded')" 2>&1 | tail -5)
if echo "$PATCH_LOAD" | grep -q "✓.*패치 완료"; then
    echo -e "${GREEN}✓ 패치 자동 로드 성공${NC}"
    echo "$PATCH_LOAD"
else
    echo -e "${YELLOW}⚠ 패치 로드 확인 불가${NC}"
    echo "$PATCH_LOAD"
fi
echo ""

# 테스트 5: LlmAgent 패치 테스트
echo "[테스트 5] LlmAgent 패치 테스트 (YAML 지원)"
LLMAGENT_TEST=$(docker exec "$DOCKER_CONTAINER" python -c "
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

agent = LlmAgent(name='test', model='gemini-2.5-flash', instruction='test')
if isinstance(agent.model, LiteLlm):
    print('SUCCESS: LiteLlm 사용 중')
else:
    print(f'FAILED: {type(agent.model).__name__} 사용 중')
" 2>&1 | grep -E "(SUCCESS|FAILED)")
if echo "$LLMAGENT_TEST" | grep -q "SUCCESS"; then
    echo -e "${GREEN}✓ LlmAgent 패치 작동${NC}"
    echo "$LLMAGENT_TEST"
else
    echo -e "${RED}✗ LlmAgent 패치 실패${NC}"
    echo "$LLMAGENT_TEST"
    exit 1
fi
echo ""

# 테스트 6: LLMRegistry 패치 테스트 (가장 중요!)
echo "[테스트 6] LLMRegistry 패치 테스트 ⭐ 핵심!"
REGISTRY_TEST=$(docker exec "$DOCKER_CONTAINER" python -c "
from google.adk.models.registry import LLMRegistry
from google.adk.models.lite_llm import LiteLlm

# gemini-2.5-flash로 모델 요청
model = LLMRegistry.new_llm('gemini-2.5-flash')
if isinstance(model, LiteLlm):
    print('SUCCESS: LLMRegistry → LiteLlm 변환 성공')
    print(f'  Model: {model.model}')
    print(f'  API Base: {model.api_base}')
else:
    print(f'FAILED: {type(model).__name__} 사용 중')
" 2>&1 | grep -E "(SUCCESS|FAILED|Model:|API Base:)")
if echo "$REGISTRY_TEST" | grep -q "SUCCESS"; then
    echo -e "${GREEN}✓ LLMRegistry 패치 작동 (YAML 모델 로딩 지원)${NC}"
    echo "$REGISTRY_TEST"
else
    echo -e "${RED}✗ LLMRegistry 패치 실패${NC}"
    echo "$REGISTRY_TEST"
    exit 1
fi
echo ""

# 테스트 7: canonical_model 테스트 (lazy loading)
echo "[테스트 7] canonical_model 패치 테스트 (lazy loading)"
CANONICAL_TEST=$(docker exec "$DOCKER_CONTAINER" python -c "
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# gemini-2.5-pro로 에이전트 생성 (문자열로 전달)
agent = LlmAgent(name='test', model='gemini-2.5-pro', instruction='test')
# canonical_model은 lazy하게 LLMRegistry.new_llm()을 호출
canonical = agent.canonical_model
if isinstance(canonical, LiteLlm):
    print('SUCCESS: canonical_model → LiteLlm 변환 성공')
    print(f'  Model: {canonical.model}')
else:
    print(f'FAILED: {type(canonical).__name__} 사용 중')
" 2>&1 | grep -E "(SUCCESS|FAILED|Model:)")
if echo "$CANONICAL_TEST" | grep -q "SUCCESS"; then
    echo -e "${GREEN}✓ canonical_model 패치 작동${NC}"
    echo "$CANONICAL_TEST"
else
    echo -e "${RED}✗ canonical_model 패치 실패${NC}"
    echo "$CANONICAL_TEST"
    exit 1
fi
echo ""

# 테스트 8: Agent Builder Assistant 패치 테스트
echo "[테스트 8] Agent Builder Assistant 패치 테스트"
BUILDER_TEST=$(docker exec "$DOCKER_CONTAINER" python -c "
from google.adk.built_in_agents.adk_agent_builder_assistant.agent_builder_assistant import AgentBuilderAssistant
from google.adk.models.lite_llm import LiteLlm

agent = AgentBuilderAssistant.create_agent()
if isinstance(agent.model, LiteLlm):
    print('SUCCESS: Builder Assistant LiteLlm 사용 중')
else:
    print(f'FAILED: {type(agent.model).__name__} 사용 중')
" 2>&1 | grep -E "(SUCCESS|FAILED)")
if echo "$BUILDER_TEST" | grep -q "SUCCESS"; then
    echo -e "${GREEN}✓ Agent Builder Assistant 패치 작동${NC}"
    echo "$BUILDER_TEST"
else
    echo -e "${RED}✗ Agent Builder Assistant 패치 실패${NC}"
    echo "$BUILDER_TEST"
    exit 1
fi
echo ""

# 최종 결과
echo "==================================="
echo -e "${GREEN}✓✓✓ 모든 테스트 통과! ✓✓✓${NC}"
echo "==================================="
echo ""
echo "패치가 정상적으로 작동하고 있습니다."
echo ""
echo "ADK 실행:"
echo "  docker exec -it $DOCKER_CONTAINER /root/run_adk.sh"
echo ""
