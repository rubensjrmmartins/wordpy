# Template Tags Customizados - WordPy CMS

## Visão Geral

O WordPy CMS fornece template tags customizados para facilitar a exibição de conteúdo dinâmico em seus templates.

## Como Usar

Para usar os template tags customizados, adicione no topo do seu template:

```django
{% load blog_tags %}
```

## Template Tags Disponíveis

### 1. get_recent_posts

Retorna os posts mais recentes publicados.

**Sintaxe:**
```django
{% get_recent_posts [número] as [variável] %}
```

**Parâmetros:**
- `número` (opcional): Quantidade de posts a retornar (padrão: 3)

**Exemplo:**
```django
{% load blog_tags %}

{% get_recent_posts 5 as recent_posts %}

<div class="recent-posts">
    {% for post in recent_posts %}
        <article>
            <h3><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h3>
            <p>{{ post.excerpt }}</p>
        </article>
    {% endfor %}
</div>
```

**Retorno:**
- QuerySet de Post objects
- Ordenado por data de publicação (mais recente primeiro)
- Apenas posts com status 'published'
- Inclui relacionamentos: author, category, tags (otimizado)

---

### 2. get_popular_posts

Retorna os posts mais populares baseado no número de visualizações.

**Sintaxe:**
```django
{% get_popular_posts [número] as [variável] %}
```

**Parâmetros:**
- `número` (opcional): Quantidade de posts a retornar (padrão: 5)

**Exemplo:**
```django
{% load blog_tags %}

<aside class="popular-posts">
    <h3>Posts Populares</h3>
    {% get_popular_posts 5 as popular %}

    <ul>
        {% for post in popular %}
            <li>
                <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
                <span>{{ post.views }} visualizações</span>
            </li>
        {% endfor %}
    </ul>
</aside>
```

**Retorno:**
- QuerySet de Post objects
- Ordenado por visualizações (mais visto primeiro)
- Apenas posts com status 'published'
- Inclui relacionamentos: author, category (otimizado)

---

### 3. get_categories_with_count

Retorna todas as categorias com a contagem de posts publicados.

**Sintaxe:**
```django
{% get_categories_with_count as [variável] %}
```

**Exemplo:**
```django
{% load blog_tags %}

<nav class="categories">
    <h3>Categorias</h3>
    {% get_categories_with_count as categories %}

    <ul>
        {% for category in categories %}
            <li>
                <a href="{% url 'blog:category' category.slug %}">
                    {{ category.name }}
                    <span class="count">({{ category.post_count }})</span>
                </a>
            </li>
        {% endfor %}
    </ul>
</nav>
```

**Retorno:**
- QuerySet de Category objects
- Cada categoria tem atributo `post_count` (anotação)
- Apenas categorias com posts (post_count > 0)
- Ordenado por contagem de posts (maior primeiro)

---

### 4. truncate_words (Filtro)

Trunca um texto para um número específico de palavras.

**Sintaxe:**
```django
{{ texto|truncate_words:número }}
```

**Parâmetros:**
- `número`: Quantidade de palavras a manter

**Exemplos:**
```django
{% load blog_tags %}

<!-- Exemplo 1: Resumo de 20 palavras -->
<p>{{ post.content|striptags|truncate_words:20 }}</p>

<!-- Exemplo 2: Título curto -->
<h3>{{ page.title|truncate_words:5 }}</h3>

<!-- Exemplo 3: Descrição -->
<div class="excerpt">
    {{ post.excerpt|default:post.content|striptags|truncate_words:30 }}
</div>
```

**Comportamento:**
- Se o texto tiver mais palavras que o limite, adiciona "..." no final
- Se o texto tiver menos palavras, retorna o texto completo
- Separa palavras por espaços em branco

**Combinações úteis:**
```django
<!-- Remover HTML e truncar -->
{{ post.content|striptags|truncate_words:15 }}

<!-- Fallback + truncar -->
{{ post.excerpt|default:post.content|striptags|truncate_words:25 }}

<!-- Truncar e converter para maiúsculas -->
{{ post.title|truncate_words:10|upper }}
```

---

## Exemplo Completo: Sidebar

