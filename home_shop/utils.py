from catalog.models import Product, Category
from django.utils.text import slugify


def add_to_model():
    goods = [
        {'image': 'deps/images/goods/set_of_tea_table_and_two_chairs.jpg',
         'name': 'Чайный столик и два стула',
         'description': 'Набор из стола и двух стульев в минималистическом стиле.',
         'category': 'livingroom',
         'price': 93.00},

        {'image': 'deps/images/goods/double bed.jpg',
         'name': 'Двухспальная кровать',
         'description': 'Кровать двухспальная с надголовником и вообще очень ортопедичная.',
         'category': 'bedroom',
         'price': 670.00},

        {'image': 'deps/images/goods/kitchen table.jpg',
         'name': 'Кухонный стол с раковиной',
         'description': 'Кухонный стол для обеда с встроенной раковиной и стульями.',
         'category': 'kitchen',
         'price': 365.00},

        {'image': 'deps/images/goods/kitchen table 2.jpg',
         'name': 'Кухонный стол с встройкой',
         'description': 'Кухонный стол со встроенной плитой и раковиной. Много полок и вообще красивый.',
         'category': 'kitchen',
         'price': 430.00},

        {'image': 'deps/images/goods/corner sofa.jpg',
         'name': 'Угловой диван для гостинной',
         'description': 'Угловой диван, раскладывается в двухспальную кровать, для гостинной и приема гостей самое то!',
         'category': 'livingroom',
         'price': 610.00},

        {'image': 'deps/images/goods/bedside table.jpg',
         'name': 'Прикроватный столик',
         'description': 'Прикроватный столик с двумя выдвижными ящиками (цветок не входит в комплект).',
         'category': 'bedroom',
         'price': 55.00},

        {'image': 'deps/images/goods/sofa.jpg',
         'category': 'livingroom',
         'name': 'Диван обыкновенный',
         'description': 'Диван, он же софа обыкновенная, ничего примечательного для описания.',
         'price': 190.00},

        {'image': 'deps/images/goods/office chair.jpg',
         'name': 'Стул офисный',
         'description': 'Описание товара, про то какой он классный, но это стул, что тут сказать...',
         'category': 'office',
         'price': 30.00},

        {'image': 'deps/images/goods/plants.jpg',
         'name': 'Растение',
         'description': 'Растение для украшения вашего интерьера подарит свежесть и безмятежность обстановке.',
         'category': 'decoration',
         'price': 10.00},

        {'image': 'deps/images/goods/flower.jpg',
         'name': 'Цветок стилизированный',
         'description': 'Дизайнерский цветок (возможно искусственный) для украшения интерьера.',
         'category': 'decoration',
         'price': 15.00},

        {'image': 'deps/images/goods/strange table.jpg',
         'name': 'Прикроватный столик',
         'description': 'Столик, довольно странный на вид, но подходит для размещения рядом с кроватью.',
         'category': 'bedroom',
         'price': 25.00},
    ]
    categories = {c.key: c for c in Category.objects.all()}
    for card in goods:
        image = card['image']
        image = image[image.find('/') + 1:].replace(' ', '_')
        name = card['name']
        description = card['description']
        category = categories.get(card['category'])
        price = card['price']
        if not category:
            print(f'Пропущена вот эта категория. Проверьте на опечатки: {card['category']}')
            continue
        slug = str(slugify(image[image.rfind('/') + 1:image.find('.')])).replace('_', '-')
        card = Product(name=name, description=description, image=image, price=price, slug=slug, category=category)
        card.save()
