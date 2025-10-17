# 📚 Guias em Português - Neodoo18Framework

Documentação completa em português para o Neodoo18Framework.

## 🎯 Guias Disponíveis

### 📖 [Guia Completo](./GUIA_COMPLETO.md)
Documentação completa do framework em português, incluindo:
- Instalação e configuração
- Criação de projetos
- Desenvolvimento de módulos
- Deploy e manutenção

### 🔍 [Como Usar o Validator Neo Sempre](./COMO_USAR_VALIDATOR_NEO_SEMPRE.md)
Guia detalhado sobre como usar o plugin de validação específico para o projeto Neo Sempre:
- ✅ O que o plugin valida
- 🚀 Comandos básicos e avançados
- 🛠️ Correções comuns
- 📊 Entendendo a saída do validator
- 🎯 Integração com VSCode e CI/CD

### ⚡ [Guia Rápido - Validator](./GUIA_RAPIDO_VALIDATOR.md)
Referência rápida para uso do validator:
- 3 formas de usar o validator
- Principais erros encontrados
- Checklist de correção
- Comandos úteis

## 🚀 Início Rápido

### Para Começar

```bash
# 1. Clone o repositório
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# 2. Validar seu módulo
./validate_neo_sempre.sh semprereal
```

### Para Validação Completa

```bash
# Validar todos os módulos do projeto
./validate_neo_sempre.sh

# Ver detalhes completos
./validate_neo_sempre.sh semprereal --verbose
```

## 🎓 Ordem de Leitura Recomendada

Para novos usuários, sugerimos a seguinte ordem:

1. **[Guia Rápido - Validator](./GUIA_RAPIDO_VALIDATOR.md)** - Para começar rapidamente
2. **[Como Usar o Validator](./COMO_USAR_VALIDATOR_NEO_SEMPRE.md)** - Para entender em detalhes
3. **[Guia Completo](./GUIA_COMPLETO.md)** - Para dominar o framework

## 📋 Casos de Uso

### Desenvolvedores
- Validar código antes de commit
- Garantir compliance com Odoo 18+
- Identificar problemas de qualidade

### Tech Leads
- Definir padrões de código
- Revisar código do time
- Automatizar quality gates

### DevOps
- Integrar validação no CI/CD
- Automatizar verificações
- Garantir qualidade em produção

## 🆘 Precisa de Ajuda?

- **Issues:** [GitHub Issues](https://github.com/neoand/neodoo18framework/issues)
- **Documentação:** [Documentação Principal](../../index.md)
- **FAQ:** [Perguntas Frequentes](../../faq.md)

## 🤝 Contribuindo

Quer melhorar a documentação em português? Veja:
- [Como Contribuir](../../../CONTRIBUTING.md)
- [Contribuir para Documentação](../../contributing-to-docs.md)

## 📝 Notas

- Toda documentação está em formato Markdown
- Links internos usam formato Obsidian `[[]]`
- Exemplos de código incluem comentários explicativos
- Comandos incluem explicações sobre o que fazem

---

**Última atualização:** Outubro 2025  
**Versão do Framework:** 1.0.0+  
**Compatibilidade:** Odoo 18.0+
