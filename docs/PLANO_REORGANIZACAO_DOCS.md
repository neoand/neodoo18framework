# 📋 Plano de Reorganização da Documentação - Neo Sempre

## 🎯 Objetivo

Reorganizar a documentação do projeto Neo Sempre para:
1. **Facilitar o trabalho de LLMs** (contexto claro e acessível)
2. **Preservar o histórico** de decisões e evolução
3. **Guiar o desenvolvimento** com padrões e práticas
4. **Manter rastreabilidade** de requisitos e implementações

## 📊 Análise da Situação Atual

### 📁 **docs_procedure/** (7 arquivos)
**Natureza:** Documentos **orientadores** e formais

| Arquivo | Conteúdo | Uso |
|---------|----------|-----|
| `prd.md` | Product Requirements Document | Define O QUE construir |
| `arquitetura.md` | Decisões arquiteturais | Define COMO construir |
| `contexto_negocio.md` | Domínio de negócio | Explica POR QUE |
| `glossario.md` | Termos do domínio | Vocabulário comum |
| `padroes_codigo.md` | Convenções de código | Padrões de desenvolvimento |
| `roadmap.md` | Cronograma e fases | Planejamento temporal |
| `testes.md` | Estratégia de testes | Qualidade e validação |

**💡 Valor:** Documentos bem estruturados, prontos para referência

---

### 📁 **levantamento_inicial/** (19 arquivos)
**Natureza:** Documentos de **descoberta** e evolução

| Tipo | Arquivos | Conteúdo |
|------|----------|----------|
| **Fonte da Verdade** | `00_fonte_da_verdade.md` | Documento mestre consolidado |
| **Iterações Técnicas** | `01-13_*.md` | Análises progressivas, decisões, correções |
| **Documentação Técnica** | `Documento Técnico...`, `Especificação...` | Detalhes de implementação |
| **Regras de Negócio** | `inss_*.md` | Regras específicas INSS |
| **Exemplos/APIs** | `exemplo_api_*.md` | Referências de integração |
| **Backlog** | `backlog_tecnico_inicial.csv` | Lista de tarefas/pendências |

**💡 Valor:** Mostra o PROCESSO de pensamento, decisões tomadas, problemas resolvidos

---

## 🏗️ Estrutura Proposta

### 🎨 Nova Organização

```
neo_sempre/docs/
│
├── 📂 project/                           # Documentação formal do projeto
│   ├── business/
│   │   ├── contexto_negocio.md          ← de docs_procedure
│   │   ├── glossario.md                 ← de docs_procedure
│   │   └── regras_consignado.md         ← consolidado de levantamento_inicial
│   │
│   ├── architecture/
│   │   ├── overview.md                  ← arquitetura.md + insights
│   │   ├── data_model.md                ← extraído de análises técnicas
│   │   ├── integrations.md              ← APIs e integrações
│   │   └── decisions/                   ← ADRs (Architecture Decision Records)
│   │       ├── adr-001-estrutura-beneficiarios.md
│   │       ├── adr-002-workflow-crm-sales.md
│   │       ├── adr-003-calculo-margem.md
│   │       └── adr-004-comissionamento.md
│   │
│   ├── development/
│   │   ├── prd.md                       ← de docs_procedure
│   │   ├── padroes_codigo.md            ← de docs_procedure
│   │   ├── testes.md                    ← de docs_procedure
│   │   └── roadmap.md                   ← de docs_procedure
│   │
│   └── operations/
│       ├── deployment.md
│       ├── monitoring.md
│       └── maintenance.md
│
├── 📂 guides/                            # Guias práticos para desenvolvimento
│   ├── domain-knowledge/
│   │   ├── consignado-101.md            ← simplificado para LLMs
│   │   ├── inss-rules.md                ← consolidado de inss_*.md
│   │   ├── margin-calculation.md        ← regras de cálculo
│   │   └── commission-rules.md          ← regras de comissão
│   │
│   ├── implementation-patterns/
│   │   ├── odoo-inheritance.md          ← padrões descobertos
│   │   ├── import-wizard.md             ← como fazer importações
│   │   ├── crm-workflow.md              ← fluxo CRM→Sales
│   │   └── queue-jobs.md                ← processamento assíncrono
│   │
│   └── api-integrations/
│       ├── in100-api.md                 ← exemplo_api_in100.md
│       ├── banco-digitacao.md           ← exemplo_api_digitacao_banco
│       └── conciliacao-bancaria.md      ← extraído de docs técnicos
│
├── 📂 history/                           # Preservar histórico de descoberta
│   ├── discovery/
│   │   ├── 00_fonte_da_verdade.md       ← preservado original
│   │   ├── README.md                    ← índice explicativo
│   │   └── backlog_inicial.csv          ← backlog original
│   │
│   └── iterations/
│       ├── fase-01-analise-tecnica.md   ← 01_analise_tecnica_consolidada.md
│       ├── fase-02-gaps-framework.md    ← 02_analise_gaps_neodoo_framework.md
│       ├── fase-03-modulos-br.md        ← 03-04 consolidados
│       ├── fase-04-cep-solucao.md       ← 05-11 consolidados
│       └── fase-05-beneficiarios.md     ← 12-13 consolidados
│
├── 📂 knowledge-base/                    # Documentos otimizados para LLMs
│   ├── README.md                        ← como usar esta base
│   ├── project-context.md               ← contexto completo em 1 doc
│   ├── quick-reference.md               ← referência rápida
│   ├── business-rules.md                ← todas as regras consolidadas
│   ├── technical-patterns.md            ← padrões técnicos usados
│   └── faq.md                           ← perguntas frequentes
│
└── 📂 docs_procedure/                    # MOVER PARA history/original/
    └── [arquivos originais preservados]

levantamento_inicial/                     # MOVER PARA history/raw/
└── [arquivos originais preservados]
```

