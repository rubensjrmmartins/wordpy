# Interface Admin Moderna - WordPy CMS

## Visão Geral

O WordPy CMS agora possui uma interface de administração moderna e profissional usando **Django Jazzmin**, oferecendo:

- ✨ Design moderno e responsivo
- 📊 Dashboard com widgets de estatísticas
- 🎨 Temas claro e escuro
- 🔍 Busca global no admin
- 📱 Interface mobile-friendly
- 🎯 Ícones personalizados para cada modelo
- 📈 Visualizações de dados em tempo real

## Características

### 1. Interface Visual Moderna

- **Design**: Baseado em AdminLTE 3, Bootstrap 4 e Font Awesome
- **Cores**: Esquema de cores profissional e customizável
- **Navegação**: Menu lateral fixo com ícones e hierarquia clara
- **Responsividade**: Funciona perfeitamente em desktop, tablet e mobile

### 2. Dashboard de Estatísticas

Acesse: **`/admin/dashboard/stats/`**

O dashboard exibe métricas em tempo real organizadas por módulos:

#### Visão Geral
- Posts publicados e rascunhos
- Produtos ativos e sem estoque
- Pedidos pendentes
- Mensagens não lidas

#### Blog
- Total de posts (publicados vs rascunhos)
- Total de comentários (pendentes de aprovação)
- Total de categorias
- Posts mais populares (top 5)
- Posts recentes

#### E-commerce
- Total de produtos (ativos vs inativos)
- Produtos sem estoque
- Total de pedidos (pendentes vs concluídos)
- Receita total (pedidos pagos)
- Pedidos recentes
- Produtos mais vendidos (top 5)

#### Mensagens
- Total de conversas
- Total de mensagens
- Mensagens não lidas

#### Usuários e Sistema
- Total de usuários (ativos vs inativos)
- Novos usuários (últimos 30 dias)
- Usuários staff
- Módulos ativos vs total

#### Atividade Recente (7 dias)
- Novos posts da semana
- Novos pedidos da semana
- Novas mensagens da semana

### 3. Ícones Personalizados

Todos os modelos possuem ícones Font Awesome customizados:

**Autenticação:**
- 👥 Usuários: `fas fa-user`
- 👨‍👨‍👦 Grupos: `fas fa-users`

**Módulos:**
- 🧩 Módulos: `fas fa-cube`
- ⚙️ Configurações: `fas fa-cog`
- 🔑 Permissões: `fas fa-key`

**Blog:**
- 📰 Posts: `fas fa-newspaper`
- 📁 Categorias: `fas fa-folder`
- 💬 Comentários: `fas fa-comments`
- 📄 Páginas: `fas fa-file-alt`
- 🎨 Temas: `fas fa-palette`
- 🖼️ Mídias: `fas fa-images`

**E-commerce:**
- 📦 Produtos: `fas fa-box`
- 🏷️ Categorias: `fas fa-tags`
- 🛒 Carrinho: `fas fa-shopping-basket`
- 🧾 Pedidos: `fas fa-receipt`

**Mensagens:**
- 💬 Conversas: `fas fa-comments`
- 💌 Mensagens: `fas fa-comment`
- ✅ Confirmações: `fas fa-check-double`
- 🚫 Bloqueios: `fas fa-ban`
- 🔔 Notificações: `fas fa-bell`

### 4. Menu Superior

- **Home**: Volta para o índice do admin
- **Dashboard**: Acessa o dashboard de estatísticas
- **Suporte**: Link para repositório GitHub
- **Usuário**: Atalho rápido para gestão de usuários

### 5. Busca Global

Busca integrada no topo que pesquisa em:
- Usuários (username, email)
- Posts do blog (título, conteúdo)
- Produtos (nome, SKU, descrição)

### 6. Temas

#### Tema Padrão (Claro)
- Navbar: Azul escuro (`navbar-dark navbar-primary`)
- Sidebar: Escura com destaque azul (`sidebar-dark-primary`)
- Fundo: Branco limpo
- Acentos: Azul primário

#### Modo Escuro
- Ativável nas configurações
- Tema: Darkly
- Cores invertidas mantendo legibilidade

### 7. Personalização de Formulários

**Formato dos Formulários:**
- **Padrão**: Abas horizontais (`horizontal_tabs`)
- **Usuários**: Collapsible
- **Grupos**: Abas verticais

## Configuração

### Instalação

O Django Jazzmin já está instalado e configurado. Para referência:

```bash
pip install django-jazzmin==3.0.1
```

### Settings.py

As configurações estão em `wordpy_cms/settings.py`:

```python
INSTALLED_APPS = [
    'jazzmin',  # DEVE vir antes do admin
    'django.contrib.admin',
    ...
]

JAZZMIN_SETTINGS = {
    # Configurações do Jazzmin
}

JAZZMIN_UI_TWEAKS = {
    # Ajustes de UI
}
```

### URLs

Dashboard configurado em `wordpy_cms/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/dashboard/', include('dashboard.urls')),
    ...
]
```

## Estrutura de Arquivos

```
wordpy/
├── dashboard/                      # App do dashboard
│   ├── views.py                   # View de estatísticas
│   ├── urls.py                    # URLs do dashboard
│   └── templates/
│       └── admin/
│           └── dashboard_stats.html  # Template do dashboard
│
├── wordpy_cms/
│   ├── settings.py                # Configurações do Jazzmin
│   └── urls.py                    # URLs principais
│
└── requirements.txt               # django-jazzmin==3.0.1
```

## Personalização

### Alterar Cores

Edite `JAZZMIN_UI_TWEAKS` em `settings.py`:

```python
JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-primary",  # Cores do navbar
    "sidebar": "sidebar-dark-primary",       # Cores do sidebar
    "brand_colour": "navbar-dark",          # Cor da marca
    "accent": "accent-primary",             # Cor de acento
}
```

**Opções de cores:**
- `navbar-primary` (azul)
- `navbar-success` (verde)
- `navbar-info` (ciano)
- `navbar-warning` (amarelo)
- `navbar-danger` (vermelho)
- `navbar-dark` (escuro)

### Adicionar Novos Widgets ao Dashboard

Edite `dashboard/views.py`:

```python
@staff_member_required
def dashboard_stats(request):
    # Adicione suas consultas aqui
    nova_metrica = MeuModelo.objects.count()

    context = {
        'nova_metrica': nova_metrica,
        ...
    }
    return render(request, 'admin/dashboard_stats.html', context)
```

Edite `dashboard/templates/admin/dashboard_stats.html`:

```html
<div class="col-md-3">
    <div class="stat-card stat-card-primary">
        <div class="stat-card-header">
            <h3 class="stat-card-title">Nova Métrica</h3>
            <i class="fas fa-icon stat-card-icon icon-primary"></i>
        </div>
        <p class="stat-card-value">{{ nova_metrica }}</p>
        <p class="stat-card-label">descrição</p>
    </div>
</div>
```

### Adicionar Ícones a Novos Modelos

Edite `JAZZMIN_SETTINGS['icons']` em `settings.py`:

```python
"icons": {
    "seu_app.SeuModelo": "fas fa-seu-icone",
}
```

**Encontre ícones em:** https://fontawesome.com/icons

### Modificar Menu Superior

Edite `JAZZMIN_SETTINGS['topmenu_links']` em `settings.py`:

```python
"topmenu_links": [
    {"name": "Nome", "url": "url_name", "icon": "fas fa-icon"},
    {"name": "Link Externo", "url": "https://...", "new_window": True},
    {"model": "app.Model"},  # Link direto para modelo
],
```

## Acesso

### URL Principal do Admin
```
http://localhost:8000/admin/
```

### URL do Dashboard
```
http://localhost:8000/admin/dashboard/stats/
```

### Tela de Login
- Mensagem: "Bem-vindo ao WordPy CMS"
- Logo: Personalizável (configure em `JAZZMIN_SETTINGS['login_logo']`)

## Recursos Avançados

### 1. Custom CSS

Adicione CSS customizado criando um arquivo e referenciando em `settings.py`:

```python
JAZZMIN_SETTINGS = {
    "custom_css": "admin/custom.css",
}
```

### 2. Custom JavaScript

Adicione JavaScript customizado:

```python
JAZZMIN_SETTINGS = {
    "custom_js": "admin/custom.js",
}
```

### 3. UI Builder

Para desenvolvedores, ative o construtor de UI:

```python
JAZZMIN_SETTINGS = {
    "show_ui_builder": True,  # Mostra botão para ajustar UI
}
```

## Widgets de Estatísticas

### Tipos de Cards

**stat-card-primary** (Azul)
- Usado para: Informações gerais, posts, usuários

**stat-card-success** (Verde)
- Usado para: Métricas positivas, produtos, receita

**stat-card-warning** (Amarelo)
- Usado para: Alertas, pendências, pedidos

**stat-card-danger** (Vermelho)
- Usado para: Problemas, estoque zerado

**stat-card-info** (Ciano)
- Usado para: Informações secundárias, mensagens

**stat-card-purple** (Roxo)
- Usado para: Módulos, recursos especiais

## Permissões

### Acesso ao Dashboard

Requer permissão de staff:
```python
@staff_member_required
def dashboard_stats(request):
    ...
```

### Controle de Visibilidade

Esconda apps ou modelos específicos:

```python
JAZZMIN_SETTINGS = {
    "hide_apps": ["app_name"],
    "hide_models": ["app.Model"],
}
```

## Performance

### Otimizações Implementadas

1. **Queries otimizadas**: Uso de `select_related` e `prefetch_related`
2. **Agregações no banco**: Cálculos feitos pelo Django ORM
3. **Cache-ready**: Estrutura preparada para adicionar cache

### Adicionar Cache (Opcional)

Para melhor performance em produção, adicione cache às estatísticas:

```python
from django.core.cache import cache

@staff_member_required
def dashboard_stats(request):
    cache_key = 'dashboard_stats'
    context = cache.get(cache_key)

    if not context:
        # Calcular estatísticas
        context = {...}
        cache.set(cache_key, context, 300)  # 5 minutos

    return render(request, 'admin/dashboard_stats.html', context)
```

## Troubleshooting

### Admin não carrega com o novo tema

**Problema**: CSS do Jazzmin não é carregado

**Solução**:
```bash
python manage.py collectstatic
```

### Dashboard retorna 404

**Problema**: URLs não configuradas corretamente

**Solução**:
1. Verifique se 'dashboard' está em `INSTALLED_APPS`
2. Confirme que a URL está em `urlpatterns`
3. Reinicie o servidor

### Ícones não aparecem

**Problema**: Font Awesome não carregado

**Solução**:
```python
JAZZMIN_SETTINGS = {
    "use_google_fonts_cdn": True,  # Certifique-se que está True
}
```

### Estatísticas não atualizam

**Problema**: Cache ou queries incorretas

**Solução**:
1. Limpe o cache se estiver usando
2. Verifique as queries em `dashboard/views.py`
3. Teste as queries no shell Django

## Próximos Passos

### Melhorias Futuras

- [ ] Adicionar gráficos interativos (Chart.js ou D3.js)
- [ ] Exportação de relatórios (PDF, Excel)
- [ ] Filtros de data no dashboard
- [ ] Comparações período a período
- [ ] Notificações em tempo real
- [ ] Widgets personalizáveis por usuário
- [ ] Dashboard para módulos específicos
- [ ] Analytics avançados

### Integrações Sugeridas

- **Chart.js**: Gráficos de linha e barras
- **DataTables**: Tabelas interativas
- **Select2**: Dropdowns melhorados
- **Toastr**: Notificações toast
- **Fullcalendar**: Calendário de eventos

## Conclusão

O admin moderno do WordPy CMS oferece uma experiência profissional e intuitiva para gerenciar todos os aspectos do sistema. Com widgets de estatísticas em tempo real, design responsivo e personalização completa, você tem total controle sobre seu conteúdo.

Para mais informações sobre o Django Jazzmin, visite: https://django-jazzmin.readthedocs.io/
