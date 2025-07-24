from PIL import Image, ImageDraw


class Grommet:
    @staticmethod
    def add_border(file_name: str, border_width: int):
        '''
        расширяем поля на заданное количесьвл см
        :param file_name: имя файла
        :param border_width: ширина края баннера в см
        :return:
        '''
        with Image.open(file_name) as file:
            resolution = round(file.info['dpi'][0], 0)
            print(resolution)
            border = int((border_width * resolution) / 2.54)  # из см в пиксели
            print(file.size)
            width = file.width + border * 2
            height = file.height + border * 2
            image_bordered = Image.new('CMYK', (width, height), 0)
            image_bordered.paste(file, (border, border))
            image_bordered.save('new_banner.tif')


    def luvers(file_name, circle_diameter_mm=8, step_cm=30):
        '''

        :param file_name: имя файла
        :param circle_diameter_mm:  диаметр кргуга
        :param step_cm: шаг между
        :return:
        '''
        with Image.open(file_name) as file:
            resolution = 150 #round(file.info['dpi'][0], 0)
            draw = ImageDraw.Draw(file)
            circle_radius_px = int((circle_diameter_mm /10 * resolution) / 2.54) // 2  # 8 мм → радиус
            print(resolution)
            print(circle_radius_px)
            step_px = int((step_cm * resolution) / 2.54)  # 30 см → шаг в пикселях

            # Рисуем круги
            #
            # Ширина и высота изображения
            width, height = file.size

            # for x in range(step_px, width, step_px):
            #     for y in range(step_px, height, step_px):
            #          # Рисуем круг (граница: чёрная, заливка: белая)
            #         draw.ellipse(
            #             [
            #                 (x - circle_radius_px, y - circle_radius_px),  # Левый верхний угол
            #                 (x + circle_radius_px, y + circle_radius_px)  # Правый нижний угол
            #             ],
            #             fill="white",  # Заливка
            #             outline="black"  # Контур
            #         )
            x1 = int((1.5 * resolution) / 2.54)  # из см в пиксели
            y1 = int((1.5 * resolution) / 2.54)  # из см в пиксели
            draw.ellipse(
                [
                    (x1, y1),  # Левый верхний угол
                    (x1+circle_radius_px, y1+circle_radius_px)  # Правый нижний угол
                ],
                fill="white",  # Заливка
                outline="black"  # Контур
            )
            # Сохраняем изображение
            file.save('new_banner_1.tif', dpi=(resolution, resolution))



if __name__ == '__main__':
    Grommet.add_border('banner.tif', 1)
    # add_border('banner.tif', 5)
    # luvers('new_banner.tif', 8,30)