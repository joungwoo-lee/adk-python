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

###############################################################################
# ADK Web with Patched Agent Builder Assistant
#
# This script sets up environment variables and launches ADK Web with the
# custom LiteLlm model patch automatically applied.
#
# Usage:
#   ./setup_patched_adk_web.sh path/to/agents
#
# Or with custom settings:
#   MODEL=gpt-4 API_BASE=https://api.openai.com/v1 ./setup_patched_adk_web.sh
###############################################################################

set -e  # Exit on error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if google-adk is installed
if ! python -c "import google.adk" 2>/dev/null; then
    echo_error "google-adk is not installed"
    echo "Please install it first: pip install --upgrade google-adk"
    exit 1
fi

echo_info "google-adk is installed"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if patch file exists
if [ ! -f "$SCRIPT_DIR/patch_adk_builder_model.py" ]; then
    echo_error "patch_adk_builder_model.py not found in $SCRIPT_DIR"
    exit 1
fi

echo_info "Found patch file: $SCRIPT_DIR/patch_adk_builder_model.py"

# Set default environment variables if not already set
export model="${model:-${MODEL:-gpt-4}}"
export api_base="${api_base:-${API_BASE:-https://api.openai.com/v1}}"
export api_key="${api_key:-${API_KEY:-your-api-key}}"
export x_dep_ticket="${x_dep_ticket:-${X_DEP_TICKET:-api_key}}"
export Send_System_Name="${Send_System_Name:-${SEND_SYSTEM_NAME:-Chain_Reaction}}"
export User_Id="${User_Id:-${USER_ID:-joungwoo.lee}}"
export User_Type="${User_Type:-${USER_TYPE:-AD_ID}}"

echo_info "Environment variables configured:"
echo "  model: $model"
echo "  api_base: $api_base"
echo "  api_key: ${api_key:0:10}..."
echo "  x-dep-ticket: $x_dep_ticket"
echo "  Send-System-Name: $Send_System_Name"
echo "  User-Id: $User_Id"
echo "  User-Type: $User_Type"

# Add current directory to PYTHONPATH so the patch can be imported
export PYTHONPATH="$SCRIPT_DIR:${PYTHONPATH:-}"
echo_info "Added $SCRIPT_DIR to PYTHONPATH"

# Set PYTHONSTARTUP to automatically load the patch
export PYTHONSTARTUP="$SCRIPT_DIR/patch_adk_builder_model.py"
echo_info "Set PYTHONSTARTUP to load patch automatically"

# Get agents directory from argument or use default
AGENTS_DIR="${1:-.}"

echo_info "Starting ADK Web with patched Agent Builder Assistant..."
echo_info "Agents directory: $AGENTS_DIR"
echo ""
echo "=========================================="
echo "ADK Web will now use custom LiteLlm model"
echo "=========================================="
echo ""

# Run adk web
exec adk web "$AGENTS_DIR"
