#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# Neodoo18Framework - setup.sh (LEGACY WRAPPER)
# Este script é mantido apenas por compatibilidade e delega para ./neodoo

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[DEPRECATION] setup.sh foi substituído pelo novo CLI 'neodoo'."
echo "Use: ./neodoo create|list|delete|doctor|update"
echo "Redirecionando para './neodoo' com os argumentos informados..."

exec "$SCRIPT_DIR/neodoo" "$@"

    echo -e "${GREEN}📦 COMPLETE ODOO PROJECT CREATION${NC}"    show_bannerread -p "🛠️ Escolha o ambiente [1/2]: " ENV_OPTION

    echo ""

        echo -e "${RED}🗑️  PROJECT DELETION${NC}"ENV_OPTION=${ENV_OPTION:-2}

    # Project configuration

    echo -e "${BLUE}Step 1: Project Information${NC}"    echo ""

    read -p "Project name (no spaces, lowercase recommended): " PROJECT_NAME

        # 3. CONFIGURAÇÃO DO BANCO DE DADOS

    if [ -z "$PROJECT_NAME" ]; then

        echo -e "${RED}❌ Project name is required${NC}"    list_projectsecho ""

        return 1

    fi    echo -e "${CYAN}${BOLD}3. CONFIGURAÇÃO DO BANCO DE DADOS${NC}"

    

    # Validate project name    if [ ! -d "$PROJECTS_DIR" ] || [ -z "$(ls -A $PROJECTS_DIR 2>/dev/null)" ]; thenecho "------------------------------"

    if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then

        echo -e "${RED}❌ Project name can only contain letters, numbers, underscores, and hyphens${NC}"        echo -e "${YELLOW}No projects available to delete.${NC}"read -p "🗄️ Nome do banco de dados PostgreSQL: " DB_NAME

        return 1

    fi        return 1DB_NAME=${DB_NAME:-$PROJECT_NAME}

    

    local PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"    fi

    

    if [ -d "$PROJECT_PATH" ]; then    read -p "👤 Usuário PostgreSQL: " DB_USER

        echo -e "${RED}❌ Project '$PROJECT_NAME' already exists at $PROJECT_PATH${NC}"

        return 1    echo -e "${YELLOW}Enter the name of the project to delete:${NC}"DB_USER=${DB_USER:-"odoo"}

    fi

        read -p "Project name: " PROJECT_NAME

    # Module information

    echo ""    read -p "🔑 Senha PostgreSQL: " DB_PASSWORD

    echo -e "${BLUE}Step 2: Module Configuration${NC}"

    read -p "Module name (will be created in custom_addons/): " MODULE_NAME    if [ -z "$PROJECT_NAME" ]; thenDB_PASSWORD=${DB_PASSWORD:-"odoo"}

    MODULE_NAME=${MODULE_NAME:-$PROJECT_NAME}

            echo -e "${RED}❌ Project name cannot be empty${NC}"

    read -p "Module description: " MODULE_DESC

    MODULE_DESC=${MODULE_DESC:-"Custom module for $PROJECT_NAME"}        return 1# 4. CONFIGURAÇÃO DO PROJETO E AMBIENTE

    

    read -p "Author name: " AUTHOR_NAME    fiecho ""

    AUTHOR_NAME=${AUTHOR_NAME:-"Your Company"}

        echo -e "${CYAN}${BOLD}4. CONFIGURANDO AMBIENTE...${NC}"

    # Template selection

    echo ""    local PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"echo "------------------------------"

    echo -e "${BLUE}Step 3: Template Selection${NC}"

    echo "Available templates:"    

    echo "1. minimal - Basic project structure"

    echo "2. advanced - Full-featured enterprise module"    if [ ! -d "$PROJECT_PATH" ]; thenecho -e "${YELLOW}Criando estrutura do projeto...${NC}"

    echo "3. ecommerce - E-commerce specific module"

            echo -e "${RED}❌ Project '$PROJECT_NAME' not found at $PROJECT_PATH${NC}"

    read -p "Choose template [1-3] (default: 1): " TEMPLATE_CHOICE

    TEMPLATE_CHOICE=${TEMPLATE_CHOICE:-1}        return 1# Create project directory if not exists

    

    case $TEMPLATE_CHOICE in    fimkdir -p "$FRAMEWORK_DIR/$PROJECT_NAME"

        1) TEMPLATE_TYPE="minimal" ;;

        2) TEMPLATE_TYPE="advanced" ;;    

        3) TEMPLATE_TYPE="ecommerce" ;;

        *)     echo ""# Setup environment based on choice

            echo -e "${RED}❌ Invalid template choice${NC}"

            return 1    echo -e "${RED}⚠️  WARNING: This will permanently delete:${NC}"if [ "$ENV_OPTION" == "1" ]; then

            ;;

    esac    echo -e "   📁 Project directory: $PROJECT_PATH"    echo -e "${GREEN}Configurando ambiente Python local...${NC}"

    

    # Environment selection    echo -e "   🗄️  Database (if exists): $PROJECT_NAME"    

    echo ""

    echo -e "${BLUE}Step 4: Environment Configuration${NC}"    echo -e "   🐍 Virtual environment and all dependencies"    # Check if Python is installed

    echo "Choose development environment:"

    echo "1. Python Virtual Environment (recommended for development)"    echo -e "   📦 All source code and configurations"    if ! command -v python3 &> /dev/null; then

    echo "2. Docker (recommended for production-like testing)"

        echo ""        echo -e "${RED}❌ Python 3 não encontrado. Por favor, instale o Python 3 primeiro.${NC}"

    read -p "Choose environment [1-2] (default: 1): " ENV_CHOICE

    ENV_CHOICE=${ENV_CHOICE:-1}    echo -e "${RED}This action CANNOT be undone!${NC}"        exit 1

    

    # Database configuration    echo ""    fi

    echo ""

    echo -e "${BLUE}Step 5: Database Configuration${NC}"        

    read -p "Database name (default: $PROJECT_NAME): " DB_NAME

    DB_NAME=${DB_NAME:-$PROJECT_NAME}    read -p "Type 'DELETE' to confirm deletion: " CONFIRMATION    # Setup virtual environment

    

    read -p "Database user (default: odoo): " DB_USER        echo -e "${YELLOW}Criando ambiente virtual...${NC}"

    DB_USER=${DB_USER:-odoo}

        if [ "$CONFIRMATION" != "DELETE" ]; then    python3 -m venv "$FRAMEWORK_DIR/$PROJECT_NAME/.venv"

    read -s -p "Database password (default: odoo): " DB_PASSWORD

    echo ""        echo -e "${YELLOW}❌ Deletion cancelled${NC}"    

    DB_PASSWORD=${DB_PASSWORD:-odoo}

            return 0    # Activate virtual environment

    read -p "Database host (default: localhost): " DB_HOST

    DB_HOST=${DB_HOST:-localhost}    fi    source "$FRAMEWORK_DIR/$PROJECT_NAME/.venv/bin/activate"

    

    read -p "Database port (default: 5432): " DB_PORT        

    DB_PORT=${DB_PORT:-5432}

        echo ""    # Upgrade pip

    # Start creation

    echo ""    echo -e "${YELLOW}🛑 Stopping project if running...${NC}"    echo -e "${YELLOW}Atualizando pip...${NC}"

    echo -e "${GREEN}🚀 Creating complete Odoo project...${NC}"

    echo ""        pip install --upgrade pip

    

    # Create project directory    # Stop Odoo if running    

    echo -e "${YELLOW}📁 Creating project structure...${NC}"

    mkdir -p "$PROJECTS_DIR"    if [ -f "$PROJECT_PATH/.odoo_pid" ]; then    # Install requirements

    mkdir -p "$PROJECT_PATH"

            local pid=$(cat "$PROJECT_PATH/.odoo_pid")    echo -e "${YELLOW}Instalando dependências...${NC}"

    cd "$PROJECT_PATH"

            if kill -0 "$pid" 2>/dev/null; then    pip install -r "$FRAMEWORK_DIR/requirements-dev.txt"

    # Create directory structure

    mkdir -p custom_addons            echo "Stopping Odoo process (PID: $pid)..."    

    mkdir -p community_addons

    mkdir -p logs            kill -TERM "$pid" 2>/dev/null || true    # Create activation script

    mkdir -p filestore

    mkdir -p backups            sleep 2    cat > "$FRAMEWORK_DIR/$PROJECT_NAME/activate.sh" << EOL

    

    # Clone Odoo source            kill -KILL "$pid" 2>/dev/null || true#!/bin/bash

    echo -e "${YELLOW}📦 Cloning Odoo $ODOO_VERSION source...${NC}"

    git clone --depth 1 --branch "$ODOO_VERSION" "$ODOO_REPO" odoo_source        fi# Activate the virtual environment

    

    # Clone OCA web modules        rm -f "$PROJECT_PATH/.odoo_pid"source "$(pwd)/.venv/bin/activate"

    echo -e "${YELLOW}🌐 Cloning OCA web modules...${NC}"

    git clone --depth 1 --branch "$ODOO_VERSION" "$OCA_WEB_REPO" community_addons/web    fiecho "✅ Ambiente virtual ativado. Use 'deactivate' para sair."

    

    # Setup environment based on choice    EOL

    if [ "$ENV_CHOICE" = "1" ]; then

        setup_python_environment    # Stop Docker containers if they exist    chmod +x "$FRAMEWORK_DIR/$PROJECT_NAME/activate.sh"

    else

        setup_docker_environment    if [ -f "$PROJECT_PATH/docker-compose.yml" ]; then    

    fi

            echo "Stopping Docker containers..."    echo -e "${GREEN}✅ Ambiente Python configurado com sucesso!${NC}"

    # Create custom module

    echo -e "${YELLOW}🔧 Creating custom module '$MODULE_NAME'...${NC}"        (cd "$PROJECT_PATH" && docker-compose down -v 2>/dev/null || true)    

    python3 "$FRAMEWORK_DIR/framework/generator/create_project.py" \

        --name="$MODULE_NAME" \    fielse

        --type="$TEMPLATE_TYPE" \

        --output="custom_addons" \        # Docker setup

        --author="$AUTHOR_NAME" \

        --description="$MODULE_DESC"    echo -e "${YELLOW}🗑️  Deleting project directory...${NC}"    echo -e "${GREEN}Configurando ambiente Docker...${NC}"

    

    # Create Odoo configuration        

    create_odoo_config

        # Remove project directory    # Check if Docker is installed

    # Create run script

    create_run_script    if rm -rf "$PROJECT_PATH"; then    if ! command -v docker &> /dev/null; then

    

    # Create project README        echo -e "${GREEN}✅ Project directory deleted successfully${NC}"        echo -e "${YELLOW}⚠️ Docker não encontrado. Você precisará instalar o Docker para continuar.${NC}"

    create_project_readme

        else        echo -e "${YELLOW}Visite: https://docs.docker.com/get-docker/${NC}"

    # Create requirements.txt

    create_requirements_file        echo -e "${RED}❌ Failed to delete project directory${NC}"    fi

    

    echo ""        return 1    

    echo -e "${GREEN}🎉 Project '$PROJECT_NAME' created successfully!${NC}"

    echo ""    fi    # Create docker-compose.yml

    echo -e "${BLUE}📁 Project location: $PROJECT_PATH${NC}"

    echo ""        cat > "$FRAMEWORK_DIR/$PROJECT_NAME/docker-compose.yml" << EOL

    echo -e "${GREEN}🚀 To start your project:${NC}"

    echo -e "   ${YELLOW}cd $PROJECT_PATH${NC}"    # Optional: Drop databaseversion: '3'

    if [ "$ENV_CHOICE" = "1" ]; then

        echo -e "   ${YELLOW}source .venv/bin/activate${NC}"    echo ""services:

    fi

    echo -e "   ${YELLOW}./run.sh${NC}"    read -p "Do you want to drop the PostgreSQL database '$PROJECT_NAME'? (y/N): " DROP_DB  odoo:

    echo ""

    echo -e "${GREEN}🌐 Odoo will be available at: http://localhost:8069${NC}"        image: odoo:18

    echo -e "${GREEN}📊 Database: $DB_NAME${NC}"

    echo ""    if [[ "$DROP_DB" =~ ^[Yy]$ ]]; then    depends_on:

}

        echo -e "${YELLOW}🗄️  Dropping database...${NC}"      - db

