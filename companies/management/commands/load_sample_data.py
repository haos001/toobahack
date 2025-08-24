from django.core.management.base import BaseCommand
from companies.models import Category, Company


class Command(BaseCommand):
    help = 'Load sample data for the charity showcase'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'Рестораны и кафе', 'slug': 'restaurants'},
            {'name': 'Продуктовые магазины', 'slug': 'grocery'},
            {'name': 'Одежда и обувь', 'slug': 'fashion'},
            {'name': 'Электроника и техника', 'slug': 'electronics'},
            {'name': 'Хозтовары и быт', 'slug': 'household'},
            {'name': 'Строительство', 'slug': 'construction'},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create companies
        companies_data = [
            {
                'name': 'Магазин одежды "ZARA"',
                'description': 'Популярный бренд модной одежды для мужчин и женщин. Актуальные коллекции и доступные цены.',
                'address': 'г. Махачкала, ТРК "Леон", 2 этаж',
                'phone': '+7 (8722) 93-45-67',
                'email': 'makhachkala@zara.com',
                'website': 'https://zara.com',
                'charity_description': 'Передаем одежду из прошлых коллекций в детские дома и социальные центры. Организуем акции для малоимущих семей.',
                'charity_amount': 150000,
                'charity_frequency': 'monthly',
                'category_slug': 'fashion',
                'latitude': 42.9849,
                'longitude': 47.5047,
                'is_verified': True,
            },
            {
                'name': 'Кофейня "Coffee Bean"',
                'description': 'Сеть уютных кофеен с качественным кофе и свежей выпечкой. Популярное место встреч в Махачкале.',
                'address': 'г. Махачкала, пр. Имама Шамиля, 32',
                'phone': '+7 (8722) 67-12-34',
                'email': 'info@coffeebean-msk.ru',
                'website': 'https://coffeebean.ru',
                'charity_description': 'Организуем благотворительные кофе-брейки для медработников. Поддерживаем акции помощи пожилым людям бесплатными обедами.',
                'charity_amount': 95000,
                'charity_frequency': 'monthly',
                'category_slug': 'restaurants',
                'latitude': 42.9743,
                'longitude': 47.5024,
                'is_verified': True,
            },
            {
                'name': 'Сеть супермаркетов "Семья"',
                'description': 'Крупнейшая розничная сеть Дагестана с широким ассортиментом продуктов питания и товаров первой необходимости.',
                'address': 'г. Махачкала, пр. Имама Шамиля, 67',
                'phone': '+7 (8722) 51-20-30',
                'email': 'info@semya-market.ru',
                'website': 'https://semya-market.ru',
                'charity_description': 'Ежемесячно передаем продуктовые наборы нуждающимся семьям. Предоставляем скидки пенсионерам и многодетным.',
                'charity_amount': 350000,
                'charity_frequency': 'monthly',
                'category_slug': 'grocery',
                'latitude': 42.9739,
                'longitude': 47.5125,
                'is_verified': True,
            },
            {
                'name': 'Ресторан "Жи есть"',
                'description': 'Популярная сеть ресторанов быстрого питания в Махачкале с домашней кухней и демократичными ценами.',
                'address': 'г. Махачкала, ул. Ярагского, 75',
                'phone': '+7 (8722) 94-33-22',
                'email': 'info@ji-est.ru',
                'website': 'https://ji-est.ru',
                'charity_description': 'Организуем бесплатные обеды для малообеспеченных семей и пожилых людей. Участвуем в благотворительных акциях.',
                'charity_amount': 180000,
                'charity_frequency': 'tooba_collections',
                'category_slug': 'restaurants',
                'latitude': 42.9821,
                'longitude': 47.5186,
                'is_verified': True,
            },
            {
                'name': 'Строительная группа "Дагестанские дороги"',
                'description': 'Ведущая дорожно-строительная компания Республики Дагестан, специализирующаяся на инфраструктурных проектах.',
                'address': 'г. Махачкала, ул. Магомета Гаджиева, 12',
                'phone': '+7 (8722) 55-77-88',
                'email': 'info@dagdorogi.ru',
                'website': 'https://dagdorogi.ru',
                'charity_description': 'Безвозмездно ремонтируем дороги к школам в отдаленных селах. Строим детские площадки и спортивные комплексы.',
                'charity_amount': 800000,
                'charity_frequency': 'yearly',
                'category_slug': 'construction',
                'latitude': 42.9692,
                'longitude': 47.5156,
                'is_verified': True,
            },
            {
                'name': 'DNS - цифровая техника',
                'description': 'Крупнейшая сеть магазинов цифровой и бытовой техники. Широкий ассортимент электроники по доступным ценам.',
                'address': 'г. Махачкала, пр. Акушинского, 15',
                'phone': '+7 (8722) 67-45-45',
                'email': 'makhachkala@dns-shop.ru',
                'website': 'https://dns-shop.ru',
                'charity_description': 'Передаем компьютерную технику в школы и библиотеки. Организуем компьютерные курсы для пенсионеров.',
                'charity_amount': 180000,
                'charity_frequency': 'monthly',
                'category_slug': 'electronics',
                'latitude': 42.9716,
                'longitude': 47.4969,
                'is_verified': True,
            },
            {
                'name': 'Магазин "Хозяйственный двор"',
                'description': 'Крупный магазин товаров для дома и дачи. Инструменты, сантехника, строительные материалы и хозтовары.',
                'address': 'г. Махачкала, ул. Магомета Гаджиева, 88',
                'phone': '+7 (8722) 78-90-12',
                'email': 'info@hozdvor-msk.ru',
                'website': 'https://hozdvor.ru',
                'charity_description': 'Бесплатно предоставляем стройматериалы для ремонта домов малоимущих семей. Помогаем в обустройстве детских площадок.',
                'charity_amount': 200000,
                'charity_frequency': 'monthly',
                'category_slug': 'household',
                'latitude': 42.9856,
                'longitude': 47.5098,
                'is_verified': True,
            },
            {
                'name': 'Магазин "М.Видео"',
                'description': 'Федеральная сеть магазинов электроники и бытовой техники. Смартфоны, ноутбуки, телевизоры и другая техника от ведущих брендов.',
                'address': 'г. Махачкала, ТЦ "Столица", 1 этаж',
                'phone': '+7 (8722) 55-33-44',
                'email': 'makhachkala@mvideo.ru',
                'website': 'https://mvideo.ru',
                'charity_description': 'Передаем планшеты и ноутбуки в школы для дистанционного обучения. Организуем мастер-классы по цифровой грамотности для пожилых.',
                'charity_amount': 220000,
                'charity_frequency': 'monthly',
                'category_slug': 'electronics',
                'latitude': 42.9801,
                'longitude': 47.5134,
                'is_verified': True,
            },
            {
                'name': 'Кафе "Старый город"',
                'description': 'Уютное семейное кафе с традиционной дагестанской и европейской кухней. Популярное место для семейного отдыха и деловых встреч.',
                'address': 'г. Махачкала, ул. Коркмасова, 25',
                'phone': '+7 (8722) 77-88-99',
                'email': 'info@oldcity-cafe.ru',
                'website': 'https://oldcity-cafe.ru',
                'charity_description': 'Каждое воскресенье организуем бесплатные завтраки для многодетных семей. Поддерживаем благотворительные мероприятия, предоставляя еду и площадку.',
                'charity_amount': 140000,
                'charity_frequency': 'monthly',
                'category_slug': 'restaurants',
                'latitude': 42.9665,
                'longitude': 47.5089,
                'is_verified': True,
            },
        ]

        for company_data in companies_data:
            category = Category.objects.get(slug=company_data['category_slug'])
            company_data['category'] = category
            del company_data['category_slug']

            company, created = Company.objects.get_or_create(
                name=company_data['name'],
                defaults=company_data
            )
            if created:
                self.stdout.write(f'Created company: {company.name}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data!'))