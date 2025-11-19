from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, ProductCategory, Cart, CartItem, Order


def product_list(request):
    """Lista de produtos"""
    products = Product.objects.filter(is_active=True).select_related('category').order_by('-created_at')

    # Busca
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )

    # Filtro por categoria
    category_slug = request.GET.get('categoria')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Categorias para o filtro
    categories = ProductCategory.objects.filter(is_active=True)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }

    return render(request, 'ecommerce/product_list.html', context)


def product_detail(request, slug):
    """Detalhes de um produto"""
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Incrementar visualizações
    product.views += 1
    product.save(update_fields=['views'])

    # Produtos relacionados (mesma categoria)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'ecommerce/product_detail.html', context)


def category_products(request, slug):
    """Produtos de uma categoria"""
    category = get_object_or_404(ProductCategory, slug=slug, is_active=True)
    products = Product.objects.filter(
        category=category,
        is_active=True
    ).order_by('-created_at')

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'ecommerce/category_products.html', context)


@login_required
def cart_view(request):
    """Visualizar carrinho"""
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_items = cart.items.select_related('product').all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }

    return render(request, 'ecommerce/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Adicionar produto ao carrinho"""
    product = get_object_or_404(Product, id=product_id, is_active=True)

    # Verificar estoque
    if product.stock_quantity <= 0:
        messages.error(request, 'Produto sem estoque disponível.')
        return redirect('ecommerce:product_detail', slug=product.slug)

    # Obter ou criar carrinho
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

    # Obter ou criar item no carrinho
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1, 'price': product.price}
    )

    if not created:
        # Se já existe, incrementar quantidade
        if cart_item.quantity < product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'{product.name} adicionado ao carrinho!')
        else:
            messages.warning(request, 'Quantidade máxima em estoque atingida.')
    else:
        messages.success(request, f'{product.name} adicionado ao carrinho!')

    return redirect('ecommerce:cart_view')


@login_required
def remove_from_cart(request, item_id):
    """Remover item do carrinho"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()

    messages.success(request, f'{product_name} removido do carrinho.')
    return redirect('ecommerce:cart_view')


@login_required
def update_cart_item(request, item_id):
    """Atualizar quantidade de item no carrinho"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removido do carrinho.')
        elif quantity <= cart_item.product.stock_quantity:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Carrinho atualizado.')
        else:
            messages.error(request, 'Quantidade indisponível em estoque.')

    return redirect('ecommerce:cart_view')


@login_required
def checkout(request):
    """Processo de checkout"""
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('ecommerce:product_list')

    if request.method == 'POST':
        # Criar pedido
        order = Order.objects.create(
            user=request.user,
            total=cart.get_total(),
            status='pending',
            payment_status='pending'
        )

        # Adicionar itens do carrinho ao pedido
        for cart_item in cart_items:
            order.items.create(
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price
            )

            # Atualizar estoque
            product = cart_item.product
            product.stock_quantity -= cart_item.quantity
            product.save()

        # Limpar carrinho
        cart_items.delete()
        cart.is_active = False
        cart.save()

        messages.success(request, 'Pedido realizado com sucesso!')
        return redirect('ecommerce:order_success', order_id=order.id)

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }

    return render(request, 'ecommerce/checkout.html', context)


@login_required
def order_success(request, order_id):
    """Página de sucesso do pedido"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order,
    }

    return render(request, 'ecommerce/order_success.html', context)
