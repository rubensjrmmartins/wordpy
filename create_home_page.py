import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Page, Section, PageSection, SiteSettings

print("=" * 60)
print("CRIANDO PAGINA HOME")
print("=" * 60)

# Obter admin
admin = User.objects.get(username='admin')

# Criar página Home
home_page, created = Page.objects.get_or_create(
    slug='home',
    defaults={
        'title': 'Home',
        'author': admin,
        'content': '',  # Sem conteúdo, só seções
        'is_published': True,
        'show_in_menu': False,  # Não mostrar no menu (já tem link Início)
        'meta_title': 'Bem-vindo ao WordPy CMS',
        'meta_description': 'Sistema de gerenciamento de conteúdo moderno desenvolvido com Python e Django',
    }
)

if created:
    print(f"\nOK - Pagina criada: {home_page.title}")
else:
    print(f"\nINFO - Pagina ja existe: {home_page.title}")

# Criar seções para a home
sections_data = [
    {
        'name': 'Hero - Home',
        'section_type': 'hero',
        'title': 'Bem-vindo ao WordPy CMS',
        'subtitle': 'Sistema de Gerenciamento de Conteúdo com Python e Django',
        'content': '<p>Crie sites incríveis com o poder e flexibilidade do Django</p>',
        'background_color': 'primary',
        'button_text': 'Explorar Recursos',
        'button_link': '#recursos',
    },
    {
        'name': 'Home - Por que escolher',
        'section_type': 'text_image',
        'title': 'Por que escolher o WordPy?',
        'subtitle': 'A alternativa Python ao WordPress',
        'content': '''
        <p>O WordPy CMS combina o melhor dos dois mundos: a simplicidade do WordPress com o poder do Django.</p>
        <ul style="list-style-type: none; padding: 0; margin-top: 1.5rem;">
            <li style="padding: 0.5rem 0;">✅ <strong>100% Open Source:</strong> Código livre e customizável</li>
            <li style="padding: 0.5rem 0;">✅ <strong>Tecnologia Moderna:</strong> Python 3.12 + Django 5.2</li>
            <li style="padding: 0.5rem 0;">✅ <strong>Seções Modulares:</strong> Crie páginas complexas facilmente</li>
            <li style="padding: 0.5rem 0;">✅ <strong>SEO Otimizado:</strong> Pronto para os mecanismos de busca</li>
            <li style="padding: 0.5rem 0;">✅ <strong>Editor Visual:</strong> CKEditor integrado</li>
            <li style="padding: 0.5rem 0;">✅ <strong>Seguro:</strong> Proteções do Django incluídas</li>
        </ul>
        ''',
        'image_position': 'right',
        'background_color': 'white',
    },
    {
        'name': 'Home - Recursos',
        'section_type': 'features',
        'title': 'Recursos Poderosos',
        'subtitle': 'Tudo que você precisa em um CMS moderno',
        'content': '''
        <div id="recursos" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
                <h3 style="color: #3498db; margin-bottom: 1rem;">Posts & Páginas</h3>
                <p>Sistema completo de blog com categorias, tags e comentários</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎨</div>
                <h3 style="color: #3498db; margin-bottom: 1rem;">Page Builder</h3>
                <p>Crie páginas com seções modulares - Hero, CTA, Features e mais</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📸</div>
                <h3 style="color: #3498db; margin-bottom: 1rem;">Biblioteca de Mídia</h3>
                <p>Gerencie imagens, vídeos e documentos com facilidade</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                <h3 style="color: #3498db; margin-bottom: 1rem;">Comentários</h3>
                <p>Sistema completo com moderação, respostas e notificações</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <h3 style="color: #3498db; margin-bottom: 1rem;">SEO Avançado</h3>
                <p>Meta tags, URLs amigáveis e integração com Analytics</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🛡️</div>
                <h3 style="color: #3498db; margin-bottom: 1rem;">Segurança</h3>
                <p>Proteção CSRF, XSS, SQL Injection - tudo do Django</p>
            </div>
        </div>
        ''',
        'background_color': 'light',
    },
    {
        'name': 'Home - CTA Final',
        'section_type': 'cta',
        'title': 'Comece a Criar Hoje Mesmo',
        'subtitle': 'Configure seu site em minutos',
        'content': '<p>O WordPy CMS está pronto para uso. Acesse o painel admin e comece a criar conteúdo agora!</p>',
        'background_color': 'dark',
        'button_text': 'Acessar Painel Admin',
        'button_link': '/admin/',
    },
]

# Criar as seções
sections_created = []
for idx, section_data in enumerate(sections_data, 1):
    section, created = Section.objects.get_or_create(
        name=section_data['name'],
        defaults=section_data
    )

    if created:
        print(f"OK - Secao criada: {section.name}")
    else:
        print(f"INFO - Secao ja existe: {section.name}")

    sections_created.append(section)

# Vincular seções à página Home
print(f"\nVinculando secoes a pagina '{home_page.title}'...")

# Limpar seções antigas se existirem
PageSection.objects.filter(page=home_page).delete()

for idx, section in enumerate(sections_created):
    page_section = PageSection.objects.create(
        page=home_page,
        section=section,
        order=idx,
        is_active=True
    )
    print(f"OK - Secao '{section.name}' adicionada (ordem: {idx})")

# Configurar como página inicial nas configurações
site_settings = SiteSettings.get_settings()
site_settings.home_page = home_page
site_settings.save()

print("\n" + "=" * 60)
print("PAGINA HOME CRIADA E CONFIGURADA!")
print("=" * 60)
print(f"\nPagina: {home_page.title}")
print(f"Secoes vinculadas: {home_page.page_sections.count()}")
print(f"Configurada como home: SIM")
print("\nAcesse:")
print("  Home: http://127.0.0.1:8000/")
print("  Admin: http://127.0.0.1:8000/admin/blog/page/")
print("\nO site agora tem:")
print("  / - Página Home customizada com seções")
print("  /blog/ - Lista de posts do blog")
print("=" * 60)
