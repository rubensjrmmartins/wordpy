from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Page, Section, PageSection
from ecommerce.models import Product, ProductCategory
from decimal import Decimal


class Command(BaseCommand):
    help = 'Cria uma página de Loja com seção de produtos e 15 produtos de exemplo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando criação da loja...'))

        # Obter ou criar o primeiro usuário (admin)
        try:
            admin_user = User.objects.filter(is_staff=True).first()
            if not admin_user:
                admin_user = User.objects.first()
            if not admin_user:
                self.stdout.write(self.style.ERROR('Nenhum usuário encontrado. Crie um superusuário primeiro.'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar usuário: {e}'))
            return

        # Criar ou obter categorias de produtos
        categories = []
        category_names = ['Eletrônicos', 'Roupas', 'Livros', 'Casa e Jardim', 'Esportes']
        for cat_name in category_names:
            try:
                # Tentar pegar por nome primeiro
                category = ProductCategory.objects.get(name=cat_name)
                self.stdout.write(self.style.WARNING(f'Categoria já existe: {cat_name}'))
            except ProductCategory.DoesNotExist:
                # Se não existir, criar nova
                category = ProductCategory.objects.create(
                    name=cat_name,
                    slug=slugify(cat_name),
                    description=f'Produtos de {cat_name}'
                )
                self.stdout.write(self.style.SUCCESS(f'Categoria criada: {cat_name}'))
            categories.append(category)

        # Criar 15 produtos de exemplo
        produtos_data = [
            {
                'name': 'Smartphone Galaxy X',
                'short_description': 'Smartphone de última geração com câmera de 108MP',
                'description': '<p>O Smartphone Galaxy X oferece o melhor em tecnologia móvel com processador octa-core, 8GB de RAM e 256GB de armazenamento.</p>',
                'price': Decimal('2999.00'),
                'sale_price': Decimal('2499.00'),
                'stock_quantity': 50,
                'category': categories[0],
                'sku': 'SMARTPHONE-001'
            },
            {
                'name': 'Notebook Pro 15',
                'short_description': 'Notebook profissional com Intel i7 e 16GB RAM',
                'description': '<p>Ideal para trabalho e entretenimento, com tela Full HD de 15.6 polegadas e SSD de 512GB.</p>',
                'price': Decimal('4999.00'),
                'sale_price': Decimal('4499.00'),
                'stock_quantity': 30,
                'category': categories[0],
                'sku': 'NOTEBOOK-001'
            },
            {
                'name': 'Fones Bluetooth Premium',
                'short_description': 'Fones com cancelamento de ruído e bateria de 30h',
                'description': '<p>Qualidade de som excepcional com tecnologia de cancelamento ativo de ruído.</p>',
                'price': Decimal('599.00'),
                'sale_price': Decimal('499.00'),
                'stock_quantity': 100,
                'category': categories[0],
                'sku': 'FONE-001'
            },
            {
                'name': 'Camiseta Básica Premium',
                'short_description': 'Camiseta 100% algodão em diversas cores',
                'description': '<p>Conforto e qualidade em uma camiseta básica que combina com tudo.</p>',
                'price': Decimal('79.90'),
                'sale_price': None,
                'stock_quantity': 200,
                'category': categories[1],
                'sku': 'CAMISA-001'
            },
            {
                'name': 'Jaqueta Jeans Clássica',
                'short_description': 'Jaqueta jeans resistente e estilosa',
                'description': '<p>Jaqueta jeans de alta qualidade, perfeita para qualquer ocasião.</p>',
                'price': Decimal('249.90'),
                'sale_price': Decimal('199.90'),
                'stock_quantity': 80,
                'category': categories[1],
                'sku': 'JAQUETA-001'
            },
            {
                'name': 'Tênis Esportivo Runner',
                'short_description': 'Tênis para corrida com tecnologia de amortecimento',
                'description': '<p>Desenvolvido para proporcionar máximo conforto durante suas corridas.</p>',
                'price': Decimal('399.00'),
                'sale_price': Decimal('349.00'),
                'stock_quantity': 120,
                'category': categories[4],
                'sku': 'TENIS-001'
            },
            {
                'name': 'Livro: Programação Python',
                'short_description': 'Guia completo de Python para iniciantes',
                'description': '<p>Aprenda Python do zero com exemplos práticos e exercícios.</p>',
                'price': Decimal('89.90'),
                'sale_price': None,
                'stock_quantity': 150,
                'category': categories[2],
                'sku': 'LIVRO-001'
            },
            {
                'name': 'Livro: Django Avançado',
                'short_description': 'Domine o framework Django',
                'description': '<p>Técnicas avançadas e boas práticas para desenvolvimento web com Django.</p>',
                'price': Decimal('99.90'),
                'sale_price': Decimal('79.90'),
                'stock_quantity': 100,
                'category': categories[2],
                'sku': 'LIVRO-002'
            },
            {
                'name': 'Cafeteira Elétrica Smart',
                'short_description': 'Cafeteira programável com timer',
                'description': '<p>Prepare seu café perfeito com controle de temperatura e tempo programável.</p>',
                'price': Decimal('299.00'),
                'sale_price': Decimal('249.00'),
                'stock_quantity': 60,
                'category': categories[3],
                'sku': 'CAFETEIRA-001'
            },
            {
                'name': 'Kit Panelas Inox',
                'short_description': 'Kit com 5 panelas de aço inoxidável',
                'description': '<p>Panelas de alta qualidade para sua cozinha, com cabos térmicos.</p>',
                'price': Decimal('699.00'),
                'sale_price': Decimal('599.00'),
                'stock_quantity': 40,
                'category': categories[3],
                'sku': 'PANELA-001'
            },
            {
                'name': 'Smartwatch Fitness Pro',
                'short_description': 'Relógio inteligente com monitor cardíaco',
                'description': '<p>Acompanhe sua saúde e atividades físicas com precisão.</p>',
                'price': Decimal('899.00'),
                'sale_price': Decimal('749.00'),
                'stock_quantity': 70,
                'category': categories[4],
                'sku': 'WATCH-001'
            },
            {
                'name': 'Bicicleta Mountain Bike',
                'short_description': 'Bike profissional para trilhas',
                'description': '<p>Suspensão dianteira, 21 marchas e quadro em alumínio.</p>',
                'price': Decimal('1899.00'),
                'sale_price': Decimal('1699.00'),
                'stock_quantity': 25,
                'category': categories[4],
                'sku': 'BIKE-001'
            },
            {
                'name': 'Tablet Pro 10"',
                'short_description': 'Tablet Android com tela Full HD',
                'description': '<p>Perfeito para estudos, trabalho e entretenimento.</p>',
                'price': Decimal('1499.00'),
                'sale_price': None,
                'stock_quantity': 45,
                'category': categories[0],
                'sku': 'TABLET-001'
            },
            {
                'name': 'Câmera Digital 4K',
                'short_description': 'Câmera profissional com gravação em 4K',
                'description': '<p>Capture momentos incríveis com qualidade profissional.</p>',
                'price': Decimal('3499.00'),
                'sale_price': Decimal('2999.00'),
                'stock_quantity': 20,
                'category': categories[0],
                'sku': 'CAMERA-001'
            },
            {
                'name': 'Mesa de Escritório Ergonômica',
                'short_description': 'Mesa ajustável para home office',
                'description': '<p>Mesa com regulagem de altura e design moderno.</p>',
                'price': Decimal('1299.00'),
                'sale_price': Decimal('999.00'),
                'stock_quantity': 35,
                'category': categories[3],
                'sku': 'MESA-001'
            },
        ]

        # Criar os produtos
        produtos_criados = []
        for produto_data in produtos_data:
            produto, created = Product.objects.get_or_create(
                sku=produto_data['sku'],
                defaults={
                    'name': produto_data['name'],
                    'slug': slugify(produto_data['name']),
                    'short_description': produto_data['short_description'],
                    'description': produto_data['description'],
                    'price': produto_data['price'],
                    'compare_price': produto_data.get('sale_price'),
                    'stock_quantity': produto_data['stock_quantity'],
                    'category': produto_data['category'],
                    'is_active': True,
                    'is_featured': False,
                }
            )
            produtos_criados.append(produto)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Produto criado: {produto.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Produto já existe: {produto.name}'))

        # Criar a seção de produtos
        section, created = Section.objects.get_or_create(
            name='Seção de Produtos - Loja',
            defaults={
                'section_type': 'products',
                'title': 'Nossos Produtos',
                'subtitle': 'Confira nossa seleção de produtos incríveis',
                'content': '<p>Oferecemos uma ampla variedade de produtos de alta qualidade para você.</p>',
                'background_color': 'light',
                'button_text': 'Ver Todos os Produtos',
                'button_link': '/produtos/',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Seção de produtos criada!'))
        else:
            self.stdout.write(self.style.WARNING('Seção de produtos já existe!'))

        # Criar a página Loja
        page, created = Page.objects.get_or_create(
            slug='loja',
            defaults={
                'title': 'Loja',
                'content': '<p>Bem-vindo à nossa loja! Aqui você encontra os melhores produtos.</p>',
                'author': admin_user,
                'is_published': True,
                'show_in_menu': True,
                'menu_order': 2,
                'meta_title': 'Loja - Produtos Incríveis',
                'meta_description': 'Confira nossa seleção de produtos de alta qualidade',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Página Loja criada!'))
        else:
            self.stdout.write(self.style.WARNING('Página Loja já existe!'))

        # Vincular a seção à página
        page_section, created = PageSection.objects.get_or_create(
            page=page,
            section=section,
            defaults={
                'order': 1,
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Seção vinculada à página!'))
        else:
            self.stdout.write(self.style.WARNING('Seção já estava vinculada à página!'))

        self.stdout.write(self.style.SUCCESS('\n=== Resumo ==='))
        self.stdout.write(self.style.SUCCESS(f'Produtos criados: {len([p for p in produtos_criados])}'))
        self.stdout.write(self.style.SUCCESS(f'Página: {page.title} ({page.slug})'))
        self.stdout.write(self.style.SUCCESS(f'Seção: {section.name}'))
        self.stdout.write(self.style.SUCCESS(f'\nAcesse a loja em: http://127.0.0.1:8000/page/loja/'))
        self.stdout.write(self.style.SUCCESS('Criação da loja concluída com sucesso!'))
