from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # Conversas
    path('conversas/', views.conversation_list, name='conversation_list'),
    path('conversa/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversa/nova/<int:user_id>/', views.new_conversation, name='new_conversation'),

    # Mensagens
    path('conversa/<int:conversation_id>/enviar/', views.send_message, name='send_message'),

    # API
    path('conversas/api/unread-count/', views.unread_count_api, name='unread_count_api'),
]