# Setup Python virtual environment

setup_python_environment() {        if command -v dropdb >/dev/null 2>&1; then    ports:

    echo -e "${YELLOW}🐍 Setting up Python virtual environment...${NC}"

                if dropdb "$PROJECT_NAME" 2>/dev/null; then      - "8069:8069"

    # Create virtual environment

    python3 -m venv .venv                echo -e "${GREEN}✅ Database '$PROJECT_NAME' dropped successfully${NC}"    volumes:

    source .venv/bin/activate

                else      - ./addons:/mnt/extra-addons

    # Upgrade pip

    pip install --upgrade pip                echo -e "${YELLOW}⚠️  Database '$PROJECT_NAME' not found or already dropped${NC}"    environment:

    

    # Install Odoo dependencies            fi      - HOST=db

    pip install -r odoo_source/requirements.txt

            else      - USER=$DB_USER

    # Install additional development tools

    pip install psycopg2-binary python-decouple watchdog            echo -e "${YELLOW}⚠️  PostgreSQL tools not found. Please drop database manually:${NC}"      - PASSWORD=$DB_PASSWORD

}

            echo -e "   ${BLUE}dropdb $PROJECT_NAME${NC}"  

# Setup Docker environment

setup_docker_environment() {        fi  db:

    echo -e "${YELLOW}🐳 Setting up Docker environment...${NC}"

        fi    image: postgres:15

    # Create docker-compose.yml

    cat > docker-compose.yml << EOF        environment:

version: '3.8'

    echo ""      - POSTGRES_DB=$DB_NAME

services:

  odoo:    echo -e "${GREEN}🎉 Project '$PROJECT_NAME' deleted successfully!${NC}"      - POSTGRES_PASSWORD=$DB_PASSWORD

    image: odoo:18.0

    container_name: ${PROJECT_NAME}_odoo    echo ""      - POSTGRES_USER=$DB_USER

    ports:

      - "8069:8069"}    ports:

    volumes:

      - ./custom_addons:/mnt/extra-addons/custom_addons      - "5432:5432"

      - ./community_addons:/mnt/extra-addons/community_addons

      - ./odoo.conf:/etc/odoo/odoo.conf# Create complete project structure    volumes:

      - ./logs:/var/log/odoo

      - ./filestore:/var/lib/odoo/filestorecreate_project() {      - pg_data:/var/lib/postgresql/data

    environment:

      - HOST=db    show_banner

      - USER=${DB_USER}

      - PASSWORD=${DB_PASSWORD}    echo -e "${GREEN}📦 COMPLETE ODOO PROJECT CREATION${NC}"volumes:

    depends_on:

      - db    echo ""  pg_data:

    command: ["odoo", "-c", "/etc/odoo/odoo.conf"]

    EOL

  db:

    image: postgres:15    # Project configuration

    container_name: ${PROJECT_NAME}_db

    environment:    echo -e "${BLUE}Step 1: Project Information${NC}"    # Create start script

      - POSTGRES_DB=${DB_NAME}

      - POSTGRES_USER=${DB_USER}    read -p "Project name (no spaces, lowercase recommended): " PROJECT_NAME    cat > "$FRAMEWORK_DIR/$PROJECT_NAME/start-docker.sh" << EOL

      - POSTGRES_PASSWORD=${DB_PASSWORD}

    volumes:    #!/bin/bash

      - postgres_data:/var/lib/postgresql/data

    ports:    if [ -z "$PROJECT_NAME" ]; thendocker-compose up -d

      - "5432:5432"

        echo -e "${RED}❌ Project name is required${NC}"echo "✅ Ambiente Docker iniciado!"

volumes:

  postgres_data:        return 1echo "Acesse o Odoo em: http://localhost:8069"

EOF

}    fiEOL



