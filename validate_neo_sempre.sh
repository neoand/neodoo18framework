#!/bin/bash
# Script de validação para módulos Neo Sempre
# Uso: ./validate_neo_sempre.sh [modulo]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretórios
FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEO_SEMPRE_DIR="$(dirname "$FRAMEWORK_DIR")/neo_sempre"
VALIDATOR="$FRAMEWORK_DIR/framework/validator/validate.py"
PLUGINS_DIR="$FRAMEWORK_DIR/corporate_plugins/neo_sempre"

# Função para exibir uso
show_usage() {
    echo "🔍 Validator Neo Sempre - Validação de Módulos Odoo 18+"
    echo ""
    echo "Uso:"
    echo "  $0                    # Validar todos os módulos"
    echo "  $0 semprereal         # Validar módulo específico"
    echo "  $0 neo_sempre         # Validar módulo neo_sempre"
    echo "  $0 neodoo_ai          # Validar módulo neodoo_ai"
    echo ""
    echo "Opções:"
    echo "  -h, --help           Mostrar esta ajuda"
    echo "  -v, --verbose        Modo verboso"
    echo "  --no-strict          Não usar modo estrito"
    echo ""
}

# Função para validar um módulo
validate_module() {
    local module_name=$1
    local module_path="$NEO_SEMPRE_DIR/custom_addons/$module_name"
    
    if [ ! -d "$module_path" ]; then
        echo -e "${RED}❌ Módulo não encontrado: $module_path${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📦 Validando módulo: ${YELLOW}$module_name${NC}"
    echo "   Caminho: $module_path"
    echo ""
    
    # Construir comando
    local cmd="python3 $VALIDATOR $module_path --plugins-dir $PLUGINS_DIR"
    
    if [ "$USE_STRICT" = true ]; then
        cmd="$cmd --strict"
    fi
    
    if [ "$VERBOSE" = true ]; then
        cmd="$cmd --verbose"
    fi
    
    # Executar validação
    if eval $cmd; then
        echo -e "${GREEN}✅ $module_name passou na validação${NC}"
        return 0
    else
        echo -e "${RED}❌ $module_name falhou na validação${NC}"
        return 1
    fi
}

# Função para validar todos os módulos
validate_all() {
    echo -e "${BLUE}🔍 Validando todos os módulos Neo Sempre...${NC}"
    echo ""
    
    local modules=("semprereal" "neo_sempre" "neodoo_ai")
    local failed=0
    local passed=0
    
    for module in "${modules[@]}"; do
        if validate_module "$module"; then
            ((passed++))
        else
            ((failed++))
        fi
        echo ""
    done
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}✅ Passou: $passed${NC} | ${RED}❌ Falhou: $failed${NC}"
    
    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}🎉 Todos os módulos validados com sucesso!${NC}"
        return 0
    else
        echo -e "${RED}⚠️  Alguns módulos falharam na validação${NC}"
        return 1
    fi
}

# Verificar se o diretório do validator existe
if [ ! -f "$VALIDATOR" ]; then
    echo -e "${RED}❌ Validator não encontrado: $VALIDATOR${NC}"
    echo "   Certifique-se de estar no diretório correto"
    exit 1
fi

# Verificar se o diretório de plugins existe
if [ ! -d "$PLUGINS_DIR" ]; then
    echo -e "${YELLOW}⚠️  Diretório de plugins não encontrado: $PLUGINS_DIR${NC}"
    echo "   Criando diretório e movendo plugin..."
    
    mkdir -p "$PLUGINS_DIR"
    
    # Se o plugin está na raiz de corporate_plugins, mover
    if [ -f "$FRAMEWORK_DIR/corporate_plugins/neo_sempre_rules.py" ]; then
        mv "$FRAMEWORK_DIR/corporate_plugins/neo_sempre_rules.py" "$PLUGINS_DIR/"
        echo -e "${GREEN}✅ Plugin movido para: $PLUGINS_DIR${NC}"
    else
        echo -e "${RED}❌ Plugin neo_sempre_rules.py não encontrado${NC}"
        exit 1
    fi
fi

# Configurações padrão
USE_STRICT=true
VERBOSE=false

# Parse argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --no-strict)
            USE_STRICT=false
            shift
            ;;
        *)
            MODULE_NAME=$1
            shift
            ;;
    esac
done

# Executar validação
if [ -z "$MODULE_NAME" ]; then
    validate_all
else
    validate_module "$MODULE_NAME"
fi
