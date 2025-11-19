# Guia de Início Rápido - WordPy CMS

## Bem-vindo ao WordPy CMS! 🎉

Este guia irá ajudá-lo a começar rapidamente com o seu novo sistema de gerenciamento de conteúdo moderno.

## 📋 Pré-requisitos

- Python 3.12+
- Pip instalado
- Git (opcional)

## 🚀 Instalação

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados

As migrations já foram aplicadas, mas se necessário:

```bash
python manage.py migrate
```

### 3. Inicializar Módulos

```bash
python initialize_modules.py
```

Este script irá:
- ✅ Criar registros dos módulos (Blog, E-commerce, Mensagens)
- ✅ Configurar settings dos módulos
- ✅ Ativar todos os módulos

### 4. Criar Superusuário (se ainda não existe)

```bash
python manage.py createsuperuser
```

Siga as instruções para criar um usuário admin.

### 5. Coletar Arquivos Estáticos

```bash
python manage.py collectstatic
```

### 6. Iniciar o Servidor

```bash
python manage.py runserver
```

## 🎯 Primeiros Passos

### Acessar o Admin

1. Abra seu navegador em: **http://localhost:8000/admin/**
2. Faça login com suas credenciais
3. Você verá a interface moderna do Jazzmin!

### Explorar o Dashboard

1. No menu superior, clique em **"Dashboard"**
2. Ou acesse diretamente: **http://localhost:8000/admin/dashboard/stats/**
3. Visualize estatísticas em tempo real de:
   - Blog (posts, comentários, categorias)
   - E-commerce (produtos, pedidos, receita)
   - Mensagens (conversas, mensagens não lidas)
   - Usuários e Sistema

### Gerenciar Módulos

1. No menu lateral, navegue até **"Módulos"**
2. Clique em **"Módulos"** para ver todos os módulos
3. Ative/desative módulos conforme necessário
4. Configure settings específicos de cada módulo

## 📦 Módulos Disponíveis

### 1. Blog (Módulo Core)
- ✅ Criação e gestão de posts
- ✅ Categorias e tags
- ✅ Comentários com moderação
- ✅ Páginas estáticas
- ✅ Seções modulares
- ✅ Temas customizáveis
- ✅ Gestão de mídia

**Acesso**: Admin → Blog

### 2. E-commerce
- ✅ Catálogo de produtos
- ✅ Categorias hierárquicas
- ✅ Gestão de estoque
- ✅ Carrinho de compras
- ✅ Sistema de pedidos
- ✅ Gestão de preços e descontos

**Acesso**: Admin → Ecommerce

### 3. Mensagens
- ✅ Mensagens privadas
- ✅ Conversas em grupo
- ✅ Anexos em mensagens
- ✅ Confirmação de leitura
- ✅ Bloqueio de usuários
- ✅ Notificações

**Acesso**: Admin → Messaging

## 🎨 Personalizar o Admin

### Alterar Cores

Edite `wordpy_cms/settings.py`:

```python
JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-success",  # Mude para verde
    "sidebar": "sidebar-dark-success",       # Sidebar verde
}
```

**Opções de cores:**
- `primary` (azul)
- `success` (verde)
- `info` (ciano)
- `warning` (amarelo)
- `danger` (vermelho)
- `dark` (escuro)

### Ativar Modo Escuro

```python
JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
}
```

### Adicionar Logo Personalizado

1. Coloque seu logo em `media/` ou `static/`
2. Configure em `settings.py`:

```python
JAZZMIN_SETTINGS = {
    "site_logo": "caminho/para/logo.png",
}
```

## 📊 Usando o Dashboard

### Métricas Principais

O dashboard exibe automaticamente:

**Visão Geral:**
- Posts publicados
- Produtos ativos
- Pedidos pendentes
- Mensagens não lidas

**Por Módulo:**
- Estatísticas detalhadas de Blog
- Métricas de E-commerce (incluindo receita)
- Dados de Mensagens
- Informações de Usuários

**Listas Dinâmicas:**
- Posts mais populares (top 5)
- Pedidos recentes (últimos 5)
- Produtos mais vendidos (top 5)

**Atividade Recente:**
- Novos posts (7 dias)
- Novos pedidos (7 dias)
- Novas mensagens (7 dias)

### Atualizar Dados

O dashboard exibe dados em tempo real. Basta recarregar a página para ver as atualizações.

## 📝 Criar Conteúdo

### Criar um Post

1. Admin → Blog → Posts
2. Clique em "Adicionar Post"
3. Preencha título, conteúdo, categoria
4. Escolha status: Rascunho, Publicado ou Agendado
5. Adicione imagem destacada (opcional)
6. Configure SEO (meta título, descrição)
7. Salvar

### Criar um Produto

1. Admin → Ecommerce → Produtos
2. Clique em "Adicionar Produto"
3. Preencha informações básicas:
   - Nome, SKU, Categoria
   - Preço, Preço comparativo (para mostrar desconto)
   - Estoque
