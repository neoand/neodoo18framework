# 🚀 Guia Completo: Neodoo18Framework

> **Framework Universal para Desenvolvimento Odoo 18+ com Sistema SOIL**

## 📚 **ÍNDICE**

1. [Instalação Rápida](#instalação-rápida)
2. [Primeiro Projeto](#primeiro-projeto)  
3. [Desenvolvimento com IA](#desenvolvimento-com-ia)
4. [Padrões Obrigatórios](#padrões-obrigatórios)
5. [Validação Automática](#validação-automática)
6. [Exemplos Práticos](#exemplos-práticos)
7. [Integração com Odoo](#integração-com-odoo)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 **INSTALAÇÃO RÁPIDA**

### 🐍 Método 1: Setup Completo com Ambiente Python (RECOMENDADO)
```bash
# 1. Clone o framework
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# 2. Setup automático do ambiente Python
./env.sh setup
# ✅ Cria virtual environment (.venv/)
# ✅ Instala todas as dependências Odoo 18+
# ✅ Configura ferramentas de desenvolvimento

# 3. Criar primeiro projeto
./env.sh activate
./quick-start.sh meu_primeiro_projeto

# 4. Validar qualidade
python3 framework/validator.py meu_primeiro_projeto/
# Expected: 100% compliance ✅
```

### ⚡ Método 2: Projeto com Ambiente Automático
```bash
# Clone + projeto + ambiente em uma sequência
# 🚀 Guia Completo: Neodoo18Framework

> Framework universal para Odoo 18+ com SOIL e um CLI de um comando.

## 📚 Índice

1. Início Rápido (recomendado)
2. Anatomia do Projeto
3. Fluxos Essenciais (criar, gerenciar, validar)
4. Padrões Obrigatórios (Odoo 18+)
5. Modos do Validador: strict e template-mode
6. Desenvolvimento com IA (LLM)
7. Update e Doctor
8. Troubleshooting e Checklist

---

## ⚡ Início Rápido (30s)

> [!tip]
> O novo CLI é o caminho mais rápido. Scripts legados existem, mas o CLI oferece a melhor DX.

```bash
# 1) Clonar
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# 2) Criar um projeto Odoo 18+ completo (assistente)
./neodoo create

# 3) Executar
cd ~/odoo_projects/<seu_projeto>
./run.sh
```

Não interativo (reprodutível) via config:
```bash
./neodoo create --from-config /caminho/para/.neodoo.yml
```

Exemplo mínimo de .neodoo.yml
```yaml
version: 1
name: meu_projeto_odoo18
base_dir: ~/odoo_projects
module: meu_modulo
template: minimal
venv: true
odoo_branch: 18.0
```

Você também pode usar o exemplo compartilhado diretamente:
```bash
./neodoo create --from-config ./docs/.neodoo.yml
```

> [!note]
> O CLI cria: Odoo source, OCA/web, custom_addons, venv (opcional), odoo.conf e run.sh.

---

## 🏗 Anatomia do Projeto

```
~/odoo_projects/seu_projeto/
├── odoo_source/           # Código do Odoo 18+ (git clone)
├── community_addons/      # Módulos OCA (inclui web)
│   └── web/
├── custom_addons/         # Seus módulos
├── .venv/                 # Ambiente Python isolado (opcional)
├── odoo.conf              # Pré-configurado para dev
├── run.sh                 # Inicia o Odoo
└── .neodoo.yml            # Config do projeto (para create reprodutível)
```

> [!example]
> Rode o validador na pasta dos seus módulos customizados:
> 
> ```bash
> python framework/validator/validate.py ~/odoo_projects/seu_projeto/custom_addons --strict --auto-fix
> ```

---

## 🔁 Fluxos Essenciais

Criar
```bash
./neodoo create                         # assistente
./neodoo create --from-config .neodoo.yml  # reprodutível
```

Gerenciar
```bash
./neodoo list
./neodoo delete
./neodoo doctor                         # checa env (python, git, portas)
./neodoo doctor --path /caminho/do/projeto
./neodoo update --path /caminho/do/projeto  # puxa repos + atualiza deps
```

Validar (conformidade Odoo 18+)
```bash
# Na raiz do repositório
python framework/validator/validate.py caminho/para/modulo --strict --auto-fix
python framework/validator/validate.py templates/minimal --template-mode --auto-fix
```

---

## 📏 Padrões Obrigatórios (Odoo 18+)

> [!warning]
> Nunca use <tree>. Sempre use <list>. Actions devem declarar view_mode="list,form".

XML (correto)
```xml
<record id="book_view_list" model="ir.ui.view">
  <field name="name">book.view.list</field>
  <field name="model">bjj.book</field>
  <field name="arch" type="xml">
    <list string="Livros">
      <field name="title"/>
      <field name="author"/>
    </list>
  </field>
</record>

<record id="book_action" model="ir.actions.act_window">
  <field name="name">Livros</field>
  <field name="res_model">bjj.book</field>
  <field name="view_mode">list,form</field>
</record>
```

Python (básico do modelo)
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Book(models.Model):
    _name = 'bjj.book'
    _description = 'Livro da Biblioteca'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(required=True, tracking=True)
    author = fields.Char(required=True)
    isbn = fields.Char(size=13)

    @api.constrains('isbn')
    def _check_isbn(self):
        for rec in self:
            if rec.isbn and len(rec.isbn) != 13:
                raise ValidationError(_('O ISBN deve conter 13 dígitos'))
```

---

## 🧪 Modos do Validador

> [!info]
> strict: promove certos avisos a erros para projetos de usuário.
> 
> template-mode: mantém placeholders/cosméticos como avisos em templates, mantendo regras críticas do Odoo 18+ como erros.

Exemplos
```bash
# Strict (recomendado para módulos reais)
python framework/validator/validate.py meu_modulo --strict --auto-fix

# Template (permissivo para placeholders)
python framework/validator/validate.py templates/advanced --template-mode --auto-fix
```

---

## 🤖 Desenvolvimento com IA

> [!tip]
> Comece por: framework/standards/ODOO18_CORE_STANDARDS.md e framework/standards/SOIL_CORE.md.

Contexto
```bash
cat framework/standards/ODOO18_CORE_STANDARDS.md
cat framework/standards/SOIL_CORE.md
```

Prompt inicial
```
Crie um módulo Biblioteca seguindo Odoo 18+:
- Modelo: bjj.book (title, author, isbn, category)
- Views: list + form (sem tree)
- Action: view_mode="list,form"
- Segurança: access.csv básico
Depois rode: python framework/validator/validate.py <path> --strict --auto-fix
```

---

## � Update e 🩺 Doctor

```bash
./neodoo doctor                         # checa python3, git, docker/psql e portas 8069/8072
./neodoo doctor --path /projeto         # checa também odoo_source, addons e venv

./neodoo update --path /projeto         # git pull Odoo + OCA/web e atualiza deps do venv
```

> [!success]
> Use o doctor antes de iniciar e após updates para detectar conflitos de portas e ferramentas ausentes.

---

## � CI & Sanity Checks

Este repositório inclui verificações automáticas para manter a experiência do desenvolvedor sólida:

- Verificações rápidas (CI, em push/PR):
  - Lista templates do gerador
  - Gera um módulo minimal (offline)
  - Valida o módulo gerado com o validador em modo strict

- Teste smoke (manual):
  - Acione o workflow "CI" com "Run workflow" (workflow_dispatch)
  - Executa `scripts/dev/quick_sanity.sh` que realiza um fluxo completo end-to-end (clona Odoo e OCA/web)

Execução local do sanity:

```bash
# Na raiz do repo
bash scripts/dev/quick_sanity.sh

# Ou passo a passo
python3 framework/generator/create_project.py --name tmp --list-templates
./neodoo create --name sanity_proj --base-dir /tmp/neodoo_sanity --module sanity_mod --template minimal --no-venv
./neodoo doctor --path /tmp/neodoo_sanity/sanity_proj
python3 framework/validator/validate.py /tmp/neodoo_sanity/sanity_proj/custom_addons/sanity_mod --strict --auto-fix
```

Notas:
- O template "minimal" gera um módulo que passa na validação strict por padrão.
- Nomes de arquivos com placeholders são automaticamente renomeados durante a geração.

---

## �🧯 Troubleshooting

> [!failure] Invalid view mode 'tree'
```bash
python framework/validator/validate.py meu_modulo --auto-fix
```

> [!question] Module not found
```bash
ls meu_modulo/__init__.py
cat meu_modulo/models/__init__.py  # confira os imports
```

> [!warning] Access rights
```bash
ls meu_modulo/security/
grep "group_" meu_modulo/security/*.xml || true
```

---

## ✅ Checklist de Qualidade

- [ ] Validador passa (strict) sem erros
- [ ] XML usa <list>, actions usam "list,form"
- [ ] Modelos com _description e constraints básicas
- [ ] Segurança: ir.model.access.csv presente e listado no manifest
- [ ] README e testes mínimos presentes

> [!tip]
> Para templates, valide com --template-mode para evitar ruído de placeholders mantendo problemas reais visíveis.
- **Discussions**: Ajuda e dicas da comunidade

### Suporte:
- **Wiki**: Casos de uso avançados
- **Examples**: Projetos exemplo  
- **Updates**: Framework sempre atualizado

---

## 🎯 **CONCLUSÃO**

O **Neodoo18Framework** transforma desenvolvimento Odoo de **semanas em minutos**:

✅ **Templates Battle-Tested** - Padrões validados em produção  
✅ **100% Odoo 18+ Compliance** - Sem erros de compatibilidade  
✅ **Validação Automática** - Qualidade enterprise garantida  
✅ **IA-Friendly** - Sistema SOIL otimizado para LLMs  
✅ **Open Source** - MIT License, liberdade total  

**🚀 Start coding now!**

```bash
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework  
./quick-start.sh amazing_project
python3 framework/validator.py amazing_project/
# 100% = Ready for production! 🎉
```

---

## 🔎 OCA Watch & Rollups Semanais

Fique por dentro do ecossistema OCA direto deste repositório:

- Digests diários: o workflow “OCA Watch” monitora repositórios OCA selecionados e grava resumos em `docs/oca-digests/`. Quando há novidades, abre um PR com labels/assignee automáticos e auto‑merge habilitado.
- Rollups semanais: toda segunda (03:00 UTC), o workflow “OCA Weekly Rollup” consolida os últimos 7 dias em `docs/oca-digests/rollups/YYYY-Www.md`.

Execução manual:
- Na aba Actions do GitHub, rode “OCA Watch” (opcionalmente com bootstrap na primeira execução) ou “OCA Weekly Rollup”.

Saiba mais: consulte `docs/oca-digests/README.md`.

---

**Happy Coding! 🎯**