# Create Odoo configuration file        chmod +x "$FRAMEWORK_DIR/$PROJECT_NAME/start-docker.sh"

create_odoo_config() {

    echo -e "${YELLOW}⚙️ Creating Odoo configuration...${NC}"    # Validate project name    

    

    cat > odoo.conf << EOF    if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then    # Create stop script

[options]

# Database settings        echo -e "${RED}❌ Project name can only contain letters, numbers, underscores, and hyphens${NC}"    cat > "$FRAMEWORK_DIR/$PROJECT_NAME/stop-docker.sh" << EOL

db_host = ${DB_HOST}

db_port = ${DB_PORT}        return 1#!/bin/bash

db_user = ${DB_USER}

db_password = ${DB_PASSWORD}    fidocker-compose down

db_name = ${DB_NAME}

    echo "✅ Ambiente Docker parado!"

# Server settings

xmlrpc_port = 8069    local PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"EOL

longpolling_port = 8072

        chmod +x "$FRAMEWORK_DIR/$PROJECT_NAME/stop-docker.sh"

# Addons paths

addons_path = odoo_source/addons,custom_addons,community_addons/web    if [ -d "$PROJECT_PATH" ]; then    



# Log settings        echo -e "${RED}❌ Project '$PROJECT_NAME' already exists at $PROJECT_PATH${NC}"    echo -e "${GREEN}✅ Ambiente Docker configurado com sucesso!${NC}"

log_level = info

logfile = logs/odoo.log        return 1fi

log_rotate = True

log_db = False    fi



# Performance settings    # 5. Generate project using generator

workers = 2

limit_memory_hard = 2684354560    # Module informationecho ""

limit_memory_soft = 2147483648

limit_request = 8192    echo ""echo -e "${CYAN}${BOLD}5. GERANDO ESTRUTURA DO MÓDULO ODOO...${NC}"

limit_time_cpu = 600

limit_time_real = 1200    echo -e "${BLUE}Step 2: Module Configuration${NC}"echo "------------------------------"



# Development settings    read -p "Module name (will be created in custom_addons/): " MODULE_NAME

dev_mode = reload,qweb,werkzeug,xml

    MODULE_NAME=${MODULE_NAME:-$PROJECT_NAME}# Create addons directory

# Data directory

data_dir = filestore    mkdir -p "$FRAMEWORK_DIR/$PROJECT_NAME/addons"



# Auto-install web_responsive from OCA    read -p "Module description: " MODULE_DESC

init = web_responsive

EOF    MODULE_DESC=${MODULE_DESC:-"Custom module for $PROJECT_NAME"}# Copy template files based on project type

}

    echo -e "${YELLOW}Aplicando template $PROJECT_TYPE...${NC}"

