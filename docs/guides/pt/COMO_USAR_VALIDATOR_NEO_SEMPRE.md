# 🔍 Como Usar o Validator Neo Sempre

Este guia mostra como usar o plugin de validação `neo_sempre_rules.py` para verificar e garantir a qualidade dos módulos do projeto Neo Sempre.

## 📋 O Que o Plugin Valida

O plugin `neo_sempre_rules.py` verifica:

✅ **Prefixos de Módulo**: Permite `semprereal`, `neo_sempre`, `neodoo_ai`, `ns_`  
✅ **Campos CPF**: Deve usar o campo padrão `vat` do Odoo, não criar campo `cpf` customizado  
✅ **Campos Monetários**: Devem ter `currency_field` definido  
✅ **Campos INSS**: Verificar presença de campos obrigatórios (numero_beneficio, margem_consignavel, valor_beneficio)  
✅ **Docstrings**: Métodos de ação devem ter documentação  
✅ **Views Odoo 18+**: Uso de `<list>` em vez de `<tree>`, `view_mode='list,form'` em vez de `'tree,form'`  
✅ **Segurança**: Verificar grupos de acesso para beneficiários  
✅ **Versão Odoo**: Módulos devem ter versão `18.0.x.x.x`  

## 🚀 Uso Básico

### 1. Validar um Módulo Específico

```bash
# No diretório do neodoo18framework
cd ~/neo_sempre/neodoo18framework

# Validar o módulo semprereal
python3 framework/validator/validate.py \
    ../neo_sempre/custom_addons/semprereal \
    --plugins-dir corporate_plugins/neo_sempre \
    --strict
```

### 2. Validar Todos os Módulos Custom

```bash
# Validar neo_sempre
python3 framework/validator/validate.py \
    ../neo_sempre/custom_addons/neo_sempre \
    --plugins-dir corporate_plugins/neo_sempre \
    --strict

# Validar neodoo_ai
python3 framework/validator/validate.py \
    ../neo_sempre/custom_addons/neodoo_ai \
    --plugins-dir corporate_plugins/neo_sempre \
    --strict
```

### 3. Modo Verboso (Ver Todos os Detalhes)

```bash
python3 framework/validator/validate.py \
    ../neo_sempre/custom_addons/semprereal \
    --plugins-dir corporate_plugins/neo_sempre \
    --strict \
    --verbose
```

## 📊 Entendendo a Saída

### ✅ Validação Bem-Sucedida

```
INFO: ✅ Validation successful!
```

Significa que não há erros críticos. Pode ter avisos (warnings) que não impedem o módulo de funcionar.

### ⚠️ Validação com Avisos

```
WARNING: Validation passed with 6 warnings
WARNING:   - Method action_archive should call self.ensure_one() in models/partner.py
WARNING:   - Campo monetário 'margem_consignavel' deve especificar 'currency_field'
INFO: ✅ Validation successful!
```

Avisos indicam melhorias recomendadas, mas não impedem a execução.

### ❌ Validação com Erros

```
ERROR: Validation failed: 2 errors, 5 warnings
ERROR:   - Use o campo 'vat' padrão do Odoo para CPF, não crie campo 'cpf' customizado
ERROR:   - Odoo 18+ requer tag <list> em vez de <tree> para list views
ERROR: ❌ Validation failed!
```

Erros críticos que devem ser corrigidos antes de usar o módulo.

## 🛠️ Correções Comuns

### 1. Campo CPF Customizado

❌ **Errado:**
```python
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    cpf = fields.Char(string='CPF')
```

✅ **Correto:**
```python
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Usar o campo 'vat' padrão do Odoo
    vat = fields.Char(string='CPF/CNPJ')
```

### 2. Campos Monetários sem Currency

❌ **Errado:**
```python
margem_consignavel = fields.Monetary(string='Margem Consignável')
```

✅ **Correto:**
```python
margem_consignavel = fields.Monetary(
    string='Margem Consignável',
    currency_field='currency_id'
)
currency_id = fields.Many2one('res.currency', string='Moeda', default=lambda self: self.env.company.currency_id)
```

### 3. Views com Tag <tree> (Odoo 18+)

❌ **Errado:**
```xml
<record id="view_beneficio_tree" model="ir.ui.view">
    <field name="model">semprereal.beneficio</field>
    <field name="arch" type="xml">
        <tree string="Benefícios">
            <field name="numero_beneficio"/>
        </tree>
    </field>
</record>
```

✅ **Correto:**
```xml
<record id="view_beneficio_list" model="ir.ui.view">
    <field name="model">semprereal.beneficio</field>
    <field name="arch" type="xml">
        <list string="Benefícios">
            <field name="numero_beneficio"/>
        </list>
    </field>
</record>
```

### 4. Actions com view_mode Antigo

❌ **Errado:**
```xml
<field name="view_mode">tree,form</field>
```

✅ **Correto:**
```xml
<field name="view_mode">list,form</field>
```

### 5. Métodos de Ação sem ensure_one()

❌ **Errado:**
```python
def action_validate(self):
    self.state = 'validated'
```

