from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.contrib import messages
from django.http import HttpResponse
from .models import Post, Category, Page, Comment, SiteSettings, Theme
from taggit.models import Tag


def get_site_context():
    """Retorna contexto global do site"""
    return {
        'site_settings': SiteSettings.get_settings(),
        'menu_pages': Page.objects.filter(is_published=True, show_in_menu=True),
        'categories': Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0),
        'active_theme': Theme.get_active_theme(),
    }


class HomeView(TemplateView):
    """View para página inicial - pode ser uma página customizada ou lista de posts"""

    def get(self, request, *args, **kwargs):
        site_settings = SiteSettings.get_settings()

        # Se há uma página configurada como home, renderiza ela
        if site_settings.home_page and site_settings.home_page.is_published:
            return self.render_custom_home(site_settings.home_page)

        # Caso contrário, renderiza lista de posts
        return self.render_post_list()

    def render_custom_home(self, page):
        """Renderiza página customizada como home"""
        from ecommerce.models import Product
        context = get_site_context()
        context['page'] = page
        context['page_sections'] = page.page_sections.filter(is_active=True).select_related('section').order_by('order')
        context['is_home'] = True
        # Adicionar produtos para seções de produtos
        context['products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:15]
        return render(self.request, 'blog/home_page.html', context)

    def render_post_list(self):
        """Renderiza lista de posts como home (fallback)"""
        posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags').order_by('-published_at')[:10]
        context = get_site_context()
        context['posts'] = posts
        context['is_home'] = True
        return render(self.request, 'blog/post_list.html', context)


class PostListView(ListView):
    """Lista de posts publicados"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
        return queryset.order_by('-published_at')

    def get_paginate_by(self, queryset):
        return SiteSettings.get_settings().posts_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_site_context())
        return context


class PostDetailView(DetailView):
    """Detalhes de um post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')

    def get_object(self):
        obj = super().get_object()
        # Incrementar visualizações
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_site_context())

        # Comentários aprovados
        post = self.get_object()
        context['comments'] = post.comments.filter(is_approved=True, parent=None).select_related('author')

        # Posts relacionados
        context['related_posts'] = Post.objects.filter(
            status='published',
            category=post.category
        ).exclude(pk=post.pk)[:3]

        return context

    def post(self, request, *args, **kwargs):
        """Processar comentário"""
        post = self.get_object()

        if not post.allow_comments:
            messages.error(request, 'Comentários não permitidos neste post.')
            return redirect(post.get_absolute_url())

        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        if not content:
            messages.error(request, 'O comentário não pode estar vazio.')
            return redirect(post.get_absolute_url())

        comment = Comment(
            post=post,
            content=content
        )

        if request.user.is_authenticated:
            comment.author = request.user
        else:
            comment.author_name = request.POST.get('author_name', '')
            comment.author_email = request.POST.get('author_email', '')

        if parent_id:
            comment.parent_id = parent_id

        # Auto-aprovar comentários de usuários autenticados
        if request.user.is_authenticated:
            comment.is_approved = True
        else:
            site_settings = SiteSettings.get_settings()
            comment.is_approved = not site_settings.comments_require_approval

        comment.save()

        if comment.is_approved:
            messages.success(request, 'Comentário adicionado com sucesso!')
        else:
            messages.info(request, 'Seu comentário está aguardando aprovação.')

        return redirect(post.get_absolute_url())


class CategoryPostListView(ListView):
    """Lista de posts por categoria"""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            category=self.category
        ).select_related('author', 'category').order_by('-published_at')

    def get_paginate_by(self, queryset):
        return SiteSettings.get_settings().posts_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_site_context())
        context['category'] = self.category
        return context


class TagPostListView(ListView):
    """Lista de posts por tag"""
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            tags__in=[self.tag]
        ).select_related('author', 'category').order_by('-published_at')

    def get_paginate_by(self, queryset):
        return SiteSettings.get_settings().posts_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_site_context())
        context['tag'] = self.tag
        return context


