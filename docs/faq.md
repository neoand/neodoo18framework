# FAQ - Perguntas Frequentes

## Sobre o Framework

### O que é o Neodoo18Framework?
O Neodoo18Framework é um framework de desenvolvimento para Odoo 18+ com design LLM-first, que fornece ferramentas, padrões e guias para desenvolvimento rápido e eficiente. O framework impõe padrões modernos do Odoo 18+ e fornece validadores, geradores e templates para desenvolvimento acelerado.

### Por que usar o Neodoo18Framework em vez de desenvolver diretamente para o Odoo?
O Neodoo18Framework garante conformidade com as melhores práticas do Odoo 18+, acelera o desenvolvimento com templates e geradores, e possui um sistema de validação que minimiza erros comuns. Além disso, inclui diretrizes LLM-first que permitem usar modelos de linguagem para auxiliar no desenvolvimento.

### O que significa "LLM-first design"?
Significa que o framework foi projetado considerando a interação com Modelos de Linguagem de Grande Escala (LLMs). Isso inclui documentação estruturada, padrões claros e consistentes, e diretrizes específicas (SOIL - Sistema de Orientação Integrada LLM) para que os modelos possam gerar código compatível e de alta qualidade.

## Instalação e Configuração

### Quais são os requisitos para usar o Neodoo18Framework?
- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Git
- Conhecimento básico de Odoo e desenvolvimento Python

### Como instalar o Neodoo18Framework?
```bash
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework
./env.sh setup
./env.sh activate
```

Para configuração completa com projeto:
```bash
./setup.sh
```

### Posso usar o framework com Docker?
Sim, o script `setup.sh` oferece opção para configuração com Docker, facilitando a criação de ambientes isolados e consistentes.

## Desenvolvimento

### Qual é a diferença entre os templates disponíveis?
- **Minimal**: Estrutura básica para módulos simples
- **Advanced**: Estrutura completa para módulos empresariais com recursos avançados
- **E-commerce**: Estrutura específica para módulos de comércio eletrônico

### Como faço para validar se meu código está em conformidade com os padrões do Odoo 18+?
```bash
python framework/validator/validate.py path/to/file.py
```
ou para validar um projeto inteiro:
```bash
python framework/validator/validate.py my_project/
```

### Quais são os erros mais comuns encontrados pelo validador?
- Uso de `<tree>` em vez de `<list>` nas views
- Falta de decorador `@api.depends()` em métodos computados
- Ausência de cabeçalhos UTF-8
- Falta de arquivos de segurança
- Padrões de herança incorretos

## Papéis e Especialidades

### Quais são os papéis especializados definidos no framework?
- OWL Specialist (Frontend)
- Backend Developer
- UX/UI Designer
- DevOps Engineer
- Security Expert
- Integration Specialist
- Data Migration Specialist
- Business Analyst

### Como utilizar os papéis definidos no framework?
Os papéis são definidos em arquivos markdown detalhados na pasta `framework/roles/`. Eles podem ser usados para:
1. Atribuir responsabilidades específicas em equipes
2. Guiar modelos de linguagem na geração de código especializado
3. Definir padrões e melhores práticas para cada área

## Solução de Problemas

### O que fazer se o validador encontrar erros?
1. Revise os erros reportados
2. Consulte a documentação relevante no framework
3. Aplique as correções necessárias
4. Execute o validador novamente
5. Para correções automáticas, use o parâmetro `--auto-fix`

### Qual a diferença entre os scripts disponíveis?
- `env.sh` - Gerenciamento unificado do ambiente Python (setup/activate/deactivate)
- `quick_start.sh` - Criação rápida de projetos (`./quick_start.sh my_project`)
- `setup.sh` - Assistente interativo completo para ambiente e projeto
- `create_odoo_project.sh` - Criação de projetos Odoo completos com ambiente

### Como usar o gerenciamento de ambiente?
```bash
# Configurar ambiente Python pela primeira vez
./env.sh setup

# Ativar ambiente para trabalhar
./env.sh activate

# Desativar quando terminar
./env.sh deactivate

# Ver ajuda
./env.sh help
```

### Como posso contribuir para o framework?
Consulte o arquivo [[../CONTRIBUTING|Guia de Contribuição]] para obter informações detalhadas sobre como contribuir, incluindo padrões de código, processo de pull request e diretrizes de testes.

### Onde encontrar ajuda adicional?
- Consulte a [[index|Documentação Principal]]
- Verifique os [[../examples/README|Exemplos]] fornecidos
- Entre em contato com a comunidade através do repositório GitHub