# WordPy CMS - WordPress com Python e Django

Um sistema completo de gerenciamento de conteúdo (CMS) inspirado no WordPress, desenvolvido com Python e Django. Não foi realizada uma conversão do PHP para o Python.

## Características Principais

### Sistema de Conteúdo
- **Posts**: Sistema completo de blog com editor WYSIWYG (CKEditor)
- **Páginas**: Criação de páginas estáticas personalizadas
- **Página Home Customizável**: 🆕 Configure qualquer página como home do site
- **Seções Modulares**: 🆕 Crie páginas complexas com seções reutilizáveis (Hero, CTA, Features, etc.)
- **Categorias**: Organização de conteúdo por categorias
- **Tags**: Sistema de tags para melhor organização
- **Comentários**: Sistema de comentários com aprovação moderada

### Sistema de Temas 🆕
- **5 Temas Pré-definidos**: Light, Dark Mode, Professional Blue, Vibrant Colors, Minimalist
- **CSS Dinâmico**: Geração automática de CSS baseado no tema ativo
- **Customização Total**: Mais de 20 propriedades configuráveis (cores, fontes, layout)
- **Troca Instantânea**: Mude de tema sem reiniciar o servidor
- **CSS Customizado**: Adicione estilos personalizados por tema

### Gestão de Mídia
- **Upload de Arquivos**: Biblioteca de mídia completa
- **Imagens**: Suporte para imagens com metadados (alt text, legenda)
- **Tipos de Arquivo**: Suporte para imagens, vídeos, documentos

### SEO e Configurações
- **Meta Tags**: Título, descrição e keywords personalizáveis
- **URLs Amigáveis**: Slugs automáticos baseados no título
- **Google Analytics**: Integração fácil com GA
- **Redes Sociais**: Links para Facebook, Twitter, Instagram, LinkedIn

### Painel Administrativo
- **Interface Intuitiva**: Admin do Django customizado
- **Filtros Avançados**: Busca e filtros em todas as seções
- **Estatísticas**: Contador de visualizações e outras métricas
- **Bulk Actions**: Ações em lote para comentários

## Tecnologias Utilizadas

- Python 3.12
- Django 5.2
- CKEditor (Editor WYSIWYG)
- Django Taggit (Sistema de Tags)
- Pillow (Manipulação de Imagens)
- SQLite (Banco de Dados)

## Instalação e Configuração

### 1. Clonar/Baixar o Projeto

```bash
# Se você já tem os arquivos, navegue até a pasta
cd wordpy
```

### 2. Ambiente Virtual (Já Criado)

O ambiente virtual já está configurado. Para ativá-lo:

**No Windows:**
```bash
venv\Scripts\activate
```

**No Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Dependências (Já Instaladas)

As seguintes dependências já estão instaladas:
- django
- pillow
- django-ckeditor
- django-taggit

### 4. Banco de Dados (Já Configurado)

As migrações já foram executadas e o banco de dados está pronto.

### 5. Coletar Arquivos Estáticos (IMPORTANTE)

Antes de iniciar o servidor pela primeira vez, colete os arquivos estáticos do CKEditor:

```bash
python manage.py collectstatic --no-input
```

Isso copiará todos os arquivos CSS, JavaScript e imagens necessários.

### 6. Testar Configuração (Recomendado)

Execute o script de teste para verificar se tudo está configurado:

```bash
python test_server.py
```

### 7. Iniciar o Servidor

**Opção 1 - Script Automático (Windows):**
```bash
start_server.bat
```

**Opção 2 - Comando Manual:**
```bash
python manage.py runserver
```

O servidor estará disponível em: **http://127.0.0.1:8000/**

