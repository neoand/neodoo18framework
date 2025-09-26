#!/bin/bash
# -*- coding: utf-8 -*-
"""
Neodoo18Framework Environment Setup
Complete Python environment setup for Odoo 18+ development
"""

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
if python3 -c 'import sys; exit(1 if sys.version_info < (3,8) else 0)'; then
    echo -e "${GREEN}✅ Python version is compatible${NC}"
else
    echo -e "${RED}❌ Python 3.8+ is required for Odoo 18+${NC}"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo -e "${BLUE}📦 Creating Python virtual environment...${NC}"

if [ -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .venv
        echo -e "${YELLOW}🗑️  Removed existing virtual environment${NC}"
    else
        echo -e "${BLUE}📦 Using existing virtual environment${NC}"
    fi
fi

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✅ Virtual environment created: .venv${NC}"
fi

# Activate virtual environment
source .venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Upgrade pip and essential tools
echo -e "${BLUE}⬆️  Upgrading pip and development tools...${NC}"
pip install --upgrade pip setuptools wheel

# Create comprehensive requirements file
echo -e "${BLUE}📝 Creating Odoo 18+ requirements file...${NC}"

cat > requirements-dev.txt << 'EOF'
# Neodoo18Framework - Odoo 18+ Development Dependencies
# Generated automatically by setup-env.sh

# Core Odoo Dependencies
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

# Development Tools
pytest>=7.0.0
pytest-cov>=4.0.0
flake8>=5.0.0
black>=22.0.0
isort>=5.10.0
pre-commit>=2.20.0

# Framework-specific tools
click>=8.0.0
colorama>=0.4.0
rich>=12.0.0
EOF

# Install dependencies
echo -e "${BLUE}📦 Installing Odoo 18+ dependencies...${NC}"
echo "This may take a few minutes..."

pip install -r requirements-dev.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All dependencies installed successfully!${NC}"
else
    echo -e "${RED}❌ Some dependencies failed to install${NC}"
    echo "You may need to install system dependencies first"
    echo "See documentation for platform-specific requirements"
fi

# Create activation helper script
echo -e "${BLUE}📄 Creating environment activation helper...${NC}"

cat > activate-env.sh << 'EOF'
#!/bin/bash
# Neodoo18Framework Environment Activation Helper

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "🐍 Neodoo18Framework Python environment activated!"
    echo "📦 Framework location: $(pwd)"
    echo "🔧 Python version: $(python --version)"
    echo "📚 To create project: ./quick-start.sh my_project"
    echo "✅ To validate: python3 framework/validator.py my_project/"
else
    echo "❌ Virtual environment not found!"
    echo "Run: ./setup-env.sh to create it"
fi
EOF

chmod +x activate-env.sh

# Create deactivation helper
cat > deactivate-env.sh << 'EOF'
#!/bin/bash
# Neodoo18Framework Environment Deactivation Helper

if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
    echo "🐍 Neodoo18Framework environment deactivated"
else
    echo "ℹ️  No active virtual environment"
fi
EOF

chmod +x deactivate-env.sh

# Summary
echo ""
echo -e "${GREEN}🎉 ENVIRONMENT SETUP COMPLETE!${NC}"
echo "================================="
echo ""
echo -e "${BLUE}📋 What was set up:${NC}"
echo "  ✅ Python virtual environment (.venv/)"
echo "  ✅ Odoo 18+ dependencies installed"
echo "  ✅ Development tools configured"
echo "  ✅ Activation helpers created"
echo ""
echo -e "${YELLOW}🚀 Quick Start Commands:${NC}"
echo "  • Activate env:    ./activate-env.sh"
echo "  • Create project:  ./quick-start.sh my_project"
echo "  • Validate:        python3 framework/validator.py my_project/"
echo "  • Deactivate:      ./deactivate-env.sh"
echo ""
echo -e "${BLUE}📚 Next Steps:${NC}"
echo "  1. Run: ./activate-env.sh"
echo "  2. Create project: ./quick-start.sh my_awesome_project"
echo "  3. Follow guides in: guides/ (PT/EN/ES)"
echo ""
echo -e "${GREEN}✨ Happy Coding with Neodoo18Framework! ✨${NC}"