#!/bin/bash
# -*- coding: utf-8 -*-
"""
Neodoo18Framework Quick Start Script
Sets up a new Odoo 18+ project in minutes
"""

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Framework paths
FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR_DIR="$FRAMEWORK_DIR/generator"

echo -e "${BLUE}🚀 NEODOO18FRAMEWORK QUICK START${NC}"
echo "=================================="

# Check if project name provided
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ Error: Project name required${NC}"
    echo "Usage: $0 <project_name> [options]"
    echo ""
    echo "Examples:"
    echo "  $0 my_crm_module"
    echo "  $0 inventory_tracking --type=enterprise"
    exit 1
fi

PROJECT_NAME=$1
shift  # Remove first argument

echo -e "${YELLOW}📦 Creating project: $PROJECT_NAME${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not found${NC}"
    exit 1
fi

# Run the generator
echo -e "${BLUE}🔧 Running project generator...${NC}"
python3 "$GENERATOR_DIR/create-project.py" "$PROJECT_NAME" "$@"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Project created successfully!${NC}"
    echo ""
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "  1. cd $PROJECT_NAME"
    echo "  2. Review the generated files"
    echo "  3. Set up your Odoo development environment"
    echo "  4. Run: python framework/dev-tools/smart-validator.py . --auto-fix"
    echo ""
    echo -e "${BLUE}📚 Documentation:${NC}"
    echo "  • Framework Guide: framework/llm-guidance/SOIL_CORE.md"
    echo "  • Standards: framework/standards/ODOO18_CORE_STANDARDS.md"
    echo "  • Validation: framework/dev-tools/smart-validator.py --help"
else
    echo -e "${RED}❌ Project creation failed${NC}"
    exit 1
fi