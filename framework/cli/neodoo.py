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
from textwrap import dedent

# Constants
REPO_ROOT = Path(__file__).resolve().parents[2]  # neodoo18framework/
FRAMEWORK_DIR = REPO_ROOT
DEFAULT_BASE_DIR = Path.home() / "odoo_projects"
ODOO_REPO = "https://github.com/odoo/odoo.git"
OCA_WEB_REPO = "https://github.com/OCA/web.git"
ODOO_BRANCH = "18.0"

# Helpers

def _print(step):
    print(step, flush=True)


def prompt(question, default=None, validator=None):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        ans = input(f"{question}{suffix}: ").strip()
        if ans == "" and default is not None:
            ans = default
        if validator and not validator(ans):
            print("  -> Valor invalido, tente novamente.")
            continue
        return ans


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


def create_odoo_conf(project_dir, db_name, addons):
    addons_path = ",".join(addons)
    conf = dedent(
        f"""
        [options]
        db_host = localhost
        db_port = 5432
        db_user = odoo
        db_password = odoo
        db_name = {db_name}
        xmlrpc_port = 8069
        longpolling_port = 8072
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
    _print("Criando virtualenv...")
    run([sys.executable, "-m", "venv", str(venv_dir)])
    pip = venv_dir / "bin" / "pip"
    try:
        run([str(pip), "install", "--upgrade", "pip"])
        req = project_dir / "odoo_source" / "requirements.txt"
        if req.exists():
            _print("Instalando dependencias do Odoo (isso pode demorar)...")
            run([str(pip), "install", "-r", str(req)])
    except subprocess.CalledProcessError:
        _print("Falha ao instalar dependencias. Voce pode tentar manualmente depois.")


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
        _print("Wizard interativo - Criar projeto Odoo 18+")
        name = prompt("Nome do projeto (snake_case)", validator=is_snake)
        base_dir = Path(prompt("Diretorio base", str(DEFAULT_BASE_DIR)))
        module_name = prompt("Nome tecnico do modulo inicial", name)
        template = prompt("Template [minimal|advanced|ecommerce]", "minimal")
        author = prompt("Autor", "Your Company")
        description = prompt("Descricao", f"Modulo {module_name} gerado pelo Neodoo")
        use_venv = prompt("Usar virtualenv local? [y/N]", "y").lower() in ("y", "yes")
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
        else:
            name = args.name
            base_dir = Path(args.base_dir or DEFAULT_BASE_DIR)
            module_name = args.module or name
            template = args.template or "minimal"
            author = args.author
            description = args.description or f"Modulo {module_name} gerado pelo Neodoo"
            use_venv = not args.no_venv

    project_dir = base_dir / name
    if project_dir.exists():
        print(f"Diretorio ja existe: {project_dir}")
        sys.exit(1)

    _print(f"Criando projeto em: {project_dir}")
    ensure_dir(project_dir)

    for d in ("custom_addons", "community_addons", "logs", "filestore"):
        ensure_dir(project_dir / d)

    _print("Baixando Odoo 18+ (shallow clone)...")
    clone_repo(ODOO_REPO, ODOO_BRANCH, project_dir / "odoo_source")

    _print("Baixando OCA/web (inclui web_responsive)...")
    clone_repo(OCA_WEB_REPO, ODOO_BRANCH, project_dir / "community_addons" / "web")

    if use_venv:
        create_virtualenv(project_dir)

    _print(f"Gerando modulo inicial: {module_name} ({template})")
    call_generator(module_name, template, project_dir / "custom_addons", author, description)

    create_odoo_conf(project_dir, db_name=name, addons=[
        "odoo_source/addons",
        "custom_addons",
        "community_addons/web",
    ])
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

    _print("Projeto criado com sucesso!")
    _print(f"Para iniciar: cd {project_dir} && ./run.sh")


def cmd_list(_args):
    base = Path(_args.base_dir or DEFAULT_BASE_DIR)
    if not base.exists():
        print(f"(vazio) {base}")
        return
    items = [p for p in base.iterdir() if p.is_dir()]
    if not items:
        print(f"(vazio) {base}")
        return
    for i, p in enumerate(sorted(items), start=1):
        print(f"{i}. {p.name} - {p}")


def cmd_delete(args):
    base = Path(args.base_dir or DEFAULT_BASE_DIR)
    name = args.name or prompt("Nome do projeto a excluir")
    path = base / name
    if not path.exists():
        print(f"Nao encontrado: {path}")
        sys.exit(1)
    conf = prompt(f"Tem certeza que deseja remover '{name}'? (DELETE para confirmar)")
    if conf != "DELETE":
        print("Cancelado.")
        return
    shutil.rmtree(path)
    print("Removido com sucesso.")


def cmd_doctor(args):
    print("neodoo doctor - verificando ambiente...")
    ok = True
    for label, cmdname in [("python3", Path(sys.executable).name), ("git", "git"), ("psql", "psql"), ("docker", "docker")]:
        exists = _check_cmd_exists(cmdname)
        print(f" - {label}: {'OK' if exists else 'NAO ENCONTRADO'}")
        if label in ("python3", "git") and not exists:
            ok = False
    for port in (8069, 8072):
        free = _port_free(port)
        print(f" - porta {port}: {'livre' if free else 'ocupada'}")
    if getattr(args, "path", None):
        p = Path(args.path)
        print(f" - checando projeto em: {p}")
        if not p.exists():
            print("   diretorio nao existe")
            ok = False
        else:
            for sub in ("odoo_source", "custom_addons", "community_addons", "odoo.conf"):
                present = (p / sub).exists()
                print(f"   - {sub}: {'OK' if present else 'faltando'}")
                if not present:
                    ok = False
            venv_ok = (p / ".venv" / "bin" / "python").exists()
            print(f"   - venv: {'OK' if venv_ok else 'ausente'}")
    if not ok:
        print("Problemas detectados")
        sys.exit(1)
    print("Ambiente saudavel")


def _git_pull(path):
    if not (path / ".git").exists():
        return
    try:
        run(["git", "pull", "--rebase"], cwd=path)
    except subprocess.CalledProcessError:
        print(f"git pull falhou em {path}")


def cmd_update(args):
    p = Path(args.path)
    if not p.exists():
        print(f"Diretorio nao encontrado: {p}")
        sys.exit(1)
    print("Atualizando repositorios...")
    _git_pull(p / "odoo_source")
    _git_pull(p / "community_addons" / "web")
    if not args.no_deps:
        pip_bin = p / ".venv" / "bin" / "pip"
        req = p / "odoo_source" / "requirements.txt"
        if pip_bin.exists() and req.exists():
            try:
                run([str(pip_bin), "install", "--upgrade", "pip"])
                run([str(pip_bin), "install", "-r", str(req)])
            except subprocess.CalledProcessError:
                print("Falha ao atualizar dependencias.")
        else:
            print("venv nao encontrada ou requirements ausente; pulando deps.")


def cmd_run(args):
    """Execute um projeto Odoo com feedback detalhado"""
    project_path = Path(args.path) if args.path else Path.cwd()
    
    if not project_path.exists():
        print(f"❌ Diretorio nao encontrado: {project_path}")
        sys.exit(1)
    
    # Verificar se é um projeto Odoo válido
    run_sh = project_path / "run.sh"
    odoo_conf = project_path / "odoo.conf"
    odoo_bin = project_path / "odoo_source" / "odoo-bin"
    
    if not run_sh.exists():
        print(f"❌ Arquivo run.sh nao encontrado em: {project_path}")
        print("💡 Execute 'neodoo create' para criar um projeto Odoo")
        sys.exit(1)
    
    if not odoo_bin.exists():
        print(f"❌ Odoo nao encontrado em: {project_path / 'odoo_source'}")
        print("💡 Execute 'neodoo create' para criar um projeto completo")
        sys.exit(1)
    
    # Ler configuração para mostrar detalhes
    port = "8069"  # default
    db_name = "odoo"
    if odoo_conf.exists():
        try:
            conf_content = odoo_conf.read_text()
            for line in conf_content.split('\n'):
                if 'xmlrpc_port' in line and '=' in line:
                    port = line.split('=')[1].strip()
                elif 'db_name' in line and '=' in line:
                    db_name = line.split('=')[1].strip()
        except Exception:
            pass
    
    print(f"\n🚀 Iniciando projeto Odoo...")
    print(f"📁 Projeto: {project_path.name}")
    print(f"🗄️  Database: {db_name}")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"📝 Logs: {project_path}/logs/odoo.log")
    print("\n⏳ Carregando Odoo (isso pode demorar alguns segundos...)")
    print("\n" + "="*60)
    
    # Executar o run.sh
    try:
        os.chdir(project_path)
        os.execv("/bin/bash", ["bash", str(run_sh)])
    except Exception as e:
        print(f"❌ Erro ao executar projeto: {e}")
        sys.exit(1)


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
    if not getattr(args, "cmd", None):
        args = parser.parse_args(["create"])  # type: ignore
    try:
        args.func(args)
    except subprocess.CalledProcessError as e:
        cmd_str = e.cmd if isinstance(e.cmd, list) else [str(e.cmd)]
        print(f"Erro em comando externo (exit {e.returncode}): {' '.join(cmd_str)}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
