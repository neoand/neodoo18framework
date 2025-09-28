# Guia de Deployment do Neodoo18Framework

Este documento descreve os passos necessários para realizar o deploy do Neodoo18Framework em diferentes ambientes.

## 1. Requisitos do Sistema

### Requisitos Mínimos
- Python 3.8+
- Git
- Pip

### Requisitos Recomendados
- Docker e Docker Compose (para ambientes containerizados)
- PostgreSQL 12+ (para desenvolvimento local sem Docker)
- Node.js 18+ (para assets)

## 2. Instalação Básica

### Clone do Repositório
```bash
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework
```

### Configuração do Ambiente
```bash
# Configurar o ambiente Python
./env.sh setup

# Ativar o ambiente
./env.sh activate
```

## 3. Criação de Projeto

```bash
# Criar um novo projeto
./neodoo create --name my_project
```

## 4. Deploy em Ambientes de Desenvolvimento

### Ambiente Local
```bash
# Navegar para o projeto
cd my_project

# Iniciar o servidor Odoo
python3 odoo-bin -c odoo.conf
```

### Ambiente Docker
```bash
# Iniciar containers
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 5. Deploy em Ambientes de Produção

### Preparação do Servidor
1. Instale as dependências no servidor:
   ```bash
   sudo apt-get update
   sudo apt-get install -y git python3 python3-pip python3-venv postgresql nginx
   ```

2. Clone o repositório:
   ```bash
   git clone https://github.com/your-org/your-odoo-project.git
   cd your-odoo-project
   ```

3. Configure o ambiente:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Configuração do Serviço Systemd
1. Crie um arquivo de serviço:
   ```bash
   sudo nano /etc/systemd/system/odoo.service
   ```

2. Adicione o seguinte conteúdo:
   ```ini
   [Unit]
   Description=Odoo Server
   After=network.target postgresql.service

   [Service]
   Type=simple
   User=odoo
   Group=odoo
   ExecStart=/path/to/your-odoo-project/venv/bin/python3 /path/to/your-odoo-project/odoo-bin -c /path/to/your-odoo-project/odoo.conf
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Ative e inicie o serviço:
   ```bash
   sudo systemctl enable odoo
   sudo systemctl start odoo
   ```

### Configuração do Nginx
1. Crie um arquivo de configuração:
   ```bash
   sudo nano /etc/nginx/sites-available/odoo
   ```

2. Adicione o seguinte conteúdo:
   ```nginx
   upstream odoo {
     server 127.0.0.1:8069;
   }

   server {
     listen 80;
     server_name your-domain.com;

     proxy_read_timeout 720s;
     proxy_connect_timeout 720s;
     proxy_send_timeout 720s;

     location / {
       proxy_pass http://odoo;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
     }

     location ~* /web/static/ {
       proxy_cache_valid 200 90m;
       proxy_buffering on;
       expires 864000;
       proxy_pass http://odoo;
     }
   }
   ```

3. Ative a configuração:
   ```bash
   sudo ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

## 6. Atualizações e Manutenção

### Atualização do Framework
```bash
cd neodoo18framework
git pull
./env.sh setup  # Atualizar dependências
```

### Backup de Banco de Dados
```bash
pg_dump -U odoo -h localhost -d odoo_db > backup_$(date +%Y%m%d).sql
```

## 7. Solução de Problemas

### Logs do Framework
Os logs do framework estão localizados em:
- `/var/log/odoo/odoo.log` (instalação de sistema)
- `./logs/odoo.log` (instalação local)
- Saída do Docker: `docker-compose logs -f`

### Verificação do Status do Serviço
```bash
sudo systemctl status odoo
```

### Reinício de Serviços
```bash
sudo systemctl restart odoo
sudo systemctl restart nginx
```

## 8. Recursos Adicionais

- [Documentação Oficial do Odoo](https://www.odoo.com/documentation/18.0/)
- [Fórum da Comunidade Odoo](https://www.odoo.com/forum/help-1)
- [Canal do Neodoo18Framework no GitHub](https://github.com/neoand/neodoo18framework/discussions)