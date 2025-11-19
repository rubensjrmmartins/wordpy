import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from blog.models import Theme

print("=" * 60)
print("CRIANDO TEMAS PRE-DEFINIDOS")
print("=" * 60)

themes_data = [
    {
        'name': 'WordPy Light (Padrão)',
        'description': 'Tema claro e moderno, ideal para a maioria dos sites',
        'primary_color': '#3498db',
        'secondary_color': '#2c3e50',
        'accent_color': '#e74c3c',
        'text_color': '#333333',
        'heading_color': '#2c3e50',
        'link_color': '#3498db',
        'link_hover_color': '#2980b9',
        'background_color': '#ffffff',
        'secondary_bg_color': '#f5f5f5',
        'header_bg_color': '#2c3e50',
        'header_text_color': '#ffffff',
        'footer_bg_color': '#34495e',
        'footer_text_color': '#ffffff',
        'button_bg_color': '#3498db',
        'button_text_color': '#ffffff',
        'button_hover_bg_color': '#2980b9',
        'font_family': "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif",
        'heading_font_family': '',
        'font_size_base': '16px',
        'line_height': '1.6',
        'border_radius': '8px',
        'box_shadow': '0 2px 5px rgba(0,0,0,0.1)',
        'is_default': True,
        'is_active': True,
    },
    {
        'name': 'Dark Mode',
        'description': 'Tema escuro elegante para reduzir fadiga visual',
        'primary_color': '#1abc9c',
        'secondary_color': '#2c3e50',
        'accent_color': '#e74c3c',
        'text_color': '#ecf0f1',
        'heading_color': '#ffffff',
        'link_color': '#1abc9c',
        'link_hover_color': '#16a085',
        'background_color': '#1a1a1a',
        'secondary_bg_color': '#2d2d2d',
        'header_bg_color': '#000000',
        'header_text_color': '#ffffff',
        'footer_bg_color': '#000000',
        'footer_text_color': '#ffffff',
        'button_bg_color': '#1abc9c',
        'button_text_color': '#ffffff',
        'button_hover_bg_color': '#16a085',
        'font_family': "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif",
        'heading_font_family': '',
        'font_size_base': '16px',
        'line_height': '1.7',
        'border_radius': '4px',
        'box_shadow': '0 4px 6px rgba(0,0,0,0.3)',
        'is_default': False,
        'is_active': False,
    },
    {
        'name': 'Professional Blue',
        'description': 'Tema profissional em tons de azul para empresas',
        'primary_color': '#2563eb',
        'secondary_color': '#1e40af',
        'accent_color': '#f59e0b',
        'text_color': '#374151',
        'heading_color': '#1f2937',
        'link_color': '#2563eb',
        'link_hover_color': '#1d4ed8',
        'background_color': '#ffffff',
        'secondary_bg_color': '#f3f4f6',
        'header_bg_color': '#1e40af',
        'header_text_color': '#ffffff',
        'footer_bg_color': '#111827',
        'footer_text_color': '#f9fafb',
        'button_bg_color': '#2563eb',
        'button_text_color': '#ffffff',
        'button_hover_bg_color': '#1d4ed8',
        'font_family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        'heading_font_family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        'font_size_base': '15px',
        'line_height': '1.75',
        'border_radius': '6px',
        'box_shadow': '0 1px 3px rgba(0,0,0,0.12)',
        'is_default': False,
        'is_active': False,
    },
    {
        'name': 'Vibrant Colors',
        'description': 'Tema colorido e vibrante para sites criativos',
        'primary_color': '#8b5cf6',
        'secondary_color': '#ec4899',
        'accent_color': '#f59e0b',
        'text_color': '#1f2937',
        'heading_color': '#7c3aed',
        'link_color': '#8b5cf6',
        'link_hover_color': '#7c3aed',
        'background_color': '#ffffff',
        'secondary_bg_color': '#faf5ff',
        'header_bg_color': '#7c3aed',
        'header_text_color': '#ffffff',
        'footer_bg_color': '#581c87',
        'footer_text_color': '#faf5ff',
        'button_bg_color': '#8b5cf6',
        'button_text_color': '#ffffff',
        'button_hover_bg_color': '#7c3aed',
        'font_family': "'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        'heading_font_family': "'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        'font_size_base': '16px',
        'line_height': '1.6',
        'border_radius': '12px',
        'box_shadow': '0 4px 12px rgba(139,92,246,0.15)',
        'is_default': False,
        'is_active': False,
    },
    {
        'name': 'Minimalist',
        'description': 'Tema minimalista e clean para conteúdo em foco',
        'primary_color': '#000000',
        'secondary_color': '#404040',
        'accent_color': '#ff0000',
        'text_color': '#333333',
        'heading_color': '#000000',
        'link_color': '#000000',
        'link_hover_color': '#666666',
        'background_color': '#ffffff',
        'secondary_bg_color': '#fafafa',
        'header_bg_color': '#ffffff',
        'header_text_color': '#000000',
        'footer_bg_color': '#f5f5f5',
        'footer_text_color': '#333333',
        'button_bg_color': '#000000',
        'button_text_color': '#ffffff',
        'button_hover_bg_color': '#333333',
        'font_family': "'Georgia', 'Times New Roman', serif",
        'heading_font_family': "'Helvetica Neue', Arial, sans-serif",
        'font_size_base': '18px',
        'line_height': '1.8',
        'border_radius': '0px',
        'box_shadow': 'none',
        'custom_css': '''
        /* Tema Minimalista - Estilos adicionais */
        header {
            border-bottom: 1px solid #e0e0e0;
        }
        footer {
            border-top: 1px solid #e0e0e0;
        }
        .sidebar, article {
            box-shadow: none !important;
            border: 1px solid #e0e0e0;
        }
        ''',
        'is_default': False,
        'is_active': False,
    },
]

created_count = 0
for theme_data in themes_data:
    theme, created = Theme.objects.get_or_create(
        name=theme_data['name'],
        defaults=theme_data
    )

    if created:
        print(f"\nOK - Tema criado: {theme.name}")
        created_count += 1
    else:
        print(f"\nINFO - Tema ja existe: {theme.name}")

print("\n" + "=" * 60)
print("TEMAS PRE-DEFINIDOS CRIADOS!")
print("=" * 60)
print(f"\nTotal de temas criados: {created_count}")
print(f"Total de temas disponiveis: {Theme.objects.count()}")

# Verificar tema ativo
active_theme = Theme.get_active_theme()
if active_theme:
    print(f"\nTema ativo: {active_theme.name}")
else:
    print("\nNenhum tema ativo!")

print("\nPara trocar o tema:")
print("1. Acesse: http://127.0.0.1:8000/admin/blog/theme/")
print("2. Selecione um tema")
print("3. Marque como 'Tema Ativo'")
print("4. Salve")
print("\nOu use a acao 'Ativar tema selecionado' na lista de temas")
print("=" * 60)
