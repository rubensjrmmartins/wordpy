from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from blog.models import Post, Comment, Category
from ecommerce.models import Product, Order, Cart
from messaging.models import Conversation, Message
from modules.models import Module
from django.contrib.auth.models import User


@staff_member_required
def dashboard_stats(request):
    """
    View para exibir estatísticas gerais do sistema no dashboard.
    """

    # Estatísticas de Blog
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='published').count()
    draft_posts = Post.objects.filter(status='draft').count()
    total_comments = Comment.objects.count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    total_categories = Category.objects.count()

    # Posts mais visualizados
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]

    # Posts recentes
    recent_posts = Post.objects.filter(status='published').order_by('-published_at')[:5]

    # Estatísticas de E-commerce
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    out_of_stock = Product.objects.filter(stock_quantity=0).count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='delivered').count()

    # Valor total de pedidos
    total_revenue = Order.objects.filter(
        payment_status='paid'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    # Pedidos recentes
    recent_orders = Order.objects.order_by('-created_at')[:5]

    # Produtos mais vendidos
    bestsellers = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).filter(
        total_sold__isnull=False
    ).order_by('-total_sold')[:5]

    # Estatísticas de Mensagens
    total_conversations = Conversation.objects.count()
    total_messages = Message.objects.count()
    unread_messages = Message.objects.filter(is_read=False).count()

    # Estatísticas de Usuários
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()

    # Novos usuários (últimos 30 dias)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()

    # Módulos ativos
    active_modules = Module.objects.filter(is_active=True).count()
    total_modules = Module.objects.count()

    # Atividade recente (últimos 7 dias)
    seven_days_ago = timezone.now() - timedelta(days=7)
    new_posts_week = Post.objects.filter(created_at__gte=seven_days_ago).count()
    new_orders_week = Order.objects.filter(created_at__gte=seven_days_ago).count()
    new_messages_week = Message.objects.filter(created_at__gte=seven_days_ago).count()

    context = {
        # Blog
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_comments': total_comments,
        'pending_comments': pending_comments,
        'total_categories': total_categories,
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,

        # E-commerce
        'total_products': total_products,
        'active_products': active_products,
        'out_of_stock': out_of_stock,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'bestsellers': bestsellers,

        # Mensagens
        'total_conversations': total_conversations,
        'total_messages': total_messages,
        'unread_messages': unread_messages,

        # Usuários
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'new_users': new_users,

        # Módulos
        'active_modules': active_modules,
        'total_modules': total_modules,

        # Atividade recente
        'new_posts_week': new_posts_week,
        'new_orders_week': new_orders_week,
        'new_messages_week': new_messages_week,
    }

    return render(request, 'admin/dashboard_stats.html', context)
