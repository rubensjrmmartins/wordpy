import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post, Page, SiteSettings

# Obter o usuário admin
admin = User.objects.get(username='admin')

# Criar configurações do site
site_settings, created = SiteSettings.objects.get_or_create(pk=1)
site_settings.site_name = "Meu Blog Python"
site_settings.site_description = "Um CMS poderoso criado com Django, similar ao WordPress"
site_settings.footer_text = "© 2025 Meu Blog Python. Desenvolvido com Django."
site_settings.posts_per_page = 5
site_settings.save()
print("OK - Configuracoes do site criadas")

# Criar categorias
categories_data = [
    {"name": "Tecnologia", "description": "Artigos sobre tecnologia e inovação"},
    {"name": "Python", "description": "Tutoriais e dicas sobre Python"},
    {"name": "Django", "description": "Desenvolvimento web com Django"},
    {"name": "Web Development", "description": "Desenvolvimento web em geral"},
]

for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data["name"],
        defaults={"description": cat_data["description"]}
    )
    if created:
        print(f"OK - Categoria criada: {cat.name}")

# Criar posts de exemplo
posts_data = [
    {
        "title": "Bem-vindo ao Meu Blog Python!",
        "content": """
        <h2>Olá, seja bem-vindo!</h2>
        <p>Este é um sistema de gerenciamento de conteúdo (CMS) completo, similar ao WordPress, mas desenvolvido com Python e Django.</p>

        <h3>Recursos Principais:</h3>
        <ul>
            <li>Sistema completo de posts e páginas</li>
            <li>Editor de conteúdo WYSIWYG (CKEditor)</li>
            <li>Sistema de categorias e tags</li>
            <li>Comentários com aprovação</li>
            <li>Upload de mídia</li>
            <li>SEO otimizado</li>
            <li>Painel administrativo poderoso</li>
            <li>Totalmente responsivo</li>
        </ul>

        <p>Explore o site e veja todas as funcionalidades disponíveis!</p>
        """,
        "excerpt": "Conheça o novo CMS desenvolvido com Python e Django, com recursos similares ao WordPress.",
        "category": "Tecnologia",
        "tags": ["django", "python", "cms", "wordpress"],
    },
    {
        "title": "Como Criar um Blog com Django",
        "content": """
        <h2>Tutorial: Criando um Blog com Django</h2>
        <p>Django é um framework web Python poderoso que facilita o desenvolvimento de aplicações web robustas.</p>

        <h3>Passos Básicos:</h3>
        <ol>
            <li>Instale o Django: <code>pip install django</code></li>
            <li>Crie um projeto: <code>django-admin startproject meublog</code></li>
            <li>Crie um app: <code>python manage.py startapp blog</code></li>
            <li>Defina seus models no arquivo models.py</li>
            <li>Crie as views e templates</li>
            <li>Configure as URLs</li>
            <li>Execute as migrações</li>
        </ol>

        <p>Com Django, você tem controle total sobre sua aplicação e pode criar sistemas complexos com facilidade.</p>
        """,
        "excerpt": "Aprenda a criar um blog completo usando o framework Django.",
        "category": "Django",
        "tags": ["django", "tutorial", "python", "web"],
    },
    {
        "title": "10 Dicas para Melhorar seu Código Python",
        "content": """
        <h2>Boas Práticas em Python</h2>
        <p>Python é uma linguagem elegante e poderosa. Aqui estão algumas dicas para escrever código melhor:</p>

        <h3>1. Use List Comprehensions</h3>
        <p>Ao invés de loops tradicionais, use list comprehensions para código mais limpo.</p>

        <h3>2. Aproveite os Context Managers</h3>
        <p>Use 'with' statements para gerenciar recursos de forma segura.</p>

        <h3>3. Siga o PEP 8</h3>
        <p>Mantenha seu código consistente seguindo o guia de estilo Python.</p>

        <h3>4. Use Type Hints</h3>
        <p>Adicione type hints para melhor documentação e detecção de erros.</p>

        <h3>5. Escreva Testes</h3>
        <p>Sempre escreva testes para seu código usando unittest ou pytest.</p>

        <p>E há muito mais! Continue aprendendo e melhorando suas habilidades.</p>
        """,
        "excerpt": "Dicas práticas para escrever código Python mais limpo e eficiente.",
        "category": "Python",
        "tags": ["python", "boas-praticas", "dicas", "codigo"],
    },
]

for post_data in posts_data:
    category = Category.objects.get(name=post_data["category"])
    post, created = Post.objects.get_or_create(
        title=post_data["title"],
        defaults={
            "author": admin,
            "content": post_data["content"],
            "excerpt": post_data["excerpt"],
            "category": category,
            "status": "published",
            "published_at": datetime.now(),
        }
    )

    if created:
        for tag in post_data["tags"]:
            post.tags.add(tag)
        print(f"OK - Post criado: {post.title}")

# Criar páginas de exemplo
pages_data = [
    {
        "title": "Sobre",
        "content": """
        <h2>Sobre Este Blog</h2>
        <p>Este é um CMS completo desenvolvido com Python e Django, inspirado no WordPress.</p>

        <h3>Tecnologias Utilizadas:</h3>
        <ul>
            <li>Python 3.12</li>
            <li>Django 5.2</li>
            <li>CKEditor para edição de conteúdo</li>
            <li>SQLite como banco de dados</li>
        </ul>

        <p>O projeto demonstra como é possível criar um sistema completo de gerenciamento de conteúdo usando tecnologias open-source.</p>
        """,
        "show_in_menu": True,
        "menu_order": 1,
    },
    {
        "title": "Contato",
        "content": """
        <h2>Entre em Contato</h2>
        <p>Tem alguma dúvida ou sugestão? Entre em contato conosco!</p>

        <p><strong>Email:</strong> contato@example.com</p>
        <p><strong>Telefone:</strong> (11) 1234-5678</p>

        <h3>Redes Sociais</h3>
        <p>Siga-nos nas redes sociais para ficar por dentro das novidades!</p>
        """,
        "show_in_menu": True,
        "menu_order": 2,
    },
]

for page_data in pages_data:
    page, created = Page.objects.get_or_create(
        title=page_data["title"],
        defaults={
            "author": admin,
            "content": page_data["content"],
            "show_in_menu": page_data["show_in_menu"],
            "menu_order": page_data["menu_order"],
            "is_published": True,
        }
    )
    if created:
        print(f"OK - Pagina criada: {page.title}")

print("\nOK - Dados de exemplo criados com sucesso!")
print("\nAcesse o admin em: http://127.0.0.1:8000/admin/")
print("Username: admin")
print("Password: admin123")
