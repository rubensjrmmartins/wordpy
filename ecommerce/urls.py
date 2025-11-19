from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    # Produtos
    path('produtos/', views.product_list, name='product_list'),
    path('produto/<slug:slug>/', views.product_detail, name='product_detail'),

    # Categorias
    path('categoria/<slug:slug>/', views.category_products, name='category_products'),

    # Carrinho
    path('carrinho/', views.cart_view, name='cart_view'),
    path('carrinho/adicionar/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrinho/remover/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('carrinho/atualizar/<int:item_id>/', views.update_cart_item, name='update_cart_item'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('pedido/<int:order_id>/sucesso/', views.order_success, name='order_success'),
]
