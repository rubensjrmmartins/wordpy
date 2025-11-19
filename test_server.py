import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

print("=" * 60)
print("TESTE DE CONFIGURACAO - WordPy CMS")
print("=" * 60)

# Verificar configurações básicas
from django.conf import settings
print(f"\nDEBUG: {settings.DEBUG}")
print(f"DATABASES: {settings.DATABASES['default']['ENGINE']}")
print(f"INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps")

# Verificar models
from blog.models import Post, Category, SiteSettings
print(f"\nTotal de Posts: {Post.objects.count()}")
print(f"Total de Categorias: {Category.objects.count()}")

# Verificar CKEditor
try:
    import ckeditor
    print(f"\nCKEditor instalado: OK")
except ImportError:
    print(f"\nCKEditor: ERRO - Nao instalado")

# Verificar Taggit
try:
    import taggit
    print(f"Taggit instalado: OK")
except ImportError:
    print(f"Taggit: ERRO - Nao instalado")

# Verificar Pillow
try:
    from PIL import Image
    print(f"Pillow instalado: OK")
except ImportError:
    print(f"Pillow: ERRO - Nao instalado")

# Verificar diretorios
import pathlib
media_dir = pathlib.Path("media")
static_dir = pathlib.Path("staticfiles")
print(f"\nDiretorio media existe: {media_dir.exists()}")
print(f"Diretorio staticfiles existe: {static_dir.exists()}")

# Verificar arquivos CKEditor
ckeditor_files = list(static_dir.glob("ckeditor/**/*.js"))
print(f"Arquivos CKEditor coletados: {len(ckeditor_files)}")

print("\n" + "=" * 60)
print("TESTE COMPLETO!")
print("=" * 60)
print("\nO servidor esta pronto para rodar.")
print("Execute: python manage.py runserver")
print("\nAcesse:")
print("  Frontend: http://127.0.0.1:8000/")
print("  Admin: http://127.0.0.1:8000/admin/")
print("  Usuario: admin / Senha: admin123")
print("=" * 60)
