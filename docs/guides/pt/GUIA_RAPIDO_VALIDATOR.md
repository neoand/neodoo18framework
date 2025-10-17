# 🚀 Guia Rápido - Validator Neo Sempre

## ✅ Como Usar (3 formas)

### 1️⃣ **Forma Mais Fácil - Script Automatizado**

```bash
cd ~/neo_sempre/neodoo18framework

# Validar um módulo específico
./validate_neo_sempre.sh semprereal

# Validar todos os módulos
./validate_neo_sempre.sh

# Modo verboso (mais detalhes)
./validate_neo_sempre.sh semprereal -v
```

### 2️⃣ **Comando Direto Python**

```bash
cd ~/neo_sempre/neodoo18framework

python3 framework/validator/validate.py \
    ../neo_sempre/custom_addons/semprereal \
    --plugins-dir corporate_plugins/neo_sempre \
    --strict
```

### 3️⃣ **Variável de Ambiente (Configurar uma vez)**

```bash
# Adicionar ao ~/.zshrc
export NEODOO_VALIDATOR_PLUGINS="$HOME/neo_sempre/neodoo18framework/corporate_plugins/neo_sempre"

# Depois pode usar simplesmente:
cd ~/neo_sempre/neodoo18framework
python3 framework/validator/validate.py ../neo_sempre/custom_addons/semprereal --strict
```

## 🔍 Principais Erros Encontrados no Semprereal

### ❌ **ERRO 1: Campo CPF Customizado**
**Arquivo:** `wizard/import_partner_wizard.py`

```python
# ❌ ERRADO
cpf = fields.Char(string='CPF')

# ✅ CORRETO
# Remover o campo cpf e usar o campo vat padrão do Odoo
vat = fields.Char(string='CPF/CNPJ')
```

### ❌ **ERRO 2: View Mode com 'tree' (Odoo 18+)**
**Arquivo:** `views/semprereal_beneficio_views.xml`

```xml
<!-- ❌ ERRADO -->
<field name="view_mode">tree,form</field>

<!-- ✅ CORRETO -->
<field name="view_mode">list,form</field>
```

### ❌ **ERRO 3: Tag <tree> em vez de <list>**
**Arquivo:** `views/semprereal_beneficio_views.xml`

```xml
<!-- ❌ ERRADO -->
<tree string="Benefícios">
    <field name="numero_beneficio"/>
</tree>

<!-- ✅ CORRETO -->
<list string="Benefícios">
    <field name="numero_beneficio"/>
</list>
```

## ⚠️ Principais Warnings (Avisos)

### 1. **Métodos sem ensure_one()**
```python
# ⚠️ AVISO
def action_toggle_ativo(self):
    self.ativo = not self.ativo

# ✅ MELHOR
def action_toggle_ativo(self):
    """Alterna o status ativo do benefício."""
    self.ensure_one()
    self.ativo = not self.ativo
```

### 2. **Campo margem_consignavel faltando**
```python
# ⚠️ AVISO: Modelo de benefício deve ter campo 'margem_consignavel'

# ✅ ADICIONAR
class SemprerealBeneficio(models.Model):
    _name = 'semprereal.beneficio'
    
    margem_consignavel = fields.Monetary(
        string='Margem Consignável',
        currency_field='currency_id',
        help='Margem disponível para empréstimos consignados'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moeda',
        default=lambda self: self.env.company.currency_id
    )
```

### 3. **IDs XML sem prefixo do módulo**
```xml
<!-- ⚠️ AVISO -->
<record id="view_semprereal_beneficio_tree" model="ir.ui.view">

<!-- ✅ MELHOR -->
<record id="semprereal_view_beneficio_list" model="ir.ui.view">
```

## 📊 Resumo dos Erros Encontrados

```
❌ 3 ERROS CRÍTICOS:
   1. Campo 'cpf' customizado (usar 'vat')
   2. view_mode='tree,form' (mudar para 'list,form')
   3. Tag <tree> (mudar para <list>)

⚠️ 28 AVISOS:
   - 14 IDs XML sem prefixo
   - 8 Actions sem 'list' no view_mode
   - 2 Campos INSS faltando
   - 1 Método sem ensure_one()
   - 1 Autor não especificado
   - 2 Views sem campos importantes
```

## 🛠️ Prioridade de Correção

### 🔴 **URGENTE (Erros Críticos)**
1. ✅ Remover campo `cpf` e usar `vat` em `import_partner_wizard.py`
2. ✅ Trocar `tree` por `list` em todas as views
3. ✅ Mudar `view_mode='tree,form'` para `'list,form'`

### 🟡 **IMPORTANTE (Melhorias)**
1. Adicionar campo `margem_consignavel` no modelo de benefício
2. Adicionar `ensure_one()` em métodos de ação
3. Adicionar docstrings nos métodos

### 🟢 **OPCIONAL (Padrões)**
1. Renomear IDs XML com prefixo do módulo
2. Adicionar 'Neo Sempre' como autor no manifest
3. Adicionar campos faltantes nas views

## 📝 Checklist de Correção

```bash
# 1. Fazer backup
cd ~/neo_sempre
git status
git add -A
git commit -m "backup antes de correções do validator"

# 2. Corrigir erros críticos
# - Editar wizard/import_partner_wizard.py (remover campo cpf)
# - Editar views/semprereal_beneficio_views.xml (tree → list, view_mode)

# 3. Validar novamente
cd ~/neo_sempre/neodoo18framework
./validate_neo_sempre.sh semprereal

# 4. Corrigir avisos importantes
# - Adicionar margem_consignavel
# - Adicionar ensure_one()

# 5. Validar final
./validate_neo_sempre.sh semprereal --verbose

# 6. Commitar correções
cd ~/neo_sempre
git add -A
git commit -m "fix: correções do validator Neo Sempre - Odoo 18+"
```

## 🎯 Comandos Úteis

```bash
# Ver ajuda
./validate_neo_sempre.sh --help

# Validar com detalhes
./validate_neo_sempre.sh semprereal -v

# Validar sem modo estrito (só avisos)
./validate_neo_sempre.sh semprereal --no-strict

# Validar todos os módulos
./validate_neo_sempre.sh

# Validar módulo específico
./validate_neo_sempre.sh neo_sempre
./validate_neo_sempre.sh neodoo_ai
```

## 📚 Documentação Completa

- [Guia Completo em Português](./COMO_USAR_VALIDATOR_NEO_SEMPRE.md)
- [Validator Best Practices](../../VALIDATOR_BEST_PRACTICES.md)
- [Validator Plugin Guide](../en/VALIDATOR_PLUGINS.md)

## 💡 Dica Final

**Sempre valide antes de commitar:**
```bash
cd ~/neo_sempre/neodoo18framework
./validate_neo_sempre.sh semprereal && echo "✅ Pronto para commit!" || echo "❌ Corrigir erros primeiro"
```