# Create run script

create_run_script() {    read -p "Author name: " AUTHOR_NAME

    echo -e "${YELLOW}🚀 Creating run script...${NC}"

        AUTHOR_NAME=${AUTHOR_NAME:-"Your Company"}if [ -d "$TEMPLATES_DIR/$PROJECT_TYPE" ]; then

    if [ "$ENV_CHOICE" = "1" ]; then

        # Python environment run script        cp -r "$TEMPLATES_DIR/$PROJECT_TYPE"/* "$FRAMEWORK_DIR/$PROJECT_NAME/addons/$PROJECT_NAME/"

        cat > run.sh << 'EOF'

#!/bin/bash    # Template selectionelse



# Neodoo18Framework - Project Run Script    echo ""    cp -r "$TEMPLATES_DIR/minimal"/* "$FRAMEWORK_DIR/$PROJECT_NAME/addons/$PROJECT_NAME/"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_NAME=$(basename "$PROJECT_DIR")    echo -e "${BLUE}Step 3: Template Selection${NC}"fi



# Colors    echo "Available templates:"

GREEN='\033[0;32m'

YELLOW='\033[1;33m'    echo "1. minimal - Basic project structure"# Replace placeholders in files

BLUE='\033[0;34m'

NC='\033[0m'    echo "2. advanced - Full-featured enterprise module"echo -e "${YELLOW}Personalizando arquivos...${NC}"



echo -e "${BLUE}🚀 Starting Odoo Project: $PROJECT_NAME${NC}"    echo "3. ecommerce - E-commerce specific module"

echo ""

    find "$FRAMEWORK_DIR/$PROJECT_NAME/addons/$PROJECT_NAME" -type f -name "*.py" -o -name "*.xml" -o -name "__manifest__.py" | while read file; do

# Activate virtual environment

if [ -f ".venv/bin/activate" ]; then    read -p "Choose template [1-3] (default: 1): " TEMPLATE_CHOICE    sed -i'.bak' "s/{{MODULE_NAME}}/$PROJECT_NAME/g" "$file"

    echo -e "${YELLOW}🐍 Activating virtual environment...${NC}"

    source .venv/bin/activate    TEMPLATE_CHOICE=${TEMPLATE_CHOICE:-1}    sed -i'.bak' "s/{{MODULE_TECHNICAL_NAME}}/$PROJECT_NAME/g" "$file"

else

    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"        sed -i'.bak' "s/{{AUTHOR}}/$COMPANY/g" "$file"

fi

    case $TEMPLATE_CHOICE in    sed -i'.bak' "s/{{SUMMARY}}/$PROJECT_NAME/g" "$file"

# Check if PostgreSQL is running

if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then        1) TEMPLATE_TYPE="minimal" ;;    sed -i'.bak' "s/{{DESCRIPTION}}/$DESCRIPTION/g" "$file"

    echo -e "${YELLOW}⚠️  PostgreSQL not running. Please start PostgreSQL first.${NC}"

    echo -e "   ${BLUE}brew services start postgresql${NC}  # macOS"        2) TEMPLATE_TYPE="advanced" ;;    sed -i'.bak' "s/{{MODEL_NAME}}/model/g" "$file"

    echo -e "   ${BLUE}sudo systemctl start postgresql${NC}  # Linux"

    exit 1        3) TEMPLATE_TYPE="ecommerce" ;;    sed -i'.bak' "s/{{MODEL_DESCRIPTION}}/Model/g" "$file"

fi

        *)     sed -i'.bak' "s/{{MODULE_CLASS}}/$(echo $PROJECT_NAME | sed -r 's/(^|_)([a-z])/\U\2/g')/g" "$file"

# Validate project before starting

echo -e "${YELLOW}✅ Validating project...${NC}"            echo -e "${RED}❌ Invalid template choice${NC}"    sed -i'.bak' "s/{{CATEGORY}}/Extra Tools/g" "$file"

if [ -d "../framework" ]; then

    python ../framework/validator/validate.py custom_addons/            return 1    sed -i'.bak' "s/{{WEBSITE}}/https:\/\/example.com/g" "$file"

else

    echo -e "${YELLOW}⚠️  Framework validator not found, skipping validation${NC}"            ;;    sed -i'.bak' "s/{{IS_APPLICATION}}/True/g" "$file"

fi

    esac    rm -f "${file}.bak"

# Start Odoo

echo -e "${YELLOW}🌐 Starting Odoo server...${NC}"    done

echo -e "${GREEN}📊 Access Odoo at: http://localhost:8069${NC}"

