#!/usr/bin/env python
"""
Script para inicializar e ativar os módulos do WordPy CMS.
Este script cria registros dos módulos no sistema e os ativa.
"""

import os
import sys
import django

# Configurar o ambiente Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordpy_cms.settings')
django.setup()

from modules.models import Module


def create_modules():
    """Cria os módulos principais do sistema"""

    modules_data = [
        {
            'name': 'Blog',
            'slug': 'blog',
            'module_type': 'blog',
            'description': 'Módulo principal de blog do WordPy CMS. Gerencia posts, categorias, comentários e páginas.',
            'version': '1.0.0',
            'is_active': True,
            'is_core': True,
            'app_name': 'blog',
            'icon': 'fa fa-pencil',
            'order': 1
        },
        {
            'name': 'E-commerce',
            'slug': 'ecommerce',
            'module_type': 'ecommerce',
            'description': 'Módulo completo de e-commerce com produtos, categorias, carrinho de compras e gestão de pedidos.',
            'version': '1.0.0',
            'is_active': True,
            'is_core': False,
            'app_name': 'ecommerce',
            'icon': 'fa fa-shopping-cart',
            'order': 2
        },
        {
            'name': 'Mensagens',
            'slug': 'messaging',
            'module_type': 'messages',
            'description': 'Sistema de mensagens entre usuários com suporte a conversas privadas e em grupo, anexos e notificações.',
            'version': '1.0.0',
            'is_active': True,
            'is_core': False,
            'app_name': 'messaging',
            'icon': 'fa fa-comments',
            'order': 3
        },
    ]

    created_count = 0
    updated_count = 0

    for module_data in modules_data:
        module, created = Module.objects.get_or_create(
            slug=module_data['slug'],
            defaults=module_data
        )

        if created:
            created_count += 1
            print(f"[OK] Modulo '{module.name}' criado com sucesso!")
        else:
            # Atualiza os dados do módulo existente
            for key, value in module_data.items():
                setattr(module, key, value)
            module.save()
            updated_count += 1
            print(f"[OK] Modulo '{module.name}' atualizado!")

    return created_count, updated_count


def create_ecommerce_settings():
    """Cria configurações padrão para o módulo de e-commerce"""
    from modules.models import ModuleSettings

    try:
        ecommerce_module = Module.objects.get(slug='ecommerce')
    except Module.DoesNotExist:
        print("[AVISO] Modulo de e-commerce nao encontrado!")
        return 0

    settings_data = [
        {
            'key': 'currency',
            'value': 'BRL',
            'value_type': 'string',
            'description': 'Moeda padrão do e-commerce'
        },
        {
            'key': 'currency_symbol',
            'value': 'R$',
            'value_type': 'string',
            'description': 'Símbolo da moeda'
        },
        {
            'key': 'enable_cart',
            'value': 'true',
            'value_type': 'boolean',
            'description': 'Habilitar carrinho de compras'
        },
        {
            'key': 'min_order_value',
            'value': '0',
            'value_type': 'integer',
            'description': 'Valor mínimo do pedido'
        },
        {
            'key': 'products_per_page',
            'value': '12',
            'value_type': 'integer',
            'description': 'Número de produtos por página'
        },
    ]

    created_count = 0

    for setting_data in settings_data:
        setting, created = ModuleSettings.objects.get_or_create(
            module=ecommerce_module,
            key=setting_data['key'],
            defaults=setting_data
        )

        if created:
            created_count += 1
            print(f"  [OK] Configuracao '{setting.key}' criada para E-commerce")

    return created_count


def create_messaging_settings():
    """Cria configurações padrão para o módulo de mensagens"""
    from modules.models import ModuleSettings

    try:
        messaging_module = Module.objects.get(slug='messaging')
    except Module.DoesNotExist:
        print("[AVISO] Modulo de mensagens nao encontrado!")
        return 0

    settings_data = [
        {
            'key': 'enable_group_messages',
            'value': 'true',
            'value_type': 'boolean',
            'description': 'Habilitar mensagens em grupo'
        },
        {
            'key': 'enable_attachments',
            'value': 'true',
            'value_type': 'boolean',
            'description': 'Permitir anexos nas mensagens'
        },
        {
            'key': 'max_attachment_size',
            'value': '5',
            'value_type': 'integer',
            'description': 'Tamanho máximo de anexo em MB'
        },
        {
            'key': 'enable_notifications',
            'value': 'true',
            'value_type': 'boolean',
            'description': 'Habilitar notificações de mensagens'
        },
        {
            'key': 'messages_per_page',
            'value': '50',
            'value_type': 'integer',
            'description': 'Número de mensagens por página'
        },
    ]

    created_count = 0

    for setting_data in settings_data:
        setting, created = ModuleSettings.objects.get_or_create(
            module=messaging_module,
            key=setting_data['key'],
            defaults=setting_data
        )

        if created:
            created_count += 1
            print(f"  [OK] Configuracao '{setting.key}' criada para Mensagens")

    return created_count


def main():
    """Função principal"""
    print("=" * 70)
    print("INICIALIZAÇÃO DO SISTEMA DE MÓDULOS - WordPy CMS")
    print("=" * 70)
    print()

    # Criar módulos
    print("1. Criando/Atualizando módulos...")
    created, updated = create_modules()
    print(f"\n   Total: {created} módulo(s) criado(s), {updated} módulo(s) atualizado(s)\n")

    # Criar configurações do e-commerce
    print("2. Configurando módulo de E-commerce...")
    ecommerce_settings = create_ecommerce_settings()
    print(f"\n   Total: {ecommerce_settings} configuração(ões) criada(s)\n")

    # Criar configurações de mensagens
    print("3. Configurando módulo de Mensagens...")
    messaging_settings = create_messaging_settings()
    print(f"\n   Total: {messaging_settings} configuração(ões) criada(s)\n")

    # Listar módulos ativos
    print("=" * 70)
    print("MÓDULOS ATIVOS NO SISTEMA:")
    print("=" * 70)

    active_modules = Module.objects.filter(is_active=True).order_by('order')

    for module in active_modules:
        status = "CORE" if module.is_core else "ATIVO"
        print(f"\n  [{status}] {module.name} (v{module.version})")
        print(f"  |-- {module.description}")
        print(f"     App: {module.app_name} | Icone: {module.icon}")

    print("\n" + "=" * 70)
    print("[OK] Inicializacao concluida com sucesso!")
    print("=" * 70)
    print()
    print("Proximos passos:")
    print("  1. Execute: python manage.py runserver")
    print("  2. Acesse: http://localhost:8000/admin/")
    print("  3. Navegue ate 'Modulos' para gerenciar os modulos instalados")
    print()


if __name__ == '__main__':
    main()
