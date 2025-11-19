# Changelog - WordPy CMS

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.2.3] - 2025-11-18

### 🆕 Adicionado

#### Carrossel de Banners (Banner Carousel)
- **Novo Tipo de Seção**: "Carrossel de Banners" para páginas
- **Rolagem Automática**: Troca de banners a cada 5 segundos
- **Navegação Manual**: Setas para avançar/voltar
- **Indicadores (Dots)**: Navegação por pontos
- **Responsivo**: Adapta-se a diferentes tamanhos de tela
- **Pausar ao Interagir**: Para a rolagem quando usuário interage

**Funcionalidades:**
- 3 slides com gradientes coloridos de exemplo
- Overlay com conteúdo (título, subtítulo, texto, botão)
- Transições suaves (fade in/out)
- Controles estilizados com hover
- JavaScript puro (sem dependências)
- Suporte a múltiplos carrosséis na mesma página

**Customização:**
- Título, subtítulo e conteúdo configuráveis
- Imagem de fundo personalizável
- Botão call-to-action com link
- Altura responsiva (500px desktop, 400px mobile)

**Scripts:**
- `create_banner_carousel.py`: Cria seção de carrossel automaticamente

### 🔧 Técnico
- Template `banner_carousel.html` criado
- JavaScript com sistema de gerenciamento de múltiplos carrosséis
- CSS inline para melhor portabilidade
- Auto-inicialização via DOMContentLoaded
- Sistema de pause/resume no autoplay

---

## [1.2.2] - 2025-11-18

### 🆕 Adicionado

#### Seção de Posts Recentes na Página Inicial
- **Cards de Posts na Home**: Exibição dos 3 últimos posts em cards visuais
- **Template Tags Customizados**: Criado `blog_tags.py` com template tags úteis
- **Design Responsivo**: Layout em grid que se adapta a diferentes telas
- **Informações Completas**: Cada card mostra:
  - Imagem destacada (ou gradiente padrão)
  - Categoria com link
  - Título do post
  - Resumo (primeiras 20 palavras)
  - Data de publicação
  - Autor
  - Contador de visualizações
  - Link "Ler mais"

**Template Tags Disponíveis:**
- `get_recent_posts`: Retorna os N posts mais recentes
- `get_popular_posts`: Retorna os N posts mais populares
- `get_categories_with_count`: Categorias com contagem de posts
- `truncate_words`: Filtro para truncar texto

**Visual:**
- Cards com hover animado (elevação e zoom na imagem)
- Gradiente colorido para posts sem imagem
- Grid responsivo (3 colunas desktop, 1 coluna mobile)
- Botão "Ver Todas as Postagens" centralizado

### ✨ Melhorado
- Template `home_page.html` com seção de blog aprimorada
- Design mais profissional e moderno
- Melhor experiência do usuário na home

### 🔧 Técnico
- Criada pasta `blog/templatetags/`
- Arquivo `blog_tags.py` com template tags reutilizáveis
- Query otimizada com `select_related` e `prefetch_related`
- Script de teste `test_recent_posts.py`

---

## [1.2.1] - 2025-11-18

### ✨ Melhorado

#### Seleção de Temas Via Configurações do Site
- **Campo `active_theme` em SiteSettings**: Selecione o tema diretamente nas Configurações do Site
- **Hierarquia de Prioridade**: SiteSettings > is_active > is_default
- **Admin Atualizado**: Campo "Tema Ativo" adicionado em "Configurações de Exibição"
- **Método `Theme.get_active_theme()` Aprimorado**: Verifica primeiro o SiteSettings

**Como usar:**
1. Acesse "Configurações do Site" no admin
2. Selecione o tema no dropdown "Tema Ativo"
3. Salve - pronto!

**Benefícios:**
- ✅ Mais intuitivo e centralizado
- ✅ Não precisa navegar até o admin de temas
- ✅ Gerenciamento simplificado