⚠️ **Problemas ao iniciar?** Veja o arquivo [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Acesso ao Sistema

### Painel Administrativo

URL: **http://127.0.0.1:8000/admin/**

Credenciais padrão:
- **Username:** admin
- **Password:** admin123

⚠️ **IMPORTANTE:** Altere a senha padrão em produção!

### Frontend

URL: **http://127.0.0.1:8000/**

O site já vem com dados de exemplo:
- 3 posts publicados
- 4 categorias
- 2 páginas (Sobre e Contato)

## Estrutura do Projeto

```
wordpy/
├── blog/                    # App principal do CMS
│   ├── models.py           # Models (Post, Category, Page, etc)
│   ├── views.py            # Views do frontend
│   ├── admin.py            # Configuração do admin
│   ├── urls.py             # URLs do blog
│   └── templates/          # Templates HTML
│       └── blog/
│           ├── base.html
│           ├── post_list.html
│           ├── post_detail.html
│           ├── category_posts.html
│           ├── tag_posts.html
│           ├── page_detail.html
│           └── search.html
├── wordpy_cms/             # Configurações do projeto
│   ├── settings.py         # Settings do Django
│   └── urls.py             # URLs principais
├── media/                  # Arquivos de mídia (uploads)
├── staticfiles/            # Arquivos estáticos
├── manage.py               # Gerenciador Django
├── db.sqlite3             # Banco de dados SQLite
└── README.md              # Este arquivo
```

## Guia de Uso

### Criar um Novo Post

1. Acesse o admin: http://127.0.0.1:8000/admin/
2. Vá em "Posts" > "Adicionar Post"
3. Preencha:
   - Título
   - Conteúdo (use o editor visual)
   - Categoria
   - Tags
   - Imagem destacada (opcional)
4. Configure:
   - Status: "Publicado" para publicar imediatamente
   - Data de publicação
   - Permitir comentários
5. Configure SEO (opcional):
   - Meta título
   - Meta descrição
   - Meta keywords
6. Salve

### Criar uma Página

1. Acesse "Páginas" > "Adicionar Página"
2. Preencha título e conteúdo
3. Configure:
   - "Mostrar no Menu" para aparecer no menu principal
   - "Ordem no Menu" para ordenar as páginas
4. Salve

### Gerenciar Comentários

1. Acesse "Comentários" no admin
2. Visualize todos os comentários
3. Use as ações em lote:
   - Aprovar comentários selecionados
   - Desaprovar comentários selecionados
4. Filtre por aprovados/não aprovados

### Configurar o Site

1. Acesse "Configurações do Site" no admin
2. Configure:
   - Nome do site
   - Descrição
   - Logo e favicon
   - Links de redes sociais
   - Google Analytics ID
   - Configurações de comentários
   - Posts por página
3. Salve

### Upload de Mídia

1. Acesse "Mídias" > "Adicionar Mídia"
2. Faça upload do arquivo
3. Adicione:
   - Título
   - Texto alternativo (para imagens)
   - Legenda
4. Salve

### Criar Páginas com Seções 🆕

O sistema de seções permite criar páginas modulares e complexas:

1. **Criar uma Seção:**
   - Acesse "Seções" > "Adicionar Seção"
   - Escolha o tipo (Hero, Texto, CTA, Features, etc.)
   - Preencha título, conteúdo, imagem, botão
   - Configure cor de fundo e estilo
   - Salve

2. **Adicionar Seções a uma Página:**
   - Edite ou crie uma página
   - Role até "Seções da Página" (no final)
   - Adicione seções existentes
   - Defina a ordem de exibição
   - Marque como ativa
   - Salve

3. **Tipos de Seções Disponíveis:**
   - **Hero/Banner:** Cabeçalho principal com call-to-action
   - **Texto:** Conteúdo textual simples
   - **Texto com Imagem:** Layout com texto e imagem lado a lado
   - **Call to Action:** Seções de conversão destacadas
   - **Features:** Apresentação de recursos e benefícios
   - **Carrossel de Banners:** 🆕 Slides rotativos com navegação automática
   - **HTML Customizado:** Seções totalmente personalizadas

4. **Ver Exemplo:**
   ```bash
   python create_sample_sections.py
   ```
   Isso cria seções de exemplo na página "Sobre"

📖 **Documentação Completa:** Veja [SISTEMA_SECOES.md](SISTEMA_SECOES.md) para detalhes

### Criar Carrossel de Banners 🆕

Adicione um carrossel rotativo de banners às suas páginas:

1. **Criar Automaticamente:**
   ```bash
   python create_banner_carousel.py
   ```
   Isso cria a seção "Carrossel Principal" e adiciona à home

2. **Funcionalidades:**
   - ✅ Rolagem automática (5 segundos)
   - ✅ Navegação por setas
   - ✅ Indicadores (dots) clicáveis
   - ✅ Pausa ao interagir
   - ✅ 100% responsivo
   - ✅ JavaScript puro (sem jQuery)

3. **Customizar:**
   - Admin → Seções → Edite "Carrossel Principal"
   - Configure título, imagem, conteúdo e botão
   - Edite o template para adicionar mais slides

📖 **Documentação Completa:** Veja [CARROSSEL_BANNERS.md](CARROSSEL_BANNERS.md) para detalhes

### Configurar Página Home Customizada 🆕

Transforme qualquer página em uma landing page profissional:

1. **Criar Página Home Automática:**
   ```bash
   python create_home_page.py
   ```
   Isso cria uma home completa com 4 seções profissionais

2. **Ou Configurar Manualmente:**
   - Crie uma página com seções
   - Acesse "Configurações do Site" no admin
   - Em "Página Inicial", selecione a página criada
   - Salve

3. **Resultado:**
   - `/` - Sua página customizada (home)
   - `/blog/` - Lista de posts do blog
   - Menu atualizado com "Início" e "Blog"

4. **Desativar:**
   - Em "Configurações do Site", deixe "Página Inicial" vazio
   - A home voltará a mostrar lista de posts

📖 **Documentação Completa:** Veja [PAGINA_HOME.md](PAGINA_HOME.md) para detalhes

### Gerenciar Temas Visuais 🆕

O sistema de temas permite customizar completamente a aparência do site:

1. **Trocar Tema (Método Mais Fácil):**
   - Acesse "Configurações do Site" no admin
   - Role até "Configurações de Exibição"
   - No campo "Tema Ativo", selecione o tema desejado
   - Clique em "Salvar"
   - O tema será aplicado instantaneamente!

2. **Ou via Admin de Temas:**
   - Acesse "Temas" no admin
   - Selecione o tema desejado (checkbox)
   - No dropdown "Ação", escolha "Ativar tema selecionado"
   - Clique em "Ir"

3. **Criar Tema Customizado:**
   - Acesse "Temas" > "Adicionar Tema"
   - Preencha:
     - Nome e descrição
     - Cores (primária, secundária, destaque, textos, fundos)
     - Tipografia (família de fontes, tamanhos)
     - Layout (border-radius, box-shadow)
     - CSS customizado (opcional)
   - Marque "Tema Ativo" para aplicar imediatamente
   - Salve

3. **Temas Disponíveis:**
   - **WordPy Light (Padrão)**: Tema claro e moderno
   - **Dark Mode**: Tema escuro elegante
   - **Professional Blue**: Tons de azul corporativo
   - **Vibrant Colors**: Colorido e criativo
   - **Minimalist**: Clean e focado no conteúdo

4. **Popular Temas:**
   ```bash
   python create_themes.py
   ```
   Isso cria os 5 temas pré-definidos no banco de dados

📖 **Documentação Completa:** Veja [SISTEMA_TEMAS.md](SISTEMA_TEMAS.md) para detalhes

### Usar Template Tags Customizados 🆕

O WordPy CMS oferece template tags úteis para exibir conteúdo dinâmico:

**Template Tags Disponíveis:**

1. **get_recent_posts** - Busca os N posts mais recentes
   ```django
   {% load blog_tags %}
   {% get_recent_posts 5 as recent %}
   ```

2. **get_popular_posts** - Busca os N posts mais populares
   ```django
   {% get_popular_posts 5 as popular %}
   ```

3. **get_categories_with_count** - Categorias com contagem
   ```django
   {% get_categories_with_count as categories %}
   ```

4. **truncate_words** - Filtro para truncar texto
   ```django
   {{ post.content|striptags|truncate_words:20 }}
   ```

**Exemplo de Uso:**
```django
{% load blog_tags %}

{% get_recent_posts 3 as posts %}
{% for post in posts %}
    <h3>{{ post.title }}</h3>
    <p>{{ post.excerpt|truncate_words:30 }}</p>
{% endfor %}
```

📖 **Documentação Completa:** Veja [TEMPLATE_TAGS.md](TEMPLATE_TAGS.md) para exemplos detalhados

## Models Disponíveis

### Post
- Título, slug, conteúdo
- Autor, categoria, tags
- Status (rascunho, publicado, agendado)
- Imagem destacada
- Campos SEO
- Contador de visualizações
- Controle de comentários

### Category
- Nome, slug, descrição
- Contador automático de posts

### Page
- Título, slug, conteúdo
- Controle de publicação
- Opção de menu
- Suporte a seções modulares 🆕
- Campos SEO

### Section 🆕
- 10 tipos de seções (Hero, Texto, CTA, Features, Carrossel, etc.)
- Título, subtítulo, conteúdo rico
- Imagem com posicionamento
- Botão call-to-action
- Cores de fundo personalizáveis
- Carrossel de banners com rolagem automática 🆕
- HTML customizado
- Reutilizável em múltiplas páginas

### PageSection 🆕
- Vincula seções a páginas
- Controle de ordem de exibição
- Ativar/desativar seções
- Permite múltiplas seções por página

### Comment
- Suporte a comentários aninhados (respostas)
- Sistema de aprovação
- Comentários de usuários autenticados ou anônimos

### Media
- Upload de arquivos
- Metadados (alt text, legenda)
- Detecção automática de tipo
- Informações de tamanho

### SiteSettings
- Configurações globais do site
- Singleton (apenas uma instância)
- Configurações de SEO, redes sociais, comentários
- Página inicial customizável 🆕

### Theme 🆕
- Temas visuais do site
- Mais de 20 propriedades configuráveis
- Cores (primária, secundária, destaque, textos, fundos, header, footer, botões)
- Tipografia (família de fontes, tamanhos, line-height)
- Layout (border-radius, box-shadow)
- CSS customizado adicional
- Sistema de ativação (apenas um tema ativo)
- Tema padrão como fallback

## URLs Disponíveis

- `/` - Página inicial (home customizada ou lista de posts)
- `/blog/` - Lista de posts do blog 🆕
- `/post/<slug>/` - Detalhe do post
- `/category/<slug>/` - Posts por categoria
- `/tag/<slug>/` - Posts por tag
- `/page/<slug>/` - Página estática
- `/search/?q=termo` - Busca de posts
- `/theme.css` - CSS dinâmico do tema ativo 🆕
- `/admin/` - Painel administrativo
- `/ckeditor/` - Upload de imagens do CKEditor

## Funcionalidades Implementadas

✅ Sistema completo de posts e páginas
✅ 🆕 Página home customizável
✅ 🆕 Seções modulares para páginas (Page Builder)
✅ 🆕 10 tipos de seções reutilizáveis
✅ 🆕 Carrossel de banners com rolagem automática
✅ 🆕 Sistema de temas com 5 temas pré-definidos
✅ 🆕 CSS dinâmico e customizável
✅ 🆕 Posts recentes na home em cards visuais
✅ 🆕 Template tags customizados
✅ Editor WYSIWYG (CKEditor)
✅ Sistema de categorias e tags
✅ Comentários com aprovação
✅ Upload e gestão de mídia
✅ SEO otimizado
✅ Painel administrativo poderoso
✅ Busca de conteúdo
✅ Sistema de visualizações
✅ Configurações globais
✅ Templates responsivos
✅ Integração com Google Analytics

## Comandos Úteis

### Criar novo superusuário
```bash
python manage.py createsuperuser
```

### Executar testes
```bash
python manage.py test
```

### Coletar arquivos estáticos
```bash
python manage.py collectstatic
```

### Criar seções de exemplo 🆕
```bash
python create_sample_sections.py
```
Isso cria 4 seções de exemplo e adiciona à página "Sobre"

### Criar página home customizada 🆕
```bash
python create_home_page.py
```
Isso cria uma página home completa com seções e configura como página inicial

### Criar temas pré-definidos 🆕
```bash
python create_themes.py
```
Isso cria 5 temas profissionais (Light, Dark, Professional Blue, Vibrant Colors, Minimalist)

### Criar carrossel de banners 🆕
```bash
python create_banner_carousel.py
```
Isso cria um carrossel rotativo de banners e adiciona à página home

### Fazer backup do banco de dados
```bash
# O arquivo db.sqlite3 contém todos os dados
# Faça uma cópia de segurança regularmente
```

## Próximos Passos

Para melhorarmos ainda mais o CMS, vamos considerar adicionar:

- Sistema de usuários frontend (registro, login, perfis)
- Sistema de widgets/sidebars customizáveis
- Sistema de plugins
- Multi-idioma
- API REST para integração
- Sistema de newsletter
- Estatísticas avançadas
- Cache para melhor performance
- Suporte a múltiplos autores
- Preview de temas antes de ativar
- Biblioteca de temas compartilhados

## Segurança

⚠️ **Para uso em produção:**

1. Altere a `SECRET_KEY` no settings.py
2. Configure `DEBUG = False`
3. Adicione domínios em `ALLOWED_HOSTS`
4. Use um banco de dados robusto (PostgreSQL)
5. Configure HTTPS
6. Use variáveis de ambiente para senhas
7. Implemente backup regular
8. Mantenha as dependências atualizadas

## Suporte

Para questões e melhorias, abra uma issue no repositório.

## Licença

Este projeto é de código aberto e está disponível sob a licença GPL-3.0.

---

**Desenvolvido com Python e Django** 🐍 ❤️
