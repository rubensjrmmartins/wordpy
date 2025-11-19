# Sistema de Temas do WordPy CMS

## Visão Geral

O WordPy CMS possui um sistema completo de temas que permite customizar a aparência visual do site sem modificar código. O sistema utiliza CSS dinâmico gerado em tempo real baseado nas configurações do tema ativo.

## Características

- **5 Temas Pré-definidos**: Light, Dark Mode, Professional Blue, Vibrant Colors e Minimalist
- **Customização Completa**: Mais de 20 propriedades configuráveis por tema
- **CSS Dinâmico**: Geração automática de CSS com variáveis personalizadas
- **Interface Admin**: Gerenciamento visual com preview de cores
- **Troca Instantânea**: Mudança de tema sem necessidade de reiniciar o servidor

## Temas Pré-definidos

### 1. WordPy Light (Padrão)
- **Descrição**: Tema claro e moderno, ideal para a maioria dos sites
- **Cores**: Azul (#3498db) e cinza escuro (#2c3e50)
- **Estilo**: Profissional e limpo
- **Uso recomendado**: Blogs, sites corporativos, portfólios

### 2. Dark Mode
- **Descrição**: Tema escuro elegante para reduzir fadiga visual
- **Cores**: Verde água (#1abc9c) em fundo escuro (#1a1a1a)
- **Estilo**: Moderno e sofisticado
- **Uso recomendado**: Sites tech, blogs de programação, conteúdo noturno

### 3. Professional Blue
- **Descrição**: Tema profissional em tons de azul para empresas
- **Cores**: Azul corporativo (#2563eb) e cinza (#374151)
- **Estilo**: Corporativo e confiável
- **Uso recomendado**: Sites empresariais, portfolios profissionais

### 4. Vibrant Colors
- **Descrição**: Tema colorido e vibrante para sites criativos
- **Cores**: Roxo (#8b5cf6), rosa (#ec4899) e âmbar (#f59e0b)
- **Estilo**: Criativo e energético
- **Uso recomendado**: Sites criativos, agências, artistas

### 5. Minimalist
- **Descrição**: Tema minimalista e clean para conteúdo em foco
- **Cores**: Preto, branco e vermelho para acentos
- **Estilo**: Clean e focado no conteúdo
- **Uso recomendado**: Blogs literários, magazines, portfolios fotográficos

## Como Trocar de Tema

### Método 1: Via Configurações do Site (Recomendado) 🆕

Esta é a forma mais fácil e recomendada para trocar de tema:

1. Acesse o painel admin: `http://127.0.0.1:8000/admin/`
2. Navegue até **Configurações do Site** ou acesse: `http://127.0.0.1:8000/admin/blog/sitesettings/1/change/`
3. Role até a seção **"Configurações de Exibição"**
4. No campo **"Tema Ativo"**, selecione o tema desejado no dropdown
5. Clique em **"Salvar"**
6. O tema será aplicado instantaneamente em todo o site!

**Vantagens deste método:**
- ✅ Mais intuitivo - tudo centralizado nas configurações
- ✅ Mais rápido - apenas um dropdown
- ✅ Não precisa navegar até o admin de temas

### Método 2: Via Admin de Temas

1. Acesse o painel admin: `http://127.0.0.1:8000/admin/`
2. Navegue até **Blog → Temas** ou acesse: `http://127.0.0.1:8000/admin/blog/theme/`
3. Na lista de temas, selecione o checkbox do tema desejado
4. No dropdown "Ação", escolha **"Ativar tema selecionado"**
5. Clique em **"Ir"**
6. O tema será ativado instantaneamente

### Método 3: Editando o Tema

1. Acesse **Blog → Temas**
2. Clique no nome do tema que deseja ativar
3. Marque o checkbox **"Tema Ativo"**
4. Clique em **"Salvar"**

**Nota sobre Prioridade**: Se você configurar um tema nas "Configurações do Site", ele terá prioridade sobre os temas marcados como ativos na lista de temas. Isso permite gerenciar o tema do site de forma centralizada.

## Como Criar um Tema Customizado

### Via Admin

1. Acesse **Blog → Temas**
2. Clique em **"Adicionar Tema"**
3. Preencha os campos:

#### Informações Básicas
- **Nome do Tema**: Nome único e descritivo
- **Descrição**: Breve descrição do tema
- **Tema Ativo**: Marque para ativar imediatamente
- **Tema Padrão**: Marque para ser o tema padrão de fallback

#### Cores Principais
- **Cor Primária**: Cor principal do site (botões, links)
- **Cor Secundária**: Cor de apoio (cabeçalhos, menus)
- **Cor de Destaque**: Cor para CTAs e elementos importantes

#### Cores de Texto
- **Cor do Texto**: Cor padrão para textos
- **Cor dos Títulos**: Cor para h1, h2, h3, etc.
- **Cor dos Links**: Cor dos links
- **Cor dos Links (Hover)**: Cor ao passar o mouse

#### Cores de Fundo
- **Cor de Fundo**: Cor de fundo principal
- **Cor de Fundo Secundária**: Cor para sidebars, seções alternadas

#### Header e Footer
- **Cor de Fundo do Header**: Cor do cabeçalho
- **Cor do Texto do Header**: Cor dos textos no cabeçalho
- **Cor de Fundo do Footer**: Cor do rodapé
- **Cor do Texto do Footer**: Cor dos textos no rodapé

#### Botões
- **Cor de Fundo dos Botões**: Cor padrão dos botões
- **Cor do Texto dos Botões**: Cor do texto nos botões
- **Cor de Fundo dos Botões (Hover)**: Cor ao passar o mouse

#### Tipografia
- **Família de Fonte**: Família de fonte para textos (CSS font-family)
- **Família de Fonte dos Títulos**: Família para títulos (opcional)
- **Tamanho Base da Fonte**: Tamanho padrão (ex: 16px)
- **Altura da Linha**: Line-height (ex: 1.6)

#### Espaçamento e Layout
- **Border Radius**: Arredondamento de bordas (ex: 8px)
- **Box Shadow**: Sombra dos elementos (ex: 0 2px 5px rgba(0,0,0,0.1))

#### CSS Customizado
- **CSS Customizado**: CSS adicional aplicado após as variáveis do tema

4. Clique em **"Salvar"**

### Via Código (Avançado)

Crie um script Python para adicionar temas programaticamente:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from blog.models import Theme

theme = Theme.objects.create(
    name='Meu Tema Customizado',
    description='Descrição do meu tema',
    primary_color='#ff6b6b',
    secondary_color='#4ecdc4',
    accent_color='#ffe66d',
    text_color='#2d3436',
    heading_color='#000000',
    link_color='#ff6b6b',
    link_hover_color='#ee5a6f',
    background_color='#ffffff',
    secondary_bg_color='#f8f9fa',
    header_bg_color='#4ecdc4',
    header_text_color='#ffffff',
    footer_bg_color='#2d3436',
    footer_text_color='#ffffff',
    button_bg_color='#ff6b6b',
    button_text_color='#ffffff',
    button_hover_bg_color='#ee5a6f',
    font_family="'Montserrat', sans-serif",
    heading_font_family="'Playfair Display', serif",
    font_size_base='17px',
    line_height='1.7',
    border_radius='10px',
    box_shadow='0 3px 10px rgba(0,0,0,0.1)',
    is_active=False,
    is_default=False,
)

print(f'Tema "{theme.name}" criado com sucesso!')
```

## Prioridade na Seleção de Temas

O sistema de temas utiliza uma hierarquia de prioridade ao determinar qual tema aplicar:

1. **Primeira Prioridade - Configurações do Site** 🥇
   - Tema selecionado em "Configurações do Site" → "Tema Ativo"
   - Este método sobrescreve qualquer outra configuração

2. **Segunda Prioridade - Tema Marcado como Ativo** 🥈
   - Tema com campo `is_active = True` na lista de temas
   - Usado quando não há tema configurado nas Configurações do Site

3. **Terceira Prioridade - Tema Padrão** 🥉
   - Tema com campo `is_default = True`
   - Usado como fallback quando nenhum tema está ativo

**Exemplo:**
```
Se você tem:
- Configurações do Site → Tema Ativo: "Dark Mode"
- Blog/Temas → "Professional Blue" marcado como ativo
- Blog/Temas → "WordPy Light" marcado como padrão

O tema aplicado será: "Dark Mode" (prioridade 1)
```

Esta hierarquia permite flexibilidade total no gerenciamento de temas.

## Estrutura Técnica

### Model Theme

O modelo Theme (`blog/models.py`) contém todos os campos de configuração:

```python
class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    # Cores (20+ campos)
    primary_color = models.CharField(max_length=7, default="#3498db")
    # ... mais campos

    # Tipografia
    font_family = models.CharField(max_length=200, default="...")
    # ... mais campos

    # Layout
    border_radius = models.CharField(max_length=10, default="8px")
    box_shadow = models.CharField(max_length=100, default="...")

    # CSS Customizado
    custom_css = models.TextField(blank=True)

    # Controle
    is_active = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    @classmethod
    def get_active_theme(cls):
        """Retorna o tema ativo ou o tema padrão"""
        theme = cls.objects.filter(is_active=True).first()
        if not theme:
            theme = cls.objects.filter(is_default=True).first()
        return theme
```

### View de CSS Dinâmico

A view `theme_css_view` (`blog/views.py`) gera o CSS em tempo real:

```python
def theme_css_view(request):
    """Gera CSS dinâmico baseado no tema ativo"""
    theme = Theme.get_active_theme()

    if not theme:
        return HttpResponse('/* Nenhum tema configurado */', content_type='text/css')

    # Gera CSS com variáveis CSS
    css = f"""
    :root {{
        --primary-color: {theme.primary_color};
        --secondary-color: {theme.secondary_color};
        /* ... mais variáveis ... */
    }}

    body {{
        font-family: var(--font-family);
        color: var(--text-color);
    }}

    /* CSS Customizado */
    {theme.custom_css}
    """

    return HttpResponse(css, content_type='text/css')
```

### Template Base

O template base (`blog/templates/blog/base.html`) carrega o CSS dinâmico:

```html
<!-- CSS Dinâmico do Tema -->
<link rel="stylesheet" href="{% url 'blog:theme_css' %}">
```

### Contexto Global

O tema ativo é disponibilizado em todos os templates via `get_site_context()`:

```python
def get_site_context():
    return {
        'site_settings': SiteSettings.get_settings(),
        'menu_pages': Page.objects.filter(is_published=True, show_in_menu=True),
        'categories': Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0),
        'active_theme': Theme.get_active_theme(),
    }
```

## Variáveis CSS Disponíveis

Todas as propriedades do tema são expostas como variáveis CSS que podem ser usadas em templates customizados:

```css
:root {
    /* Cores principais */
    --primary-color: #3498db;
    --secondary-color: #2c3e50;
    --accent-color: #e74c3c;

    /* Cores de texto */
    --text-color: #333333;
    --heading-color: #2c3e50;
    --link-color: #3498db;
    --link-hover-color: #2980b9;

    /* Cores de fundo */
    --background-color: #ffffff;
    --secondary-bg-color: #f5f5f5;

    /* Header e Footer */
    --header-bg-color: #2c3e50;
    --header-text-color: #ffffff;
    --footer-bg-color: #34495e;
    --footer-text-color: #ffffff;

    /* Botões */
    --button-bg-color: #3498db;
    --button-text-color: #ffffff;
    --button-hover-bg-color: #2980b9;

    /* Tipografia */
    --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --heading-font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-size-base: 16px;
    --line-height: 1.6;

    /* Layout */
    --border-radius: 8px;
    --box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
```

## Usando Variáveis CSS em Templates Customizados

Você pode criar templates customizados que utilizam as variáveis do tema:

```html
<style>
.meu-elemento {
    background: var(--primary-color);
    color: var(--button-text-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
}

.meu-elemento:hover {
    background: var(--button-hover-bg-color);
}
</style>
```

## CSS Customizado por Tema

Cada tema pode ter CSS adicional que é injetado após as variáveis. Exemplo no tema Minimalist:

```css
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
```

## Boas Práticas

1. **Teste o Contraste**: Certifique-se de que as cores de texto têm contraste suficiente com os fundos
2. **Use Cores Hexadecimais**: Sempre use formato #RRGGBB para cores
3. **Font Stacks**: Sempre inclua fontes de fallback na família de fontes
4. **CSS Customizado**: Use com moderação, prefira as variáveis do tema
5. **Apenas Um Tema Ativo**: O sistema garante isso, mas não force múltiplos temas ativos
6. **Teste em Dispositivos**: Verifique a aparência em diferentes tamanhos de tela

## Troubleshooting

### O tema não está sendo aplicado

1. Verifique se há um tema marcado como ativo em **Blog → Temas**
2. Limpe o cache do navegador (Ctrl+Shift+R)
3. Verifique se a URL do CSS está carregando: `http://127.0.0.1:8000/theme.css`
4. Verifique logs do servidor para erros

### Cores não aparecem corretamente

1. Verifique se as cores estão no formato #RRGGBB (6 caracteres hexadecimais)
2. Certifique-se de salvar o tema após editar
3. Recarregue a página sem cache

### CSS customizado não funciona

1. Verifique a sintaxe CSS no campo "CSS Customizado"
2. Use `!important` se necessário para sobrescrever estilos
3. Verifique no navegador (DevTools) se o CSS foi injetado

### Tema padrão não carrega

1. Certifique-se de que pelo menos um tema está marcado como "Tema Padrão"
2. Execute novamente `python create_themes.py` se necessário

## Scripts Úteis

### Listar Todos os Temas

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from blog.models import Theme

for theme in Theme.objects.all():
    status = "ATIVO" if theme.is_active else "Inativo"
    default = " (PADRÃO)" if theme.is_default else ""
    print(f"{status}{default}: {theme.name} - {theme.description}")
```

### Resetar para Tema Padrão

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from blog.models import Theme

# Desativar todos
Theme.objects.update(is_active=False)

# Ativar o padrão
default_theme = Theme.objects.filter(is_default=True).first()
if default_theme:
    default_theme.is_active = True
    default_theme.save()
    print(f'Tema "{default_theme.name}" ativado!')
```

## Roadmap Futuro

Possíveis melhorias para o sistema de temas:

- [ ] Preview de temas antes de ativar
- [ ] Importar/Exportar temas (JSON)
- [ ] Tema por página/seção
- [ ] Dark mode automático baseado em horário
- [ ] Biblioteca de temas compartilhados
- [ ] Editor visual de temas
- [ ] Suporte a Google Fonts integration
- [ ] Modo de visualização (preview sem ativar)

## Conclusão

O sistema de temas do WordPy CMS oferece flexibilidade total para customizar a aparência do seu site sem tocar em código. Com 5 temas pré-definidos e capacidade de criar temas ilimitados, você tem controle completo sobre o design visual do seu site.

Para mais informações, consulte a documentação do projeto ou entre em contato com a equipe de desenvolvimento.