### 🔧 Técnico
- Migration `0005_sitesettings_active_theme.py`: Adiciona ForeignKey para Theme
- Atualização de `SiteSettingsAdmin` com novo campo
- Lógica de prioridade implementada em `Theme.get_active_theme()`

### 📝 Documentação
- SISTEMA_TEMAS.md atualizado com novo método
- README.md atualizado com instruções simplificadas
- Seção "Prioridade na Seleção de Temas" adicionada

---

## [1.2.0] - 2025-11-18

### 🆕 Adicionado

#### Sistema de Temas Dinâmicos
- **Novo Model `Theme`**: Temas visuais totalmente customizáveis
- **5 Temas Pré-definidos:**
  - WordPy Light (Padrão): Tema claro e moderno
  - Dark Mode: Tema escuro elegante
  - Professional Blue: Tons de azul corporativo
  - Vibrant Colors: Colorido e criativo
  - Minimalist: Clean e focado no conteúdo

#### Propriedades de Temas (20+ configurações)
- **Cores Principais**: Primária, secundária, destaque
- **Cores de Texto**: Texto, títulos, links, hover
- **Cores de Fundo**: Background, secundário
- **Header e Footer**: Cores de fundo e texto
- **Botões**: Background, texto, hover
- **Tipografia**: Família de fontes, tamanhos, line-height
- **Layout**: Border-radius, box-shadow
- **CSS Customizado**: CSS adicional por tema

#### Sistema de CSS Dinâmico
- **View `theme_css_view`**: Gera CSS em tempo real baseado no tema ativo
- **URL `/theme.css`**: Endpoint para CSS dinâmico
- **Variáveis CSS**: Todas as propriedades expostas como CSS custom properties
- **Template Tag**: Tema ativo disponível em `{{ active_theme }}`

#### Admin de Temas
- **ThemeAdmin**: Interface administrativa completa
- **Color Preview**: Visualização de cores principais
- **Ação em Lote**: "Ativar tema selecionado"
- **Fieldsets Organizados**: Cores, tipografia, layout
- **CSS Customizado**: Editor para CSS adicional

#### Scripts e Ferramentas
- `create_themes.py`: Cria os 5 temas pré-definidos automaticamente

#### Documentação
- `SISTEMA_TEMAS.md`: Guia completo do sistema de temas (estrutura técnica, customização, troubleshooting)
- Atualização do README com seção de temas
- Exemplos de código para criar temas programaticamente

### ✨ Melhorado
- Template `base.html` agora carrega CSS dinâmico do tema
- Function `get_site_context()` inclui tema ativo
- Sistema garante apenas um tema ativo por vez
- Fallback automático para tema padrão se nenhum estiver ativo
- Templates agora usam variáveis CSS para estilização

### 🔧 Técnico
- Migration `0004_theme.py`: Criação do model Theme
- CSS variables (:root) para todas as propriedades do tema
- HttpResponse com content_type='text/css' para CSS dinâmico
- Método `Theme.get_active_theme()` para recuperar tema ativo
- Sistema de ativação com is_active e is_default flags

### 🐛 Corrigido
- N/A nesta versão

---

## [1.1.0] - 2025-11-18

### 🆕 Adicionado

#### Página Home Customizável
- **Campo `home_page` em SiteSettings**: Configure qualquer página como home
- **Nova View `HomeView`**: Renderiza página customizada ou lista de posts
- **Template `home_page.html`**: Layout específico para página home
- **URL `/blog/`**: Lista de posts sempre disponível (home agora é `/`)
- **Script `create_home_page.py`**: Cria página home completa automaticamente
- **Documentação `PAGINA_HOME.md`**: Guia completo da funcionalidade

#### Sistema de Seções Modulares
- **Novo Model `Section`**: Seções reutilizáveis para páginas
- **Novo Model `PageSection`**: Relacionamento entre páginas e seções com controle de ordem
- **9 Tipos de Seções:**
  - Hero/Banner: Cabeçalhos principais com call-to-action
  - Texto: Seções de conteúdo textual
  - Texto com Imagem: Layout de duas colunas
  - Call to Action (CTA): Seções de conversão
  - Features: Apresentação de recursos
  - Cards: Grid de cartões (template genérico)
  - Testimonials: Depoimentos (template genérico)
  - Galeria de Imagens: Grid de imagens (template genérico)
  - HTML Customizado: Liberdade total

