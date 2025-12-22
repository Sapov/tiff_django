from PIL import Image, ImageDraw


class Grommet:
    WHIDTH = None
    height = None

    @classmethod
    def add_border(cls, file_name: str, border_width: int):
        '''
        расширяем поля на заданное количество  см
        :param file_name: имя файла
        :param border_width: ширина края баннера в см
        :return:
        '''
        with Image.open(file_name) as file:
            resolution = round(file.info['dpi'][0], 0)
            print(f' resolution: {resolution} DPI')
            border = int((border_width * resolution) / 2.54)  # из см в пиксели
            print(file.size)
            width = file.width + border * 2
            WHIDTH = file.width + border * 2
            height = file.height + border * 2
            image_bordered = Image.new('CMYK', (width, height), 0)
            image_bordered.paste(file, (border, border))
            image_bordered.save('new_banner.tif')

    @staticmethod
    def luvers(file_name: str, circle_diameter_mm=8, step_cm=30):
        '''

        :param file_name: имя файла
        :param circle_diameter_mm:  диаметр круга
        :param step_cm: шаг между
        :return:
        '''
        with Image.open(file_name) as file:
            resolution = 150  # round(file.info['dpi'][0], 0) #!!!!!!!!!
            # resolution = round(file.info['dpi'][0], 0)

            draw = ImageDraw.Draw(file)
            circle_radius_px = int((circle_diameter_mm / 10 * resolution) / 2.54) // 2  # 8 мм → радиус
            print(f'РАЗРЕШЕНИЕ: {resolution}')
            print(circle_radius_px)

            step_px = int((step_cm * resolution) / 2.54)  # 30 см → шаг в пикселях

            # Рисуем круги
            #
            # Ширина и высота изображения
            width, height = file.size
            # Получаем ширину изображения и рассчитываем сколько люверсов поместиться

            print(f'Поместиться {count_luvers} люверсов')
            range_luvers = width // count_luvers
            print(f'Люверсы нужно ставить через {range_luvers} PX')

            ident = 2  # отступ от края в см
            x1 = int((ident * resolution) / 2.54)
            y1 = int((ident * resolution) / 2.54)
            x2 = x1 + circle_radius_px
            y2 = y1 + circle_radius_px
            # ставим по ширине

            for i in range(count_luvers):
                # ставим по ширине
                draw.ellipse(
                    [
                        (x1, y1),  # Левый верхний угол
                        (x2, y2)  # Правый нижний угол
                    ],
                    fill="white",  # Заливка
                    outline="black"  # Контур
                )
                print(f'люверс x1:{x1} y1:{y1} - x2: {x2} y2: {y2}')
                # по ширине снизу
                draw.ellipse(
                    [
                        (x1, height - y1),  # Левый верхний угол
                        (x2, height - y2)  # Правый нижний угол
                    ],
                    fill="white",  # Заливка
                    outline="black"  # Контур
                )
                print(f'люверс x1:{x1} y1:{y1} - x2: {x2} y2: {y2}')

                x1 += range_luvers
                x2 += range_luvers
            # Сохраняем изображение
            file.save('new_banner_1.tif', dpi=(resolution, resolution))


if __name__ == '__main__':
    # Grommet.add_border('banner.tif', 5)

    Grommet.luvers('new_banner.tif', 8, 19)

""" 
1. Общую ширину за минусом расстояния до люверсов от края  (200 - (2,5 * 2) = 195 см) делим на расстояние между 
люверсами: 195 / 30 = 6,5 люверсов помещается от края до края
2. Округляем всегда вниз raund(x)
3. Делим на округленное значение ширину 195/6 = 32,5 см
4. расставляем люверсы с этим интервалам
