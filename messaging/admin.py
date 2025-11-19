from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Conversation, Message, MessageReadReceipt, BlockedUser, MessageNotification
)


class MessageInline(admin.TabularInline):
    """Inline para visualizar mensagens de uma conversa"""
    model = Message
    extra = 0
    readonly_fields = ['sender', 'content', 'is_read', 'created_at']
    fields = ['sender', 'content', 'is_read', 'created_at']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin para conversas"""
    list_display = [
        'conversation_display',
        'is_group',
        'participants_count',
        'last_message_preview',
        'created_at',
        'updated_at'
    ]
    list_filter = ['is_group', 'created_at', 'updated_at']
    search_fields = ['title', 'participants__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['participants']

    fieldsets = [
        ('Informações da Conversa', {
            'fields': ['title', 'is_group', 'created_by']
        }),
        ('Participantes', {
            'fields': ['participants']
        }),
        ('Datas', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    inlines = [MessageInline]

    def conversation_display(self, obj):
        """Exibe o título ou participantes da conversa"""
        return str(obj)
    conversation_display.short_description = 'Conversa'

    def participants_count(self, obj):
        """Exibe a quantidade de participantes"""
        count = obj.participants.count()
        return format_html(
            '<span style="font-weight: bold;">{} participante(s)</span>',
            count
        )
    participants_count.short_description = 'Participantes'

    def last_message_preview(self, obj):
        """Exibe uma prévia da última mensagem"""
        last_msg = obj.last_message
        if last_msg:
            preview = last_msg.content[:30]
            if len(last_msg.content) > 30:
                preview += '...'
            return format_html(
                '<span style="color: gray;">{}: {}</span>',
                last_msg.sender.username,
                preview
            )
        return format_html('<span style="color: gray;">Sem mensagens</span>')
    last_message_preview.short_description = 'Última Mensagem'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin para mensagens"""
    list_display = [
        'sender',
        'conversation_display',
        'message_preview',
        'is_read_display',
        'attachment_display',
        'created_at'
    ]
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'content', 'conversation__title']
    readonly_fields = ['created_at', 'updated_at', 'read_at']

    fieldsets = [
        ('Mensagem', {
            'fields': ['conversation', 'sender', 'content']
        }),
        ('Anexo e Resposta', {
            'fields': ['attachment', 'reply_to']
        }),
        ('Status', {
            'fields': ['is_read', 'read_at']
        }),
        ('Datas', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    actions = ['mark_as_read', 'mark_as_unread']

    def conversation_display(self, obj):
        """Exibe a conversa"""
        return str(obj.conversation)
    conversation_display.short_description = 'Conversa'

    def message_preview(self, obj):
        """Exibe uma prévia da mensagem"""
        preview = obj.content[:50]
        if len(obj.content) > 50:
            preview += '...'
        return preview
    message_preview.short_description = 'Mensagem'

    def is_read_display(self, obj):
        """Exibe o status de leitura"""
        if obj.is_read:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Lida</span>'
            )
        return format_html(
            '<span style="color: orange;">✗ Não lida</span>'
        )
    is_read_display.short_description = 'Status'

    def attachment_display(self, obj):
        """Exibe se a mensagem tem anexo"""
        if obj.attachment:
            return format_html(
                '<span style="color: blue;">📎 Anexo</span>'
            )
        return '-'
    attachment_display.short_description = 'Anexo'

    def mark_as_read(self, request, queryset):
        """Action para marcar mensagens como lidas"""
        count = 0
        for message in queryset:
            message.mark_as_read()
            count += 1
        self.message_user(request, f'{count} mensagem(ns) marcada(s) como lida(s).')
    mark_as_read.short_description = 'Marcar como lida'

    def mark_as_unread(self, request, queryset):
        """Action para marcar mensagens como não lidas"""
        count = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{count} mensagem(ns) marcada(s) como não lida(s).')
    mark_as_unread.short_description = 'Marcar como não lida'


@admin.register(MessageReadReceipt)
class MessageReadReceiptAdmin(admin.ModelAdmin):
    """Admin para confirmações de leitura"""
    list_display = ['message_preview', 'user', 'read_at']
    list_filter = ['read_at']
    search_fields = ['user__username', 'message__content']
    readonly_fields = ['read_at']

    def message_preview(self, obj):
        """Exibe uma prévia da mensagem"""
        preview = obj.message.content[:30]
        if len(obj.message.content) > 30:
            preview += '...'
        return preview
    message_preview.short_description = 'Mensagem'


@admin.register(BlockedUser)
class BlockedUserAdmin(admin.ModelAdmin):
    """Admin para usuários bloqueados"""
    list_display = ['blocker', 'blocked', 'reason_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blocker__username', 'blocked__username', 'reason']
    readonly_fields = ['created_at']

    fieldsets = [
        ('Bloqueio', {
            'fields': ['blocker', 'blocked']
        }),
        ('Motivo', {
            'fields': ['reason']
        }),
        ('Data', {
            'fields': ['created_at'],
            'classes': ['collapse']
        }),
    ]

    def reason_preview(self, obj):
        """Exibe uma prévia do motivo do bloqueio"""
        if obj.reason:
            preview = obj.reason[:50]
            if len(obj.reason) > 50:
                preview += '...'
            return preview
        return '-'
    reason_preview.short_description = 'Motivo'


@admin.register(MessageNotification)
class MessageNotificationAdmin(admin.ModelAdmin):
    """Admin para notificações de mensagens"""
    list_display = [
        'user',
        'message_preview',
        'is_read_display',
        'created_at',
        'read_at'
    ]
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'message__content']
    readonly_fields = ['created_at', 'read_at']

    fieldsets = [
        ('Notificação', {
            'fields': ['user', 'message']
        }),
        ('Status', {
            'fields': ['is_read', 'read_at']
        }),
        ('Data', {
            'fields': ['created_at'],
            'classes': ['collapse']
        }),
    ]

    actions = ['mark_as_read', 'mark_as_unread']

    def message_preview(self, obj):
        """Exibe uma prévia da mensagem"""
        preview = obj.message.content[:30]
        if len(obj.message.content) > 30:
            preview += '...'
        return format_html(
            '<span>{}: {}</span>',
            obj.message.sender.username,
            preview
        )
    message_preview.short_description = 'Mensagem'

    def is_read_display(self, obj):
        """Exibe o status de leitura"""
        if obj.is_read:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Lida</span>'
            )
        return format_html(
            '<span style="color: orange;">✗ Não lida</span>'
        )
    is_read_display.short_description = 'Status'

    def mark_as_read(self, request, queryset):
        """Action para marcar notificações como lidas"""
        count = 0
        for notification in queryset:
            notification.mark_as_read()
            count += 1
        self.message_user(request, f'{count} notificação(ões) marcada(s) como lida(s).')
    mark_as_read.short_description = 'Marcar como lida'

    def mark_as_unread(self, request, queryset):
        """Action para marcar notificações como não lidas"""
        count = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{count} notificação(ões) marcada(s) como não lida(s).')
    mark_as_unread.short_description = 'Marcar como não lida'
