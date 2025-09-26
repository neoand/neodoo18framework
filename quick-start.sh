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
    echo "Options:"
    echo "  --setup-venv    Create Python virtual environment"
    echo "  --install-deps  Install Odoo dependencies in venv"
    echo "  --full-setup    Complete setup (venv + dependencies)"
    echo ""
    echo "Examples:"
    echo "  $0 my_crm_module"
    echo "  $0 inventory_tracking --full-setup"
    echo "  $0 library_system --setup-venv"
    exit 1
fi

PROJECT_NAME=$1
shift  # Remove first argument

# Parse options
SETUP_VENV=false
INSTALL_DEPS=false
FULL_SETUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --setup-venv)
            SETUP_VENV=true
            shift
            ;;
        --install-deps)
            INSTALL_DEPS=true
            shift
            ;;
        --full-setup)
            FULL_SETUP=true
            SETUP_VENV=true
            INSTALL_DEPS=true
            shift
            ;;
        *)
            # Pass other arguments to generator
            break
            ;;
    esac
done

echo -e "${YELLOW}📦 Creating project: $PROJECT_NAME${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not found${NC}"
    exit 1
fi

# Setup virtual environment if requested
if [ "$SETUP_VENV" = true ]; then
    echo -e "${BLUE}🐍 Setting up Python virtual environment...${NC}"
    
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        echo -e "${GREEN}✅ Virtual environment created: .venv${NC}"
    else
        echo -e "${YELLOW}⚠️  Virtual environment already exists: .venv${NC}"
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
    
    # Upgrade pip
    pip install --upgrade pip
    
    if [ "$INSTALL_DEPS" = true ]; then
        echo -e "${BLUE}📦 Installing Odoo development dependencies...${NC}"
        
        # Create requirements.txt if it doesn't exist
        if [ ! -f "requirements-dev.txt" ]; then
            cat > requirements-dev.txt << EOF
# Odoo 18+ Development Dependencies
psycopg2-binary>=2.9.0
babel>=2.9.1
chardet>=4.0.0
cryptography>=3.4.8
decorator>=4.4.2
docutils>=0.17
ebaysdk>=2.1.5
feedparser>=6.0.8
freezegun>=1.2.0
gevent>=21.8.0
greenlet>=1.1.2
idna>=3.2
jinja2>=3.0.2
libsass>=0.21.0
lxml>=4.6.3
markupsafe>=2.0.1
num2words>=0.5.10
ofxparse>=0.21
passlib>=1.7.4
pillow>=9.0.0
polib>=1.1.1
psutil>=5.8.0
pydot>=1.4.2
pypdf2>=1.27.5
python-dateutil>=2.8.2
python-stdnum>=1.17
pytz>=2021.3
pyusb>=1.2.1
qrcode>=7.3.1
reportlab>=3.6.2
requests>=2.25.1
urllib3>=1.26.7
vobject>=0.9.6.1
werkzeug>=2.0.2
xlrd>=2.0.1
xlsxwriter>=3.0.1
xlwt>=1.3.0
zeep>=4.1.0
EOF
        fi
        
        pip install -r requirements-dev.txt
        echo -e "${GREEN}✅ Odoo dependencies installed${NC}"
    fi
fi

# Run the generator
echo -e "${BLUE}🔧 Running project generator...${NC}"
python3 "$GENERATOR_DIR/create-project.py" "$PROJECT_NAME" "$@"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Project created successfully!${NC}"
    
    # Final setup message
    if [ "$SETUP_VENV" = true ]; then
        echo ""
        echo -e "${GREEN}🐍 Python Environment Ready!${NC}"
        echo -e "${BLUE}To activate virtual environment:${NC} source .venv/bin/activate"
    fi
    
    echo ""
    echo -e "${YELLOW}📋 Next steps:${NC}"
    if [ "$SETUP_VENV" = false ]; then
        echo "  1. Optional: ./quick-start.sh $PROJECT_NAME --full-setup (for Python venv)"
        echo "  2. cd $PROJECT_NAME"
        echo "  3. Review the generated files"
        echo "  4. Set up your Odoo development environment"
    else
        echo "  1. cd $PROJECT_NAME"
        echo "  2. Review the generated files" 
        echo "  3. Copy to your Odoo addons directory"
    fi
    echo "  • Validate: python3 framework/validator.py $PROJECT_NAME/"
    echo ""
    echo -e "${BLUE}📚 Documentation:${NC}"
    echo "  • Complete Guides: guides/ (PT/EN/ES)"
    echo "  • Framework Guide: framework/SOIL_CORE.md"
    echo "  • Standards: framework/standards/ODOO18_CORE_STANDARDS.md"
    echo "  • Examples: examples/"
    
    if [ "$SETUP_VENV" = true ]; then
        echo ""
        echo -e "${GREEN}🎉 Ready for development!${NC}"
    else
        echo ""
        echo -e "${YELLOW}💡 Tip: Use --full-setup for complete Python environment${NC}"
    fi
else
    echo -e "${RED}❌ Project creation failed${NC}"
    exit 1
fi