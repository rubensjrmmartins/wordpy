from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Conversation(models.Model):
    """
    Modelo para representar uma conversa entre usuários.
    Uma conversa pode ter múltiplos participantes.
    """
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Título'),
        help_text=_('Título da conversa (opcional para conversas em grupo)')
    )

    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        verbose_name=_('Participantes')
    )

    is_group = models.BooleanField(
        default=False,
        verbose_name=_('Conversa em Grupo'),
        help_text=_('Define se é uma conversa em grupo ou privada')
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_conversations',
        verbose_name=_('Criado por')
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
        verbose_name = _('Conversa')
        verbose_name_plural = _('Conversas')
        ordering = ['-updated_at']

    def __str__(self):
        if self.title:
            return self.title
        # Para conversas privadas, mostra os nomes dos participantes
        participants_names = ', '.join([p.username for p in self.participants.all()[:3]])
        if self.participants.count() > 3:
            participants_names += f' +{self.participants.count() - 3}'
        return f"Conversa: {participants_names}"

    @property
    def last_message(self):
        """Retorna a última mensagem da conversa"""
        return self.messages.order_by('-created_at').first()

    @property
    def unread_count(self, user):
        """Retorna a quantidade de mensagens não lidas para um usuário"""
        if not hasattr(self, '_user'):
            return 0
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    """
    Modelo para representar uma mensagem dentro de uma conversa.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Conversa')
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_('Remetente')
    )

    content = models.TextField(
        verbose_name=_('Mensagem')
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Lida')
    )

    read_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Lida em')
    )

    # Anexos (opcional)
    attachment = models.FileField(
        upload_to='messaging/attachments/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name=_('Anexo')
    )

    # Mensagem respondendo a outra
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='replies',
        verbose_name=_('Responder a')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Enviada em')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizada em')
    )

    class Meta:
        verbose_name = _('Mensagem')
        verbose_name_plural = _('Mensagens')
        ordering = ['created_at']

    def __str__(self):
        preview = self.content[:50]
        if len(self.content) > 50:
            preview += '...'
        return f"{self.sender.username}: {preview}"

    def mark_as_read(self):
        """Marca a mensagem como lida"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class MessageReadReceipt(models.Model):
    """
    Modelo para rastrear quando cada usuário leu uma mensagem.
    Útil para conversas em grupo onde queremos saber quem leu cada mensagem.
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='read_receipts',
        verbose_name=_('Mensagem')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_receipts',
        verbose_name=_('Usuário')
    )

    read_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Lida em')
    )

    class Meta:
        verbose_name = _('Confirmação de Leitura')
        verbose_name_plural = _('Confirmações de Leitura')
        unique_together = ['message', 'user']
        ordering = ['-read_at']

    def __str__(self):
        return f"{self.user.username} leu mensagem em {self.read_at}"


class BlockedUser(models.Model):
    """
    Modelo para gerenciar usuários bloqueados.
    Usuários bloqueados não podem enviar mensagens uns aos outros.
    """
    blocker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocked_users',
        verbose_name=_('Bloqueador')
    )

    blocked = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocked_by_users',
        verbose_name=_('Bloqueado')
    )

    reason = models.TextField(
        blank=True,
        verbose_name=_('Motivo')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Bloqueado em')
    )

    class Meta:
        verbose_name = _('Usuário Bloqueado')
        verbose_name_plural = _('Usuários Bloqueados')
        unique_together = ['blocker', 'blocked']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.blocker.username} bloqueou {self.blocked.username}"


class MessageNotification(models.Model):
    """
    Modelo para notificações de novas mensagens.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_notifications',
        verbose_name=_('Usuário')
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Mensagem')
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Lida')
    )

    read_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Lida em')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criada em')
    )

    class Meta:
        verbose_name = _('Notificação de Mensagem')
        verbose_name_plural = _('Notificações de Mensagens')
        ordering = ['-created_at']

    def __str__(self):
        return f"Notificação para {self.user.username}"

    def mark_as_read(self):
        """Marca a notificação como lida"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
