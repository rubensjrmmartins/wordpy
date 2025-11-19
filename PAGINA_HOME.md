# Página Home Customizável - WordPy CMS

## Visão Geral

O WordPy CMS agora permite configurar uma página customizada como página inicial (home) do site, ao invés de sempre mostrar a lista de posts. Isso é perfeito para criar landing pages profissionais.

## Como Funciona

### Configuração nas Settings

1. Acesse `/admin/blog/sitesettings/1/change/`
2. Na seção "Configurações de Exibição"
3. Selecione uma página no campo "Página Inicial"
4. Salve

### Comportamento

- **Com página configurada:** A home (/) mostra a página selecionada com suas seções
- **Sem página configurada:** A home (/) mostra a lista de posts (comportamento padrão)

## URLs do Sistema

Após configurar a página home:

- `/` - Página inicial (home customizada ou lista de posts)
- `/blog/` - Lista de posts do blog (sempre disponível)
- `/post/<slug>/` - Detalhe de um post
- `/page/<slug>/` - Páginas estáticas
- `/admin/` - Painel administrativo

## Criar uma Página Home

### Opção 1: Script Automático

Execute o script que cria uma home completa com 4 seções:

```bash
python create_home_page.py
```

Isso cria:
- Página "Home" com slug `home`
- 4 seções modulares (Hero, Features, Texto com Imagem, CTA)
- Configuração automática como página inicial

### Opção 2: Manual

1. **Criar a Página:**
   - Vá em `/admin/blog/page/add/`
   - Preencha:
     - Título: "Home" (ou qualquer nome)
     - Slug: "home" (ou outro)
     - Deixe "Conteúdo" vazio (usaremos seções)
     - Marque "Publicado"
     - **Desmarque** "Mostrar no Menu" (o link Início já existe)
   - Salve

2. **Adicionar Seções:**
   - No formulário da página, role até "Seções da Página"
   - Adicione seções existentes ou crie novas
   - Defina a ordem (0, 1, 2, 3...)
   - Marque todas como "Ativa"
   - Salve

3. **Configurar como Home:**
   - Vá em `/admin/blog/sitesettings/1/change/`
   - Em "Página Inicial", selecione a página criada
   - Salve

## Estrutura da Home de Exemplo

A home criada pelo script tem esta estrutura:

```
Home (/)
├── Seção 1: Hero - Apresentação
│   ├── Título: "Bem-vindo ao WordPy CMS"
│   ├── Subtítulo: "Sistema de Gerenciamento..."
│   ├── Botão: "Explorar Recursos"
│   └── Fundo: Azul primário
│
├── Seção 2: Texto com Imagem - Por que escolher
│   ├── Título: "Por que escolher o WordPy?"
│   ├── Lista de benefícios
│   └── Fundo: Branco
│
├── Seção 3: Features - Recursos
│   ├── Grid de 6 recursos
│   ├── Ícones e descrições
│   └── Fundo: Cinza claro
│
└── Seção 4: CTA - Chamada final
    ├── Título: "Comece a Criar Hoje Mesmo"
    ├── Botão: "Acessar Painel Admin"
    └── Fundo: Escuro
```

## Navegação Atualizada

O menu principal agora tem:

```
[Logo] Início | Blog | Sobre | Contato
```

- **Início:** Leva para a home (/ - página customizada)
- **Blog:** Leva para lista de posts (/blog/)
- **Sobre/Contato:** Páginas no menu (se configuradas)

## Editar a Página Home

1. Acesse `/admin/blog/page/`
2. Clique na página "Home"
3. Você pode:
   - Editar o título e meta tags
   - Adicionar/remover seções
   - Reordenar seções (campo "Ordem")
   - Ativar/desativar seções
4. Salve e veja as mudanças em `/`

## Trocar a Página Home

Você pode ter várias páginas e trocar qual é a home:

1. Crie páginas diferentes (ex: "Home Verão", "Home Promoção")
2. Em SiteSettings, selecione qual página usar
3. A mudança é instantânea

## Desativar Página Home

Para voltar a mostrar lista de posts na home:

1. Acesse `/admin/blog/sitesettings/1/change/`
2. Em "Página Inicial", selecione "-------" (vazio)
3. Salve
4. A home (/) voltará a mostrar posts

## Template Usado

A página home usa o template `blog/home_page.html`:

- Renderiza todas as seções da página em ordem
- Adiciona um link para o blog no final (se há seções)
- Suporta fallback para conteúdo básico (se sem seções)

## Customizar o Template

Para customizar, edite:

```
blog/templates/blog/home_page.html
```

Você pode:
- Mudar o layout
- Adicionar widgets
- Inserir conteúdo fixo
- Modificar estilos

## Diferenças: Home vs Página Normal

| Aspecto | Página Home | Página Normal |
|---------|-------------|---------------|
| URL | `/` | `/page/<slug>/` |
| Menu | Não aparece | Pode aparecer |
| Template | `home_page.html` | `page_detail.html` |
| Link Blog | Sim (automático) | Não |
| Configuração | Via SiteSettings | Individual |

## Casos de Uso

### Landing Page Corporativa
- Hero com chamada principal
- Seção de benefícios
- Features/serviços
- Depoimentos
- CTA de contato

### Portfolio
- Hero com apresentação
- Galeria de trabalhos
- Sobre mim
- CTA para contato

### Site de Produto
- Hero do produto
- Recursos principais
- Comparação
- Preços
- CTA de compra

### Blog Pessoal
- Desmarque página home
- A home mostrará lista de posts
- Use páginas para About, Contact

## Comandos Úteis

### Criar home de exemplo
```bash
python create_home_page.py
```

### Ver qual página é a home (Django Shell)
```python
python manage.py shell

from blog.models import SiteSettings
settings = SiteSettings.get_settings()
print(f"Home: {settings.home_page}")
```

### Limpar configuração de home
```python
from blog.models import SiteSettings
settings = SiteSettings.get_settings()
settings.home_page = None
settings.save()
```

## Boas Práticas

1. **Use seções:** Não coloque conteúdo no campo "Conteúdo" da página, use seções modulares

2. **Não adicione ao menu:** A home já tem link "Início", não precisa aparecer no menu

3. **SEO:** Configure meta_title e meta_description apropriados

4. **Performance:** Não adicione muitas seções pesadas (imagens grandes)

5. **Mobile:** Teste em dispositivos móveis - as seções são responsivas

6. **Atualize regularmente:** Mude as seções conforme campanhas/sazonalidade

## Troubleshooting

### Home não aparece diferente

**Problema:** Configurei página mas a home ainda mostra posts

**Solução:**
- Verifique se a página está marcada como "Publicado"
- Verifique se SiteSettings.home_page está configurado
- Limpe cache do navegador (Ctrl+F5)

### Seções não aparecem

**Problema:** Página home está vazia

**Solução:**
- Verifique se a página tem seções vinculadas
- Verifique se as seções estão marcadas como "Ativa"
- Verifique a ordem das seções

### Link do menu quebrado

**Problema:** Link "Início" não funciona

**Solução:**
- Verifique se a URL `blog:home` existe em `blog/urls.py`
- Execute `python manage.py check`

## Exemplos de Conteúdo

### Hero Impactante
```
Tipo: Hero
Título: Transforme Sua Presença Online
Subtítulo: Crie sites profissionais em minutos
Botão: Começar Agora
Fundo: Primária (azul)
```

### Recursos em Grid
```
Tipo: Features
Título: O Que Oferecemos
Conteúdo: [HTML com grid de cards]
Fundo: Cinza claro
```

### CTA de Conversão
```
Tipo: CTA
Título: Pronto para Começar?
Subtítulo: Junte-se a milhares de usuários
Botão: Criar Conta Grátis
Fundo: Escuro
```

---

**Atualizado em:** 2025-11-18
**Versão:** 1.1.0
