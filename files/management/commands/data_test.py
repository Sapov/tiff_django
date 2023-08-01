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
    ("Проклейка баннера", 30, 60),
    ("Проклейка баннера люверсы через 30 ", 75, 140),
]

StatusOrder_data = [
    "Оформлен",
    "В работе",
    "Готов",
]

Material_data = [
    ('Баннер 440 грамм ламинированный', TypePrint.objects.get_or_create(id=1)[0], 165, 280, 72),
    ('Баннер 510 грамм литой', TypePrint.objects.get_or_create(id=1)[0], 290, 600, 72),
    ('Баннер 340 грамм ламинированный', TypePrint.objects.get_or_create(id=1)[0], 130, 260, 72),



]
