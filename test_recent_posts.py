import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from blog.templatetags.blog_tags import get_recent_posts

print("=" * 60)
print("TESTANDO TEMPLATE TAGS - POSTS RECENTES")
print("=" * 60)

# Testar get_recent_posts
recent_posts = get_recent_posts(3)

print(f"\nTotal de posts encontrados: {len(recent_posts)}")
print("\nPosts:")

for i, post in enumerate(recent_posts, 1):
    print(f"\n{i}. {post.title}")
    print(f"   Autor: {post.author.get_full_name() or post.author.username}")
    print(f"   Categoria: {post.category.name if post.category else 'Sem categoria'}")
    print(f"   Data: {post.published_at.strftime('%d/%m/%Y')}")
    print(f"   Visualizações: {post.views}")
    if post.excerpt:
        excerpt = post.excerpt[:100] + "..." if len(post.excerpt) > 100 else post.excerpt
        print(f"   Resumo: {excerpt}")
    print(f"   URL: {post.get_absolute_url()}")

print("\n" + "=" * 60)
print("TESTE CONCLUÍDO COM SUCESSO!")
print("=" * 60)
print("\nA página inicial agora mostrará estes 3 posts em cards bonitos!")
print("Acesse: http://127.0.0.1:8000/")
