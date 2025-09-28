#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neodoo18Framework - One-command CLI (Odoo 18+)

Usage:
    - Interactive: ./neodoo create
    - Non-interactive: ./neodoo create --name my_project --template minimal --base-dir ~/odoo_projects

Subcommands: create | list | delete | doctor | update | help
"""

import argparse
import os
import sys
import shutil
import subprocess
from pathlib import Path
import socket
import time
from textwrap import dedent
import threading

# Import colorama for colored output
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# Constants
REPO_ROOT = Path(__file__).resolve().parents[2]  # neodoo18framework/
FRAMEWORK_DIR = REPO_ROOT
DEFAULT_BASE_DIR = Path.home() / "odoo_projects"
ODOO_REPO = "https://github.com/odoo/odoo.git"
OCA_WEB_REPO = "https://github.com/OCA/web.git"
ODOO_BRANCH = "18.0"

# Visual Interface Functions

def show_banner():
    """Mostra banner bonito do Neodoo Framework"""
    banner = """
[36m╔═══════════════════════════════════════════════════════════════════════════════╗
║                          🚀 NEODOO18 FRAMEWORK                               ║
║                    [1mOdoo 18+ Development Made Easy & Beautiful[0m[36m                ║
║                                                                               ║
║                        [35mBy NeoAnd for you with ❤️[36m                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝[0m
    """
    print(banner)

def print_colored(text, color='white', bold=False):
    """Print text with color using colorama if available"""
    if COLORAMA_AVAILABLE:
        colors = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'purple': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
            'gray': Fore.LIGHTBLACK_EX
        }
        
        style = Style.BRIGHT if bold else Style.NORMAL
        color_code = colors.get(color, Fore.WHITE)
        
        print(f"{style}{color_code}{text}{Style.RESET_ALL}")
    else:
        # Fallback to plain text if colorama is not available
        print(text)


def print_success(text):
    """Print success message in green"""
    print_colored(text, 'green', bold=True)


def print_error(text):
    """Print error message in red"""
    print_colored(text, 'red', bold=True)


def print_warning(text):
    """Print warning message in yellow"""
    print_colored(text, 'yellow', bold=True)


def print_info(text):
    """Print info message in blue"""
    print_colored(text, 'blue')


def show_progress(message, seconds):
    """Show progress message with dots animation"""
    print_colored(f"🔄 {message}", 'cyan', bold=True)
    for i in range(seconds):
        time.sleep(1)
        print(".", end="", flush=True)
    print(" ✓")
    time.sleep(0.5)

def print_success(text):
    print_colored(f"✅ {text}", 'green', bold=True)

def print_info(text):
    print_colored(f"ℹ️  {text}", 'cyan')

def print_warning(text):
    print_colored(f"⚠️  {text}", 'yellow')

def print_error(text):
    print_colored(f"❌ {text}", 'red', bold=True)

def print_step(text):
    print_colored(f"🔄 {text}", 'blue')

def show_progress(text, duration=2):
    """Mostra progresso animado"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for char in chars:
            if time.time() >= end_time:
                break
            print(f"\r\033[96m{char} {text}\033[0m", end="", flush=True)
            time.sleep(0.1)
    
    print(f"\r\033[92m✅ {text} - Concluído!\033[0m")

def show_main_menu():
    """Mostra menu principal interativo"""
    while True:
        show_banner()
        print_colored("\n🎯 O que você deseja fazer hoje?", 'cyan', bold=True)
        print()
        
        menu_options = [
            ("🚀 Criar novo projeto Odoo", "Cria um projeto completo com Odoo 18+"),
            ("📋 Listar projetos existentes", "Mostra todos os projetos criados"),
            ("▶️  Executar projeto", "Inicia um projeto Odoo existente"),
            ("🗑️  Deletar projeto", "Remove um projeto existente"),
            ("🔧 Verificar ambiente", "Checa se tudo está funcionando"),
            ("🔄 Atualizar projeto", "Atualiza Odoo e dependências"),
            ("❓ Ajuda", "Mostra informações detalhadas"),
            ("🚪 Sair", "Encerra o programa")
        ]
        
        for i, (title, desc) in enumerate(menu_options, 1):
            print_colored(f"  {i}. {title}", 'white', bold=True)
            print_colored(f"     {desc}", 'gray')
            print()
        
        print_colored("\n" + "─" * 79, 'gray')
        choice = input("\n\033[1m\033[96m👉 Digite o número da opção desejada: \033[0m").strip()
        
        if choice == '1':
            return 'create'
        elif choice == '2':
            return 'list'
        elif choice == '3':
            return 'run'
        elif choice == '4':
            return 'delete'
        elif choice == '5':
            return 'doctor'
        elif choice == '6':
            return 'update'
        elif choice == '7':
            return 'help'
        elif choice == '8':
            print_colored("\n👋 Obrigado por usar o Neodoo Framework!", 'purple', bold=True)
            print_colored("   By NeoAnd for you with ❤️\n", 'purple')
            sys.exit(0)
        else:
            print_error("\nOpção inválida! Por favor, escolha um número de 1 a 8.")
            input("\nPressione Enter para continuar...")
            os.system('clear' if os.name != 'nt' else 'cls')

# Helpers

def _print(step):
    print_step(step)


def prompt(question, default=None, validator=None, color='cyan'):
    """Prompt melhorado com cores e validação"""
    suffix = f" [{default}]" if default is not None else ""
    while True:
        print_colored(f"🤔 {question}{suffix}: ", color, bold=True)
        ans = input("   ").strip()
        if ans == "" and default is not None:
            ans = default
        if validator and not validator(ans):
            print_error("   Valor inválido, tente novamente.")
            continue
        return ans

def prompt_port(question, default_port, check_conflicts=True):
    """Prompt específico para portas com verificação de conflitos"""
    while True:
        port = prompt(question, str(default_port), lambda x: x.isdigit() and 1024 <= int(x) <= 65535)
        port = int(port)
        
        if check_conflicts and not _port_free(port):
            print_warning(f"   Porta {port} já está em uso!")
            
            # Encontrar próxima porta disponível
            suggested_port = port + 1
            while not _port_free(suggested_port) and suggested_port < 65535:
                suggested_port += 1
            
            if suggested_port < 65535:
                use_suggested = input(f"   🎯 Usar porta {suggested_port}? (s/N): ").strip().lower()
                if use_suggested == 's':
                    return suggested_port
            
            print_info("   Tente uma porta diferente.")
            continue
        
        return port


def is_snake(s):
    return bool(s) and s[0].islower() and all(c.islower() or c.isdigit() or c == '_' for c in s)


def ensure_dir(p):
    p.mkdir(parents=True, exist_ok=True)


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# Scaffolding

def create_run_sh(project_dir, venv):
    run_sh = dedent(
        f"""
        #!/bin/bash
        PROJECT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
        cd "$PROJECT_DIR"
        set -e
        
        # Ler configuração
        PORT=$(grep xmlrpc_port odoo.conf | cut -d'=' -f2 | tr -d ' ' || echo "8069")
        DB_NAME=$(grep db_name odoo.conf | cut -d'=' -f2 | tr -d ' ' || echo "odoo")
        
        echo "🚀 Iniciando Odoo..."
        echo "📁 Projeto: $(basename "$PWD")"
        echo "🗄️  Database: $DB_NAME"
        echo "🌐 URL: http://localhost:$PORT"
        echo "📝 Logs: $PWD/logs/odoo.log"
        echo ""
        echo "✅ Odoo está iniciando..."
        echo "📋 Para parar: Ctrl+C"
        echo "" 
        echo "$(date): Odoo starting..." >> logs/startup.log
        
        {'source .venv/bin/activate' if venv else ''}
        python odoo_source/odoo-bin -c odoo.conf
        """
    ).strip() + "\n"
    write_file(project_dir / "run.sh", run_sh)
    os.chmod(project_dir / "run.sh", 0o755)


def create_odoo_conf(project_dir, db_name, addons, odoo_port=8069, websocket_port=8072):
    addons_path = ",".join(addons)
    conf = dedent(
        f"""
        [options]
        db_host = localhost
        db_port = 5432
        db_user = odoo
        db_password = odoo
        db_name = {db_name}
        xmlrpc_port = {odoo_port}
        longpolling_port = {websocket_port}
        addons_path = {addons_path}
        logfile = logs/odoo.log
        log_level = info
        dev_mode = reload,qweb,werkzeug,xml
        data_dir = filestore
        """
    ).strip() + "\n"
    write_file(project_dir / "odoo.conf", conf)


def write_neodoo_yaml(project_dir, cfg):
    lines = ["# Neodoo project configuration", "version: 1"]
    for k, v in cfg.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {v}")
    write_file(project_dir / ".neodoo.yml", "\n".join(lines) + "\n")


def read_neodoo_yaml(path):
    """Very small YAML reader for simple key: value and key:\n  - list items
    Converts common scalars (true/false/yes/no/1/0) to bool and digits to int.
    """
    def _parse_scalar(s):
        s = s.strip()
        low = s.lower()
        if low in ("true", "yes", "y", "1"):  # bool true
            return True
        if low in ("false", "no", "n", "0"):  # bool false
            return False
        if low.isdigit():
            try:
                return int(low)
            except Exception:
                return s
        return s

    data = {}
    if not path.exists():
        return data
    current_list_key = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith(":") and not line.startswith("- "):
            key = line[:-1].strip()
            data[key] = []
            current_list_key = key
            continue
        if line.startswith("- ") and current_list_key:
            lst = data.get(current_list_key)
            if isinstance(lst, list):
                lst.append(_parse_scalar(line[2:]))
            continue
        current_list_key = None
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = _parse_scalar(v)
    return data


def call_generator(module_name, template, output_dir, author, description):
    gen = FRAMEWORK_DIR / "framework/generator/create_project.py"
    cmd = [sys.executable, str(gen), "--name", module_name, "--type", template, "--output", str(output_dir)]
    if author:
        cmd += ["--author", author]
    if description:
        cmd += ["--description", description]
    run(cmd)


def clone_repo(url, branch, dest):
    run(["git", "clone", "--depth", "1", "--branch", branch, url, str(dest)])


def create_virtualenv(project_dir):
    venv_dir = project_dir / ".venv"
    show_progress("Criando ambiente virtual Python", 2)
    run([sys.executable, "-m", "venv", str(venv_dir)])
    pip = venv_dir / "bin" / "pip"
    try:
        show_progress("Atualizando pip", 1)
        run([str(pip), "install", "--upgrade", "pip"])
        req = project_dir / "odoo_source" / "requirements.txt"
        if req.exists():
            show_progress("Instalando dependências do Odoo (pode demorar vários minutos)", 5)
            run([str(pip), "install", "-r", str(req)])
    except subprocess.CalledProcessError:
        print_warning("Falha ao instalar dependências. Você pode tentar manualmente depois.")


def _check_cmd_exists(cmd):
    return shutil.which(cmd) is not None


def _port_free(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) != 0


def _load_from_config(config_path):
    cfg = read_neodoo_yaml(config_path)
    return {
        "name": cfg.get("name"),
        "base_dir": cfg.get("base_dir"),
        "module": cfg.get("module"),
        "template": cfg.get("template"),
        "venv": cfg.get("venv", True),
        "odoo_branch": cfg.get("odoo_branch", ODOO_BRANCH),
    }


# Commands

def cmd_create(args):
    interactive = not any([args.name])
    if interactive:
        os.system('clear' if os.name != 'nt' else 'cls')
        show_banner()
        print_colored("\n🎯 Vamos criar seu projeto Odoo 18+ incrível!", 'green', bold=True)
        print_colored("   Responda algumas perguntas e tudo será configurado automaticamente.\n", 'gray')
        
        # Nome do projeto
        name = prompt("Como você quer chamar seu projeto? (use snake_case)", validator=is_snake, color='cyan')
        
        # Diretório base
        base_dir = Path(prompt("Onde salvar o projeto?", str(DEFAULT_BASE_DIR), color='cyan'))
        
        # Template com explicação visual
        print_colored("\n📦 Escolha o tipo de projeto:", 'purple', bold=True)
        templates = [
            ("minimal", "📋 Projeto Simples", "Estrutura básica para módulos personalizados"),
            ("advanced", "🏢 Projeto Empresarial", "Inclui relatórios, wizards e recursos avançados"),  
            ("ecommerce", "🛒 E-commerce", "Sistema completo para loja online")
        ]
        
        for i, (key, title, desc) in enumerate(templates, 1):
            print_colored(f"  {i}. {title}", 'white', bold=True)
            print_colored(f"     {desc}", 'gray')
        
        while True:
            choice = input(f"\n🎯 Escolha o template (1-{len(templates)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(templates):
                template = templates[int(choice)-1][0]
                break
            print_error("Escolha inválida! Digite um número de 1 a 3.")
        
        # Configuração de rede
        print_colored(f"\n🌐 Configuração de Rede:", 'blue', bold=True)
        odoo_port = prompt_port("Porta para acessar o Odoo", 8069)
        websocket_port = prompt_port("Porta para WebSocket/Chat", 8072)
        
        # Informações do desenvolvedor
        print_colored(f"\n👤 Informações do Desenvolvedor:", 'yellow', bold=True)
        author = prompt("Seu nome ou empresa", "Your Company", color='yellow')
        
        # Nome técnico do módulo
        module_name = prompt("Nome técnico do módulo inicial", name, color='cyan')
        description = prompt("Descrição do projeto", f"Projeto {name} criado com Neodoo Framework", color='cyan')
        
        # Virtual environment
        print_colored(f"\n🐍 Ambiente Python:", 'green', bold=True)
        use_venv = prompt("Criar ambiente virtual Python? (Recomendado)", "s", color='green').lower() in ("s", "sim", "y", "yes")
    else:
        if args.from_config:
            cfg = _load_from_config(Path(args.from_config))
            name = str(cfg.get("name") or args.name)
            base_dir = Path(str(cfg.get("base_dir") or args.base_dir or DEFAULT_BASE_DIR))
            module_name = str(cfg.get("module") or args.module or name)
            template = str(cfg.get("template") or args.template or "minimal")
            author = args.author
            description = args.description or f"Modulo {module_name} gerado pelo Neodoo"
            vcfg = cfg.get("venv", True)
            if isinstance(vcfg, bool):
                vcfg_bool = vcfg
            else:
                vcfg_bool = str(vcfg).strip().lower() in ("1", "true", "yes", "y")
            use_venv = vcfg_bool and (not args.no_venv)
            odoo_port = 8069  # Default para config
            websocket_port = 8072
        else:
            name = args.name
            base_dir = Path(args.base_dir or DEFAULT_BASE_DIR)
            module_name = args.module or name
            template = args.template or "minimal"
            author = args.author
            description = args.description or f"Modulo {module_name} gerado pelo Neodoo"
            use_venv = not args.no_venv
            odoo_port = 8069  # Default para modo não-interativo
            websocket_port = 8072

    project_dir = base_dir / name
    if project_dir.exists():
        print(f"Diretorio ja existe: {project_dir}")
        sys.exit(1)

    print_colored(f"\n\n🚀 Iniciando criação do projeto...", 'green', bold=True)
    print_info(f"📁 Local: {project_dir}")
    
    ensure_dir(project_dir)
    
    show_progress("Criando estrutura de diretórios", 1)
    for d in ("custom_addons", "community_addons", "logs", "filestore"):
        ensure_dir(project_dir / d)

    show_progress("Baixando Odoo 18+ (pode demorar alguns minutos)", 3)
    clone_repo(ODOO_REPO, ODOO_BRANCH, project_dir / "odoo_source")

    show_progress("Baixando módulos OCA (web_responsive incluído)", 2)
    clone_repo(OCA_WEB_REPO, ODOO_BRANCH, project_dir / "community_addons" / "web")

    if use_venv:
        create_virtualenv(project_dir)

    show_progress(f"Gerando módulo inicial: {module_name} ({template})", 2)
    call_generator(module_name, template, project_dir / "custom_addons", author, description)

    create_odoo_conf(project_dir, db_name=name, addons=[
        "odoo_source/addons", 
        "custom_addons",
        "community_addons/web",
    ], odoo_port=odoo_port if interactive else 8069, websocket_port=websocket_port if interactive else 8072)
    create_run_sh(project_dir, venv=use_venv)

    write_neodoo_yaml(project_dir, {
        "name": name,
        "base_dir": str(base_dir),
        "module": module_name,
        "template": template,
        "venv": bool(use_venv),
        "odoo_branch": ODOO_BRANCH,
        "oca_web": True,
    })

    print_success("\n🎉 Projeto criado com sucesso!")
    print_colored("\n📋 Para iniciar seu projeto:", 'cyan', bold=True)
    print_colored(f"   cd {project_dir}", 'white')
    print_colored(f"   ./run.sh", 'white')
    print_colored(f"\n🌐 Seu Odoo estará disponível em:", 'blue', bold=True)
    print_colored(f"   http://localhost:{odoo_port if interactive else 8069}", 'white')
    print_colored("\n" + "By NeoAnd for you with ❤️", 'purple')
    
    input("\nPressione Enter para voltar ao menu principal...")


def cmd_list(_args):
    os.system('clear' if os.name != 'nt' else 'cls')
    show_banner()
    
    base = Path(_args.base_dir or DEFAULT_BASE_DIR)
    print_colored(f"\n📋 Projetos em: {base}\n", 'cyan', bold=True)
    
    if not base.exists():
        print_warning(f"Diretório não encontrado: {base}")
        input("\nPressione Enter para continuar...")
        return
        
    items = [p for p in base.iterdir() if p.is_dir()]
    if not items:
        print_info("📋 Nenhum projeto encontrado")
        print_colored("\n🚀 Crie seu primeiro projeto com a opção 'Criar novo projeto'!", 'yellow')
    else:
        for i, p in enumerate(sorted(items), start=1):
            # Verificar se tem odoo.conf para mostrar porta
            odoo_conf = p / "odoo.conf"
            port_info = ""
            if odoo_conf.exists():
                try:
                    conf_content = odoo_conf.read_text()
                    for line in conf_content.split('\n'):
                        if 'xmlrpc_port' in line and '=' in line:
                            port = line.split('=')[1].strip()
                            port_info = f" 🌐 :{port}"
                            break
                except:
                    pass
                    
            print_colored(f"  {i}. 📁 {p.name}{port_info}", 'white', bold=True)
            print_colored(f"     📂 {p}", 'gray')
            
    print_colored("\n" + "By NeoAnd for you with ❤️", 'purple')
    input("\nPressione Enter para continuar...")


def cmd_delete(args):
    os.system('clear' if os.name != 'nt' else 'cls')
    show_banner()
    
    base = Path(args.base_dir or DEFAULT_BASE_DIR)
    
    # Listar projetos disponíveis
    items = [p for p in base.iterdir() if p.is_dir() and p.exists()]
    if not items:
        print_warning("📋 Nenhum projeto encontrado para deletar")
        input("\nPressione Enter para continuar...")
        return
    
    if not args.name:
        print_colored("\n🗚️ Projetos disponíveis para deletar:\n", 'red', bold=True)
        for i, p in enumerate(sorted(items), start=1):
            print_colored(f"  {i}. {p.name}", 'white')
        
        while True:
            choice = input(f"\n👉 Escolha o projeto para deletar (1-{len(items)}) ou 'cancelar': ").strip()
            if choice.lower() == 'cancelar':
                print_info("Operação cancelada")
                input("\nPressione Enter para continuar...")
                return
            if choice.isdigit() and 1 <= int(choice) <= len(items):
                name = sorted(items)[int(choice)-1].name
                break
            print_error("Escolha inválida!")
    else:
        name = args.name
    
    path = base / name
    if not path.exists():
        print_error(f"Projeto não encontrado: {path}")
        input("\nPressione Enter para continuar...")
        return
        
    print_colored(f"\n⚠️  ATENÇÃO: Você está prestes a deletar:", 'yellow', bold=True)
    print_colored(f"   📁 Projeto: {name}", 'white')
    print_colored(f"   📂 Local: {path}", 'gray')
    print_colored(f"\n🗑️ Esta ação não pode ser desfeita!", 'red', bold=True)
    
    conf = input("\n🔐 Digite 'DELETE' (maiúsculas) para confirmar: ").strip()
    if conf != "DELETE":
        print_info("Operação cancelada por segurança")
    else:
        show_progress(f"Removendo projeto {name}", 2)
        shutil.rmtree(path)
        print_success(f"Projeto '{name}' removido com sucesso!")
        print_colored("\nBy NeoAnd for you with ❤️", 'purple')
    
    input("\nPressione Enter para continuar...")


def cmd_doctor(args):
    os.system('clear' if os.name != 'nt' else 'cls')
    show_banner()
    
    print_colored("\n🔧 Verificando ambiente de desenvolvimento...\n", 'blue', bold=True)
    
    ok = True
    
    # Verificar ferramentas essenciais
    print_colored("🔍 Ferramentas essenciais:", 'cyan', bold=True)
    for label, cmdname in [("python3", Path(sys.executable).name), ("git", "git"), ("psql", "psql"), ("docker", "docker")]:
        exists = _check_cmd_exists(cmdname)
        if exists:
            print_success(f"   {label}: Encontrado")
        else:
            print_error(f"   {label}: Não encontrado")
            if label in ("python3", "git"):
                ok = False
    
    # Verificar portas
    print_colored("\n🌐 Portas de rede:", 'cyan', bold=True)
    for port in (8069, 8072):
        free = _port_free(port)
        if free:
            print_success(f"   Porta {port}: Livre")
        else:
            print_warning(f"   Porta {port}: Em uso")
    
    # Verificar projeto específico se informado
    if getattr(args, "path", None):
        p = Path(args.path)
        print_colored(f"\n📁 Verificando projeto: {p.name}", 'cyan', bold=True)
        
        if not p.exists():
            print_error("   Diretório não existe")
            ok = False
        else:
            components = [
                ("odoo_source", "Código fonte do Odoo"),
                ("custom_addons", "Módulos customizados"),
                ("community_addons", "Módulos da comunidade"),
                ("odoo.conf", "Arquivo de configuração"),
                ("run.sh", "Script de execução")
            ]
            
            for component, desc in components:
                present = (p / component).exists()
                if present:
                    print_success(f"   {desc}: OK")
                else:
                    print_error(f"   {desc}: Não encontrado")
                    ok = False
            
            # Verificar ambiente virtual
            venv_ok = (p / ".venv" / "bin" / "python").exists()
            if venv_ok:
                print_success("   Ambiente virtual Python: OK")
            else:
                print_warning("   Ambiente virtual Python: Não encontrado")
    
    print_colored("\n" + "─" * 50, 'gray')
    
    if ok:
        print_success("\n✅ Ambiente saudável! Tudo pronto para desenvolvimento.")
    else:
        print_error("\n❌ Problemas detectados no ambiente.")
        print_info("💡 Execute 'neodoo create' para criar um projeto completo.")
    
    print_colored("\nBy NeoAnd for you with ❤️", 'purple')
    input("\nPressione Enter para continuar...")


def _git_pull(path):
    if not (path / ".git").exists():
        print_warning(f"   {path.name}: Não é um repositório Git")
        return
    try:
        run(["git", "pull", "--rebase"], cwd=path)
        print_success(f"   {path.name}: Atualizado")
    except subprocess.CalledProcessError:
        print_error(f"   {path.name}: Falha no git pull")


def cmd_update(args):
    os.system('clear' if os.name != 'nt' else 'cls')
    show_banner()
    
    p = Path(args.path)
    if not p.exists():
        print_error(f"Diretório não encontrado: {p}")
        input("\nPressione Enter para continuar...")
        return
    
    print_colored(f"\n🔄 Atualizando projeto: {p.name}\n", 'blue', bold=True)
    
    # Atualizar repositórios
    show_progress("Atualizando código fonte do Odoo", 2)
    _git_pull(p / "odoo_source")
    
    show_progress("Atualizando módulos OCA", 2)
    _git_pull(p / "community_addons" / "web")
    
    # Atualizar dependências Python
    if not args.no_deps:
        pip_bin = p / ".venv" / "bin" / "pip"
        req = p / "odoo_source" / "requirements.txt"
        
        if pip_bin.exists() and req.exists():
            try:
                show_progress("Atualizando pip", 1)
                run([str(pip_bin), "install", "--upgrade", "pip"])
                
                show_progress("Atualizando dependências Python (pode demorar)", 4)
                run([str(pip_bin), "install", "-r", str(req)])
                
                print_success("Dependências atualizadas com sucesso!")
            except subprocess.CalledProcessError:
                print_warning("Falha ao atualizar dependências Python.")
        else:
            print_warning("Ambiente virtual ou requirements.txt não encontrado.")
            print_info("💡 Pulando atualização de dependências Python.")
    
    print_success("\n✅ Projeto atualizado com sucesso!")
    print_colored("\nBy NeoAnd for you with ❤️", 'purple')
    input("\nPressione Enter para continuar...")


def cmd_run(args):
    """Execute um projeto Odoo com feedback detalhado"""
    
    if not args.path:
        # Se não especificou path, listar projetos disponíveis
        base = Path(DEFAULT_BASE_DIR)
        if base.exists():
            items = [p for p in base.iterdir() if p.is_dir() and (p / "run.sh").exists()]
            if items:
                os.system('clear' if os.name != 'nt' else 'cls')
                show_banner()
                print_colored("\n▶️  Escolha o projeto para executar:\n", 'green', bold=True)
                
                for i, p in enumerate(sorted(items), start=1):
                    # Mostrar porta do projeto
                    port_info = ""
                    odoo_conf = p / "odoo.conf"
                    if odoo_conf.exists():
                        try:
                            conf_content = odoo_conf.read_text()
                            for line in conf_content.split('\n'):
                                if 'xmlrpc_port' in line and '=' in line:
                                    port = line.split('=')[1].strip()
                                    port_info = f" 🌐 :{port}"
                                    break
                        except:
                            pass
                    print_colored(f"  {i}. {p.name}{port_info}", 'white', bold=True)
                
                while True:
                    choice = input(f"\n👉 Escolha o projeto (1-{len(items)}) ou 'cancelar': ").strip()
                    if choice.lower() == 'cancelar':
                        return
                    if choice.isdigit() and 1 <= int(choice) <= len(items):
                        project_path = sorted(items)[int(choice)-1]
                        break
                    print_error("Escolha inválida!")
            else:
                print_warning("Nenhum projeto Odoo encontrado")
                input("\nPressione Enter para continuar...")
                return
        else:
            project_path = Path.cwd()
    else:
        project_path = Path(args.path)
    
    if not project_path.exists():
        print_error(f"Diretório não encontrado: {project_path}")
        sys.exit(1)
    
    # Verificar se é um projeto Odoo válido
    run_sh = project_path / "run.sh"
    odoo_conf = project_path / "odoo.conf"
    odoo_bin = project_path / "odoo_source" / "odoo-bin"
    
    if not run_sh.exists():
        print_error(f"Arquivo run.sh não encontrado em: {project_path}")
        print_info("💡 Execute 'neodoo create' para criar um projeto Odoo")
        input("\nPressione Enter para continuar...")
        return
    
    if not odoo_bin.exists():
        print_error(f"Odoo não encontrado em: {project_path / 'odoo_source'}")
        print_info("💡 Execute 'neodoo create' para criar um projeto completo")
        input("\nPressione Enter para continuar...")
        return
    
    # Ler configuração para mostrar detalhes
    port = "8069"  # default
    db_name = "odoo"
    websocket_port = "8072"
    
    if odoo_conf.exists():
        try:
            conf_content = odoo_conf.read_text()
            for line in conf_content.split('\n'):
                if 'xmlrpc_port' in line and '=' in line:
                    port = line.split('=')[1].strip()
                elif 'db_name' in line and '=' in line:
                    db_name = line.split('=')[1].strip()
                elif 'longpolling_port' in line and '=' in line:
                    websocket_port = line.split('=')[1].strip()
        except Exception:
            pass
    
    os.system('clear' if os.name != 'nt' else 'cls')
    show_banner()
    
    print_colored(f"\n🚀 Iniciando projeto Odoo...", 'green', bold=True)
    print_colored(f"📁 Projeto: {project_path.name}", 'cyan')
    print_colored(f"🗄️  Database: {db_name}", 'cyan')
    print_colored(f"🌐 URL: http://localhost:{port}", 'blue', bold=True)
    print_colored(f"📱 WebSocket: :{websocket_port}", 'blue')
    print_colored(f"📝 Logs: {project_path}/logs/odoo.log", 'gray')
    print_colored(f"\n⏳ Carregando Odoo (isso pode demorar alguns segundos...)", 'yellow')
    print_colored(f"\n🛹️  Para parar o servidor: Ctrl+C", 'purple')
    print_colored(f"\nBy NeoAnd for you with ❤️\n", 'purple')
    print_colored("\n" + "═"*79, 'gray')
    
    # Executar o run.sh
    try:
        os.chdir(project_path)
        os.execv("/bin/bash", ["bash", str(run_sh)])
    except Exception as e:
        print_error(f"Erro ao executar projeto: {e}")
        input("\nPressione Enter para continuar...")


def build_parser():
    p = argparse.ArgumentParser(prog="neodoo", description="Neodoo18Framework - CLI")
    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("create", help="Criar novo projeto (wizard por padrao)")
    c.add_argument("--name", help="Nome do projeto (snake_case)")
    c.add_argument("--base-dir", help=f"Diretorio base (default: {DEFAULT_BASE_DIR})")
    c.add_argument("--module", help="Nome tecnico do modulo inicial (default: == name)")
    c.add_argument("--template", choices=["minimal", "advanced", "ecommerce"], help="Template do modulo")
    c.add_argument("--author", help="Autor")
    c.add_argument("--description", help="Descricao do modulo")
    c.add_argument("--no-venv", action="store_true", help="Nao criar virtualenv")
    c.add_argument("--from-config", help="Caminho para .neodoo.yml para execucao nao interativa")
    c.set_defaults(func=cmd_create)

    l = sub.add_parser("list", help="Listar projetos")
    l.add_argument("--base-dir", help=f"Diretorio base (default: {DEFAULT_BASE_DIR})")
    l.set_defaults(func=cmd_list)

    d = sub.add_parser("delete", help="Excluir projeto")
    d.add_argument("--name", help="Nome do projeto")
    d.add_argument("--base-dir", help=f"Diretorio base (default: {DEFAULT_BASE_DIR})")
    d.set_defaults(func=cmd_delete)

    dr = sub.add_parser("doctor", help="Checar ambiente e/ou projeto")
    dr.add_argument("--path", help="Diretorio do projeto para checagens especificas")
    dr.set_defaults(func=cmd_doctor)

    up = sub.add_parser("update", help="Atualizar Odoo/OCA e deps da venv")
    up.add_argument("--path", required=True, help="Diretorio do projeto")
    up.add_argument("--no-deps", action="store_true", help="Nao atualizar dependencias da venv")
    up.set_defaults(func=cmd_update)
    
    r = sub.add_parser("run", help="Executar projeto Odoo")
    r.add_argument("--path", help="Diretorio do projeto (default: diretorio atual)")
    r.set_defaults(func=cmd_run)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    
    # Se não há comando especificado, mostra menu principal
    if not getattr(args, "cmd", None):
        os.system('clear' if os.name != 'nt' else 'cls')
        while True:
            try:
                chosen_cmd = show_main_menu()
                # Simular argumentos para o comando escolhido
                if chosen_cmd == 'help':
                    parser.print_help()
                    input("\nPressione Enter para continuar...")
                    os.system('clear' if os.name != 'nt' else 'cls')
                    continue
                elif chosen_cmd == 'create':
                    fake_args = parser.parse_args(['create'])
                elif chosen_cmd == 'list':
                    fake_args = parser.parse_args(['list'])
                elif chosen_cmd == 'run':
                    fake_args = parser.parse_args(['run'])
                elif chosen_cmd == 'delete':
                    fake_args = parser.parse_args(['delete'])
                elif chosen_cmd == 'doctor':
                    fake_args = parser.parse_args(['doctor'])
                elif chosen_cmd == 'update':
                    # Para update precisamos pedir o path
                    project_path = prompt("Caminho do projeto para atualizar", str(DEFAULT_BASE_DIR))
                    fake_args = parser.parse_args(['update', '--path', project_path])
                else:
                    continue
                
                fake_args.func(fake_args)
                
                if chosen_cmd != 'run':  # run executa o Odoo, não volta ao menu
                    os.system('clear' if os.name != 'nt' else 'cls')
                    
            except KeyboardInterrupt:
                print_colored("\n\n👋 Até logo! By NeoAnd for you with ❤️\n", 'purple', bold=True)
                sys.exit(0)
            except Exception as e:
                print_error(f"Erro inesperado: {e}")
                input("Pressione Enter para continuar...")
                os.system('clear' if os.name != 'nt' else 'cls')
    else:
        # Modo comando direto (CLI tradicional)
        try:
            args.func(args)
        except subprocess.CalledProcessError as e:
            cmd_str = e.cmd if isinstance(e.cmd, list) else [str(e.cmd)]
            print_error(f"Erro em comando externo (exit {e.returncode}): {' '.join(cmd_str)}")
            sys.exit(e.returncode)


if __name__ == "__main__":
    main()
