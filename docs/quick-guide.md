# Guia Rápido - Neodoo18Framework

Este guia fornece instruções rápidas para começar a usar o Neodoo18Framework.

## Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Git

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework
```

2. Configure o ambiente Python:

```bash
./env.sh setup
./env.sh activate
```

3. Para configuração completa com projeto:

```bash
./setup.sh
```

## Comandos Principais

### 🎨 Nova Interface Visual (Recomendado)

```bash
# Menu interativo com interface linda
./neodoo                          # Interface visual completa (recomendado!)
```

### Criar um Novo Projeto

```bash
# Método visual interativo (recomendado)
./neodoo create                   # Assistente visual com seleção de template

# Método direto
./neodoo create --name my_project --template minimal --base-dir ~/odoo_projects

# Gerador direto (método legado)
python framework/generator/create_project.py --name=my_project --type=minimal
```

### Gerenciar Projetos

```bash
# Interface visual (recomendado)
./neodoo                          # Menu com todas as opções

# Comandos diretos
./neodoo list                     # Listar projetos com cores
./neodoo run                      # Executar projeto atual
./neodoo delete                   # Deletar projeto com confirmação
./neodoo doctor                   # Verificar ambiente
./neodoo update --path /projeto   # Atualizar projeto
```

### Validar Código

```bash
# Validar um arquivo específico
python framework/validator/validate.py path/to/file.py

# Validar um projeto inteiro
python framework/validator/validate.py my_project/

# Validação com correção automática
python framework/validator/validate.py path/to/file.py --auto-fix

# Validação detalhada
python framework/validator/validate.py . --verbose
```

## Estrutura do Projeto

Após a criação, seu projeto terá esta estrutura:

```
my_project/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── template_model.py
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── views/
│   ├── views.xml
│   └── menu.xml
└── tests/
    └── __init__.py
```

## Checklist de Qualidade

Antes de finalizar qualquer código:

- [ ] O validador retorna 100% de conformidade
- [ ] Todas as views usam `<list>`, não `<tree>`
- [ ] Todos os métodos calculados têm `@api.depends()`
- [ ] Os arquivos de segurança estão presentes
- [ ] Os cabeçalhos de codificação UTF-8 estão presentes
- [ ] Os modelos incluem atributos `_name` e `_description` adequados

## Links Úteis

- [[index|Documentação Principal]]
- [[workflows|Workflows e Processos]]
- [[../README|README do Projeto]]