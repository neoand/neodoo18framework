# 🪟 Neodoo18Framework - Windows Setup Guide

Este guia explica como usar o Neodoo18Framework no Windows.

## 🚀 Instalação Rápida

### 1. Pré-requisitos
- **Python 3.8+** instalado e no PATH
- **Git** instalado
- **PostgreSQL** (opcional, mas recomendado)

### 2. Verificar Python
```cmd
python --version
# OU
python3 --version
# OU  
py --version
```

### 3. Clone e Execute
```cmd
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# Método 1: Arquivo Batch (Recomendado)
neodoo.bat

# Método 2: PowerShell
.\neodoo.ps1

# Método 3: Python Direto (se os anteriores não funcionarem)
python framework\cli\neodoo.py
```

## 🎯 Comandos Disponíveis

### Menu Interativo (Recomendado)
```cmd
neodoo.bat                # Menu visual completo
```

### Comandos Diretos
```cmd
neodoo.bat create         # Criar novo projeto
neodoo.bat list           # Listar projetos
neodoo.bat run            # Executar projeto
neodoo.bat delete         # Deletar projeto
neodoo.bat doctor         # Verificar ambiente
neodoo.bat update         # Atualizar projeto
```

### PowerShell (Alternativo)
```powershell
.\neodoo.ps1              # Menu visual completo
.\neodoo.ps1 create       # Criar novo projeto
.\neodoo.ps1 list         # Listar projetos
```

## 🔧 Solução de Problemas

### Python não encontrado
Se aparecer erro "Python not found":

1. **Instale Python 3.8+** do site oficial: https://python.org
2. **Marque "Add Python to PATH"** durante a instalação
3. **Reinicie o terminal** após a instalação
4. **Teste**: `python --version`

### Erro de Permissão no PowerShell
Se o PowerShell bloquear a execução de scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Método Alternativo (Se nada funcionar)
```cmd
# Execute diretamente com Python
python framework\cli\neodoo.py

# Ou especifique o caminho completo do Python
C:\Python39\python.exe framework\cli\neodoo.py
```

## 🎨 Interface Visual

O Neodoo oferece uma interface visual linda com:
- 🎨 **Cores e emojis** para melhor experiência
- 📊 **Indicadores de progresso** para operações longas
- 🛡️ **Confirmações seguras** para ações destrutivas
- 🎯 **Detecção automática de portas** (8069, 8070, 8071...)

## 💡 Dicas Windows

1. **Use Command Prompt ou PowerShell** como administrador se necessário
2. **Windows Terminal** oferece melhor experiência visual
3. **WSL (Windows Subsystem for Linux)** é uma alternativa excelente
4. **Git Bash** também funciona com os comandos Unix (`./neodoo`)

## 🆘 Suporte

Se ainda tiver problemas:
1. Verifique se Python está no PATH: `python --version`
2. Tente o método direto: `python framework\cli\neodoo.py`
3. Abra uma issue no GitHub: https://github.com/neoand/neodoo18framework/issues

---
**By NeoAnd for you with ❤️**