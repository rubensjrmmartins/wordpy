from django import template
from blog.models import Post, Category
from django.db.models import Count

register = template.Library()


@register.simple_tag
def get_recent_posts(count=3):
    """Retorna os posts mais recentes publicados"""
    return Post.objects.filter(
        status='published'
    ).select_related('author', 'category').prefetch_related('tags').order_by('-published_at')[:count]


@register.simple_tag
def get_popular_posts(count=5):
    """Retorna os posts mais populares (por visualizações)"""
    return Post.objects.filter(
        status='published'
    ).select_related('author', 'category').order_by('-views')[:count]


@register.simple_tag
def get_categories_with_count():
    """Retorna categorias com contagem de posts"""
    return Category.objects.annotate(
        post_count=Count('posts')
    ).filter(post_count__gt=0).order_by('-post_count')


@register.filter
def truncate_words(value, arg):
    """Trunca texto para número específico de palavras"""
    try:
        limit = int(arg)
    except ValueError:
        return value

    words = value.split()
    if len(words) > limit:
        return ' '.join(words[:limit]) + '...'
    return value
