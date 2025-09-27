#!/bin/bash
# -*- coding: utf-8 -*-
# Neodoo18Framework Environment Management Script
# ==============================================
# Script unificado para gerenciamento do ambiente Odoo 18+
#
# Uso:
#   ./env.sh setup   - Configura o ambiente Python
#   ./env.sh activate - Ativa o ambiente Python
#   ./env.sh deactivate - Desativa o ambiente Python

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to print help message
function show_help() {
    echo -e "${BLUE}🐍 NEODOO18FRAMEWORK - ENVIRONMENT MANAGEMENT${NC}"
    echo "=================================================="
    echo "Usage: ./env.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup       - Setup Python virtual environment"
    echo "  activate    - Activate Python virtual environment"
    echo "  deactivate  - Deactivate Python virtual environment"
    echo "  help        - Show this help message"
    echo ""
}

# Function to setup environment
function setup_env() {
    echo -e "${BLUE}🐍 NEODOO18FRAMEWORK - PYTHON ENVIRONMENT SETUP${NC}"
    echo "=================================================="

    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is required but not found${NC}"
        echo "Please install Python 3.8+ first"
        exit 1
    fi

    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${BLUE}🔍 Python version detected: $PYTHON_VERSION${NC}"

    # Check Python version (require 3.8+)
    PYTHON_VERSION_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_VERSION_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_VERSION_MAJOR" -lt 3 ] || ([ "$PYTHON_VERSION_MAJOR" -eq 3 ] && [ "$PYTHON_VERSION_MINOR" -lt 8 ]); then
        echo -e "${RED}❌ Python 3.8+ is required but found $PYTHON_VERSION${NC}"
        echo "Please upgrade your Python installation"
        exit 1
    fi

    # Create virtual environment
    echo -e "${BLUE}🔧 Creating virtual environment...${NC}"
    python3 -m venv .venv
    
    # Activate virtual environment
    echo -e "${BLUE}🔌 Activating virtual environment...${NC}"
    source .venv/bin/activate
    
    # Upgrade pip
    echo -e "${BLUE}⬆️  Upgrading pip...${NC}"
    pip install --upgrade pip
    
    # Install dependencies
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    pip install -r requirements-dev.txt
    
    echo -e "${GREEN}✅ Environment setup complete!${NC}"
    echo -e "${YELLOW}📋 To activate the environment: ./env.sh activate${NC}"
}

# Function to activate environment
function activate_env() {
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        echo -e "${GREEN}🐍 Neodoo18Framework Python environment activated!${NC}"
        echo -e "${BLUE}📦 Framework location: $(pwd)${NC}"
        echo -e "${BLUE}🔧 Python version: $(python --version)${NC}"
        echo -e "${BLUE}📚 To create project: ./quick-start.sh my_project${NC}"
        echo -e "${BLUE}✅ To validate: python3 framework/validator.py my_project/${NC}"
    else
        echo -e "${RED}❌ Virtual environment not found!${NC}"
        echo -e "${YELLOW}Run: ./env.sh setup to create it${NC}"
    fi
}

# Function to deactivate environment
function deactivate_env() {
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
        echo -e "${GREEN}🐍 Neodoo18Framework environment deactivated${NC}"
    else
        echo -e "${YELLOW}ℹ️  No active virtual environment${NC}"
    fi
}

# Main logic based on arguments
case "$1" in
    setup)
        setup_env
        ;;
    activate)
        activate_env
        ;;
    deactivate)
        deactivate_env
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac