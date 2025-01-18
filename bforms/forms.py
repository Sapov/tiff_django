from django import forms

COLOR_SCHEME = (
    (1, 'Желтый фон / Черные буквы'),
    (2, 'Красный фон / белые буквы'),
    (3, 'Белый фон / красные буквы')
)

NAME_BANNER = (
    (1, 'Аренда'),
    (2, 'Аренда помещения'),
    (3, 'Аренда склада'),
    (4, 'Недвижимость в ипотеку'),
    (5, 'Сдам в аренду'),
    (6, 'Старт продаж'),
    (7, 'Продаю'),
    (8, 'Продам'),
    (9, 'Продажа магазина'),
    (10, 'Продается квартира'),
    (11, 'Продается участок'),
    (12, 'Продается дом'),
    (13, 'Продам дом'),
    (14, 'Скоро открытие'),
    (15, 'Мы открылись'),

)
SIZE_BANNER = (
    (1, '1,5 х 1 м'),
    (2, '1,5 х 0,7 м'),
    (3, '2 х 1 м'),
    (4, '1 х 0,5 м'),
)


class SaleBanner(forms.Form):
    name = forms.CharField(max_length=255, label='Имя')
    phone = forms.CharField(max_length=255, label='Телефон')
    mail = forms.CharField(max_length=255, label='Email')
    size_banner = forms.ChoiceField(choices=SIZE_BANNER, label='Размер баннера (ширина х высота)')
    name_banner = forms.ChoiceField(choices=NAME_BANNER, label='Надпись на баннере')
    color_scheme = forms.ChoiceField(choices=COLOR_SCHEME, label='Цветовая схема')