echo -e "${GREEN}🗄️  Database: $(grep '^db_name' odoo.conf | cut -d'=' -f2 | tr -d ' ')${NC}"    # Environment selection

echo ""

    echo ""# Add README to the project

# Save PID for management

python odoo_source/odoo-bin -c odoo.conf &    echo -e "${BLUE}Step 4: Environment Configuration${NC}"cat > "$FRAMEWORK_DIR/$PROJECT_NAME/README.md" << EOL

ODOO_PID=$!

echo $ODOO_PID > .odoo_pid    echo "Choose development environment:"# $PROJECT_NAME - Projeto Odoo 18+



# Open browser automatically    echo "1. Python Virtual Environment (recommended for development)"

sleep 3

if command -v open >/dev/null 2>&1; then    echo "2. Docker (recommended for production-like testing)"> $DESCRIPTION

    open http://localhost:8069

elif command -v xdg-open >/dev/null 2>&1; then    

    xdg-open http://localhost:8069

fi    read -p "Choose environment [1-2] (default: 1): " ENV_CHOICE## Inicialização Rápida



# Wait for Odoo process    ENV_CHOICE=${ENV_CHOICE:-1}

wait $ODOO_PID

rm -f .odoo_pid    ### Ambiente Local (Python venv)

EOF

    else    # Database configuration\`\`\`bash

        # Docker environment run script

        cat > run.sh << 'EOF'    echo ""# Ativar ambiente virtual

#!/bin/bash

    echo -e "${BLUE}Step 5: Database Configuration${NC}"source ./activate.sh

# Neodoo18Framework - Docker Project Run Script

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"    read -p "Database name (default: $PROJECT_NAME): " DB_NAME

PROJECT_NAME=$(basename "$PROJECT_DIR")

    DB_NAME=${DB_NAME:-$PROJECT_NAME}# Executar Odoo (a ser implementado)

# Colors

