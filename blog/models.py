from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Category(models.Model):
    """Categoria para organizar posts"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Descrição")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})


class Post(models.Model):
    """Model principal para posts do blog"""
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('scheduled', 'Agendado'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Autor")
    content = RichTextUploadingField(verbose_name="Conteúdo")
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="Resumo")
    featured_image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True, null=True, verbose_name="Imagem Destacada")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name="Categoria")
    tags = TaggableManager(blank=True, verbose_name="Tags")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Status")
    allow_comments = models.BooleanField(default=True, verbose_name="Permitir Comentários")

    views = models.IntegerField(default=0, verbose_name="Visualizações")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Publicado em")

    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True, verbose_name="Meta Título")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta Descrição")
    meta_keywords = models.CharField(max_length=200, blank=True, verbose_name="Meta Keywords")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.content:
            self.excerpt = self.content[:200]
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.excerpt
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """Comentários em posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Autor")
    author_name = models.CharField(max_length=100, blank=True, verbose_name="Nome")
    author_email = models.EmailField(blank=True, verbose_name="Email")
    content = models.TextField(verbose_name="Comentário")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name="Responder a")

    is_approved = models.BooleanField(default=False, verbose_name="Aprovado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['created_at']

    def __str__(self):
        return f'Comentário de {self.get_author_name()} em {self.post.title}'

    def get_author_name(self):
        if self.author:
            return self.author.get_full_name() or self.author.username
        return self.author_name


class Page(models.Model):
    """Páginas estáticas do site"""
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = RichTextUploadingField(verbose_name="Conteúdo")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages', verbose_name="Autor")

    featured_image = models.ImageField(upload_to='pages/', blank=True, null=True, verbose_name="Imagem Destacada")

    is_published = models.BooleanField(default=True, verbose_name="Publicado")
    show_in_menu = models.BooleanField(default=False, verbose_name="Mostrar no Menu")
    menu_order = models.IntegerField(default=0, verbose_name="Ordem no Menu")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True, verbose_name="Meta Título")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta Descrição")

    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"
        ordering = ['menu_order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:page_detail', kwargs={'slug': self.slug})


class Section(models.Model):
    """Seções reutilizáveis para páginas"""
    SECTION_TYPES = [
        ('hero', 'Hero/Banner'),
        ('text', 'Texto'),
        ('text_image', 'Texto com Imagem'),
        ('image_gallery', 'Galeria de Imagens'),
        ('cards', 'Cards/Destaques'),
        ('testimonials', 'Depoimentos'),
        ('cta', 'Call to Action'),
        ('features', 'Recursos/Features'),
        ('banner_carousel', 'Carrossel de Banners'),
        ('html', 'HTML Customizado'),
    ]

    BACKGROUND_COLORS = [
        ('white', 'Branco'),
        ('light', 'Cinza Claro'),
        ('dark', 'Escuro'),
        ('primary', 'Cor Primária'),
        ('secondary', 'Cor Secundária'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nome da Seção")
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, default='text', verbose_name="Tipo de Seção")

    # Conteúdo
    title = models.CharField(max_length=200, blank=True, verbose_name="Título")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Subtítulo")
    content = RichTextUploadingField(blank=True, verbose_name="Conteúdo")

    # Imagens
    image = models.ImageField(upload_to='sections/', blank=True, null=True, verbose_name="Imagem")
    image_position = models.CharField(max_length=10, choices=[('left', 'Esquerda'), ('right', 'Direita')], default='right', verbose_name="Posição da Imagem")

    # Botão CTA
    button_text = models.CharField(max_length=50, blank=True, verbose_name="Texto do Botão")
    button_link = models.CharField(max_length=300, blank=True, verbose_name="Link do Botão")

    # Estilo
    background_color = models.CharField(max_length=20, choices=BACKGROUND_COLORS, default='white', verbose_name="Cor de Fundo")
    custom_css_class = models.CharField(max_length=100, blank=True, verbose_name="Classe CSS Customizada")

    # HTML customizado (para section_type='html')
    custom_html = models.TextField(blank=True, verbose_name="HTML Customizado")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Seção"
        verbose_name_plural = "Seções"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_section_type_display()})"


class PageSection(models.Model):
    """Relacionamento entre páginas e seções com ordem"""
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_sections', verbose_name="Página")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Seção")
    order = models.IntegerField(default=0, verbose_name="Ordem")
    is_active = models.BooleanField(default=True, verbose_name="Ativa")

    class Meta:
        verbose_name = "Seção da Página"
        verbose_name_plural = "Seções da Página"
        ordering = ['order']
        unique_together = ['page', 'section', 'order']

    def __str__(self):
        return f"{self.page.title} - {self.section.name} (Ordem: {self.order})"


