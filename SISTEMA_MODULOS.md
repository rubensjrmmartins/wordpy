# Sistema de Gerenciamento de Módulos - WordPy CMS

## Visão Geral

O WordPy CMS agora possui um sistema completo de gerenciamento de módulos que permite ativar/desativar funcionalidades dinamicamente. O sistema foi implementado com os seguintes módulos:

1. **Blog** (Módulo Core) - Sistema de blog já existente
2. **E-commerce** - Sistema completo de loja virtual
3. **Mensagens** - Sistema de mensagens entre usuários

## Estrutura do Sistema

### 1. App `modules` - Sistema Base

O app `modules` gerencia todos os módulos do sistema através de três modelos principais:

#### Modelo `Module`
Representa cada módulo instalado no sistema.

**Campos principais:**
- `name`: Nome do módulo
- `slug`: Identificador único
- `module_type`: Tipo do módulo (ecommerce, messages, blog, etc.)
- `description`: Descrição detalhada
- `version`: Versão do módulo
- `is_active`: Define se o módulo está ativo
- `is_core`: Módulos core não podem ser desativados
- `app_name`: Nome do app Django correspondente
- `icon`: Ícone para exibição no admin
- `order`: Ordem de exibição

**Métodos:**
- `activate()`: Ativa o módulo
- `deactivate()`: Desativa o módulo (se não for core)

#### Modelo `ModuleSettings`
Armazena configurações específicas de cada módulo.

**Campos principais:**
- `module`: Referência ao módulo
- `key`: Nome da configuração
- `value`: Valor da configuração
- `value_type`: Tipo do valor (string, integer, boolean, json)
- `description`: Descrição da configuração

**Método:**
- `get_value()`: Retorna o valor convertido para o tipo apropriado

#### Modelo `ModulePermission`
Gerencia permissões de usuários por módulo.

**Campos principais:**
- `module`: Referência ao módulo
- `user`: Usuário
- `can_view`: Permissão de visualização
- `can_create`: Permissão de criação
- `can_edit`: Permissão de edição
- `can_delete`: Permissão de exclusão

### 2. Módulo E-commerce

Sistema completo de loja virtual com os seguintes modelos:

#### `ProductCategory`
- Categorias hierárquicas de produtos
- Suporte a subcategorias (campo `parent`)
- Ordenação personalizável

#### `Product`
- Informações completas do produto
- SKU único
- Preços (normal, comparativo, custo)
- Gestão de estoque
- Imagens
- Campos SEO
- Contador de visualizações
- Propriedades calculadas:
  - `has_discount`: Verifica se tem desconto
  - `discount_percentage`: Calcula % de desconto

#### `ProductImage`
- Imagens adicionais dos produtos
- Ordenação personalizada
- Texto alternativo para SEO

#### `Cart`
- Carrinho de compras
- Suporte a usuários autenticados e anônimos (via session_key)
- Propriedades:
  - `total_items`: Total de itens
  - `subtotal`: Valor total

#### `CartItem`
- Itens do carrinho
- Guarda o preço no momento da adição
- Propriedade `total_price`

#### `Order`
- Pedidos completos
- Geração automática de número do pedido
- Status do pedido e pagamento
- Informações de entrega completas
- Cálculo de valores (subtotal, frete, impostos, total)

#### `OrderItem`
- Itens do pedido
- Guarda informações do produto no momento da compra
- Cálculo automático do preço total

**Configurações do módulo:**
- `currency`: BRL
- `currency_symbol`: R$
- `enable_cart`: true
- `min_order_value`: 0
- `products_per_page`: 12

### 3. Módulo Mensagens

Sistema de mensagens privadas e em grupo:

#### `Conversation`
- Conversas privadas ou em grupo
- Múltiplos participantes
- Propriedades:
  - `last_message`: Última mensagem da conversa
  - `unread_count`: Mensagens não lidas

#### `Message`
- Mensagens individuais
- Suporte a anexos
- Respostas a mensagens (threading)
- Status de leitura
- Método `mark_as_read()`

#### `MessageReadReceipt`
- Confirmações de leitura para conversas em grupo
- Rastreamento individual por usuário

#### `BlockedUser`
- Bloqueio de usuários
- Motivo do bloqueio
- Impede envio de mensagens

#### `MessageNotification`
- Notificações de novas mensagens
- Status de leitura
- Método `mark_as_read()`

**Configurações do módulo:**
- `enable_group_messages`: true
- `enable_attachments`: true
- `max_attachment_size`: 5 (MB)
- `enable_notifications`: true
- `messages_per_page`: 50

## Interface Admin

### Admin de Módulos

**Funcionalidades:**
- Listagem com status visual (ativo/inativo, core)
- Filtros por tipo, status e data
- Busca por nome, slug, descrição
- Auto-preenchimento de slug
- Edição inline de configurações e permissões
- Actions:
  - Ativar módulos
  - Desativar módulos (exceto core)

### Admin de E-commerce

**ProductCategory:**
- Contador de produtos
- Suporte a hierarquia

