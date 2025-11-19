from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ProductCategory, Product, ProductImage, Cart, CartItem, Order, OrderItem
)


class ProductImageInline(admin.TabularInline):
    """Inline para adicionar imagens aos produtos"""
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'order']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """Admin para categorias de produtos"""
    list_display = ['name', 'parent', 'is_active', 'order', 'product_count']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Informações Básicas', {
            'fields': ['name', 'slug', 'description']
        }),
        ('Hierarquia', {
            'fields': ['parent']
        }),
        ('Mídia', {
            'fields': ['image']
        }),
        ('Configurações', {
            'fields': ['is_active', 'order']
        }),
        ('Datas', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    def product_count(self, obj):
        """Exibe a quantidade de produtos na categoria"""
        count = obj.products.count()
        return format_html(
            '<span style="font-weight: bold;">{} produto(s)</span>',
            count
        )
    product_count.short_description = 'Produtos'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin para produtos"""
    list_display = [
        'name',
        'sku',
        'category',
        'price_display',
        'stock_quantity',
        'stock_status',
        'is_active',
        'is_featured',
        'views'
    ]
    list_filter = ['is_active', 'is_featured', 'stock_status', 'category', 'created_at']
    search_fields = ['name', 'sku', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['views', 'created_at', 'updated_at']

    fieldsets = [
        ('Informações Básicas', {
            'fields': ['name', 'slug', 'sku', 'category']
        }),
        ('Descrição', {
            'fields': ['short_description', 'description']
        }),
        ('Preços', {
            'fields': ['price', 'compare_price', 'cost_price']
        }),
        ('Estoque', {
            'fields': ['stock_quantity', 'stock_status']
        }),
        ('Mídia', {
            'fields': ['featured_image']
        }),
        ('Configurações', {
            'fields': ['is_active', 'is_featured', 'weight']
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description'],
            'classes': ['collapse']
        }),
        ('Estatísticas', {
            'fields': ['views', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    inlines = [ProductImageInline]

    actions = ['activate_products', 'deactivate_products', 'mark_as_featured']

    def price_display(self, obj):
        """Exibe o preço com formatação"""
        if obj.has_discount:
            return format_html(
                '<span style="color: green; font-weight: bold;">R$ {:.2f}</span> '
                '<span style="text-decoration: line-through; color: gray;">R$ {:.2f}</span> '
                '<span style="color: red;">(-{}%)</span>',
                obj.price,
                obj.compare_price,
                obj.discount_percentage
            )
        return format_html(
            '<span style="font-weight: bold;">R$ {:.2f}</span>',
            obj.price
        )
    price_display.short_description = 'Preço'

    def activate_products(self, request, queryset):
        """Action para ativar produtos"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} produto(s) ativado(s).')
    activate_products.short_description = 'Ativar produtos selecionados'

    def deactivate_products(self, request, queryset):
        """Action para desativar produtos"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} produto(s) desativado(s).')
    deactivate_products.short_description = 'Desativar produtos selecionados'

    def mark_as_featured(self, request, queryset):
        """Action para marcar produtos como destaque"""
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} produto(s) marcado(s) como destaque.')
    mark_as_featured.short_description = 'Marcar como destaque'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin para imagens de produtos"""
    list_display = ['product', 'image_preview', 'alt_text', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'alt_text']

    def image_preview(self, obj):
        """Exibe miniatura da imagem"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'


class CartItemInline(admin.TabularInline):
    """Inline para itens do carrinho"""
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']
    fields = ['product', 'quantity', 'price', 'total_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin para carrinhos"""
    list_display = ['user', 'total_items', 'subtotal_display', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'session_key']
    readonly_fields = ['created_at', 'updated_at']

    inlines = [CartItemInline]

    def subtotal_display(self, obj):
        """Exibe o subtotal do carrinho"""
        return format_html(
            '<span style="font-weight: bold;">R$ {:.2f}</span>',
            obj.subtotal
        )
    subtotal_display.short_description = 'Subtotal'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin para itens do carrinho"""
    list_display = ['cart', 'product', 'quantity', 'price', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['cart__user__username', 'product__name']
    readonly_fields = ['created_at', 'updated_at']


class OrderItemInline(admin.TabularInline):
    """Inline para itens do pedido"""
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']
    fields = ['product_name', 'product_sku', 'quantity', 'price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin para pedidos"""
    list_display = [
        'order_number',
        'user',
        'shipping_name',
        'status_display',
        'payment_status_display',
        'total_display',
        'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = [
        'order_number',
        'user__username',
        'user__email',
        'shipping_name',
        'shipping_email'
    ]
    readonly_fields = ['order_number', 'created_at', 'updated_at']

    fieldsets = [
        ('Informações do Pedido', {
            'fields': ['order_number', 'user', 'status', 'payment_status']
        }),
        ('Dados de Entrega', {
            'fields': [
                'shipping_name',
                'shipping_email',
                'shipping_phone',
                'shipping_address',
                'shipping_city',
                'shipping_state',
                'shipping_zipcode',
                'shipping_country'
            ]
        }),
        ('Valores', {
            'fields': ['subtotal', 'shipping_cost', 'tax', 'total']
        }),
        ('Observações', {
            'fields': ['notes'],
            'classes': ['collapse']
        }),
        ('Datas', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    inlines = [OrderItemInline]

    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']

    def status_display(self, obj):
        """Exibe o status com formatação colorida"""
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'

    def payment_status_display(self, obj):
        """Exibe o status de pagamento com formatação colorida"""
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'failed': 'red',
            'refunded': 'gray',
        }
        color = colors.get(obj.payment_status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_status_display()
        )
    payment_status_display.short_description = 'Pagamento'

    def total_display(self, obj):
        """Exibe o total do pedido"""
        return format_html(
            '<span style="font-weight: bold; color: green;">R$ {:.2f}</span>',
            obj.total
        )
    total_display.short_description = 'Total'

    def mark_as_processing(self, request, queryset):
        """Action para marcar como processando"""
        count = queryset.update(status='processing')
        self.message_user(request, f'{count} pedido(s) marcado(s) como processando.')
    mark_as_processing.short_description = 'Marcar como processando'

    def mark_as_shipped(self, request, queryset):
        """Action para marcar como enviado"""
        count = queryset.update(status='shipped')
        self.message_user(request, f'{count} pedido(s) marcado(s) como enviado.')
    mark_as_shipped.short_description = 'Marcar como enviado'

    def mark_as_delivered(self, request, queryset):
        """Action para marcar como entregue"""
        count = queryset.update(status='delivered')
        self.message_user(request, f'{count} pedido(s) marcado(s) como entregue.')
    mark_as_delivered.short_description = 'Marcar como entregue'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin para itens do pedido"""
    list_display = ['order', 'product_name', 'product_sku', 'quantity', 'price', 'total_price']
    list_filter = ['created_at']
    search_fields = ['order__order_number', 'product_name', 'product_sku']
    readonly_fields = ['created_at']
