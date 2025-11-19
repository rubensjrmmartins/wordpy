import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from blog.models import Page, Section, PageSection

print("=" * 60)
print("CRIANDO SECOES DE EXEMPLO")
print("=" * 60)

# Obter a página "Sobre"
try:
    page_sobre = Page.objects.get(slug='sobre')
    print(f"\nPagina encontrada: {page_sobre.title}")
except Page.DoesNotExist:
    print("\nERRO: Pagina 'Sobre' nao encontrada!")
    print("Execute primeiro: python populate_data.py")
    exit(1)

# Criar seções de exemplo
sections_data = [
    {
        'name': 'Hero - Sobre Nós',
        'section_type': 'hero',
        'title': 'Sobre o WordPy CMS',
        'subtitle': 'Um sistema de gerenciamento de conteúdo moderno e poderoso',
        'content': '<p>Desenvolvido com Python e Django para oferecer flexibilidade total</p>',
        'background_color': 'primary',
        'button_text': 'Conheca Mais',
        'button_link': '#recursos',
    },
    {
        'name': 'Missão e Visão',
        'section_type': 'text_image',
        'title': 'Nossa Missão',
        'subtitle': 'Democratizar a criação de sites profissionais',
        'content': '''
        <p>O WordPy CMS foi criado com o objetivo de fornecer uma alternativa open-source e customizável ao WordPress, usando tecnologias Python modernas.</p>
        <p>Acreditamos que criar e gerenciar conteúdo web deve ser simples, rápido e poderoso.</p>
        <ul>
            <li>100% Open Source</li>
            <li>Baseado em Django</li>
            <li>Totalmente Customizável</li>
            <li>SEO Otimizado</li>
        </ul>
        ''',
        'image_position': 'right',
        'background_color': 'white',
    },
    {
        'name': 'Recursos Principais',
        'section_type': 'features',
        'title': 'Recursos e Funcionalidades',
        'subtitle': 'Tudo que você precisa para criar sites incríveis',
        'content': '''
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #3498db; margin-bottom: 1rem;">📝 Editor Visual</h3>
                <p>Editor WYSIWYG completo com CKEditor para criar conteúdo rico</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #3498db; margin-bottom: 1rem;">🎨 Seções Modulares</h3>
                <p>Crie páginas complexas com seções reutilizáveis e personalizáveis</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #3498db; margin-bottom: 1rem;">🔍 SEO Otimizado</h3>
                <p>Meta tags, URLs amigáveis e integração com Google Analytics</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #3498db; margin-bottom: 1rem;">💬 Comentários</h3>
                <p>Sistema completo de comentários com moderação e respostas</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #3498db; margin-bottom: 1rem;">📸 Mídia</h3>
                <p>Biblioteca de mídia completa para gerenciar imagens e arquivos</p>
            </div>
            <div style="text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3 style="color: #3498db; margin-bottom: 1rem;">🚀 Performance</h3>
                <p>Otimizado para velocidade com queries eficientes e cache</p>
            </div>
        </div>
        ''',
        'background_color': 'light',
    },
    {
        'name': 'CTA - Comece Agora',
        'section_type': 'cta',
        'title': 'Pronto para começar?',
        'subtitle': 'Crie seu site profissional em minutos',
        'content': '<p>O WordPy CMS está pronto para uso. Comece a criar conteúdo agora mesmo!</p>',
        'background_color': 'dark',
        'button_text': 'Acessar Admin',
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
        sections_created.append(section)
    else:
        print(f"INFO - Secao ja existe: {section.name}")
        sections_created.append(section)

# Vincular seções à página "Sobre"
print(f"\nVinculando secoes a pagina '{page_sobre.title}'...")
for idx, section in enumerate(sections_created):
    page_section, created = PageSection.objects.get_or_create(
        page=page_sobre,
        section=section,
        defaults={'order': idx, 'is_active': True}
    )

    if created:
        print(f"OK - Secao '{section.name}' adicionada (ordem: {idx})")
    else:
        print(f"INFO - Secao '{section.name}' ja estava vinculada")

print("\n" + "=" * 60)
print("SECOES CRIADAS COM SUCESSO!")
print("=" * 60)
print(f"\nTotal de secoes criadas: {len(sections_created)}")
print(f"Secoes vinculadas a pagina: {page_sobre.page_sections.count()}")
print("\nAcesse a pagina:")
print("  http://127.0.0.1:8000/page/sobre/")
print("\nOu edite no admin:")
print("  http://127.0.0.1:8000/admin/blog/page/")
print("=" * 60)
