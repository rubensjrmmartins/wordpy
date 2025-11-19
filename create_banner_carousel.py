import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from blog.models import Section, Page, PageSection

print("=" * 60)
print("CRIANDO SECAO DE CARROSSEL DE BANNERS")
print("=" * 60)

# Criar seção de carrossel
carousel_section, created = Section.objects.get_or_create(
    name='Carrossel Principal',
    section_type='banner_carousel',
    defaults={
        'title': 'Bem-vindo ao WordPy CMS',
        'subtitle': 'Sistema de Gerenciamento de Conteúdo Poderoso',
        'content': '''<p>Crie sites incríveis com Python e Django.
        Totalmente customizável e fácil de usar.</p>''',
        'button_text': 'Saiba Mais',
        'button_link': '/blog/',
        'background_color': 'light',
    }
)

if created:
    print("\nOK - Secao de carrossel criada com sucesso!")
else:
    print("\nINFO - Secao de carrossel ja existe")

print(f"   Nome: {carousel_section.name}")
print(f"   Tipo: {carousel_section.get_section_type_display()}")
print(f"   Titulo: {carousel_section.title}")

# Tentar adicionar à página home
try:
    from blog.models import SiteSettings
    settings = SiteSettings.get_settings()

    if settings.home_page:
        home_page = settings.home_page

        # Verificar se já existe essa seção na página
        existing = PageSection.objects.filter(
            page=home_page,
            section=carousel_section
        ).exists()

        if not existing:
            # Adicionar no início (ordem 0)
            PageSection.objects.create(
                page=home_page,
                section=carousel_section,
                order=0,
                is_active=True
            )
            print(f"\nOK - Secao adicionada a pagina home: {home_page.title}")
        else:
            print(f"\nINFO - Secao ja existe na pagina home")
    else:
        print("\nINFO - Nenhuma pagina home configurada")
        print("Para usar o carrossel:")
        print("1. Configure uma pagina como home em 'Configuracoes do Site'")
        print("2. Ou adicione manualmente a secao 'Carrossel Principal' a uma pagina")

except Exception as e:
    print(f"\nAVISO - Nao foi possivel adicionar automaticamente: {e}")

print("\n" + "=" * 60)
print("COMO USAR O CARROSSEL")
print("=" * 60)
print("""
1. ADICIONAR A UMA PAGINA:
   - Acesse: Admin → Paginas
   - Edite uma pagina existente ou crie uma nova
   - Role ate 'Secoes da Pagina'
   - Clique em 'Adicionar outra Secao da Pagina'
   - Selecione: 'Carrossel Principal'
   - Defina a ordem (0 = primeiro)
   - Marque como ativa
   - Salve

2. CUSTOMIZAR BANNERS:
   - Acesse: Admin → Secoes
   - Edite 'Carrossel Principal'
   - Configure:
     * Titulo: Texto principal do primeiro banner
     * Subtitulo: Texto secundario
     * Conteudo: Descricao
     * Imagem: Imagem de fundo do primeiro banner
     * Botao: Texto e link do botao
   - Salve

3. FUNCIONALIDADES:
   - OK Rolagem automatica (5 segundos)
   - OK Navegacao manual (setas)
   - OK Indicadores (dots)
   - OK Pausar ao interagir
   - OK Responsivo

4. ADICIONAR MAIS BANNERS:
   Atualmente o carrossel tem 3 banners fixos.
   Para personalizar todos os banners, edite o template:
   blog/templates/blog/sections/banner_carousel.html
""")

print("=" * 60)
print("CONCLUIDO!")
print("=" * 60)

# Instruções para ver
print("\nPara visualizar o carrossel:")
if settings.home_page:
    print("Acesse: http://127.0.0.1:8000/")
else:
    print("1. Configure uma pagina como home")
    print("2. Ou acesse a pagina que contem a secao")
