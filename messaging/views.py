from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Max
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Conversation, Message


@login_required
def conversation_list(request):
    """Lista de conversas do usuário"""
    conversations = Conversation.objects.filter(
        participants=request.user
    ).annotate(
        last_message_date=Max('messages__created_at')
    ).order_by('-last_message_date')

    # Contar mensagens não lidas
    for conversation in conversations:
        conversation.unread_count = conversation.messages.filter(
            is_read=False
        ).exclude(sender=request.user).count()

    context = {
        'conversations': conversations,
    }

    return render(request, 'messaging/conversation_list.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """Detalhes de uma conversa"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )

    # Marcar mensagens como lidas
    conversation.messages.filter(
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    # Obter mensagens
    messages_list = conversation.messages.select_related('sender').order_by('created_at')

    # Obter outro participante
    other_participant = conversation.participants.exclude(id=request.user.id).first()

    context = {
        'conversation': conversation,
        'messages': messages_list,
        'other_participant': other_participant,
    }

    return render(request, 'messaging/conversation_detail.html', context)


@login_required
def new_conversation(request, user_id):
    """Criar nova conversa com um usuário"""
    other_user = get_object_or_404(User, id=user_id)

    # Verificar se já existe conversa entre os dois usuários
    existing_conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if existing_conversation:
        return redirect('messaging:conversation_detail', conversation_id=existing_conversation.id)

    # Criar nova conversa
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)

    messages.success(request, f'Conversa iniciada com {other_user.username}')
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)


@login_required
def send_message(request, conversation_id):
    """Enviar mensagem em uma conversa"""
    if request.method != 'POST':
        return redirect('messaging:conversation_detail', conversation_id=conversation_id)

    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )

    message_content = request.POST.get('message', '').strip()

    if message_content:
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=message_content
        )
        messages.success(request, 'Mensagem enviada!')
    else:
        messages.error(request, 'A mensagem não pode estar vazia.')

    return redirect('messaging:conversation_detail', conversation_id=conversation_id)


@login_required
def unread_count_api(request):
    """API para retornar contador de mensagens não lidas"""
    unread_count = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()

    return JsonResponse({'count': unread_count})