class PageDetailView(DetailView):
    """Detalhes de uma página"""
    model = Page
    template_name = 'blog/page_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return Page.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        from ecommerce.models import Product
        context = super().get_context_data(**kwargs)
        context.update(get_site_context())

        # Adicionar seções da página
        page = self.get_object()
        context['page_sections'] = page.page_sections.filter(is_active=True).select_related('section').order_by('order')

        # Adicionar produtos para seções de produtos
        context['products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:15]

        return context


class SearchView(ListView):
    """Busca de posts"""
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query),
                status='published'
            ).select_related('author', 'category').order_by('-published_at')
        return Post.objects.none()

    def get_paginate_by(self, queryset):
        return SiteSettings.get_settings().posts_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_site_context())
        context['query'] = self.request.GET.get('q', '')
        return context


def about_view(request):
    """Página sobre - exemplo de view funcional"""
    context = get_site_context()
    return render(request, 'blog/about.html', context)


def theme_css_view(request):
    """Gera CSS dinâmico baseado no tema ativo"""
    theme = Theme.get_active_theme()

    if not theme:
        # Retorna CSS vazio se não há tema
        return HttpResponse('/* Nenhum tema configurado */', content_type='text/css')

    # Gerar CSS com as variáveis do tema
    css = f"""
/* WordPy CMS - CSS Dinâmico do Tema: {theme.name} */

:root {{
    /* Cores principais */
    --primary-color: {theme.primary_color};
    --secondary-color: {theme.secondary_color};
    --accent-color: {theme.accent_color};

    /* Cores de texto */
    --text-color: {theme.text_color};
    --heading-color: {theme.heading_color};
    --link-color: {theme.link_color};
    --link-hover-color: {theme.link_hover_color};

    /* Cores de fundo */
    --background-color: {theme.background_color};
    --secondary-bg-color: {theme.secondary_bg_color};

    /* Header e Footer */
    --header-bg-color: {theme.header_bg_color};
    --header-text-color: {theme.header_text_color};
    --footer-bg-color: {theme.footer_bg_color};
    --footer-text-color: {theme.footer_text_color};

    /* Botões */
    --button-bg-color: {theme.button_bg_color};
    --button-text-color: {theme.button_text_color};
    --button-hover-bg-color: {theme.button_hover_bg_color};

    /* Tipografia */
    --font-family: {theme.font_family};
    --heading-font-family: {theme.heading_font_family or theme.font_family};
    --font-size-base: {theme.font_size_base};
    --line-height: {theme.line_height};

    /* Espaçamento e Layout */
    --border-radius: {theme.border_radius};
    --box-shadow: {theme.box_shadow};
}}

/* Aplicar variáveis do tema */
body {{
    font-family: var(--font-family);
    font-size: var(--font-size-base);
    line-height: var(--line-height);
    color: var(--text-color);
    background: var(--background-color);
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: var(--heading-font-family);
    color: var(--heading-color);
}}

a {{
    color: var(--link-color);
}}

a:hover {{
    color: var(--link-hover-color);
}}

header {{
    background: var(--header-bg-color);
    color: var(--header-text-color);
}}

header a {{
    color: var(--header-text-color);
}}

footer {{
    background: var(--footer-bg-color);
    color: var(--footer-text-color);
}}

footer a {{
    color: var(--footer-text-color);
}}

button, .button, .btn {{
    background: var(--button-bg-color);
    color: var(--button-text-color);
    border-radius: var(--border-radius);
}}

button:hover, .button:hover, .btn:hover {{
    background: var(--button-hover-bg-color);
}}

.sidebar, article, .section {{
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
}}

.section-hero,
.section-text,
.section-text-image,
.section-cta,
.section-features {{
    /* Seções podem usar as variáveis de cores */
}}

/* CSS Customizado do Tema */
{theme.custom_css}
"""

    return HttpResponse(css, content_type='text/css')
