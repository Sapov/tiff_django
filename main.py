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

s = {'Data': {'Customer': [
    {'customerCode': '301576470', 'customerType': 'Business', 'isResident': True, 'taxCode': '366202910465',
     'shortName': 'Индивидуальный предприниматель Сапов Александр Николаевич',
     'fullName': 'Индивидуальный предприниматель Сапов Александр Николаевич', 'customerOgrn': '319366800019380'},
    {'customerCode': '301576474', 'customerType': 'Personal', 'isResident': True, 'taxCode': '366202910465',
     'shortName': 'Сапов А.Н.', 'fullName': 'Сапов Александр Николаевич'}]},
     'Links': {'self': 'https://enter.tochka.com/uapi/open-banking/v1.0/customers'}, 'Meta': {'totalPages': 1}}

print(s['Data']['Customer'][0]['customerCode'])