✅ **Correto:**
```python
def action_validate(self):
    """Valida o benefício após verificar os dados."""
    self.ensure_one()  # Garante operação em registro único
    self.state = 'validated'
```

## 🎯 Casos de Uso Práticos

### Antes de Commitar Código

```bash
# Validar módulo antes de git commit
python3 framework/validator/validate.py \
    ../neo_sempre/custom_addons/semprereal \
    --plugins-dir corporate_plugins/neo_sempre \
    --strict

# Se passar, pode commitar
git add .
git commit -m "feat: adicionar validação de margem consignável"
```

### Integração com VSCode

Crie uma task em `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Validar Módulo Neo Sempre",
      "type": "shell",
      "command": "python3",
      "args": [
        "neodoo18framework/framework/validator/validate.py",
        "${workspaceFolder}/neo_sempre/custom_addons/semprereal",
        "--plugins-dir",
        "neodoo18framework/corporate_plugins/neo_sempre",
        "--strict",
        "--verbose"
      ],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      },
      "problemMatcher": []
    }
  ]
}
```

Execute com: `Cmd+Shift+B` (macOS) ou `Ctrl+Shift+B` (Windows/Linux)

### Script de Validação em Lote

Crie um script `validate_all.sh`:

```bash
#!/bin/bash

echo "🔍 Validando todos os módulos Neo Sempre..."
echo ""

VALIDATOR="python3 neodoo18framework/framework/validator/validate.py"
PLUGINS="--plugins-dir neodoo18framework/corporate_plugins/neo_sempre"

modules=(
    "neo_sempre/custom_addons/semprereal"
    "neo_sempre/custom_addons/neo_sempre"
    "neo_sempre/custom_addons/neodoo_ai"
)

for module in "${modules[@]}"; do
    echo "📦 Validando $module..."
    $VALIDATOR $module $PLUGINS --strict
    if [ $? -eq 0 ]; then
        echo "✅ $module passou na validação"
    else
        echo "❌ $module falhou na validação"
        exit 1
    fi
    echo ""
done

echo "✅ Todos os módulos validados com sucesso!"
```

Execute:
```bash
chmod +x validate_all.sh
./validate_all.sh
```

## 🔧 Configuração Avançada

### Variável de Ambiente

Configure para não precisar especificar `--plugins-dir`:

```bash
# No seu ~/.zshrc ou ~/.bashrc
export NEODOO_VALIDATOR_PLUGINS="$HOME/neo_sempre/neodoo18framework/corporate_plugins/neo_sempre"

# Agora pode usar simplesmente:
python3 framework/validator/validate.py ../neo_sempre/custom_addons/semprereal --strict
```

### Ignorar Avisos Específicos (Não Recomendado)

Se precisar validar sem modo estrito:

```bash
# Modo normal (não falha em warnings)
python3 framework/validator/validate.py \
    ../neo_sempre/custom_addons/semprereal \
    --plugins-dir corporate_plugins/neo_sempre
```

## 📚 Recursos Adicionais

- [Validator Best Practices](../../VALIDATOR_BEST_PRACTICES.md) - Melhores práticas e troubleshooting
- [Validator Plugin Guide](../en/VALIDATOR_PLUGINS.md) - Como criar plugins customizados
- [SOIL Core Standards](../../standards/SOIL_CORE.md) - Padrões completos do Odoo 18+

## 🆘 Problemas Comuns

### Plugin não carrega

**Problema:** `WARNING: Plugin directory not found`

**Solução:** Certifique-se de estar no diretório correto:
```bash
cd ~/neo_sempre/neodoo18framework
pwd  # Deve mostrar: /Users/andersongoliveira/neo_sempre/neodoo18framework
```

### Muitos erros de prefixo "acme_"

**Problema:** Validador mostra erros sobre prefixo "acme_"

**Solução:** O plugin Acme está sendo carregado junto. Use o subdiretório:
```bash
# Criar estrutura isolada
mkdir -p corporate_plugins/neo_sempre
mv corporate_plugins/neo_sempre_rules.py corporate_plugins/neo_sempre/

# Agora usar o subdiretório
python3 framework/validator/validate.py module --plugins-dir corporate_plugins/neo_sempre
```

### Arquivo não encontrado

**Problema:** `ERROR: File not found: ../neo_sempre/custom_addons/semprereal`

**Solução:** Use caminhos absolutos ou verifique o caminho relativo:
```bash
# Caminho absoluto (mais confiável)
python3 framework/validator/validate.py \
    ~/neo_sempre/neo_sempre/custom_addons/semprereal \
    --plugins-dir corporate_plugins/neo_sempre \
    --strict
```

## 💡 Dicas

1. **Sempre use `--strict`** em produção e antes de commitar
2. **Use `--verbose`** quando estiver corrigindo erros para ver mais detalhes
3. **Valide frequentemente** durante o desenvolvimento, não apenas no final
4. **Configure a task do VSCode** para validar com um atalho de teclado
5. **Documente decisões** quando decidir ignorar algum warning específico

---

**Próximos Passos:**
1. Validar todos os módulos atuais
2. Corrigir erros críticos encontrados
3. Configurar validação automática no CI/CD
4. Criar script de validação pré-commit
