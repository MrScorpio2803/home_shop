from django.shortcuts import render
from django.views import View

class IndexView(View):

    def get(self, req):
        cards = [
            {
                "image_link": "images/goods/kitchen_table.jpg",
                "image_alt": "Набор кухонных ножей",
                "title": "Профессиональный набор ножей",
                "description": "Изящный 6‑предметный набор из нержавеющей стали для кухни.",
                "category": "kitchen",
                "sale": 15,
                "price": 120.00,
                "total_price": 102.00,  # 120 - 15% = 102
            },
            {
                "image_link": "images/goods/sofa.jpg",
                "image_alt": "Удобный диван",
                "title": "Угловой диван «Лаконик»",
                "description": "Просторный уголок с обивкой из микрофибры, цвет — серый.",
                "category": "livingroom",
                "sale": 0,
                "price": 850.00,
                "total_price": 850.00,  # без скидки
            },
            {
                "image_link": "images/goods/double_bed.jpg",
                "image_alt": "Двуспальная кровать",
                "title": "Кровать «Комфорт»",
                "description": "Двуспальная кровать из массива сосны, размеры 160×200 см.",
                "category": "bedroom",
                "sale": 10,
                "price": 450.00,
                "total_price": 405.00,  # 450 - 10% = 405
            },
            {
                "image_link": "images/goods/flower.jpg",
                "image_alt": "Набор махровых полотенец",
                "title": "Полотенца «Премиум» (3 шт.)",
                "description": "Мягкие махровые полотенца, 70×140 см, белый цвет.",
                "category": "bathroom",
                "sale": 5,
                "price": 35.00,
                "total_price": 33.25,  # 35 - 5% = 33.25
            },
            {
                "image_link": "images/goods/strange_table.jpg",
                "image_alt": "Офисный стол",
                "title": "Письменный стол «Минимал»",
                "description": "Лаконичный стол под работу и учебу, ламинированная поверхность.",
                "category": "office",
                "sale": 20,
                "price": 200.00,
                "total_price": 160.00,  # 200 - 20% = 160
            },
        ]
        context = {
            'cards': cards
        }
        return render(req, 'catalog/catalog.html', context=context)
# Create your views here.
