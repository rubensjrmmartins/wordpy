# Guia de Deploy do WordPy CMS na KingHost com WSGI

**Versão**: 1.0
**Data**: 19/01/2025
**Sistema**: WordPy CMS
**Plataforma**: KingHost Hospedagem
**Tecnologia**: Python/Django + WSGI

---

## Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Preparação do Projeto](#2-preparação-do-projeto)
3. [Configuração na KingHost](#3-configuração-na-kinghost)
4. [Estrutura de Diretórios](#4-estrutura-de-diretórios)
5. [Configuração do WSGI](#5-configuração-do-wsgi)
6. [Configuração do Banco de Dados](#6-configuração-do-banco-de-dados)
7. [Arquivos Estáticos e Media](#7-arquivos-estáticos-e-media)
8. [Configurações de Produção](#8-configurações-de-produção)
9. [Deploy Passo a Passo](#9-deploy-passo-a-passo)
10. [Troubleshooting](#10-troubleshooting)
11. [Manutenção e Atualizações](#11-manutenção-e-atualizações)

---

## 1. Pré-requisitos

### 1.1 Plano de Hospedagem KingHost

Certifique-se de ter:
- ✅ Plano KingHost com suporte a Python (KingHost Python)
- ✅ Acesso ao painel de controle
- ✅ Acesso SSH (recomendado)
- ✅ Banco de dados MySQL ou PostgreSQL configurado

### 1.2 Informações Necessárias

Tenha em mãos:
- URL do seu domínio (ex: `seusite.com.br`)
- Credenciais do banco de dados:
  - Host do banco
  - Nome do banco
  - Usuário
  - Senha
  - Porta
- Acesso FTP ou SSH

### 1.3 Versões Suportadas

- **Python**: 3.8+ (verificar versão disponível na KingHost)
- **Django**: 5.2
- **Banco de Dados**: MySQL 5.7+ ou PostgreSQL 12+

---

## 2. Preparação do Projeto

### 2.1 Gerar requirements.txt

No seu ambiente local, gere o arquivo de dependências:

```bash
cd C:\git\wordpy
pip freeze > requirements.txt
```

**Arquivo gerado**: `requirements.txt`

### 2.2 Criar arquivo .env para Produção

Crie um arquivo `.env.production` com as variáveis de ambiente:

```bash
# .env.production

# Django Settings
SECRET_KEY=sua_chave_secreta_super_segura_aqui_com_50_caracteres
DEBUG=False
ALLOWED_HOSTS=seudominio.com.br,www.seudominio.com.br

# Database (MySQL exemplo)
DB_ENGINE=django.db.backends.mysql
DB_NAME=seu_banco_de_dados
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_HOST=localhost
DB_PORT=3306

# Database (PostgreSQL exemplo - escolha um)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=seu_banco_de_dados
# DB_USER=seu_usuario_postgres
# DB_PASSWORD=sua_senha_postgres
# DB_HOST=localhost
# DB_PORT=5432

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email (configurar de acordo com provedor)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.seudominio.com.br
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=contato@seudominio.com.br
EMAIL_HOST_PASSWORD=senha_email
```

**⚠️ IMPORTANTE**:
- Gere uma nova `SECRET_KEY` para produção
- NUNCA commite `.env.production` no Git
- Use senhas fortes e únicas

### 2.3 Gerar Nova SECRET_KEY

No terminal Python:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copie a chave gerada para o arquivo `.env.production`

### 2.4 Atualizar settings.py para Produção

Crie um arquivo `wordpy_cms/settings_production.py`:

```python
# wordpy_cms/settings_production.py

from .settings import *
import os
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = '/home/seu_usuario/public_html/static/'
MEDIA_ROOT = '/home/seu_usuario/public_html/media/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/seu_usuario/logs/django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

## 3. Configuração na KingHost

### 3.1 Acesso ao Painel

1. Acesse o painel da KingHost
2. Vá em **Hospedagem de Sites** → Seu domínio
3. Localize a seção **Python**

### 3.2 Criar Aplicação Python

1. Clique em **Criar Aplicação Python**
2. Selecione:
   - **Versão do Python**: 3.9 ou superior
   - **Caminho da aplicação**: `/home/seu_usuario/wordpy`
   - **URL**: Seu domínio

### 3.3 Obter Informações do Banco

1. No painel, vá em **Banco de Dados**
2. Anote:
   - Host do banco
   - Nome do banco
   - Usuário
   - Porta

---

## 4. Estrutura de Diretórios

A estrutura na KingHost deve ficar assim:

```
/home/seu_usuario/
├── wordpy/                          # Projeto Django
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env                         # Variáveis de ambiente
│   ├── wordpy_cms/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── settings_production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── blog/
│   ├── accounts/
│   ├── dashboard/
│   ├── ecommerce/
│   ├── messaging/
│   ├── modules/
│   └── venv/                        # Ambiente virtual (criar no servidor)
│
├── public_html/                     # Diretório público
│   ├── static/                      # Arquivos estáticos coletados
│   │   ├── admin/
│   │   ├── css/
│   │   ├── js/
│   │   └── ...
│   ├── media/                       # Uploads de usuários
│   │   ├── products/
│   │   ├── posts/
│   │   └── ...
│   └── passenger_wsgi.py            # Arquivo WSGI principal
│
└── logs/                            # Logs da aplicação
    └── django_errors.log
```

---

## 5. Configuração do WSGI

### 5.1 Criar arquivo passenger_wsgi.py

Crie o arquivo `/home/seu_usuario/public_html/passenger_wsgi.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Passenger WSGI file for WordPy CMS on KingHost
"""

import sys
import os

# Adicionar o diretório do projeto ao path
INTERP = "/home/seu_usuario/wordpy/venv/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Caminho para o projeto
sys.path.insert(0, '/home/seu_usuario/wordpy')
sys.path.insert(0, '/home/seu_usuario/wordpy/wordpy_cms')

# Configurar variável de ambiente do Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'wordpy_cms.settings_production'

# Carregar variáveis de ambiente do .env
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('/home/seu_usuario/wordpy') / '.env'
load_dotenv(dotenv_path=env_path)

# Importar aplicação WSGI do Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ IMPORTANTE**: Substitua `seu_usuario` pelo seu usuário real da KingHost.

### 5.2 Permissões do arquivo

Dê permissão de execução ao arquivo:

```bash
chmod 755 /home/seu_usuario/public_html/passenger_wsgi.py
```

---

## 6. Configuração do Banco de Dados

### 6.1 MySQL (Recomendado para KingHost)

#### Instalar conector MySQL:

Adicione ao `requirements.txt`:
```
mysqlclient==2.1.1
```

#### Configurar no .env:
```bash
DB_ENGINE=django.db.backends.mysql
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
```

### 6.2 PostgreSQL (Alternativa)

#### Instalar conector PostgreSQL:

Adicione ao `requirements.txt`:
```
psycopg2-binary==2.9.5
```

#### Configurar no .env:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

---

## 7. Arquivos Estáticos e Media

### 7.1 Configurar settings.py

Adicione ao `settings_production.py`:

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = '/home/seu_usuario/public_html/static/'

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/seu_usuario/public_html/media/'
```

### 7.2 Coletar arquivos estáticos

Via SSH:

```bash
cd /home/seu_usuario/wordpy
source venv/bin/activate
python manage.py collectstatic --noinput --settings=wordpy_cms.settings_production
```

### 7.3 Configurar .htaccess

Crie `/home/seu_usuario/public_html/.htaccess`:

```apache
# .htaccess para WordPy CMS

# Proteger arquivos sensíveis
<FilesMatch "^\.env">
    Order allow,deny
    Deny from all
</FilesMatch>

# Configuração de arquivos estáticos
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>

# Compressão GZIP
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>

# Configuração de segurança
Header set X-Content-Type-Options "nosniff"
Header set X-Frame-Options "DENY"
Header set X-XSS-Protection "1; mode=block"
```

---

## 8. Configurações de Produção

### 8.1 Checklist de Segurança

```python
# wordpy_cms/settings_production.py

# ✅ Debug desligado
DEBUG = False

# ✅ Hosts permitidos configurados
ALLOWED_HOSTS = ['seudominio.com.br', 'www.seudominio.com.br']

# ✅ Secret key única e segura
SECRET_KEY = os.getenv('SECRET_KEY')

# ✅ HTTPS forçado
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ✅ Proteções de segurança
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ✅ CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://seudominio.com.br',
    'https://www.seudominio.com.br',
]
```

### 8.2 Otimizações

```python
# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/seu_usuario/wordpy/cache',
    }
}

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Templates
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]
```

---

## 9. Deploy Passo a Passo

### Passo 1: Upload dos Arquivos

Via FTP ou SSH, faça upload de:
- Todo o código do projeto (exceto `venv/`)
- Arquivo `requirements.txt`
- Arquivo `.env` (renomeie de `.env.production`)

```bash
# Via SCP (local → servidor)
scp -r wordpy/ seu_usuario@seu_servidor:/home/seu_usuario/
```

### Passo 2: Conectar via SSH

```bash
ssh seu_usuario@seu_servidor
```

### Passo 3: Criar Ambiente Virtual

```bash
cd /home/seu_usuario/wordpy
python3 -m venv venv
source venv/bin/activate
```

### Passo 4: Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 5: Criar Diretórios Necessários

```bash
mkdir -p /home/seu_usuario/public_html/static
mkdir -p /home/seu_usuario/public_html/media
mkdir -p /home/seu_usuario/logs
mkdir -p /home/seu_usuario/wordpy/cache
```

### Passo 6: Configurar Banco de Dados

```bash
# Testar conexão
python manage.py dbshell --settings=wordpy_cms.settings_production

# Executar migrações
python manage.py migrate --settings=wordpy_cms.settings_production
```

### Passo 7: Criar Superusuário

```bash
python manage.py createsuperuser --settings=wordpy_cms.settings_production
```

### Passo 8: Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput --settings=wordpy_cms.settings_production
```

### Passo 9: Configurar WSGI

```bash
# Criar o arquivo passenger_wsgi.py (conforme seção 5.1)
nano /home/seu_usuario/public_html/passenger_wsgi.py

# Dar permissões
chmod 755 /home/seu_usuario/public_html/passenger_wsgi.py
```

### Passo 10: Reiniciar Aplicação

```bash
# No painel da KingHost ou via SSH
touch /home/seu_usuario/public_html/tmp/restart.txt
```

### Passo 11: Testar

Acesse seu domínio: `https://seudominio.com.br`

---

## 10. Troubleshooting

### Problema 1: Erro 500 - Internal Server Error

**Sintomas**: Página em branco ou erro 500

**Soluções**:

1. **Verificar logs**:
```bash
tail -f /home/seu_usuario/logs/django_errors.log
tail -f /home/seu_usuario/logs/error.log
```

2. **Verificar permissões**:
```bash
chmod 755 /home/seu_usuario/public_html/passenger_wsgi.py
chmod 755 /home/seu_usuario/wordpy
```

3. **Verificar WSGI**:
```bash
python /home/seu_usuario/public_html/passenger_wsgi.py
```

### Problema 2: Arquivos Estáticos Não Carregam

**Sintomas**: CSS/JS não funcionam, site sem estilo

**Soluções**:

1. **Coletar novamente**:
```bash
python manage.py collectstatic --clear --noinput
```

2. **Verificar permissões**:
```bash
chmod -R 755 /home/seu_usuario/public_html/static
```

3. **Verificar STATIC_ROOT** em `settings_production.py`

### Problema 3: Erro de Banco de Dados

**Sintomas**: "Can't connect to database"

**Soluções**:

1. **Verificar credenciais** no `.env`

2. **Testar conexão**:
```bash
mysql -u seu_usuario -p -h localhost seu_banco
```

3. **Verificar se mysqlclient está instalado**:
```bash
pip show mysqlclient
```

### Problema 4: Módulo Não Encontrado

**Sintomas**: "ModuleNotFoundError: No module named 'xxx'"

**Soluções**:

1. **Reinstalar dependências**:
```bash
source /home/seu_usuario/wordpy/venv/bin/activate
pip install -r requirements.txt
```

2. **Verificar paths no passenger_wsgi.py**

### Problema 5: CSRF Verification Failed

**Sintomas**: Erro ao submeter formulários

**Soluções**:

Adicione ao `settings_production.py`:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://seudominio.com.br',
    'https://www.seudominio.com.br',
]
```

### Problema 6: Upload de Arquivos Não Funciona

**Sintomas**: Erro ao fazer upload de imagens

**Soluções**:

1. **Verificar permissões**:
```bash
chmod -R 755 /home/seu_usuario/public_html/media
```

2. **Verificar MEDIA_ROOT** em settings

---

## 11. Manutenção e Atualizações

### 11.1 Atualizar Código

```bash
# 1. Backup
cd /home/seu_usuario
tar -czf backup_wordpy_$(date +%Y%m%d).tar.gz wordpy/

# 2. Upload novos arquivos via FTP/SCP

# 3. Ativar ambiente virtual
cd /home/seu_usuario/wordpy
source venv/bin/activate

# 4. Instalar novas dependências (se houver)
pip install -r requirements.txt

# 5. Executar migrações
python manage.py migrate --settings=wordpy_cms.settings_production

# 6. Coletar estáticos
python manage.py collectstatic --noinput --settings=wordpy_cms.settings_production

# 7. Reiniciar aplicação
touch /home/seu_usuario/public_html/tmp/restart.txt
```

### 11.2 Backup do Banco de Dados

```bash
# MySQL
mysqldump -u seu_usuario -p seu_banco > backup_$(date +%Y%m%d).sql

# Restaurar
mysql -u seu_usuario -p seu_banco < backup_20250119.sql
```

### 11.3 Monitoramento

#### Verificar logs regularmente:
```bash
# Erros do Django
tail -f /home/seu_usuario/logs/django_errors.log

# Erros do servidor
tail -f /home/seu_usuario/logs/error.log

# Acesso
tail -f /home/seu_usuario/logs/access.log
```

#### Script de monitoramento (cron):
```bash
# Adicionar ao crontab
crontab -e

# Verificar espaço em disco diariamente às 2h
0 2 * * * df -h > /home/seu_usuario/logs/disk_usage.log

# Backup automático diário às 3h
0 3 * * * mysqldump -u seu_usuario -p'senha' seu_banco | gzip > /home/seu_usuario/backups/db_$(date +\%Y\%m\%d).sql.gz
```

---

## 12. Comandos Úteis

### Django Management Commands

```bash
# Sempre usar com settings de produção
alias djprod="python manage.py --settings=wordpy_cms.settings_production"

# Exemplos:
djprod migrate
djprod collectstatic
djprod createsuperuser
djprod shell
djprod dbshell
```

### Reiniciar Aplicação

```bash
# Método 1: Touch restart
touch /home/seu_usuario/public_html/tmp/restart.txt

# Método 2: Via painel KingHost
# Acessar painel → Python → Reiniciar Aplicação
```

### Verificar Status

```bash
# Processos Python
ps aux | grep python

# Uso de memória
free -h

# Espaço em disco
df -h
```

---

## 13. Checklist Final de Deploy

### Pré-Deploy
- [ ] `DEBUG = False` em settings_production.py
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Nova `SECRET_KEY` gerada
- [ ] `.env` criado com todas as variáveis
- [ ] `requirements.txt` atualizado
- [ ] Backup do banco local criado

### Durante Deploy
- [ ] Arquivos enviados via FTP/SSH
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Banco de dados criado
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Arquivos estáticos coletados
- [ ] passenger_wsgi.py configurado
- [ ] Permissões ajustadas

### Pós-Deploy
- [ ] Site acessível via HTTPS
- [ ] Admin funciona (`/admin/`)
- [ ] Login funciona
- [ ] Upload de arquivos funciona
- [ ] CSS/JS carregam corretamente
- [ ] Formulários submetem sem erro CSRF
- [ ] E-mails sendo enviados (se configurado)
- [ ] Logs funcionando
- [ ] Backup automático configurado

### Testes Funcionais
- [ ] Criar post no blog
- [ ] Criar produto no e-commerce
- [ ] Enviar mensagem
- [ ] Testar páginas customizadas
- [ ] Verificar dashboard
- [ ] Testar busca
- [ ] Verificar categorias
- [ ] Testar upload de imagens

---

## 14. Suporte e Recursos

### Documentação
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [KingHost Documentação Python](https://king.host/wiki/python/)
- [Passenger WSGI](https://www.phusionpassenger.com/docs/)

### Contatos
- **Suporte KingHost**: suporte@kinghost.com.br
- **Telefone**: 0800 8000 050
- **Chat**: Disponível no painel

### Comunidade
- Django Brasil: https://grupos.google.com/g/django-brasil
- Python Brasil: https://python.org.br

---

## 15. Glossário

- **WSGI**: Web Server Gateway Interface - Interface entre servidor web e aplicação Python
- **Passenger**: Servidor de aplicações que roda apps Python/Ruby/Node.js
- **collectstatic**: Comando Django que coleta arquivos estáticos de todos os apps
- **venv**: Ambiente virtual Python isolado
- **SSH**: Secure Shell - Protocolo para acesso remoto seguro
- **FTP**: File Transfer Protocol - Protocolo de transferência de arquivos

---

## Conclusão

Este guia cobre todo o processo de deploy do WordPy CMS na KingHost usando WSGI. Seguindo todos os passos, você terá uma aplicação Django rodando em produção de forma segura e otimizada.

**Pontos Críticos para Lembrar**:
1. ⚠️ Sempre use `DEBUG = False` em produção
2. ⚠️ Mantenha a `SECRET_KEY` segura e única
3. ⚠️ Configure SSL/HTTPS corretamente
4. ⚠️ Faça backups regulares do banco de dados
5. ⚠️ Monitore logs frequentemente

**Boa sorte com seu deploy!** 🚀

---

*Documento criado em 19/01/2025 por Claude Code*
*Versão: 1.0*
*Última atualização: 19/01/2025*
