# Guia de Solução de Problemas - WordPy CMS

## Erro do CKEditor ao Iniciar o Servidor

### Sintomas
- Aviso sobre CKEditor 4.22.1 não sendo mais suportado
- Erro ao carregar arquivos estáticos do CKEditor no admin

### Soluções

#### 1. Coletar Arquivos Estáticos

O CKEditor precisa que seus arquivos estáticos sejam coletados antes de usar:

```bash
python manage.py collectstatic --no-input
```

Isso copiará todos os arquivos necessários (CSS, JavaScript, imagens) para a pasta `staticfiles/`.

#### 2. Verificar Configuração

Certifique-se de que as seguintes configurações estão no `settings.py`:

```python
# Configurações de arquivos estáticos
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Permitir iframe do CKEditor
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Silenciar avisos (opcional)
SILENCED_SYSTEM_CHECKS = ['ckeditor.W001']
```

#### 3. Verificar Diretórios

Certifique-se de que os diretórios existem:

```bash
# Windows
mkdir media
mkdir staticfiles

# Linux/Mac
mkdir -p media staticfiles
```

#### 4. Testar Configuração

Execute o script de teste:

```bash
python test_server.py
```

Isso verificará:
- ✅ Se o CKEditor está instalado
- ✅ Se os arquivos estáticos foram coletados
- ✅ Se os diretórios existem
- ✅ Se o banco de dados está configurado

### Avisos do CKEditor

O aviso sobre CKEditor 4.22.1 é um alerta de segurança, não um erro fatal. O sistema funcionará normalmente, mas você pode:

1. **Silenciar o aviso** (já configurado):
```python
SILENCED_SYSTEM_CHECKS = ['ckeditor.W001']
```

2. **Atualizar para CKEditor 5** (futuro):
```bash
pip uninstall django-ckeditor
pip install django-ckeditor-5
```

## Outros Problemas Comuns

### 1. Erro de Importação de Módulos

**Sintoma:** `ModuleNotFoundError: No module named 'django'`

**Solução:**
```bash
# Ativar ambiente virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### 2. Erro no Banco de Dados

**Sintoma:** `no such table: blog_post`

**Solução:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Erro de Permissão de Mídia

**Sintoma:** Não consegue fazer upload de imagens

**Solução:**
- Verifique se a pasta `media/` existe
- Verifique permissões da pasta
- Windows: Clique com botão direito > Propriedades > Segurança
- Linux: `chmod 755 media/`

### 4. Admin Não Carrega Estilos

**Sintoma:** Página admin sem CSS

**Solução:**
```bash
python manage.py collectstatic --no-input
```

### 5. Erro de CSRF Token

**Sintoma:** `CSRF verification failed`

**Solução:**
Certifique-se de que o template usa `{% csrf_token %}` em todos os formulários.

### 6. Imagens Não Aparecem

**Sintoma:** Imagens não carregam no frontend

**Solução:**
Verifique as URLs em `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Comandos Úteis para Diagnóstico

### Verificar Sistema
```bash
python manage.py check
```

### Verificar Migrações
```bash
python manage.py showmigrations
```

### Verificar Configurações
```bash
python manage.py diffsettings
```

### Shell Interativo
```bash
python manage.py shell
```

Dentro do shell:
```python
from blog.models import Post
print(Post.objects.count())
```

### Ver SQL das Queries
```bash
python manage.py sqlmigrate blog 0001
```

## Logs e Debugging

### Ativar Logs Detalhados

Adicione ao `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### Debug Toolbar (Opcional)

Para desenvolvimento:

```bash
pip install django-debug-toolbar
```

Adicione ao `INSTALLED_APPS`:
```python
'debug_toolbar',
```

Adicione ao `MIDDLEWARE`:
```python
'debug_toolbar.middleware.DebugToolbarMiddleware',
```

## Performance

### Cache

Para melhorar performance, configure cache:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### Otimização de Queries

Use `select_related` e `prefetch_related` nas views (já implementado).

## Contato

Se o problema persistir:
1. Verifique os logs do servidor
2. Execute `python test_server.py`
3. Verifique se todas as dependências estão instaladas: `pip list`
4. Consulte a documentação do Django: https://docs.djangoproject.com/

---

**Última atualização:** 2025-11-18