**Product:**
- Exibição de preço com desconto visual
- Gestão de imagens inline
- Campos organizados por seção
- Actions: ativar, desativar, marcar como destaque

**Order:**
- Status visual com cores
- Itens inline
- Actions para atualizar status

### Admin de Mensagens

**Conversation:**
- Visualização de participantes
- Prévia da última mensagem
- Mensagens inline (somente visualização)

**Message:**
- Status de leitura visual
- Indicador de anexo
- Actions: marcar como lida/não lida

## Instalação e Uso

### 1. Inicialização do Sistema

Execute o script de inicialização para criar os módulos e configurações:

```bash
python initialize_modules.py
```

Este script irá:
- Criar registros dos 3 módulos
- Configurar o módulo de e-commerce
- Configurar o módulo de mensagens
- Ativar todos os módulos

### 2. Acessar o Admin

```bash
python manage.py runserver
```

Acesse: http://localhost:8000/admin/

### 3. Gerenciar Módulos

No admin Django, navegue até a seção "Módulos" para:
- Visualizar módulos instalados
- Ativar/desativar módulos
- Configurar settings de cada módulo
- Gerenciar permissões de usuários

## Arquitetura de Arquivos

```
wordpy/
├── modules/                    # Sistema de gerenciamento
│   ├── models.py              # Module, ModuleSettings, ModulePermission
│   ├── admin.py               # Interface admin
│   └── migrations/
│
├── ecommerce/                  # Módulo de e-commerce
│   ├── models.py              # 7 modelos
│   ├── admin.py               # Interface admin completa
│   └── migrations/
│
├── messaging/                  # Módulo de mensagens
│   ├── models.py              # 5 modelos
│   ├── admin.py               # Interface admin completa
│   └── migrations/
│
├── initialize_modules.py       # Script de inicialização
└── SISTEMA_MODULOS.md         # Esta documentação
```

## Apps Registrados no settings.py

```python
INSTALLED_APPS = [
    ...
    # Sistema de Módulos
    'modules',
    # Módulos
    'ecommerce',
    'messaging',
]
```

## Próximos Passos

### Funcionalidades a Implementar

**E-commerce:**
- [ ] Views e templates para catálogo de produtos
- [ ] Sistema de carrinho funcional
- [ ] Checkout e finalização de pedidos
- [ ] Integração com gateways de pagamento
- [ ] Cálculo de frete
- [ ] Cupons de desconto

**Mensagens:**
- [ ] Interface de chat em tempo real
- [ ] Sistema de notificações push
- [ ] Upload de anexos
- [ ] Busca de mensagens
- [ ] Arquivamento de conversas

**Sistema de Módulos:**
- [ ] API REST para gerenciamento de módulos
- [ ] Sistema de hooks/eventos
- [ ] Dependências entre módulos
- [ ] Instalação/desinstalação automática
- [ ] Marketplace de módulos
- [ ] Versionamento e atualizações

## Modelos de Dados

### Resumo de Modelos por App

**modules (3 modelos):**
- Module
- ModuleSettings
- ModulePermission

**ecommerce (7 modelos):**
- ProductCategory
- Product
- ProductImage
- Cart
- CartItem
- Order
- OrderItem

**messaging (5 modelos):**
- Conversation
- Message
- MessageReadReceipt
- BlockedUser
- MessageNotification

**Total: 15 novos modelos**

## Segurança

### Considerações Implementadas

1. **Módulos Core**: Não podem ser desativados
2. **Permissões por Módulo**: Sistema granular de permissões
3. **Validações**:
   - Preços mínimos (validators)
   - SKUs únicos
   - Unique constraints em relacionamentos
4. **Bloqueio de Usuários**: Impede spam/assédio

### Recomendações

- Configure permissões adequadas no admin
- Implemente rate limiting para mensagens
- Adicione verificações de estoque antes de finalizar pedidos
- Implemente logs de auditoria

## Suporte e Manutenção

### Comandos Úteis

```bash
# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Inicializar módulos
python initialize_modules.py

# Criar superusuário
python manage.py createsuperuser
```

### Logs e Debug

Para debug, ative o modo DEBUG em `settings.py`:
```python
DEBUG = True
```

## Contribuindo

Para adicionar um novo módulo:

1. Crie um novo app Django:
   ```bash
   python manage.py startapp nome_modulo
   ```

2. Adicione aos INSTALLED_APPS em `settings.py`

3. Crie os modelos necessários

4. Registre no admin

5. Crie migrations:
   ```bash
   python manage.py makemigrations nome_modulo
   python manage.py migrate
   ```

6. Adicione ao script `initialize_modules.py`

7. Execute a inicialização:
   ```bash
   python initialize_modules.py
   ```

## Conclusão

O sistema de gerenciamento de módulos do WordPy CMS fornece uma base sólida e extensível para adicionar novas funcionalidades. Com os módulos de E-commerce e Mensagens já implementados, o sistema está pronto para ser expandido com novos recursos conforme necessário.
