# # from PIL import Image, ImageOps
# # img = Image.open('media/image/1.tif')
# # img_border = ImageOps.expand(img, border=2, fill='blue')
# # img_border.save('1_border.tif')
# import math
# from PIL import Image, ImageDraw
#
# RANGE_LUVERS = 30
#
# with Image.open('media/image/1.tif') as img:
#     # image = Image.new('RGB', (90, 90), 'white')
#     draw = ImageDraw.Draw(img)
#     width, length = img.size
#     print(f'{width} px, {length}px')
#
#     resolution = round(img.info['dpi'][0], 0)
#     width = round(2.54 * width / resolution, 0)
#     length = round(2.54 * length / resolution, 0)
#     print(f'{width} cm, {length}cm')
#     print(
#         f'По ширине можно поставить {math.ceil(width / RANGE_LUVERS) + 1 if width / RANGE_LUVERS % 2 == 0 else math.ceil(width / RANGE_LUVERS)}')
#     print(f'По длине можно поставить {math.ceil(length / RANGE_LUVERS)}')
#     # draw.ellipse((0, 0, 90, 90), 'yellow', 'blue')
# #     img.save('draw-smile.jpg')
# '''
# 1. Получить ширину / длину в px = img.size
# 2. Расставить кружки диаметром 8 мм через 30 или меньше см по периметру
# Отступаем 2 см от края и расчитываем кол-во люверсов
# т.к. width - 4 /
#
# '''


def to_list(*args):
    print(args[0], type(args[0]))
    # match args:
    #     case tuple(args) as arg:
    #         print('Кортеж аргументов:', arg)
    #     case list() as args:
    #         print('Список элементов:', args)


# to_list(1, (2,), 3, )
to_list([([3, 4, 7], 8.3, True, 'Строка')])
# to_list(1, 2, 3)
# to_list('Молоко', 5, '2020 год')
# to_list([3, 4, 7], 8.3, True, 'Строка')
# Кортеж аргументов: (1, 2, 3)
# Список элементов: [1, 2, 3] - тут
# Кортеж аргументов: ('Молоко', 5, '2020 год')
# Список элементов: ['Молоко', 5, '2020 год'] - тут
# Кортеж аргументов: ([3, 4, 7], 8.3, True, 'Строка')
# Список элементов: [[3, 4, 7], 8.3, True, 'Строка'] - и тут