4. Adicione descrição detalhada
5. Faça upload de imagens
6. Configure SEO
7. Marque como "Ativo" e "Destaque" se desejado
8. Salvar

### Criar uma Página

1. Admin → Blog → Páginas
2. Clique em "Adicionar Página"
3. Defina título e conteúdo
4. Adicione seções modulares:
   - Hero/Banner
   - Texto com imagem
   - Call to Action
   - Features
   - Carrossel
   - E mais...
5. Configure ordem das seções
6. Marque "Mostrar no menu" se desejado
7. Salvar

## 🔧 Configurações Importantes

### Site Settings

Admin → Blog → Configurações do Site

Configure:
- Nome do site
- Logo e favicon
- Links de redes sociais
- Google Analytics ID
- Configurações de comentários
- Página inicial personalizada
- Tema ativo

### Módulos Settings

Admin → Módulos → Configurações de Módulos

Cada módulo tem suas próprias configurações:

**E-commerce:**
- Moeda (BRL)
- Símbolo da moeda (R$)
- Ativar carrinho
- Valor mínimo do pedido
- Produtos por página

**Mensagens:**
- Habilitar grupos
- Permitir anexos
- Tamanho máximo de anexo
- Ativar notificações
- Mensagens por página

## 🎓 Recursos Avançados

### Temas Customizados

1. Admin → Blog → Temas
2. Crie um novo tema com cores personalizadas
3. Configure:
   - Cores primárias, secundárias, accent
   - Tipografia (fontes, tamanhos)
   - Layout (bordas, sombras)
   - CSS customizado
4. Ative o tema em "Configurações do Site"

### Seções Modulares

Crie páginas dinâmicas com seções reutilizáveis:

1. Admin → Blog → Seções
2. Crie seções de diferentes tipos
3. Adicione conteúdo, imagens, botões
4. Associe seções às páginas
5. Ordene e ative/desative conforme necessário

### Permissões de Módulos

1. Admin → Módulos → Permissões de Módulos
2. Defina permissões granulares por usuário:
   - Pode visualizar
   - Pode criar
   - Pode editar
   - Pode deletar

## 📱 Mobile

O admin é totalmente responsivo:
- ✅ Interface adaptável para tablets
- ✅ Menu mobile-friendly
- ✅ Dashboard responsivo
- ✅ Formulários otimizados para touch

## 🔐 Segurança

### Boas Práticas

1. **Altere a SECRET_KEY em produção**
   ```python
   # settings.py
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

2. **Desative DEBUG em produção**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['seudominio.com']
   ```

3. **Configure HTTPS**
   ```python
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

4. **Backup regular do banco de dados**
   ```bash
   python manage.py dumpdata > backup.json
   ```

## 📚 Documentação

- **Sistema de Módulos**: `SISTEMA_MODULOS.md`
- **Admin Moderno**: `ADMIN_MODERNO.md`
- **README Principal**: `README.md`

## 🆘 Troubleshooting

### Admin não carrega

```bash
python manage.py collectstatic --noinput
python manage.py runserver
```

### Dashboard retorna erro

Verifique se o app 'dashboard' está em `INSTALLED_APPS` e reinicie o servidor.

### Estilos não aplicados

```bash
python manage.py collectstatic --clear --noinput
```

### Banco de dados com erro

```bash
python manage.py migrate
python initialize_modules.py
```

## 🎉 Próximos Passos

1. ✅ Explore todos os módulos
2. ✅ Crie conteúdo de teste
3. ✅ Personalize cores e tema
4. ✅ Configure settings do site
5. ✅ Adicione usuários e permissões
6. ✅ Explore o dashboard de estatísticas

## 💡 Dicas

- Use o **dashboard** para monitorar seu site em tempo real
- Aproveite as **actions em lote** no admin para operações múltiplas
- Use **tags** para organizar posts relacionados
- Configure **categorias hierárquicas** para melhor organização
- Ative **comentários** com moderação para engajamento
- Use **seções modulares** para criar páginas dinâmicas sem código

## 🌟 Recursos Destacados

### Interface Moderna
- Design limpo e profissional
- Ícones intuitivos
- Cores customizáveis
- Modo escuro

### Dashboard Poderoso
- Métricas em tempo real
- Widgets visuais
- Listas dinâmicas
- Filtros e buscas

### Sistema Modular
- Ative/desative recursos
- Configurações granulares
- Permissões por módulo
- Extensível

### E-commerce Completo
- Gestão de produtos
- Controle de estoque
- Sistema de pedidos
- Cálculo de receita

### Blog Profissional
- Posts com SEO
- Comentários moderados
- Páginas customizáveis
- Temas visuais

### Mensagens Integradas
- Chat privado e em grupo
- Anexos
- Notificações
- Bloqueio de usuários

## 🚀 Começe Agora!

Tudo está pronto! Acesse:

**Admin**: http://localhost:8000/admin/
**Dashboard**: http://localhost:8000/admin/dashboard/stats/

Divirta-se criando com o WordPy CMS! 🎨✨
