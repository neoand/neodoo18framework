# SOIL System - Sistema de Orientação Inicial para LLM

> **Ponto de entrada obrigatório para qualquer LLM trabalhando com Neodoo18Framework**

## 🧠 Inicialização Imediata

**LEIA ISTO PRIMEIRO** antes de qualquer desenvolvimento:

1. **Padrões Odoo 18+**: Use SEMPRE `<list>` nunca `<tree>` em XML
2. **View Mode**: Use SEMPRE `"list,form"` nunca `"tree,form"`  
3. **Validação Obrigatória**: Execute `python framework/validator.py` antes de commits
4. **Templates Base**: Use `templates/` para scaffolding correto

## 🎯 Workflow Padrão

### Para Novos Projetos:
```bash
python generator/create_project.py --name=my_project --type=base
cd projects/my_project
./init_project.sh
```

### Para Desenvolvimento:
1. **Sempre validar**: `python framework/validator.py src/`
2. **Seguir templates**: Copiar de `templates/patterns/`
3. **Usar agentes**: Backend → Frontend → Security → QA
4. **Testar conformidade**: `./validate_odoo18.sh`

## ⚠️ REGRAS CRÍTICAS - NÃO VIOLE

### XML (Views)
```xml
<!-- ✅ CORRETO (Odoo 18+) -->
<list string="Records">
    <field name="name"/>
</list>

<!-- ❌ ERRADO (Odoo ≤17) -->
<tree string="Records">
    <field name="name"/>
</tree>
```

### Python (Models)
```python
# ✅ CORRETO
class MyModel(models.Model):
    _name = 'my.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(required=True, tracking=True)
    
    @api.depends('field')
    def _compute_something(self):
        for record in self:
            record.computed_field = calculation
```

### Actions
```xml
<!-- ✅ CORRETO -->
<field name="view_mode">list,form</field>

<!-- ❌ ERRADO -->
<field name="view_mode">tree,form</field>
```

## 🛡️ Sistema de Validação Automática

O framework inclui validação automática que:
- ✅ Detecta padrões Odoo ≤17 (proibidos)
- ✅ Força conformidade Odoo 18+
- ✅ Auto-corrige problemas comuns
- ✅ Gera relatórios de qualidade

## 🤖 Para LLMs: Como Usar Este Framework

### 1. Sempre começar com:
```python
# Execute isto para carregar orientações
exec(open('framework/llm_init.py').read())
```

### 2. Para cada tarefa:
- Consulte `templates/patterns/` para o padrão correto
- Use `framework/validator.py` para validar código
- Siga `framework/standards/` para conformidade

### 3. Estrutura de desenvolvimento:
```
1. Backend Agent → Modelos e lógica
2. Frontend Agent → Views e menus  
3. Security Agent → Permissões e acesso
4. QA Agent → Validação final
```

## 📋 Checklist Obrigatório

Antes de qualquer commit/entrega:

- [ ] Executou `python framework/validator.py`
- [ ] Views usam `<list>` não `<tree>`
- [ ] Actions usam `view_mode="list,form"`
- [ ] Modelos têm `@api.depends` corretos
- [ ] Segurança implementada corretamente
- [ ] Testes passando

---

**IMPORTANTE**: Este documento é seu guia constante. Consulte sempre que iniciar uma nova sessão ou tarefa!