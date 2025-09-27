# Workflows e Processos do Neodoo18Framework

Este documento descreve os fluxos de trabalho e processos recomendados ao trabalhar com o Neodoo18Framework.

## Fluxo de Criação de Projeto

```mermaid
graph TD
    A[Início] --> B[Configurar Ambiente]
    B --> C[./env.sh setup]
    C --> D[./env.sh activate]
    D --> E[Escolha o Método]
    E --> F[Rápido: ./quick_start.sh projeto]
    E --> G[Completo: ./setup.sh]
    F --> H[Projeto Criado]
    G --> I[Escolher Tipo de Projeto]
    I --> J[Minimal/Advanced/E-commerce]
    J --> H
    H --> K[Desenvolvimento]
    K --> L[Validar Código]
    L --> M{Validação OK?}
    M -->|Sim| N[Implantar]
    M -->|Não| O[Corrigir Erros]
    O --> L
```

## Fluxo de Validação

```mermaid
graph TD
    A[Código Modificado] --> B[Executar Validador]
    B --> C{Erros Encontrados?}
    C -->|Sim| D[Revisar Erros]
    C -->|Não| E[Código Pronto]
    D --> F[Aplicar Correções]
    F --> B
```

## Papéis e Responsabilidades

```mermaid
graph TD
    A[Projeto Odoo 18+] --> B[OWL Specialist]
    A --> C[Backend Developer]
    A --> D[UX/UI Designer]
    A --> E[DevOps Engineer]
    A --> F[Security Expert]
    A --> G[Integration Specialist]
    A --> H[Data Migration Specialist]
    A --> I[Business Analyst]
    
    B --> J[Frontend]
    C --> K[Backend]
    D --> L[Interface]
    E --> M[Infraestrutura]
    F --> N[Segurança]
    G --> O[Integrações]
    H --> P[Migração]
    I --> Q[Requisitos]
```

## Ciclo de Desenvolvimento

```mermaid
graph TD
    A[Análise de Requisitos] --> B[Design]
    B --> C[Implementação]
    C --> D[Teste]
    D --> E{Validação}
    E -->|Falha| C
    E -->|Sucesso| F[Implantação]
    F --> G[Manutenção]
    G --> A
```

## Processo de Contribuição

```mermaid
graph TD
    A[Fork do Repositório] --> B[Criar Branch]
    B --> C[Implementar Mudanças]
    C --> D[Executar Validador]
    D --> E{Validação OK?}
    E -->|Não| C
    E -->|Sim| F[Enviar Pull Request]
    F --> G[Revisão de Código]
    G --> H{Aprovado?}
    H -->|Não| C
    H -->|Sim| I[Merge]
```

---

## Automação: OCA Watch & Weekly Rollup

### OCA Watch (Diário)
- Monitora repositórios OCA configurados em `.neodoo/oca_watch.yml`.
- Gera/atualiza digests em `docs/oca-digests/` e abre PR automaticamente com labels/assignee e auto‑merge.
- Agendado para rodar diariamente (02:00 UTC) e disponível via `workflow_dispatch`.

Como executar manualmente:
1. Acesse a aba Actions do GitHub
2. Selecione “OCA Watch”
3. Opcional: marque `bootstrap=true` na primeira execução
4. Dispare e acompanhe o PR criado

### Weekly Rollup (Semanal)
- Consolida os últimos 7 dias de digests em `docs/oca-digests/rollups/YYYY-Www.md`.
- Abre PR com labels (`oca-digests`, `automation`, `weekly-rollup`), assignee `@neoand` e auto‑merge habilitado.
- Agendamento: segundas às 03:00 UTC. Também disponível via `workflow_dispatch`.

Execução manual:
1. Acesse a aba Actions do GitHub
2. Selecione “OCA Weekly Rollup”
3. Execute e verifique o PR gerado