class SiteSettings(models.Model):
    """Configurações gerais do site"""
    site_name = models.CharField(max_length=100, default="Meu Blog", verbose_name="Nome do Site")
    site_description = models.TextField(blank=True, verbose_name="Descrição do Site")
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Logo do Site")
    site_favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Favicon")

    footer_text = models.TextField(blank=True, verbose_name="Texto do Rodapé")

    # Social Media
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter/X")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn")

    # SEO
    google_analytics_id = models.CharField(max_length=50, blank=True, verbose_name="Google Analytics ID")
    meta_keywords = models.TextField(blank=True, verbose_name="Meta Keywords Global")

    # Comments
    comments_enabled = models.BooleanField(default=True, verbose_name="Comentários Habilitados")
    comments_require_approval = models.BooleanField(default=True, verbose_name="Comentários Requerem Aprovação")

    # Posts per page
    posts_per_page = models.IntegerField(default=10, verbose_name="Posts por Página")

    # Home page
    home_page = models.ForeignKey('Page', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='is_home_page', verbose_name="Página Inicial",
                                   help_text="Selecione uma página para ser a home. Se vazio, mostra lista de posts.")

    # Active theme
    active_theme = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='is_active_theme', verbose_name="Tema Ativo",
                                      help_text="Selecione o tema visual do site")

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configurações do Site"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Garantir que existe apenas uma instância
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Theme(models.Model):
    """Temas visuais do site"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome do Tema")
    description = models.TextField(blank=True, verbose_name="Descrição")

    # Cores principais
    primary_color = models.CharField(max_length=7, default="#3498db", verbose_name="Cor Primária",
                                      help_text="Formato: #RRGGBB")
    secondary_color = models.CharField(max_length=7, default="#2c3e50", verbose_name="Cor Secundária")
    accent_color = models.CharField(max_length=7, default="#e74c3c", verbose_name="Cor de Destaque")

    # Cores de texto
    text_color = models.CharField(max_length=7, default="#333333", verbose_name="Cor do Texto")
    heading_color = models.CharField(max_length=7, default="#2c3e50", verbose_name="Cor dos Títulos")
    link_color = models.CharField(max_length=7, default="#3498db", verbose_name="Cor dos Links")
    link_hover_color = models.CharField(max_length=7, default="#2980b9", verbose_name="Cor dos Links (Hover)")

    # Cores de fundo
    background_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Cor de Fundo")
    secondary_bg_color = models.CharField(max_length=7, default="#f5f5f5", verbose_name="Cor de Fundo Secundária")

    # Header e Footer
    header_bg_color = models.CharField(max_length=7, default="#2c3e50", verbose_name="Cor de Fundo do Header")
    header_text_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Cor do Texto do Header")
    footer_bg_color = models.CharField(max_length=7, default="#34495e", verbose_name="Cor de Fundo do Footer")
    footer_text_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Cor do Texto do Footer")

    # Botões
    button_bg_color = models.CharField(max_length=7, default="#3498db", verbose_name="Cor de Fundo do Botão")
    button_text_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Cor do Texto do Botão")
    button_hover_bg_color = models.CharField(max_length=7, default="#2980b9", verbose_name="Cor do Botão (Hover)")

    # Tipografia
    font_family = models.CharField(max_length=200, default="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif",
                                   verbose_name="Família de Fonte")
    heading_font_family = models.CharField(max_length=200, blank=True, verbose_name="Família de Fonte dos Títulos",
                                           help_text="Se vazio, usa a mesma fonte do texto")

    font_size_base = models.CharField(max_length=10, default="16px", verbose_name="Tamanho Base da Fonte")
    line_height = models.CharField(max_length=10, default="1.6", verbose_name="Altura da Linha")

    # Espaçamento e Layout
    border_radius = models.CharField(max_length=10, default="8px", verbose_name="Raio das Bordas")
    box_shadow = models.CharField(max_length=100, default="0 2px 5px rgba(0,0,0,0.1)", verbose_name="Sombra dos Boxes")

    # CSS customizado
    custom_css = models.TextField(blank=True, verbose_name="CSS Customizado",
                                   help_text="CSS adicional para personalizar o tema")

    # Controle
    is_active = models.BooleanField(default=False, verbose_name="Tema Ativo")
    is_default = models.BooleanField(default=False, verbose_name="Tema Padrão",
                                      help_text="Tema usado quando nenhum está configurado")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Tema"
        verbose_name_plural = "Temas"
        ordering = ['-is_active', '-is_default', 'name']

    def __str__(self):
        status = ""
        if self.is_active:
            status = " [ATIVO]"
        elif self.is_default:
            status = " [PADRÃO]"
        return f"{self.name}{status}"

    def save(self, *args, **kwargs):
        # Se marcado como ativo, desativa os outros
        if self.is_active:
            Theme.objects.filter(is_active=True).update(is_active=False)

        # Garantir que há apenas um tema padrão
        if self.is_default:
            Theme.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)

        super().save(*args, **kwargs)

    @classmethod
    def get_active_theme(cls):
        """Retorna o tema ativo (prioridade: SiteSettings > is_active > is_default)"""
        # Primeiro verifica se há tema configurado nas configurações do site
        try:
            site_settings = SiteSettings.get_settings()
            if site_settings.active_theme:
                return site_settings.active_theme
        except:
            pass

        # Se não, busca tema marcado como ativo
        theme = cls.objects.filter(is_active=True).first()
        if not theme:
            # Fallback para tema padrão
            theme = cls.objects.filter(is_default=True).first()
        return theme


class Media(models.Model):
    """Biblioteca de mídia"""
    title = models.CharField(max_length=200, verbose_name="Título")
    file = models.FileField(upload_to='media/%Y/%m/%d/', verbose_name="Arquivo")
    file_type = models.CharField(max_length=50, blank=True, verbose_name="Tipo")
    file_size = models.IntegerField(default=0, verbose_name="Tamanho")

    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Enviado por")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em")

    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Texto Alternativo")
    caption = models.TextField(blank=True, verbose_name="Legenda")

    class Meta:
        verbose_name = "Mídia"
        verbose_name_plural = "Mídias"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            # Determinar tipo de arquivo
            if self.file.name:
                ext = self.file.name.split('.')[-1].lower()
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    self.file_type = 'image'
                elif ext in ['mp4', 'avi', 'mov', 'wmv']:
                    self.file_type = 'video'
                elif ext in ['pdf', 'doc', 'docx']:
                    self.file_type = 'document'
                else:
                    self.file_type = 'other'
        super().save(*args, **kwargs)
