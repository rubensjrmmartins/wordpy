from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Post, Comment, Page, SiteSettings, Media, Section, PageSection, Theme


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Nº de Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'published_at', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Informações Principais', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Conteúdo', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ('Configurações', {
            'fields': ('status', 'allow_comments', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('views',),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ['views', 'created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_author_name', 'post', 'is_approved', 'created_at', 'content_preview']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author_name', 'author_email']
    actions = ['approve_comments', 'unapprove_comments']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Preview'

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Aprovar comentários selecionados'

    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_comments.short_description = 'Desaprovar comentários selecionados'


class PageSectionInline(admin.TabularInline):
    model = PageSection
    extra = 1
    fields = ['section', 'order', 'is_active']
    autocomplete_fields = ['section']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'show_in_menu', 'menu_order', 'section_count', 'created_at']
    list_filter = ['is_published', 'show_in_menu', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PageSectionInline]

    fieldsets = (
        ('Informações Principais', {
            'fields': ('title', 'slug', 'author')
        }),
        ('Conteúdo', {
            'fields': ('content', 'featured_image'),
            'description': 'Conteúdo principal da página. Você também pode adicionar seções abaixo.'
        }),
        ('Configurações', {
            'fields': ('is_published', 'show_in_menu', 'menu_order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        })
    )

    def section_count(self, obj):
        return obj.page_sections.filter(is_active=True).count()
    section_count.short_description = 'Seções'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('site_name', 'site_description', 'site_logo', 'site_favicon', 'footer_text')
        }),
        ('Redes Sociais', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url')
        }),
        ('SEO e Analytics', {
            'fields': ('google_analytics_id', 'meta_keywords')
        }),
        ('Comentários', {
            'fields': ('comments_enabled', 'comments_require_approval')
        }),
        ('Configurações de Exibição', {
            'fields': ('home_page', 'posts_per_page', 'active_theme')
        })
    )

    def has_add_permission(self, request):
        # Permitir apenas uma instância
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Não permitir deletar as configurações
        return False

    def changelist_view(self, request, extra_context=None):
        """
        Redireciona automaticamente para a única instância de configurações.
        Se não existir, cria uma nova.
        """
        from django.shortcuts import redirect
        from django.urls import reverse

        # Obtém ou cria as configurações
        settings = SiteSettings.get_settings()

        # Redireciona para a página de edição
        return redirect(reverse('admin:blog_sitesettings_change', args=[settings.pk]))


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_thumbnail', 'file_type', 'get_file_size', 'uploaded_by', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['title', 'alt_text', 'caption']
    readonly_fields = ['file_type', 'file_size', 'uploaded_at']

    fieldsets = (
        ('Arquivo', {
            'fields': ('title', 'file')
        }),
        ('Metadados', {
            'fields': ('alt_text', 'caption')
        }),
        ('Informações', {
            'fields': ('file_type', 'file_size', 'uploaded_by', 'uploaded_at'),
            'classes': ('collapse',)
        })
    )

    def file_thumbnail(self, obj):
        if obj.file_type == 'image':
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.file.url)
        return '-'
    file_thumbnail.short_description = 'Preview'

    def get_file_size(self, obj):
        size = obj.file_size
        if size < 1024:
            return f'{size} B'
        elif size < 1024 * 1024:
            return f'{size / 1024:.2f} KB'
        else:
            return f'{size / (1024 * 1024):.2f} MB'
    get_file_size.short_description = 'Tamanho'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'section_type', 'background_color', 'preview_image', 'created_at']
    list_filter = ['section_type', 'background_color', 'created_at']
    search_fields = ['name', 'title', 'content']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'section_type')
        }),
        ('Conteúdo', {
            'fields': ('title', 'subtitle', 'content')
        }),
        ('Imagem', {
            'fields': ('image', 'image_position'),
            'classes': ('collapse',)
        }),
        ('Call to Action (Botão)', {
            'fields': ('button_text', 'button_link'),
            'classes': ('collapse',)
        }),
        ('Estilo', {
            'fields': ('background_color', 'custom_css_class'),
            'classes': ('collapse',)
        }),
        ('HTML Customizado', {
            'fields': ('custom_html',),
            'classes': ('collapse',),
            'description': 'Use apenas se o tipo de seção for "HTML Customizado"'
        })
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 80px; max-height: 80px;" />', obj.image.url)
        return '-'
    preview_image.short_description = 'Preview'


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'is_default', 'color_preview', 'created_at']
    list_filter = ['is_active', 'is_default', 'created_at']
    search_fields = ['name', 'description']
    actions = ['activate_theme']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'is_active', 'is_default')
        }),
        ('Cores Principais', {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
        ('Cores de Texto', {
            'fields': ('text_color', 'heading_color', 'link_color', 'link_hover_color'),
            'classes': ('collapse',)
        }),
        ('Cores de Fundo', {
            'fields': ('background_color', 'secondary_bg_color'),
            'classes': ('collapse',)
        }),
        ('Header e Footer', {
            'fields': ('header_bg_color', 'header_text_color', 'footer_bg_color', 'footer_text_color'),
            'classes': ('collapse',)
        }),
        ('Botões', {
            'fields': ('button_bg_color', 'button_text_color', 'button_hover_bg_color'),
            'classes': ('collapse',)
        }),
        ('Tipografia', {
            'fields': ('font_family', 'heading_font_family', 'font_size_base', 'line_height'),
            'classes': ('collapse',)
        }),
        ('Espaçamento e Layout', {
            'fields': ('border_radius', 'box_shadow'),
            'classes': ('collapse',)
        }),
        ('CSS Customizado', {
            'fields': ('custom_css',),
            'classes': ('collapse',),
            'description': 'CSS adicional aplicado após as variáveis do tema'
        })
    )

    def color_preview(self, obj):
        return format_html(
            '<div style="display: flex; gap: 5px;">'
            '<div style="width: 30px; height: 30px; background: {}; border: 1px solid #ccc; border-radius: 3px;" title="Primária"></div>'
            '<div style="width: 30px; height: 30px; background: {}; border: 1px solid #ccc; border-radius: 3px;" title="Secundária"></div>'
            '<div style="width: 30px; height: 30px; background: {}; border: 1px solid #ccc; border-radius: 3px;" title="Destaque"></div>'
            '</div>',
            obj.primary_color, obj.secondary_color, obj.accent_color
        )
    color_preview.short_description = 'Preview de Cores'

    def activate_theme(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, 'Selecione apenas um tema para ativar.', level='error')
            return

        theme = queryset.first()
        theme.is_active = True
        theme.save()
        self.message_user(request, f'Tema "{theme.name}" ativado com sucesso!')

    activate_theme.short_description = 'Ativar tema selecionado'
