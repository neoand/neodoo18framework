#!/bin/bash
# -*- coding: utf-8 -*-
# Neodoo18Framework - Quick Start Script
# This script provides the fastest way to get started with a complete Odoo 18+ project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Banner
echo -e "${BLUE}⚡ NEODOO18FRAMEWORK - QUICK START${NC}"
echo -e "${BLUE}===================================${NC}"
echo ""

# Help function
show_help() {
    echo -e "${GREEN}Usage:${NC}"
    echo -e "  ${YELLOW}./quick-start.sh${NC}         - Quick complete Odoo project setup"
    echo -e "  ${YELLOW}./quick-start.sh --help${NC}  - Show this help"
    echo ""
    echo -e "${GREEN}This script will:${NC}"
    echo -e "  1. Create a complete Odoo 18+ project with default settings"
    echo -e "  2. Clone Odoo source and OCA modules"
    echo -e "  3. Setup virtual environment"
    echo -e "  4. Create ready-to-run configuration"
    echo -e "  5. Get you coding in under 5 minutes!"
    echo ""
}

# Handle arguments
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

# Quick setup
echo -e "${YELLOW}⚡ Starting Quick Complete Odoo 18+ Project Setup...${NC}"
echo ""

# Default configuration with timestamp to avoid conflicts
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROJECT_NAME="quick_odoo_$TIMESTAMP"
MODULE_NAME="quick_module"
AUTHOR="Quick Developer"
DB_NAME="$PROJECT_NAME"

echo -e "${GREEN}Using default configuration:${NC}"
echo -e "  📦 Project: ${BLUE}$PROJECT_NAME${NC}"
echo -e "  🔧 Module: ${BLUE}$MODULE_NAME${NC}"
echo -e "  👤 Author: ${BLUE}$AUTHOR${NC}"
echo -e "  🗄️  Database: ${BLUE}$DB_NAME${NC}"
echo -e "  📁 Location: ${BLUE}$HOME/odoo_projects/$PROJECT_NAME${NC}"
echo ""

read -p "Press ENTER to continue with quick setup or Ctrl+C to use ./setup.sh for custom options: "

# Check requirements
echo -e "${YELLOW}🔍 Checking requirements...${NC}"

if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}❌ Python 3 required${NC}"
    exit 1
fi

if ! command -v git >/dev/null 2>&1; then
    echo -e "${RED}❌ Git required${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Requirements OK${NC}"

# Run setup.sh with predefined answers
echo -e "${YELLOW}🚀 Creating complete Odoo project...${NC}"
echo ""

# Create a temporary file with answers
TEMP_ANSWERS=$(mktemp)
cat > "$TEMP_ANSWERS" << EOF
$PROJECT_NAME
$MODULE_NAME
Custom module for $PROJECT_NAME
$AUTHOR
1
1
$DB_NAME
odoo
odoo
localhost
5432
EOF

# Run setup.sh with predefined answers
"$FRAMEWORK_DIR/setup.sh" create < "$TEMP_ANSWERS"

# Clean up
rm -f "$TEMP_ANSWERS"

# Success message
echo ""
echo -e "${GREEN}🎉 QUICK START COMPLETED SUCCESSFULLY!${NC}"
echo ""
echo -e "${BLUE}Your complete Odoo 18+ project is ready at:${NC}"
echo -e "${YELLOW}$HOME/odoo_projects/$PROJECT_NAME${NC}"
echo ""
echo -e "${GREEN}🚀 To start immediately:${NC}"
echo -e "  ${YELLOW}cd $HOME/odoo_projects/$PROJECT_NAME${NC}"
echo -e "  ${YELLOW}./run.sh${NC}"
echo ""
echo -e "${GREEN}🌐 Odoo will be available at: http://localhost:8069${NC}"
echo -e "${GREEN}📊 Database: $DB_NAME${NC}"
echo ""
echo -e "${BLUE}What you got:${NC}"
echo -e "  ✅ Complete Odoo 18+ source code"
echo -e "  ✅ OCA web modules (including web_responsive)"
echo -e "  ✅ Python virtual environment"
echo -e "  ✅ Your custom module: $MODULE_NAME"
echo -e "  ✅ Ready-to-run configuration"
echo -e "  ✅ Automatic browser opening"
echo ""
echo -e "${YELLOW}For project management (list/delete): ${BLUE}./setup.sh help${NC}"
echo ""