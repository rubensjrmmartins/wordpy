import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from django.template.loader import get_template
from django.conf import settings

print("INSTALLED_APPS:", settings.INSTALLED_APPS)
print("\nTemplate dirs:", settings.TEMPLATES[0]['DIRS'])
print("APP_DIRS:", settings.TEMPLATES[0]['APP_DIRS'])

# Verificar se o arquivo existe fisicamente
template_path = 'messaging/templates/messaging/conversation_list.html'
print(f"\nArquivo existe: {os.path.exists(template_path)}")

# Tentar carregar o template
try:
    template = get_template('messaging/conversation_list.html')
    print("\nOK - Template carregado com sucesso!")
    print("Origin:", template.template.origin.name)
except Exception as e:
    print(f"\nERRO ao carregar template: {e}")
    import traceback
    traceback.print_exc()
