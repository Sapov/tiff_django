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
    ('Бумага 150 грамм СytiLight"', TypePrint.objects.get_or_create(id=1)[0], 170, 340, 72),

]