---

## 🔄 Processo de Reorganização

### **Fase 1: Preparação** (Não destrutiva)
1. ✅ Criar nova estrutura de diretórios
2. ✅ Preservar originais em `history/`
3. ✅ Criar índices e READMEs

### **Fase 2: Consolidação** (Extrair e reorganizar)
1. 📋 **ADRs (Architecture Decision Records)**
   - Extrair decisões de `12_analise_arquitetural_beneficiarios_contatos.md`
   - Documentar padrão: Contexto → Decisão → Consequências

2. 📚 **Guias de Domínio**
   - Consolidar `inss_*.md` em guia único
   - Simplificar para consumo de LLMs

3. 🔧 **Padrões de Implementação**
   - Extrair soluções de `05-11_*.md` (CEP, views, etc.)
   - Documentar como "receitas" replicáveis

4. 🌐 **Integrações**
   - Organizar exemplos de APIs
   - Criar templates de integração

### **Fase 3: Knowledge Base** (Para LLMs)
1. 📖 Criar `project-context.md` unificado
2. ⚡ Criar `quick-reference.md` com comandos/padrões
3. ❓ Criar `faq.md` com decisões e justificativas

### **Fase 4: Integração com Framework**
1. 🔗 Linkar documentação no `.github/copilot-instructions.md`
2. 📍 Criar "entry points" para LLMs
3. 🎯 Configurar VSCode para acesso rápido

---

## 💡 Benefícios da Nova Estrutura

### Para LLMs (Copilot, Claude, ChatGPT):
✅ **Contexto Rápido:** `knowledge-base/project-context.md` em um arquivo  
✅ **Referências Práticas:** Guias por tópico em `guides/`  
✅ **Decisões Claras:** ADRs explicam "por quê"  
✅ **Padrões Replicáveis:** Templates e exemplos prontos  

### Para Desenvolvedores:
✅ **Documentação Formal:** `project/` mantém estrutura profissional  
✅ **Rastreabilidade:** `history/` preserva evolução  
✅ **Guias Práticos:** `guides/` acelera implementação  
✅ **Onboarding Rápido:** Novos devs entendem projeto rapidamente  

### Para Gestão do Projeto:
✅ **PRD e Roadmap:** Claros e acessíveis  
✅ **Decisões Documentadas:** ADRs para revisão  
✅ **Histórico Auditável:** Tudo preservado  
✅ **Knowledge Retention:** Conhecimento não se perde  

---

## 🎯 Próximos Passos

### Decisão Necessária:
1. **Aprovar estrutura proposta?** (ajustes são bem-vindos)
2. **Priorizar fases?** (podemos fazer incremental)
3. **Conteúdo específico para LLMs?** (o que mais seria útil?)

### Execução:
- Posso executar a reorganização automaticamente
- Preservarei TODOS os originais
- Criarei índices e cross-references
- Gera documentos consolidados

---

## 📝 Exemplo de ADR

```markdown
# ADR-001: Estrutura de Dados - Beneficiários como Extensão de res.partner

**Status:** Implementado  
**Data:** 2025-10-02  
**Decisor:** Equipe Técnica

## Contexto
Precisávamos decidir entre:
1. Estender res.partner (contatos)
2. Criar modelo separado semprereal.beneficiario
3. Solução híbrida

## Decisão
Escolhemos **estender res.partner** adicionando campos específicos de beneficiários.

## Justificativa
- ✅ Integração nativa com todo Odoo
- ✅ Views unificadas
- ✅ Performance superior
- ✅ Manutenibilidade simplificada
- ❌ "Poluição" do modelo (aceitável)

## Consequências
- Todos os beneficiários são res.partner com is_beneficiario=True
- Campos específicos INSS aparecem apenas quando is_beneficiario
- Importações criam/atualizam res.partner diretamente
- Relatórios usam filtro domain=[('is_beneficiario', '=', True)]

## Referências
- `13_implementacao_finalizada_res_partner_beneficiarios.md`
- Código: `custom_addons/semprereal/models/res_partner.py`
```

---

**Aguardando sua aprovação para prosseguir! 🚀**
