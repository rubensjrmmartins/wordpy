import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from django.contrib.auth.models import User

# Criar superusuário se não existir
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuário criado com sucesso!')
    print('Username: admin')
    print('Password: admin123')
else:
    print('Superusuário já existe!')
