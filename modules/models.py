from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Module(models.Model):
    """
    Modelo para representar módulos do sistema.
    Cada módulo pode ser ativado/desativado dinamicamente.
    """
    MODULE_TYPES = [
        ('ecommerce', 'E-commerce'),
        ('messages', 'Mensagens'),
        ('blog', 'Blog'),
        ('analytics', 'Analytics'),
        ('custom', 'Personalizado'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Nome'),
        help_text=_('Nome único do módulo')
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_('Slug'),
        help_text=_('Identificador único do módulo (usado em URLs)')
    )

    module_type = models.CharField(
        max_length=50,
        choices=MODULE_TYPES,
        default='custom',
        verbose_name=_('Tipo de Módulo')
    )

    description = models.TextField(
        blank=True,
        verbose_name=_('Descrição'),
        help_text=_('Descrição detalhada do módulo')
    )

    version = models.CharField(
        max_length=20,
        default='1.0.0',
        verbose_name=_('Versão')
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name=_('Ativo'),
        help_text=_('Define se o módulo está ativo no sistema')
    )

    is_core = models.BooleanField(
        default=False,
        verbose_name=_('Módulo Core'),
        help_text=_('Módulos core não podem ser desativados')
    )

    app_name = models.CharField(
        max_length=100,
        verbose_name=_('Nome do App Django'),
        help_text=_('Nome do app Django correspondente (ex: ecommerce, messages)')
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Ícone'),
        help_text=_('Classe CSS do ícone (ex: fa fa-shopping-cart)')
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Ordem'),
        help_text=_('Ordem de exibição no menu')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )

    class Meta:
        verbose_name = _('Módulo')
        verbose_name_plural = _('Módulos')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def activate(self):
        """Ativa o módulo"""
        self.is_active = True
        self.save()

    def deactivate(self):
        """Desativa o módulo (apenas se não for core)"""
        if not self.is_core:
            self.is_active = False
            self.save()


class ModuleSettings(models.Model):
    """
    Modelo para armazenar configurações específicas de cada módulo.
    Permite que cada módulo tenha suas próprias configurações personalizadas.
    """
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name=_('Módulo')
    )

    key = models.CharField(
        max_length=100,
        verbose_name=_('Chave'),
        help_text=_('Nome da configuração')
    )

    value = models.TextField(
        verbose_name=_('Valor'),
        help_text=_('Valor da configuração (pode ser JSON)')
    )

    value_type = models.CharField(
        max_length=20,
        choices=[
            ('string', 'String'),
            ('integer', 'Integer'),
            ('boolean', 'Boolean'),
            ('json', 'JSON'),
        ],
        default='string',
        verbose_name=_('Tipo de Valor')
    )

    description = models.TextField(
        blank=True,
        verbose_name=_('Descrição')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )

    class Meta:
        verbose_name = _('Configuração de Módulo')
        verbose_name_plural = _('Configurações de Módulos')
        unique_together = ['module', 'key']
        ordering = ['module', 'key']

    def __str__(self):
        return f"{self.module.name} - {self.key}"

    def get_value(self):
        """Retorna o valor convertido para o tipo apropriado"""
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() in ['true', '1', 'yes']
        elif self.value_type == 'json':
            import json
            return json.loads(self.value)
        return self.value


class ModulePermission(models.Model):
    """
    Modelo para gerenciar permissões de acesso aos módulos.
    """
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='permissions',
        verbose_name=_('Módulo')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='module_permissions',
        verbose_name=_('Usuário')
    )

    can_view = models.BooleanField(
        default=True,
        verbose_name=_('Pode Visualizar')
    )

    can_create = models.BooleanField(
        default=False,
        verbose_name=_('Pode Criar')
    )

    can_edit = models.BooleanField(
        default=False,
        verbose_name=_('Pode Editar')
    )

    can_delete = models.BooleanField(
        default=False,
        verbose_name=_('Pode Deletar')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )

    class Meta:
        verbose_name = _('Permissão de Módulo')
        verbose_name_plural = _('Permissões de Módulos')
        unique_together = ['module', 'user']
        ordering = ['module', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.module.name}"
