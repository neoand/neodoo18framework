# SOIL Core - Sistema de Orientação Inicial para LLM

> **Sistema Universal de Orientação para Desenvolvimento Odoo 18+**

## 🧠 Propósito

O SOIL Core é o ponto de entrada obrigatório para qualquer assistente LLM trabalhando com projetos Odoo 18+. Garante consistência, conformidade e eficiência no desenvolvimento.

## 🚀 Início Rápido para LLMs

### 1. **Contexto Obrigatório**
- Leia `framework/standards/ODOO18_CORE_STANDARDS.md` PRIMEIRO
- Consulte `framework/validator/validate.py` para validação
- Use templates em `templates/` como base

### 2. **Ferramentas Essenciais**
- **Validador**: `python framework/validator/validate.py [arquivo]`
- **Generator**: `python framework/generator/create_project.py --name=my_module`
- **Standards**: Sempre validar contra Odoo 18+ (nunca versões anteriores)

### 3. **Padrões Obrigatórios**
```xml
<!-- CORRETO: Odoo 18+ -->
<list string="Items">  <!-- NUNCA <tree> -->
    <field name="name"/>
</list>

<!-- CORRETO: Actions -->
<field name="view_mode">list,form</field>  <!-- NUNCA tree,form -->
```

```python
# CORRETO: Model template
class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model Description'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(required=True, tracking=True)
    
    @api.depends('field_name')
    def _compute_something(self):
        for record in self:
            record.computed_field = calculation
```

## 🛡️ Regras Invioláveis

### **XML Views**
- ✅ Use `<list>` para list views
- ❌ NUNCA use `<tree>`
- ✅ Use `view_mode="list,form"`
- ❌ NUNCA use `view_mode="tree,form"`

### **Python Models**
- ✅ Sempre include `# -*- coding: utf-8 -*-`
- ✅ Use `@api.depends()` em campos computados
- ✅ Include logging: `_logger = logging.getLogger(__name__)`

### **Security**
- ✅ Sempre criar `ir.model.access.csv`
- ✅ Definir grupos de segurança em XML
- ✅ Usar record rules para controle de acesso

## 🔄 Workflow Padrão

1. **Validate Current State**: Execute validator antes de começar
2. **Plan with Templates**: Use templates adequados para o tipo de módulo
3. **Implement with Standards**: Siga padrões Odoo 18+ rigorosamente
4. **Validate Changes**: Execute validator após implementação
5. **Document**: Atualize documentação se necessário

## 🚨 Protocolo de Erro

Se encontrar erros, aplicar **Imperial Rule**:
1. **Diagnóstico Completo**: Identificar erro precisamente
2. **Pesquisa Odoo 18+**: Consultar documentação oficial Odoo 18+
3. **Resolução Validada**: Aplicar solução testada
4. **Documentação**: Registrar solução para reuso

## 📋 Checklist de Conformidade

Antes de completar qualquer tarefa:

- [ ] Código valida com `framework/validator/validate.py`
- [ ] Views usam `<list>` não `<tree>`
- [ ] Actions usam `view_mode="list,form"`
- [ ] Models têm encoding UTF-8
- [ ] Security rules definidas
- [ ] Campos computados têm `@api.depends`

## 🎯 Templates Disponíveis

- `templates/minimal/` - Projeto básico funcional
- `templates/advanced/` - Módulo empresarial completo
- `templates/ecommerce/` - Base para e-commerce

## ⚡ Comandos Rápidos

```bash
# Criar novo projeto
python framework/generator/create_project.py --name=my_project --type=minimal

# Validar código
python framework/validator/validate.py path/to/file

# Iniciar desenvolvimento
./setup.sh

# Validação completa
python framework/validator/validate.py --verbose
```

## 🧩 Papéis de Agentes LLM

### Developer Role
- Implementa código seguindo os padrões
- Usa validador para garantir conformidade
- Mantém documentação atualizada

### Architect Role
- Define estrutura de módulos
- Planeja relacionamentos entre modelos
- Garante escalabilidade e manutenibilidade

### QA Role
- Valida código contra padrões Odoo 18+
- Testa funcionalidades implementadas
- Identifica possíveis problemas de segurança

---

**Lembre-se**: Este framework foi criado para eliminar confusão em desenvolvimento Odoo 18+. Siga os padrões rigorosamente para garantir sucesso.