#### Templates de Seções
- `blog/templates/blog/sections/hero.html`
- `blog/templates/blog/sections/text.html`
- `blog/templates/blog/sections/text_image.html`
- `blog/templates/blog/sections/cta.html`
- `blog/templates/blog/sections/features.html`
- `blog/templates/blog/sections/html.html`
- `blog/templates/blog/sections/section_renderer.html`

#### Admin Melhorado
- Inline admin para adicionar seções diretamente em páginas
- Autocomplete para seções
- Preview de imagens no admin de seções
- Contador de seções em páginas

#### Scripts e Ferramentas
- `create_sample_sections.py`: Cria seções de exemplo

#### Documentação
- `SISTEMA_SECOES.md`: Guia completo do sistema de seções
- Atualização do README com informações sobre seções

### ✨ Melhorado
- Template `page_detail.html` agora renderiza seções modulares
- View `PageDetailView` carrega seções relacionadas
- Admin de páginas com fieldset descritivo para conteúdo
- Menu de navegação agora tem "Início" e "Blog" separados
- Template `base.html` atualizado com novos links
- SiteSettings admin agora inclui configuração de página home

### 🐛 Corrigido
- N/A nesta versão

---

## [1.0.0] - 2025-11-18

### 🎉 Lançamento Inicial

#### Sistema de Conteúdo
- Sistema completo de posts com editor WYSIWYG (CKEditor)
- Páginas estáticas personalizáveis
- Sistema de categorias e tags (django-taggit)
- Comentários com aprovação e suporte a respostas
- Contador de visualizações

#### Gestão de Mídia
- Upload de arquivos
- Biblioteca de mídia completa
- Metadados (alt text, legenda)
- Preview de imagens
- Detecção automática de tipo de arquivo

#### SEO
- Meta tags personalizáveis (título, descrição, keywords)
- URLs amigáveis com slugs automáticos
- Integração com Google Analytics
- Sitemap (preparado)

#### Painel Administrativo
- Admin do Django customizado
- Filtros avançados e busca
- Ações em lote para comentários
- Configurações globais do site (SiteSettings)
- Fieldsets organizados
- Readonly fields apropriados

#### Templates e Frontend
- Base template responsivo
- Lista de posts com paginação
- Detalhe de post com comentários
- Páginas por categoria e tag
- Busca de conteúdo
- Menu dinâmico baseado em páginas
- Footer com redes sociais

#### Segurança
- CSRF protection
- SQL injection protection (Django ORM)
- XSS protection (template auto-escape)
- Validação de formulários
- Aprovação de comentários

#### Configuração e Deploy
- Ambiente virtual configurado
- Requirements.txt
- Scripts de inicialização
- Dados de exemplo
- Sistema de migrações

#### Documentação
- README completo
- TROUBLESHOOTING.md
- CORRECOES_CKEDITOR.md
- Comentários inline no código

---

## Tipos de Mudanças

- 🆕 **Adicionado**: Para novas funcionalidades
- ✨ **Melhorado**: Para mudanças em funcionalidades existentes
- 🐛 **Corrigido**: Para correções de bugs
- 🔒 **Segurança**: Para correções de vulnerabilidades
- ⚠️ **Deprecated**: Para funcionalidades que serão removidas
- 🗑️ **Removido**: Para funcionalidades removidas
- 📝 **Documentação**: Para mudanças apenas na documentação

---

**Legenda de Versões:**
- Versão MAJOR.MINOR.PATCH
- MAJOR: Mudanças incompatíveis com versões anteriores
- MINOR: Novas funcionalidades compatíveis
- PATCH: Correções de bugs compatíveis
