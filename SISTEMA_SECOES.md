# Sistema de Seções - WordPy CMS

## Visão Geral

O sistema de seções permite criar páginas modulares e complexas no WordPy CMS, similar aos page builders modernos. Com ele, você pode criar páginas compostas por diferentes tipos de seções reutilizáveis.

## Tipos de Seções Disponíveis

### 1. Hero/Banner
- **Uso:** Cabeçalho principal da página com call-to-action
- **Recursos:**
  - Título e subtítulo grandes
  - Imagem de fundo opcional
  - Botão de call-to-action
  - Cores de fundo personalizáveis

### 2. Texto
- **Uso:** Seções de conteúdo textual
- **Recursos:**
  - Título e subtítulo
  - Conteúdo rico (HTML/texto formatado)
  - Botão opcional
  - Centralizadoautomaticamente

### 3. Texto com Imagem
- **Uso:** Conteúdo com imagem ao lado
- **Recursos:**
  - Título, subtítulo e conteúdo
  - Imagem posicionada à esquerda ou direita
  - Botão call-to-action
  - Layout responsivo (em mobile fica em coluna)

### 4. Call to Action (CTA)
- **Uso:** Chamadas para ação destacadas
- **Recursos:**
  - Design chamativo centralizado
  - Fundo colorido
  - Botão grande e destacado
  - Ideal para conversões

### 5. Features/Recursos
- **Uso:** Apresentar recursos ou benefícios
- **Recursos:**
  - Layout flexível
  - Suporte a HTML customizado
  - Ideal para cards de features
  - Imagem opcional

### 6. HTML Customizado
- **Uso:** Seções totalmente personalizadas
- **Recursos:**
  - HTML livre
  - Máxima flexibilidade
  - Para layouts complexos

## Como Usar

### Criar uma Seção

1. Acesse o admin: `/admin/blog/section/`
2. Clique em "Adicionar Seção"
3. Preencha:
   - **Nome da Seção:** Nome interno (não aparece no site)
   - **Tipo de Seção:** Escolha o tipo desejado
   - **Título:** Título principal da seção
   - **Subtítulo:** Texto complementar
   - **Conteúdo:** Conteúdo rico usando o editor
   - **Imagem:** Upload de imagem (se aplicável)
   - **Botão:** Texto e link do botão (opcional)
   - **Cor de Fundo:** Escolha o estilo visual
4. Salve a seção

### Adicionar Seções a uma Página

#### Método 1: Inline no Admin da Página

1. Acesse `/admin/blog/page/`
2. Edite ou crie uma página
3. Role até "Seções da Página" (no final do formulário)
4. Clique em "Adicionar outra Seção da Página"
5. Selecione a seção criada
6. Defina a ordem (números menores aparecem primeiro)
7. Marque como "Ativa"
8. Salve a página

#### Método 2: Script Automatizado

Use o script `create_sample_sections.py` como exemplo:

```python
from blog.models import Page, Section, PageSection

# Obter página
page = Page.objects.get(slug='minha-pagina')

# Obter seção
section = Section.objects.get(name='Minha Seção')

# Vincular
PageSection.objects.create(
    page=page,
    section=section,
    order=0,
    is_active=True
)
```

## Cores de Fundo Disponíveis

- **Branco:** Fundo branco limpo
- **Cinza Claro:** Fundo suave (#f5f5f5)
- **Escuro:** Fundo escuro (#2c3e50) com texto branco
- **Cor Primária:** Azul (#3498db) com texto branco
- **Cor Secundária:** Cinza escuro (#34495e) com texto branco

## Estrutura das Seções

### Página com Seções

Uma página pode ter:
- **Conteúdo principal:** Editado no campo "Conteúdo" da página
- **Seções adicionais:** Adicionadas via PageSection

As seções aparecem **após** o conteúdo principal (se houver).

### Ordem das Seções

As seções são exibidas em ordem crescente do campo "Ordem":
- Ordem 0: Primeira seção
- Ordem 1: Segunda seção
- Ordem 2: Terceira seção
- etc.

## Exemplos de Uso

### Landing Page

```
Página: "Produto X"
├── Seção 1 (Ordem 0): Hero - Apresentação do produto
├── Seção 2 (Ordem 1): Texto com Imagem - Benefícios
├── Seção 3 (Ordem 2): Features - Recursos principais
└── Seção 4 (Ordem 3): CTA - Compre agora
```

### Página Institucional

```
Página: "Sobre Nós"
├── Seção 1 (Ordem 0): Hero - Quem somos
├── Seção 2 (Ordem 1): Texto - Nossa história
├── Seção 3 (Ordem 2): Texto com Imagem - Missão e visão
└── Seção 4 (Ordem 3): Features - Valores da empresa
```

### Página de Serviços

```
Página: "Nossos Serviços"
├── Seção 1 (Ordem 0): Hero - Introdução
├── Seção 2 (Ordem 1): Features - Serviço A
├── Seção 3 (Ordem 2): Features - Serviço B
├── Seção 4 (Ordem 3): Features - Serviço C
└── Seção 5 (Ordem 4): CTA - Entre em contato
```

## Personalização Avançada

### CSS Customizado

Use o campo "Classe CSS Customizada" para adicionar classes próprias:

```html
<!-- No campo CSS Customizada -->
minha-secao-especial

<!-- Adicione no seu CSS -->
.minha-secao-especial {
    background: linear-gradient(to right, #667eea 0%, #764ba2 100%);
}
```

### HTML Customizado

Para layouts complexos, use o tipo "HTML Customizado":

```html
<div style="display: flex; gap: 2rem;">
    <div style="flex: 1;">
        <h3>Coluna 1</h3>
        <p>Conteúdo da primeira coluna</p>
    </div>
    <div style="flex: 1;">
        <h3>Coluna 2</h3>
        <p>Conteúdo da segunda coluna</p>
    </div>
</div>
```

## Reutilização de Seções

Seções são **reutilizáveis**! Você pode usar a mesma seção em várias páginas:

1. Crie uma seção "Rodapé Newsletter"
2. Adicione em todas as páginas de produtos
3. Altere o texto uma vez
4. Todas as páginas são atualizadas automaticamente

## Templates das Seções

Os templates ficam em `blog/templates/blog/sections/`:

- `hero.html` - Hero/Banner
- `text.html` - Texto
- `text_image.html` - Texto com Imagem
- `cta.html` - Call to Action
- `features.html` - Features/Recursos
- `html.html` - HTML Customizado
- `section_renderer.html` - Renderizador principal

Para customizar, edite os templates diretamente.

## Comandos Úteis

### Criar Seções de Exemplo

```bash
python create_sample_sections.py
```

Este comando cria 4 seções de exemplo e adiciona à página "Sobre".

### Ver Seções de uma Página (Django Shell)

```python
python manage.py shell

from blog.models import Page
page = Page.objects.get(slug='sobre')
for ps in page.page_sections.all():
    print(f"{ps.order}: {ps.section.name} ({ps.section.section_type})")
```

### Remover Todas as Seções de uma Página

```python
from blog.models import Page, PageSection
page = Page.objects.get(slug='minha-pagina')
PageSection.objects.filter(page=page).delete()
```

## Dicas e Boas Práticas

1. **Nomeie seções de forma descritiva:** Use nomes como "Hero - Homepage" ao invés de "Seção 1"

2. **Use ordem com espaçamento:** Use 10, 20, 30 ao invés de 1, 2, 3 para facilitar inserções futuras

3. **Teste em mobile:** O layout é responsivo, mas sempre teste em diferentes tamanhos

4. **Reutilize seções:** Crie uma vez, use em várias páginas

5. **Mantenha seções focadas:** Cada seção deve ter um propósito claro

6. **Use cores com moderação:** Alterne cores de fundo para criar contraste visual

7. **Otimize imagens:** Redimensione imagens antes do upload para melhor performance

## Limitações Conhecidas

- ⚠️ Não há preview no admin (é necessário salvar para ver)
- ⚠️ Drag-and-drop para reordenar não está disponível (use campo "Ordem")
- ⚠️ Galeria de imagens e cards ainda não têm templates dedicados (use HTML customizado)

## Próximos Passos

Melhorias planejadas:
- [ ] Preview de seções no admin
- [ ] Drag-and-drop para reordenar
- [ ] Templates para galeria e cards
- [ ] Biblioteca de seções prontas
- [ ] Duplicar seções facilmente
- [ ] Exportar/importar seções

---

**Atualizado em:** 2025-11-18
