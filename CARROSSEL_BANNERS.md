# Carrossel de Banners - WordPy CMS

## Visão Geral

O WordPy CMS agora possui um sistema de carrossel de banners totalmente funcional e responsivo, perfeito para destacar conteúdo importante na home ou em outras páginas.

## Características

### Funcionalidades Principais

✅ **Rolagem Automática** - Troca de banners a cada 5 segundos
✅ **Navegação Manual** - Setas esquerda/direita para controle
✅ **Indicadores (Dots)** - Navegação direta por pontos
✅ **Pausar ao Interagir** - Para automaticamente quando usuário clica
✅ **Responsivo** - Adapta altura e controles para mobile
✅ **Múltiplos Carrosséis** - Suporte a vários carrosséis na mesma página
✅ **Sem Dependências** - JavaScript puro, sem bibliotecas externas

### Visual

**Desktop (> 768px):**
- Altura: 500px
- Setas laterais grandes (50x50px)
- Fonte de título: 3rem

**Mobile (≤ 768px):**
- Altura: 400px
- Setas menores (40x40px)
- Fonte de título: 2rem
- Texto reduzido para melhor legibilidade

## Como Criar o Carrossel

### Método 1: Script Automático (Recomendado)

Execute o script que cria automaticamente:

```bash
python create_banner_carousel.py
```

**O que o script faz:**
1. Cria seção "Carrossel Principal" do tipo "Carrossel de Banners"
2. Adiciona automaticamente à página home (se configurada)
3. Define conteúdo padrão de exemplo

### Método 2: Manual via Admin

1. **Acesse Admin → Seções → Adicionar Seção**

2. **Configure os campos:**
   - **Nome**: Nome identificador (ex: "Carrossel Home")
   - **Tipo de Seção**: Selecione "Carrossel de Banners"
   - **Título**: Texto principal do primeiro banner
   - **Subtítulo**: Texto secundário (opcional)
   - **Conteúdo**: Descrição ou texto adicional
   - **Imagem**: Imagem de fundo do primeiro banner (opcional)
   - **Texto do Botão**: Ex: "Saiba Mais"
   - **Link do Botão**: URL de destino
   - **Cor de Fundo**: Escolha entre branco, claro ou escuro

3. **Salve a seção**

4. **Adicione a uma Página:**
   - Edite a página desejada
   - Role até "Seções da Página"
   - Clique em "Adicionar outra Seção da Página"
   - Selecione a seção do carrossel
   - Defina a ordem (0 = primeiro, aparece no topo)
   - Marque como "Ativa"
   - Salve

## Estrutura do Carrossel

### Slides Padrão

O carrossel vem com **3 slides** pré-configurados:

**Slide 1:** Configurável via admin
- Imagem: A que você configurou na seção
- Título: O título da seção
- Subtítulo: O subtítulo da seção
- Conteúdo: O conteúdo HTML
- Botão: Link configurável

**Slide 2:** Banner com gradiente rosa
- Gradiente: #f093fb → #f5576c
- Título: "Banner 2"
- Texto: "Conteúdo do segundo banner"

**Slide 3:** Banner com gradiente azul
- Gradiente: #4facfe → #00f2fe
- Título: "Banner 3"
- Texto: "Conteúdo do terceiro banner"

### Customizar Todos os Banners

Para personalizar completamente os 3 banners, edite o template:

**Arquivo:** `blog/templates/blog/sections/banner_carousel.html`

**Exemplo - Alterar o Slide 2:**

```html
<!-- Localize esta seção (aproximadamente linha 58) -->
<div class="carousel-slide" style="...">
    <div style="position: relative; width: 100%; height: 100%;">
        <!-- Altere o gradiente ou adicione uma imagem -->
        <img src="/media/banner2.jpg" alt="Banner 2" style="width: 100%; height: 100%; object-fit: cover;">

        <div style="...">
            <div style="text-align: center; color: white; ...">
                <!-- Altere o título -->
                <h2>Seu Novo Título</h2>

                <!-- Altere o texto -->
                <p>Seu novo conteúdo aqui</p>

                <!-- Adicione um botão se desejar -->
                <a href="/link/" style="...">Clique Aqui</a>
            </div>
        </div>
    </div>
</div>
```

## Controles do Carrossel

### Navegação por Setas

**Seta Esquerda (‹):**
- Retorna ao slide anterior
- Loop infinito (do primeiro volta ao último)

**Seta Direita (›):**
- Avança para próximo slide
- Loop infinito (do último vai ao primeiro)

### Navegação por Indicadores (Dots)

- **3 pontos** na parte inferior
- **Ponto ativo**: Branco e maior (scale 1.3)
- **Pontos inativos**: Brancos semi-transparentes
- **Clique direto**: Vai para o slide específico

### Autoplay

**Comportamento:**
- Avança automaticamente a cada **5 segundos**
- **Pausa** quando usuário interage (clica nas setas ou dots)
- **Resume** após 5 segundos de inatividade
- Sempre em loop infinito

## Customização Avançada

### Alterar Velocidade da Transição

No arquivo `banner_carousel.html`, localize:

```javascript
carousel.autoplayInterval = setInterval(() => {
    moveSlide(carouselId, 1);
}, 5000); // ← Altere este valor (em milissegundos)
```

**Exemplos:**
- `3000` = 3 segundos
- `7000` = 7 segundos
- `10000` = 10 segundos

### Alterar Altura do Carrossel

**Desktop:**
```html
<!-- Linha ~12 -->
<div class="carousel-slides" style="... height: 500px; ...">
```

**Mobile:**
```css
/* Linha ~131 */
@media (max-width: 768px) {
    .carousel-slides {
        height: 400px !important; /* ← Altere aqui */
    }
}
```

### Mudar Efeito de Transição

Atualmente usa **fade** (opacity). Para usar **slide**, altere:

```javascript
// Trocar opacity por transform
slide.style.transform = index === carousel.currentSlide
    ? 'translateX(0)'
    : 'translateX(100%)';
```

### Adicionar Mais Slides

No template `banner_carousel.html`, duplique um bloco de slide:

```html
<!-- Novo Slide 4 -->
<div class="carousel-slide" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; transition: opacity 0.5s ease-in-out;">
    <div style="position: relative; width: 100%; height: 100%;">
        <img src="/media/banner4.jpg" alt="Banner 4" style="width: 100%; height: 100%; object-fit: cover;">

        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center; color: white; max-width: 800px; padding: 2rem;">
                <h2>Título do Banner 4</h2>
                <p>Conteúdo do quarto banner</p>
            </div>
        </div>
    </div>
</div>
```

**Importante:** Atualize também:

1. **Total de slides** no JavaScript:
```javascript
carousels[carouselId] = {
    currentSlide: 0,
    totalSlides: 4, // ← Altere de 3 para 4
    autoplayInterval: null
};
```

2. **Indicadores** (dots):
```html
<div class="carousel-indicators" style="...">
    <span class="indicator active" onclick="goToSlide({{ section.id }}, 0)" ...></span>
    <span class="indicator" onclick="goToSlide({{ section.id }}, 1)" ...></span>
    <span class="indicator" onclick="goToSlide({{ section.id }}, 2)" ...></span>
    <span class="indicator" onclick="goToSlide({{ section.id }}, 3)" ...></span> <!-- Novo -->
</div>
```

## Exemplos de Uso

### Home Page Institucional

```
┌────────────────────────────────────┐
│     [CARROSSEL DE BANNERS]         │
│  ← Banner 1: Bem-vindo →           │
│     ● ○ ○                          │
├────────────────────────────────────┤
│  [Outras seções da página]         │
└────────────────────────────────────┘
```

### Landing Page de Produto

```
┌────────────────────────────────────┐
│  [CARROSSEL: Recursos do Produto]  │
│  ← Recurso 1 | Recurso 2 | 3 →     │
│     ○ ● ○                          │
├────────────────────────────────────┤
│  [CTA: Compre Agora]               │
├────────────────────────────────────┤
│  [Features]                        │
└────────────────────────────────────┘
```

### Portfolio

```
┌────────────────────────────────────┐
│  [CARROSSEL: Projetos Destaque]    │
│  ← Projeto A | B | C →             │
│     ○ ○ ●                          │
├────────────────────────────────────┤
│  [Galeria de Trabalhos]            │
└────────────────────────────────────┘
```

## Boas Práticas

### Imagens

✅ **Usar imagens otimizadas** (WebP ou JPEG comprimido)
✅ **Resolução recomendada**: 1920x500px (desktop)
✅ **Peso máximo**: 200KB por imagem
✅ **Formato**: WebP > JPEG > PNG

### Conteúdo

✅ **Título curto**: Máximo 10 palavras
✅ **Texto resumido**: 2-3 linhas no máximo
✅ **Call-to-action claro**: "Saiba Mais", "Compre Agora", etc.
✅ **Contraste**: Texto branco em fundos escuros ou vice-versa

### Performance

✅ **Lazy loading**: Adicionar `loading="lazy"` nas imagens
✅ **Autoplay pausado**: Já implementado ao interagir
✅ **Evitar vídeos**: Use imagens estáticas para melhor performance

## Troubleshooting

### Carrossel não rola automaticamente

**Verificar:**
1. JavaScript está carregando? (Veja console do navegador F12)
2. ID do carrossel está correto?
3. `DOMContentLoaded` foi disparado?

**Solução:**
- Limpe o cache do navegador (Ctrl+Shift+R)
- Verifique erros no console (F12)

### Setas não aparecem

**Problema:** Botões podem estar atrás de outros elementos

**Solução:**
```css
.carousel-prev,
.carousel-next {
    z-index: 100 !important; /* Aumentar z-index */
}
```

### Altura incorreta no mobile

**Verificar:** CSS responsivo

**Solução:**
```css
@media (max-width: 768px) {
    .carousel-slides {
        height: 400px !important;
    }
}
```

### Múltiplos carrosséis conflitam

**Não há problema!** O sistema gerencia múltiplos carrosséis automaticamente através de IDs únicos baseados no `section.id`.

## API JavaScript

### Funções Disponíveis

```javascript
// Mover slide (direção: -1 = anterior, 1 = próximo)
moveSlide(carouselId, direction);

// Ir para slide específico (índice: 0, 1, 2...)
goToSlide(carouselId, slideIndex);

// Atualizar visualização
updateSlides(carouselId);

// Controlar autoplay
startAutoplay(carouselId);
stopAutoplay(carouselId);
```

### Exemplo de Uso Programático

```javascript
// Pausar carrossel programaticamente
stopAutoplay(1); // ID da seção = 1

// Ir para terceiro slide
goToSlide(1, 2); // Índice 2 = terceiro slide

// Iniciar novamente
startAutoplay(1);
```

## Próximas Melhorias Possíveis

- [ ] Suporte a vídeos de fundo
- [ ] Efeito de transição slide (em vez de fade)
- [ ] Controle de velocidade via admin
- [ ] Model relacionado para múltiplos banners
- [ ] Thumbnail navigation
- [ ] Suporte a legendas
- [ ] Integração com galeria de mídia
- [ ] Tela cheia (fullscreen mode)

## Conclusão

O carrossel de banners torna o WordPy CMS ainda mais completo, permitindo criar páginas iniciais impactantes e profissionais sem precisar de código!

---

**Desenvolvido com Python e Django** 🐍 ❤️