```django
{% load blog_tags %}

<aside class="sidebar">
    <!-- Posts Recentes -->
    <section class="widget">
        <h3>Posts Recentes</h3>
        {% get_recent_posts 5 as recent %}
        <ul>
            {% for post in recent %}
                <li>
                    <a href="{{ post.get_absolute_url }}">
                        {{ post.title|truncate_words:8 }}
                    </a>
                    <span class="date">{{ post.published_at|date:"d/m/Y" }}</span>
                </li>
            {% endfor %}
        </ul>
    </section>

    <!-- Posts Populares -->
    <section class="widget">
        <h3>Mais Lidos</h3>
        {% get_popular_posts 5 as popular %}
        <ul>
            {% for post in popular %}
                <li>
                    <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
                    <span class="views">👁 {{ post.views }}</span>
                </li>
            {% endfor %}
        </ul>
    </section>

    <!-- Categorias -->
    <section class="widget">
        <h3>Categorias</h3>
        {% get_categories_with_count as categories %}
        <ul>
            {% for cat in categories %}
                <li>
                    <a href="{% url 'blog:category' cat.slug %}">
                        {{ cat.name }} ({{ cat.post_count }})
                    </a>
                </li>
            {% endfor %}
        </ul>
    </section>
</aside>
```

## Exemplo Completo: Grid de Posts

```django
{% load blog_tags %}

<section class="blog-section">
    <h2>Últimas do Blog</h2>

    {% get_recent_posts 6 as posts %}

    <div class="post-grid">
        {% for post in posts %}
            <article class="post-card">
                {% if post.featured_image %}
                    <img src="{{ post.featured_image.url }}" alt="{{ post.title }}">
                {% endif %}

                <div class="content">
                    {% if post.category %}
                        <span class="category">{{ post.category.name }}</span>
                    {% endif %}

                    <h3>
                        <a href="{{ post.get_absolute_url }}">
                            {{ post.title|truncate_words:10 }}
                        </a>
                    </h3>

                    <p>{{ post.excerpt|default:post.content|striptags|truncate_words:20 }}</p>

                    <div class="meta">
                        <span>{{ post.published_at|date:"d/m/Y" }}</span>
                        <span>{{ post.author.get_full_name|default:post.author.username }}</span>
                        <span>👁 {{ post.views }}</span>
                    </div>

                    <a href="{{ post.get_absolute_url }}" class="read-more">Ler mais →</a>
                </div>
            </article>
        {% endfor %}
    </div>
</section>
```

## Performance

Os template tags foram otimizados para performance:

- **select_related**: Usado para ForeignKey (author, category)
- **prefetch_related**: Usado para ManyToMany (tags)
- **annotate**: Usado para contagens (post_count)

Isso reduz o número de queries ao banco de dados e melhora significativamente a performance.

## Criando Seus Próprios Template Tags

Para adicionar novos template tags, edite o arquivo `blog/templatetags/blog_tags.py`:

```python
from django import template
from blog.models import Post

register = template.Library()

@register.simple_tag
def meu_template_tag(parametro):
    """Descrição do que o tag faz"""
    # Sua lógica aqui
    return resultado
```

Tipos de template tags:
- **simple_tag**: Retorna um valor
- **inclusion_tag**: Renderiza um template
- **filter**: Modifica um valor (como truncate_words)

## Troubleshooting

### Tag não encontrado

**Erro:** `Invalid block tag on line X: 'get_recent_posts'`

**Solução:** Certifique-se de adicionar `{% load blog_tags %}` no topo do template.

### Nenhum resultado retornado

**Problema:** Template tag retorna lista vazia

**Verificações:**
1. Existem posts com status 'published'?
2. Os posts têm `published_at` definido?
3. O banco de dados está atualizado?

**Testar manualmente:**
```bash
python manage.py shell
>>> from blog.models import Post
>>> Post.objects.filter(status='published').count()
```

### Performance lenta

**Problema:** Página carrega devagar

**Otimizações:**
1. Limite o número de posts (use valores menores)
2. Verifique se há muitas queries no Django Debug Toolbar
3. Considere usar cache para resultados frequentes

## Referências

- [Django Template Tags Documentation](https://docs.djangoproject.com/en/stable/howto/custom-template-tags/)
- [Django Query Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)

---

**Desenvolvido com Python e Django** 🐍 ❤️