GREEN='\033[0;32m'    \`\`\`

YELLOW='\033[1;33m'

BLUE='\033[0;34m'    read -p "Database user (default: odoo): " DB_USER

NC='\033[0m'

    DB_USER=${DB_USER:-odoo}### Ambiente Docker

echo -e "${BLUE}🚀 Starting Odoo Project: $PROJECT_NAME${NC}"

echo ""    \`\`\`bash



# Check if Docker is running    read -s -p "Database password (default: odoo): " DB_PASSWORD# Iniciar containers

if ! docker info >/dev/null 2>&1; then

    echo -e "${YELLOW}⚠️  Docker not running. Please start Docker first.${NC}"    echo ""./start-docker.sh

    exit 1

fi    DB_PASSWORD=${DB_PASSWORD:-odoo}



# Validate project before starting    # Parar containers

echo -e "${YELLOW}✅ Validating project...${NC}"

if [ -d "../framework" ]; then    read -p "Database host (default: localhost): " DB_HOST./stop-docker.sh

    python ../framework/validator/validate.py custom_addons/

else    DB_HOST=${DB_HOST:-localhost}\`\`\`

    echo -e "${YELLOW}⚠️  Framework validator not found, skipping validation${NC}"

fi    



# Start Docker containers    read -p "Database port (default: 5432): " DB_PORT## Validação de Código

echo -e "${YELLOW}🐳 Starting Docker containers...${NC}"

docker-compose up -d    DB_PORT=${DB_PORT:-5432}\`\`\`bash



echo -e "${GREEN}📊 Access Odoo at: http://localhost:8069${NC}"    # Validar conformidade com Odoo 18+

echo -e "${GREEN}🗄️  Database: $(grep '^db_name' odoo.conf | cut -d'=' -f2 | tr -d ' ')${NC}"

echo ""    # Start creationpython ../framework/validator/validate.py ./addons/$PROJECT_NAME



# Follow logs    echo ""\`\`\`

echo -e "${YELLOW}📋 Following Odoo logs (Ctrl+C to stop)...${NC}"

sleep 3    echo -e "${GREEN}🚀 Creating complete Odoo project...${NC}"



# Open browser automatically    echo ""## Estrutura do Projeto

if command -v open >/dev/null 2>&1; then

    open http://localhost:8069    \`\`\`

elif command -v xdg-open >/dev/null 2>&1; then

    xdg-open http://localhost:8069    # Create project directory$PROJECT_NAME/

fi

    echo -e "${YELLOW}📁 Creating project structure...${NC}"├── addons/                 # Módulos Odoo

docker-compose logs -f odoo

EOF    mkdir -p "$PROJECTS_DIR"│   └── $PROJECT_NAME/      # Seu módulo principal

    fi

        mkdir -p "$PROJECT_PATH"├── .venv/                  # Ambiente virtual Python (se aplicável)

    chmod +x run.sh

}    └── docker-compose.yml      # Configuração Docker (se aplicável)



# Create project README    cd "$PROJECT_PATH"\`\`\`

create_project_readme() {

    echo -e "${YELLOW}📖 Creating project documentation...${NC}"    

    

    cat > README.md << EOF    # Create directory structure---

# $PROJECT_NAME

    mkdir -p custom_addonsDesenvolvido com [Neodoo18Framework](https://github.com/neoand/neodoo18framework)

Odoo 18+ project created with Neodoo18Framework.

    mkdir -p community_addonsEOL

## Project Structure

    mkdir -p logs

\`\`\`

$PROJECT_NAME/    mkdir -p filestore# 6. FINALIZAÇÃO

├── .venv/                    # Virtual environment (Python setup)

├── odoo_source/              # Odoo 18+ source code    mkdir -p backupsecho ""

├── custom_addons/            # Your custom modules

│   └── $MODULE_NAME/         # Your main module    echo -e "${GREEN}${BOLD}✅ PROJETO CONFIGURADO COM SUCESSO!${NC}"

├── community_addons/         # OCA modules

│   └── web/                  # OCA web modules (includes web_responsive)    # Clone Odoo sourceecho "==============================================="

├── logs/                     # Odoo log files

├── filestore/               # Odoo file storage    echo -e "${YELLOW}📦 Cloning Odoo $ODOO_VERSION source...${NC}"echo ""

├── backups/                 # Database backups

├── docker-compose.yml       # Docker configuration (Docker setup)    git clone --depth 1 --branch "$ODOO_VERSION" "$ODOO_REPO" odoo_sourceecho -e "${CYAN}Projeto '$PROJECT_NAME' criado em:${NC}"

├── odoo.conf               # Odoo configuration

├── requirements.txt        # Python dependencies    echo -e "${YELLOW}$FRAMEWORK_DIR/$PROJECT_NAME${NC}"

├── run.sh                  # Start Odoo script

└── README.md              # This file    # Clone OCA web modulesecho ""

\`\`\`

    echo -e "${YELLOW}🌐 Cloning OCA web modules...${NC}"echo -e "${CYAN}Próximos passos:${NC}"

## Quick Start

    git clone --depth 1 --branch "$ODOO_VERSION" "$OCA_WEB_REPO" community_addons/webecho -e "1. Entre no diretório: ${YELLOW}cd $PROJECT_NAME${NC}"

1. **Start the project:**

   \`\`\`bash    

   cd $PROJECT_PATH

   ./run.sh    # Setup environment based on choiceif [ "$ENV_OPTION" == "1" ]; then

   \`\`\`

    if [ "$ENV_CHOICE" = "1" ]; then    echo -e "2. Ative o ambiente: ${YELLOW}source ./activate.sh${NC}"

2. **Access Odoo:**

   - URL: http://localhost:8069        setup_python_environmentelse

   - Database: $DB_NAME

   - Create admin user on first access    else    echo -e "2. Inicie o Docker: ${YELLOW}./start-docker.sh${NC}"



## Development        setup_docker_environment    echo -e "   Acesse o Odoo em: ${YELLOW}http://localhost:8069${NC}"



### Adding New Modules    fifi



1. Create new module in \`custom_addons/\`:    

   \`\`\`bash

   python ../framework/generator/create_project.py --name=my_new_module --type=minimal --output=custom_addons    # Create custom moduleecho -e "3. Para validar o código: ${YELLOW}python ../framework/validator/validate.py ./addons/$PROJECT_NAME${NC}"

   \`\`\`

    echo -e "${YELLOW}🔧 Creating custom module '$MODULE_NAME'...${NC}"echo ""

2. Add module to addons_path in \`odoo.conf\`

3. Restart Odoo and update apps list    python3 "$FRAMEWORK_DIR/generator/create_project.py" \echo -e "${BLUE}${BOLD}Obrigado por usar o Neodoo18Framework!${NC}"



### Validation        --name="$MODULE_NAME" \echo -e "${BLUE}Para mais informações, consulte a documentação em: ${YELLOW}docs/README.md${NC}"



Always validate your code before committing:        --type="$TEMPLATE_TYPE" \echo ""

\`\`\`bash        --output="custom_addons" \

python ../framework/validator/validate.py custom_addons/        --author="$AUTHOR_NAME" \

\`\`\`        --description="$MODULE_DESC"

    

### Database Management    # Create Odoo configuration

    create_odoo_config

- **Backup database:**    

  \`\`\`bash    # Create run script

  pg_dump $DB_NAME > backups/$DB_NAME-\$(date +%Y%m%d_%H%M%S).sql    create_run_script

  \`\`\`    

    # Create project README

- **Restore database:**    create_project_readme

  \`\`\`bash    

  dropdb $DB_NAME    # Create requirements.txt

  createdb $DB_NAME    create_requirements_file

  psql $DB_NAME < backups/backup_file.sql    

  \`\`\`    echo ""

    echo -e "${GREEN}🎉 Project '$PROJECT_NAME' created successfully!${NC}"

## Configuration    echo ""

    echo -e "${BLUE}📁 Project location: $PROJECT_PATH${NC}"

### Environment: $([ "$ENV_CHOICE" = "1" ] && echo "Python Virtual Environment" || echo "Docker")    echo ""

### Template: $TEMPLATE_TYPE    echo -e "${GREEN}🚀 To start your project:${NC}"

### Module: $MODULE_NAME    echo -e "   ${YELLOW}cd $PROJECT_PATH${NC}"

### Author: $AUTHOR_NAME    if [ "$ENV_CHOICE" = "1" ]; then

        echo -e "   ${YELLOW}source .venv/bin/activate${NC}"

## Installed OCA Modules    fi

    echo -e "   ${YELLOW}./run.sh${NC}"

- **web_responsive**: Responsive web interface for mobile devices    echo ""

    echo -e "${GREEN}🌐 Odoo will be available at: http://localhost:8069${NC}"

## Support    echo -e "${GREEN}📊 Database: $DB_NAME${NC}"

    echo ""

- Framework Documentation: ../docs/}

- Odoo 18 Documentation: https://www.odoo.com/documentation/18.0/

- OCA Documentation: https://github.com/OCA/# Setup Python virtual environment

setup_python_environment() {

---    echo -e "${YELLOW}🐍 Setting up Python virtual environment...${NC}"

    

Generated by Neodoo18Framework on $(date)    # Create virtual environment

EOF    python3 -m venv .venv

}    source .venv/bin/activate

    

# Create requirements file    # Upgrade pip

create_requirements_file() {    pip install --upgrade pip

    echo -e "${YELLOW}📋 Creating requirements file...${NC}"    

        # Install Odoo dependencies

    cat > requirements.txt << EOF    pip install -r odoo_source/requirements.txt

# Neodoo18Framework Project Requirements    

# Generated on $(date)    # Install additional development tools

    pip install psycopg2-binary python-decouple watchdog

# Core Odoo dependencies (from odoo_source/requirements.txt)}

Babel==2.9.1

chardet==4.0.0# Setup Docker environment

cryptography==3.4.8setup_docker_environment() {

decorator==4.4.2    echo -e "${YELLOW}🐳 Setting up Docker environment...${NC}"

docutils==0.17    

ebaysdk==2.1.5    # Create docker-compose.yml

freezegun==0.3.11    cat > docker-compose.yml << EOF

gevent==21.8.0version: '3.8'

greenlet==1.1.2

idna==2.8services:

Jinja2==2.11.3  odoo:

libsass==0.20.1    image: odoo:18.0

lxml==4.6.5    container_name: ${PROJECT_NAME}_odoo

MarkupSafe==1.1.1    ports:

num2words==0.5.10      - "8069:8069"

ofxparse==0.21    volumes:

passlib==1.7.4      - ./custom_addons:/mnt/extra-addons/custom_addons

Pillow==8.4.0      - ./community_addons:/mnt/extra-addons/community_addons

polib==1.1.1      - ./odoo.conf:/etc/odoo/odoo.conf

psutil==5.8.0      - ./logs:/var/log/odoo

psycopg2==2.8.6      - ./filestore:/var/lib/odoo/filestore

pydot==1.4.2    environment:

pyopenssl==22.0.0      - HOST=db

PyPDF2==1.26.0      - USER=${DB_USER}

pyserial==3.4      - PASSWORD=${DB_PASSWORD}

python-dateutil==2.8.1    depends_on:

python-stdnum==1.16      - db

pytz==2021.3    command: ["odoo", "-c", "/etc/odoo/odoo.conf"]

pyusb==1.0.2

qrcode==6.1  db:

reportlab==3.5.59    image: postgres:15

requests==2.25.1    container_name: ${PROJECT_NAME}_db

zeep==4.0.0    environment:

python-ldap==3.4.0      - POSTGRES_DB=${DB_NAME}

vobject==0.9.6.1      - POSTGRES_USER=${DB_USER}

Werkzeug==2.0.2      - POSTGRES_PASSWORD=${DB_PASSWORD}

xlrd==1.2.0    volumes:

XlsxWriter==1.4.5      - postgres_data:/var/lib/postgresql/data

xlwt==1.3.0    ports:

      - "5432:5432"

# Additional development dependencies

psycopg2-binary==2.9.1volumes:

python-decouple==3.4  postgres_data:

watchdog==2.1.6EOF

}

# Development and testing tools

pytest==6.2.4# Create Odoo configuration file

pytest-odoo==0.5.0create_odoo_config() {

coverage==5.5    echo -e "${YELLOW}⚙️ Creating Odoo configuration...${NC}"

flake8==3.9.2    

black==21.7b0    cat > odoo.conf << EOF

isort==5.9.3[options]

EOF# Database settings

}db_host = ${DB_HOST}

db_port = ${DB_PORT}

# Main script logicdb_user = ${DB_USER}

case "${1:-}" indb_password = ${DB_PASSWORD}

    "create")db_name = ${DB_NAME}

        create_project

        ;;# Server settings

    "delete")xmlrpc_port = 8069

        delete_projectlongpolling_port = 8072

        ;;

    "list")# Addons paths

        list_projectsaddons_path = odoo_source/addons,custom_addons,community_addons/web

        ;;

    "help"|"-h"|"--help")# Log settings

        show_helplog_level = info

        ;;logfile = logs/odoo.log

    "")log_rotate = True

        create_projectlog_db = False

        ;;

    *)# Performance settings

        echo -e "${RED}❌ Unknown command: $1${NC}"workers = 2

        echo ""limit_memory_hard = 2684354560

        show_helplimit_memory_soft = 2147483648

        exit 1limit_request = 8192

        ;;limit_time_cpu = 600

esaclimit_time_real = 1200

# Development settings
dev_mode = reload,qweb,werkzeug,xml

# Data directory
data_dir = filestore

# Auto-install web_responsive from OCA
init = web_responsive
EOF
}

# Create run script
create_run_script() {
    echo -e "${YELLOW}🚀 Creating run script...${NC}"
    
    if [ "$ENV_CHOICE" = "1" ]; then
        # Python environment run script
        cat > run.sh << 'EOF'
#!/bin/bash

# Neodoo18Framework - Project Run Script
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME=$(basename "$PROJECT_DIR")

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Starting Odoo Project: $PROJECT_NAME${NC}"
echo ""

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    echo -e "${YELLOW}🐍 Activating virtual environment...${NC}"
    source .venv/bin/activate
else
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
fi

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  PostgreSQL not running. Please start PostgreSQL first.${NC}"
    echo -e "   ${BLUE}brew services start postgresql${NC}  # macOS"
    echo -e "   ${BLUE}sudo systemctl start postgresql${NC}  # Linux"
    exit 1
fi

# Validate project before starting
echo -e "${YELLOW}✅ Validating project...${NC}"
if [ -d "../framework" ]; then
    python ../framework/validator/validate.py custom_addons/
else
    echo -e "${YELLOW}⚠️  Framework validator not found, skipping validation${NC}"
fi

# Start Odoo
echo -e "${YELLOW}🌐 Starting Odoo server...${NC}"
echo -e "${GREEN}📊 Access Odoo at: http://localhost:8069${NC}"
echo -e "${GREEN}🗄️  Database: $(grep '^db_name' odoo.conf | cut -d'=' -f2 | tr -d ' ')${NC}"
echo ""

# Save PID for management
python odoo_source/odoo-bin -c odoo.conf &
ODOO_PID=$!
echo $ODOO_PID > .odoo_pid

# Open browser automatically
sleep 3
if command -v open >/dev/null 2>&1; then
    open http://localhost:8069
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open http://localhost:8069
fi

# Wait for Odoo process
wait $ODOO_PID
rm -f .odoo_pid
EOF
    else
        # Docker environment run script
        cat > run.sh << 'EOF'
#!/bin/bash

# Neodoo18Framework - Docker Project Run Script
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME=$(basename "$PROJECT_DIR")

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Starting Odoo Project: $PROJECT_NAME${NC}"
echo ""

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Docker not running. Please start Docker first.${NC}"
    exit 1
fi

# Validate project before starting
echo -e "${YELLOW}✅ Validating project...${NC}"
if [ -d "../framework" ]; then
    python ../framework/validator/validate.py custom_addons/
else
    echo -e "${YELLOW}⚠️  Framework validator not found, skipping validation${NC}"
fi

# Start Docker containers
echo -e "${YELLOW}🐳 Starting Docker containers...${NC}"
docker-compose up -d

echo -e "${GREEN}📊 Access Odoo at: http://localhost:8069${NC}"
echo -e "${GREEN}🗄️  Database: $(grep '^db_name' odoo.conf | cut -d'=' -f2 | tr -d ' ')${NC}"
echo ""

# Follow logs
echo -e "${YELLOW}📋 Following Odoo logs (Ctrl+C to stop)...${NC}"
sleep 3

# Open browser automatically
if command -v open >/dev/null 2>&1; then
    open http://localhost:8069
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open http://localhost:8069
fi

docker-compose logs -f odoo
EOF
    fi
    
    chmod +x run.sh
}

# Create project README
create_project_readme() {
    echo -e "${YELLOW}📖 Creating project documentation...${NC}"
    
    cat > README.md << EOF
# $PROJECT_NAME

Odoo 18+ project created with Neodoo18Framework.

## Project Structure

\`\`\`
$PROJECT_NAME/
├── .venv/                    # Virtual environment (Python setup)
├── odoo_source/              # Odoo 18+ source code
├── custom_addons/            # Your custom modules
│   └── $MODULE_NAME/         # Your main module
├── community_addons/         # OCA modules
│   └── web/                  # OCA web modules (includes web_responsive)
├── logs/                     # Odoo log files
├── filestore/               # Odoo file storage
├── backups/                 # Database backups
├── docker-compose.yml       # Docker configuration (Docker setup)
├── odoo.conf               # Odoo configuration
├── requirements.txt        # Python dependencies
├── run.sh                  # Start Odoo script
└── README.md              # This file
\`\`\`

## Quick Start

1. **Start the project:**
   \`\`\`bash
   cd $PROJECT_PATH
   ./run.sh
   \`\`\`

2. **Access Odoo:**
   - URL: http://localhost:8069
   - Database: $DB_NAME
   - Create admin user on first access

## Development

### Adding New Modules

1. Create new module in \`custom_addons/\`:
   \`\`\`bash
   python ../framework/generator/create_project.py --name=my_new_module --type=minimal --output=custom_addons
   \`\`\`

2. Add module to addons_path in \`odoo.conf\`
3. Restart Odoo and update apps list

### Validation

Always validate your code before committing:
\`\`\`bash
python ../framework/validator/validate.py custom_addons/
\`\`\`

### Database Management

- **Backup database:**
  \`\`\`bash
  pg_dump $DB_NAME > backups/$DB_NAME-\$(date +%Y%m%d_%H%M%S).sql
  \`\`\`

- **Restore database:**
  \`\`\`bash
  dropdb $DB_NAME
  createdb $DB_NAME
  psql $DB_NAME < backups/backup_file.sql
  \`\`\`

## Configuration

### Environment: $([ "$ENV_CHOICE" = "1" ] && echo "Python Virtual Environment" || echo "Docker")
### Template: $TEMPLATE_TYPE
### Module: $MODULE_NAME
### Author: $AUTHOR_NAME

## Installed OCA Modules

- **web_responsive**: Responsive web interface for mobile devices

## Support

- Framework Documentation: ../docs/
- Odoo 18 Documentation: https://www.odoo.com/documentation/18.0/
- OCA Documentation: https://github.com/OCA/

---

Generated by Neodoo18Framework on $(date)
EOF
}

# Create requirements file
create_requirements_file() {
    echo -e "${YELLOW}📋 Creating requirements file...${NC}"
    
    cat > requirements.txt << EOF
# Neodoo18Framework Project Requirements
# Generated on $(date)

# Core Odoo dependencies (from odoo_source/requirements.txt)
Babel==2.9.1
chardet==4.0.0
cryptography==3.4.8
decorator==4.4.2
docutils==0.17
ebaysdk==2.1.5
freezegun==0.3.11
gevent==21.8.0
greenlet==1.1.2
idna==2.8
Jinja2==2.11.3
libsass==0.20.1
lxml==4.6.5
MarkupSafe==1.1.1
num2words==0.5.10
ofxparse==0.21
passlib==1.7.4
Pillow==8.4.0
polib==1.1.1
psutil==5.8.0
psycopg2==2.8.6
pydot==1.4.2
pyopenssl==22.0.0
PyPDF2==1.26.0
pyserial==3.4
python-dateutil==2.8.1
python-stdnum==1.16
pytz==2021.3
pyusb==1.0.2
qrcode==6.1
reportlab==3.5.59
requests==2.25.1
zeep==4.0.0
python-ldap==3.4.0
vobject==0.9.6.1
Werkzeug==2.0.2
xlrd==1.2.0
XlsxWriter==1.4.5
xlwt==1.3.0

# Additional development dependencies
psycopg2-binary==2.9.1
python-decouple==3.4
watchdog==2.1.6

# Development and testing tools
pytest==6.2.4
pytest-odoo==0.5.0
coverage==5.5
flake8==3.9.2
black==21.7b0
isort==5.9.3
EOF
}

# Main script logic
case "${1:-}" in
    "create")
        create_project
        ;;
    "delete")
        delete_project
        ;;
    "list")
        list_projects
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    "")
        create_project
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac