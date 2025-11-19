from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal


class ProductCategory(models.Model):
    """Categorias de produtos"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Nome')
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_('Slug')
    )

    description = models.TextField(
        blank=True,
        verbose_name=_('Descrição')
    )

    image = models.ImageField(
        upload_to='ecommerce/categories/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_('Imagem')
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='subcategories',
        verbose_name=_('Categoria Pai')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Ativa')
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Ordem')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )

    class Meta:
        verbose_name = _('Categoria de Produto')
        verbose_name_plural = _('Categorias de Produtos')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Produtos do e-commerce"""
    STOCK_STATUS = [
        ('in_stock', 'Em Estoque'),
        ('out_of_stock', 'Sem Estoque'),
        ('pre_order', 'Pré-venda'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name=_('Nome')
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_('Slug')
    )

    description = models.TextField(
        verbose_name=_('Descrição')
    )

    short_description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('Descrição Curta')
    )

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('Categoria')
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Preço')
    )

    compare_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Preço Comparativo'),
        help_text=_('Preço original (para exibir desconto)')
    )

    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Preço de Custo')
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('SKU'),
        help_text=_('Código único do produto')
    )

    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Quantidade em Estoque')
    )

    stock_status = models.CharField(
        max_length=20,
        choices=STOCK_STATUS,
        default='in_stock',
        verbose_name=_('Status de Estoque')
    )

    featured_image = models.ImageField(
        upload_to='ecommerce/products/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_('Imagem Principal')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Ativo')
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name=_('Produto em Destaque')
    )

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Peso (kg)')
    )

    views = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Visualizações')
    )

    # SEO
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Meta Título')
    )

    meta_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_('Meta Descrição')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )

    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def has_discount(self):
        """Verifica se o produto tem desconto"""
        return self.compare_price and self.compare_price > self.price

    @property
    def discount_percentage(self):
        """Calcula a porcentagem de desconto"""
        if self.has_discount:
            return int(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0


class ProductImage(models.Model):
    """Imagens adicionais dos produtos"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Produto')
    )

    image = models.ImageField(
        upload_to='ecommerce/products/%Y/%m/',
        verbose_name=_('Imagem')
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Texto Alternativo')
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Ordem')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )

    class Meta:
        verbose_name = _('Imagem de Produto')
        verbose_name_plural = _('Imagens de Produtos')
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - Imagem {self.order}"


class Cart(models.Model):
    """Carrinho de compras"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name=_('Usuário')
    )

    session_key = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Chave da Sessão'),
        help_text=_('Para carrinho de usuários não autenticados')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Ativo')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )

    class Meta:
        verbose_name = _('Carrinho')
        verbose_name_plural = _('Carrinhos')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Carrinho de {self.user.username}"

    @property
    def total_items(self):
        """Retorna o total de itens no carrinho"""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Retorna o subtotal do carrinho"""
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Itens do carrinho"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Carrinho')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Produto')
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_('Quantidade')
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Preço Unitário'),
        help_text=_('Preço no momento da adição ao carrinho')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Adicionado em')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )

    class Meta:
        verbose_name = _('Item do Carrinho')
        verbose_name_plural = _('Itens do Carrinho')
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        """Retorna o preço total do item (quantidade x preço)"""
        return self.quantity * self.price


class Order(models.Model):
    """Pedidos"""
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('failed', 'Falhou'),
        ('refunded', 'Reembolsado'),
    ]

    order_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Número do Pedido')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name=_('Usuário')
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending',
        verbose_name=_('Status do Pagamento')
    )

    # Informações de entrega
    shipping_name = models.CharField(
        max_length=200,
        verbose_name=_('Nome para Entrega')
    )

    shipping_email = models.EmailField(
        verbose_name=_('Email')
    )

    shipping_phone = models.CharField(
        max_length=20,
        verbose_name=_('Telefone')
    )

    shipping_address = models.CharField(
        max_length=300,
        verbose_name=_('Endereço')
    )

    shipping_city = models.CharField(
        max_length=100,
        verbose_name=_('Cidade')
    )

    shipping_state = models.CharField(
        max_length=100,
        verbose_name=_('Estado')
    )

    shipping_zipcode = models.CharField(
        max_length=20,
        verbose_name=_('CEP')
    )

    shipping_country = models.CharField(
        max_length=100,
        default='Brasil',
        verbose_name=_('País')
    )

    # Valores
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Subtotal')
    )

    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_('Custo de Envio')
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_('Imposto')
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Total')
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_('Observações')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )

    class Meta:
        verbose_name = _('Pedido')
        verbose_name_plural = _('Pedidos')
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido #{self.order_number}"

    def save(self, *args, **kwargs):
        """Gera número do pedido automaticamente"""
        if not self.order_number:
            import random
            import string
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Itens do pedido"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Pedido')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Produto')
    )

    product_name = models.CharField(
        max_length=200,
        verbose_name=_('Nome do Produto'),
        help_text=_('Armazena o nome do produto no momento da compra')
    )

    product_sku = models.CharField(
        max_length=100,
        verbose_name=_('SKU do Produto')
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_('Quantidade')
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Preço Unitário')
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Preço Total')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )

    class Meta:
        verbose_name = _('Item do Pedido')
        verbose_name_plural = _('Itens do Pedido')

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    def save(self, *args, **kwargs):
        """Calcula o preço total automaticamente"""
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)
