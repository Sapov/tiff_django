from files.models import TypePrint

StatusProducts_data = [
    "Оформлен",
    "В работе",
    "Готов",
]

TypePrint_data = [
    "Широкоформатная печать",
    "Интерьерная печать",
    "UV-печать",
]

Fields_data = [
    "Без полей",
    "Поля 5 см",
]


FinishWork_data = [
    ('Без обработки', 0, 0),
    ("Порезка по периметру", 15, 30),
    ("Проклейка баннера", 40, 80),
    ("Проклейка баннера люверсы через 30 ", 75, 140),
    ("Установка люверсов в подворот", 60, 120),
    ("Проклейка по периметру со шнуром и установка люверсов", 90, 180),

]

StatusOrder_data = [
    "Оформлен",
    "В работе",
    "Готов",
]

Material_data = [
    # Ширка TypePrint.objects.get_or_create(id=1)
    ('Баннер 440 грамм ламинированный', TypePrint.objects.get_or_create(id=1)[0], 165, 280, 72),
    ('Баннер 510 грамм литой', TypePrint.objects.get_or_create(id=1)[0], 290, 450, 72),
    ('Баннер 340 грамм ламинированный', TypePrint.objects.get_or_create(id=1)[0], 130, 260, 72),
    ('Пленка самоклеющаяся', TypePrint.objects.get_or_create(id=1)[0], 190, 300, 72),
    ('Баннерная сетка 370 грамм', TypePrint.objects.get_or_create(id=1)[0], 240, 390, 72),
    ('Блюбек', TypePrint.objects.get_or_create(id=1)[0], 110, 220, 72),
    ('Бумага 150 грамм СytiLight', TypePrint.objects.get_or_create(id=1)[0], 170, 340, 72),
    # Интерьерка TypePrint.objects.get_or_create(id=1)
    ('Пленка Китай 80 мик Матовая', TypePrint.objects.get_or_create(id=2)[0], 280, 390, 150),
    ('Пленка Китай 80 мик Глянец', TypePrint.objects.get_or_create(id=2)[0], 280, 390, 150),
    ('Пленка Китай 80 мик Глянец + ламинация', TypePrint.objects.get_or_create(id=2)[0], 450, 800, 150),
    ('Пленка Китай 100 мик Матовая', TypePrint.objects.get_or_create(id=2)[0], 400, 520, 150),
    ('Пленка Китай 100 мик Глянец', TypePrint.objects.get_or_create(id=2)[0], 400, 520, 150),
    ('Пленка Китай 100 мик Глянец + ламинация', TypePrint.objects.get_or_create(id=2)[0], 580, 850, 150),
    ('Бумага 150 грамм СytiLight', TypePrint.objects.get_or_create(id=2)[0], 300, 500, 150),
    ('Фотобумага 200 грамм', TypePrint.objects.get_or_create(id=2)[0], 370, 480, 150),
    ('Беклит матовый 260 грамм', TypePrint.objects.get_or_create(id=2)[0], 450, 1100, 150),
    ('Баннер 450 литой', TypePrint.objects.get_or_create(id=2)[0], 320, 640, 150),
    ('Баннер 510 литой', TypePrint.objects.get_or_create(id=2)[0], 400, 800, 150),
    ('Пленка перфорированная 140 гр.', TypePrint.objects.get_or_create(id=2)[0], 380, 760, 150),
    ('Oraget (матовый, глянцевый, прозрачный', TypePrint.objects.get_or_create(id=2)[0], 450, 900, 150),
    ('Фотообои', TypePrint.objects.get_or_create(id=2)[0], 250, 900, 150),
    ('Холст натуральный', TypePrint.objects.get_or_create(id=2)[0], 750, 1400, 150),

]
