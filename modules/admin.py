from django.contrib import admin
from django.utils.html import format_html
from .models import Module, ModuleSettings, ModulePermission


class ModuleSettingsInline(admin.TabularInline):
    """Inline para editar configurações de módulos"""
    model = ModuleSettings
    extra = 1
    fields = ['key', 'value', 'value_type', 'description']


class ModulePermissionInline(admin.TabularInline):
    """Inline para editar permissões de módulos"""
    model = ModulePermission
    extra = 0
    fields = ['user', 'can_view', 'can_create', 'can_edit', 'can_delete']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Admin para gerenciar módulos do sistema"""
    list_display = [
        'name',
        'module_type',
        'version',
        'status_display',
        'is_core_display',
        'order',
        'created_at'
    ]
    list_filter = ['is_active', 'is_core', 'module_type', 'created_at']
    search_fields = ['name', 'slug', 'description', 'app_name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Informações Básicas', {
            'fields': ['name', 'slug', 'module_type', 'description']
        }),
        ('Configurações', {
            'fields': ['app_name', 'version', 'icon', 'order']
        }),
        ('Status', {
            'fields': ['is_active', 'is_core']
        }),
        ('Datas', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    inlines = [ModuleSettingsInline, ModulePermissionInline]

    actions = ['activate_modules', 'deactivate_modules']

    def status_display(self, obj):
        """Exibe o status do módulo com formatação HTML"""
        if obj.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Ativo</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Inativo</span>'
        )
    status_display.short_description = 'Status'

    def is_core_display(self, obj):
        """Exibe se é módulo core com formatação HTML"""
        if obj.is_core:
            return format_html(
                '<span style="color: blue; font-weight: bold;">★ Core</span>'
            )
        return '-'
    is_core_display.short_description = 'Core'

    def activate_modules(self, request, queryset):
        """Action para ativar módulos selecionados"""
        count = 0
        for module in queryset:
            module.activate()
            count += 1
        self.message_user(request, f'{count} módulo(s) ativado(s) com sucesso.')
    activate_modules.short_description = 'Ativar módulos selecionados'

    def deactivate_modules(self, request, queryset):
        """Action para desativar módulos selecionados"""
        count = 0
        for module in queryset:
            if not module.is_core:
                module.deactivate()
                count += 1
        self.message_user(
            request,
            f'{count} módulo(s) desativado(s). Módulos core não foram desativados.'
        )
    deactivate_modules.short_description = 'Desativar módulos selecionados'


@admin.register(ModuleSettings)
class ModuleSettingsAdmin(admin.ModelAdmin):
    """Admin para gerenciar configurações de módulos"""
    list_display = ['module', 'key', 'value_preview', 'value_type', 'updated_at']
    list_filter = ['module', 'value_type']
    search_fields = ['key', 'value', 'description']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Configuração', {
            'fields': ['module', 'key', 'value', 'value_type']
        }),
        ('Descrição', {
            'fields': ['description']
        }),
        ('Datas', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    def value_preview(self, obj):
        """Exibe uma prévia do valor (limitado a 50 caracteres)"""
        if len(obj.value) > 50:
            return f"{obj.value[:50]}..."
        return obj.value
    value_preview.short_description = 'Valor'


@admin.register(ModulePermission)
class ModulePermissionAdmin(admin.ModelAdmin):
    """Admin para gerenciar permissões de módulos"""
    list_display = [
        'user',
        'module',
        'can_view',
        'can_create',
        'can_edit',
        'can_delete',
        'created_at'
    ]
    list_filter = ['module', 'can_view', 'can_create', 'can_edit', 'can_delete']
    search_fields = ['user__username', 'user__email', 'module__name']
    readonly_fields = ['created_at']

    fieldsets = [
        ('Usuário e Módulo', {
            'fields': ['user', 'module']
        }),
        ('Permissões', {
            'fields': ['can_view', 'can_create', 'can_edit', 'can_delete']
        }),
        ('Data', {
            'fields': ['created_at'],
            'classes': ['collapse']
        }),
    ]
